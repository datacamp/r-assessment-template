/**
 * Generate Excalidraw diagrams from video script placeholders
 * 
 * SYNTAX:
 *   ![excalidraw: TEMPLATE: label1, label2, label3, ...]()
 * 
 * TEMPLATES:
 *   - flowchart: linear left-to-right flow
 *   - cycle: circular flow (last connects to first)
 *   - hierarchy: first label is root, rest are children
 *   - radial: first label is center, rest are satellites
 *   - layers: vertical stack (top to bottom)
 *   - timeline: horizontal steps with optional year|description format
 *   - funnel: top-to-bottom narrowing stages
 *   - mindmap: central concept with branches
 *   - matrix: exactly 4 labels for 2x2 grid
 *   - comparison: two groups (use | as separator)
 * 
 * TIMELINE SYNTAX:
 *   - Simple: "Step 1, Step 2, Step 3" (numbered circles)
 *   - With years: "1950|Turing Test, 1997|Deep Blue" (year in circle)
 *   - Line breaks: "1950|Alan Turing // Proposes Test" (// = newline)
 * 
 * EXAMPLES:
 *   ![excalidraw: flowchart: Input, Process, Output]()
 *   ![excalidraw: cycle: Plan, Do, Check, Act]()
 *   ![excalidraw: hierarchy: Cloud Services, IaaS, PaaS, SaaS]()
 *   ![excalidraw: radial: API Gateway, Auth, Users, Orders]()
 *   ![excalidraw: layers: UI, Logic, Data, Storage]()
 *   ![excalidraw: timeline: 1950|Turing Test, 1997|Deep Blue, 2022|ChatGPT]()
 *   ![excalidraw: funnel: Leads, Prospects, Qualified, Customers]()
 *   ![excalidraw: mindmap: AI, ML, DL, NLP, Computer Vision]()
 *   ![excalidraw: comparison: SQL | NoSQL]()
 * 
 * Usage:
 *   node from_script.mjs <script.md> --chapter N --lesson M [--update]
 */

import fs from 'fs/promises';
import path from 'path';
import { convertJsonToPng, closeBrowser } from './to_png.mjs';
import templates from './templates.mjs';

// =============================================================================
// ARGUMENT PARSING
// =============================================================================

const args = process.argv.slice(2);
const scriptPath = args.find(a => !a.startsWith('--'));
const chapterIdx = args.indexOf('--chapter');
const lessonIdx = args.indexOf('--lesson');
const outputIdx = args.indexOf('--output');
const chapter = chapterIdx !== -1 ? parseInt(args[chapterIdx + 1]) : 1;
const lesson = lessonIdx !== -1 ? parseInt(args[lessonIdx + 1]) : 1;
const outputDir = outputIdx !== -1 ? args[outputIdx + 1] : null;
const dryRun = args.includes('--dry-run');
const updateFile = args.includes('--update') || args.includes('-u');

if (!scriptPath) {
  console.error(`
Usage: node from_script.mjs <script.md> --chapter N --lesson M [options]

SYNTAX:
  ![excalidraw: TEMPLATE: label1, label2, label3, ...]()

TEMPLATES:
  flowchart   Linear left-to-right flow
  cycle       Circular flow (last connects to first)  
  hierarchy   First label is root, rest are children
  radial      First label is center, rest are satellites
  layers      Vertical stack (top to bottom)
  timeline    Horizontal steps (supports year|description and // for line breaks)
  funnel      Top-to-bottom narrowing stages
  mindmap     Central concept with branches
  matrix      Exactly 4 labels for 2x2 grid
  comparison  Two groups separated by |

OPTIONS:
  --chapter N       Chapter number (default: 1)
  --lesson M        Lesson number (default: 1)
  --output DIR      Output directory for images (default: ./images/lesson_N_M/)
  --update, -u      Update the source file with image paths
  --dry-run         Show what would be generated without creating files

OUTPUT:
  Images and editable .excalidraw files are saved to: images/lesson_N_M/
  Each diagram generates:
    - lesson_N_M_image_X_description.png       (PNG image for slides)
    - lesson_N_M_image_X_description.excalidraw (Editable file for excalidraw.com)
  
  Filenames include sanitized label text to prevent collisions across lessons.

TIMELINE SYNTAX:
  year|description  Put year in circle, description below
  text // more      Force line break with //

EXAMPLES:
  ![excalidraw: flowchart: Input, Process, Output]()
  ![excalidraw: cycle: Plan, Do, Check, Act]()
  ![excalidraw: hierarchy: Cloud, IaaS, PaaS, SaaS]()
  ![excalidraw: radial: Core, Module A, Module B, Module C]()
  ![excalidraw: layers: Frontend, API, Database]()
  ![excalidraw: timeline: 1950|Turing Test, 1997|Deep Blue]()
  ![excalidraw: funnel: Leads, Prospects, Customers]()
  ![excalidraw: mindmap: AI, ML, DL, NLP, CV]()
  ![excalidraw: comparison: Python | R]()
`);
  process.exit(1);
}

// =============================================================================
// SUPPORTED TEMPLATES
// =============================================================================

const VALID_TEMPLATES = new Set([
  'flowchart',
  'cycle', 
  'hierarchy',
  'radial',
  'layers',
  'timeline',
  'matrix',
  'comparison',
  'process',
  'architecture',
  'funnel',
  'mindmap'
]);

// =============================================================================
// SIMPLE PARSER
// =============================================================================

/**
 * Find all excalidraw placeholders in markdown
 * @param {string} content - Markdown content
 * @returns {Array} Array of {match, template, labels}
 */
function findPlaceholders(content) {
  // Match: ![excalidraw: TEMPLATE: labels]()
  const regex = /!\[excalidraw:\s*(\w+):\s*([^\]]+)\]\(\)/g;
  const placeholders = [];
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    const template = match[1].toLowerCase().trim();
    const labelsRaw = match[2].trim();
    
    // Parse labels - just split by comma
    const labels = labelsRaw
      .split(',')
      .map(l => l.trim())
      .filter(l => l.length > 0);
    
    placeholders.push({
      match: match[0],
      template,
      labels,
      raw: labelsRaw
    });
  }
  
  return placeholders;
}

// =============================================================================
// FILENAME SANITIZATION
// =============================================================================

/**
 * Sanitize text for use in filenames
 * @param {string} text - Raw label text
 * @param {number} maxLength - Maximum length of output
 * @returns {string} Sanitized filename-safe string
 */
function sanitizeForFilename(text, maxLength = 50) {
  return text
    .toLowerCase()
    .replace(/[():,\[\]{}'"]/g, '')  // Remove special chars
    .replace(/\s+/g, '_')             // Spaces to underscores
    .replace(/_+/g, '_')              // Collapse multiple underscores
    .replace(/^_|_$/g, '')            // Trim leading/trailing underscores
    .substring(0, maxLength);         // Truncate if too long
}

// =============================================================================
// DIAGRAM GENERATOR  
// =============================================================================

/**
 * Generate diagram from template name and labels
 * @param {string} template - Template name
 * @param {string[]} labels - Array of label strings
 * @returns {Object} Excalidraw JSON
 */
function generateDiagram(template, labels) {
  if (labels.length === 0) {
    console.warn(`  ⚠️  No labels provided`);
    return templates.flowchartLR(['Placeholder']);
  }
  
  switch (template) {
    case 'flowchart':
    case 'process':
      return templates.flowchartLR(labels);
    
    case 'cycle':
      return templates.cycle(labels);
    
    case 'hierarchy':
      // First label = root, rest = children
      return templates.hierarchy(labels[0], labels.slice(1));
    
    case 'radial':
      // First label = center, rest = satellites
      return templates.radial(labels[0], labels.slice(1));
    
    case 'layers':
      return templates.layers(labels);
    
    case 'timeline':
      return templates.timeline(labels);
    
    case 'matrix':
      // Need exactly 4 labels for 2x2
      if (labels.length !== 4) {
        console.warn(`  ⚠️  Matrix needs exactly 4 labels, got ${labels.length}`);
      }
      return templates.matrix(labels.slice(0, 4));
    
    case 'comparison':
      // Split by | if present, otherwise split in half
      const raw = labels.join(', ');
      if (raw.includes('|')) {
        const [left, right] = raw.split('|').map(s => s.trim());
        const leftLabels = left.split(',').map(l => l.trim()).filter(l => l);
        const rightLabels = right.split(',').map(l => l.trim()).filter(l => l);
        return templates.comparison(
          { title: leftLabels[0], items: leftLabels.slice(1) },
          { title: rightLabels[0], items: rightLabels.slice(1) }
        );
      }
      // No separator - split in half
      const mid = Math.ceil(labels.length / 2);
      return templates.comparison(
        { title: labels[0], items: labels.slice(1, mid) },
        { title: labels[mid], items: labels.slice(mid + 1) }
      );
    
    case 'architecture':
      // First = center, rest = surrounding services
      return templates.architecture({
        center: { label: labels[0] },
        services: labels.slice(1).map(l => ({ label: l }))
      });
    
    case 'funnel':
      return templates.funnel(labels);
    
    case 'mindmap':
      return templates.mindmap(labels);
    
    default:
      console.warn(`  ⚠️  Unknown template "${template}", using flowchart`);
      return templates.flowchartLR(labels);
  }
}

// =============================================================================
// MAIN
// =============================================================================

async function main() {
  console.log(`\n📄 Processing: ${scriptPath}`);
  console.log(`   Chapter: ${chapter}, Lesson: ${lesson}\n`);
  
  const content = await fs.readFile(scriptPath, 'utf-8');
  const placeholders = findPlaceholders(content);
  
  if (placeholders.length === 0) {
    console.log('   No ![excalidraw: TEMPLATE: labels]() placeholders found.');
    console.log('');
    console.log('   Expected syntax:');
    console.log('     ![excalidraw: flowchart: Step 1, Step 2, Step 3]()');
    console.log('     ![excalidraw: cycle: Plan, Do, Check, Act]()');
    console.log('     ![excalidraw: hierarchy: Root, Child A, Child B]()');
    return;
  }
  
  console.log(`   Found ${placeholders.length} placeholder(s):\n`);
  
  let updatedContent = content;
  
  // Create lesson-specific folder: images/lesson_N_M/
  const lessonDir = `lesson_${chapter}_${lesson}`;
  const imagesDir = outputDir || path.join(process.cwd(), 'images', lessonDir);
  
  for (let i = 0; i < placeholders.length; i++) {
    const { match, template, labels, raw } = placeholders[i];
    const imageNum = i + 1;
    const sanitizedLabels = sanitizeForFilename(raw);
    const baseName = `lesson_${chapter}_${lesson}_image_${imageNum}_${sanitizedLabels}`;
    const imageName = `${baseName}.png`;
    const excalidrawName = `${baseName}.excalidraw`;
    const imagePath = path.join(imagesDir, imageName);
    const excalidrawPath = path.join(imagesDir, excalidrawName);
    
    console.log(`   ${imageNum}. ${template}: [${labels.join(', ')}]`);
    
    if (!VALID_TEMPLATES.has(template)) {
      console.log(`      ⚠️  Unknown template "${template}", will use flowchart`);
    }
    
    if (dryRun) {
      console.log(`      Would create: ${imagePath}`);
      console.log(`      Would create: ${excalidrawPath}`);
      continue;
    }
    
    try {
      const diagram = generateDiagram(template, labels);
      
      // Ensure output directory exists
      await fs.mkdir(imagesDir, { recursive: true });
      
      // Save editable .excalidraw file for manual editing at excalidraw.com
      await fs.writeFile(excalidrawPath, JSON.stringify(diagram, null, 2));
      console.log(`      📝 Saved: ${excalidrawPath}`);
      
      // Convert to PNG
      await convertJsonToPng(diagram, imagePath, { silent: true });
      console.log(`      ✅ Created: ${imagePath}`);
      
      // Update markdown with relative image path
      const altText = `${template}: ${raw}`;
      const relativePath = `images/${lessonDir}/${imageName}`;
      updatedContent = updatedContent.replace(match, `![${altText}](${relativePath})`);
    } catch (err) {
      console.error(`      ❌ Error: ${err.message}`);
    }
  }
  
  console.log('');
  
  if (!dryRun && placeholders.length > 0) {
    if (updateFile) {
      await fs.writeFile(scriptPath, updatedContent, 'utf-8');
      console.log(`   📝 Updated: ${scriptPath}`);
    } else {
      console.log('   💡 Use --update flag to automatically update the markdown file');
    }
    console.log(`\n✅ Done! Generated ${placeholders.length} image(s)\n`);
  }
  
  await closeBrowser();
}

main().catch(async err => {
  console.error('Error:', err.message);
  await closeBrowser();
  process.exit(1);
});
