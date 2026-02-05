/**
 * Convert Excalidraw JSON to PNG using Kroki.io + Puppeteer
 * 
 * Uses Puppeteer (headless Chrome) for proper rendering of embedded fonts.
 * IMPORTANT: We calculate bounding box ourselves - don't trust Kroki's viewBox!
 * 
 * CLI Usage: 
 *   node excalidraw_to_png.mjs input.excalidraw [output.png]
 * 
 * Module Usage:
 *   import { convertToPng, convertJsonToPng } from './excalidraw_to_png.mjs';
 *   await convertToPng('input.excalidraw', 'output.png');
 *   await convertJsonToPng(excalidrawJson, 'output.png');
 */

import fs from 'fs/promises';
import path from 'path';
import puppeteer from 'puppeteer';

// Shared browser instance for performance
let browserInstance = null;

/**
 * Get or create a shared browser instance
 */
async function getBrowser() {
  if (!browserInstance) {
    browserInstance = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-crash-reporter',        // Disables crash reporting popups
        '--disable-breakpad',              // Disables crash dump collection
        '--disable-dev-shm-usage',         // Uses /tmp instead of /dev/shm
        '--disable-extensions',            // No extensions needed
        '--disable-background-networking', // Reduces unnecessary network calls
        '--no-first-run',                  // Skips first-run dialogs
      ]
    });
  }
  return browserInstance;
}

/**
 * Close the shared browser instance
 */
export async function closeBrowser() {
  if (browserInstance) {
    await browserInstance.close();
    browserInstance = null;
  }
}

/**
 * Calculate bounding box from Excalidraw elements
 * This is MORE RELIABLE than trusting Kroki's SVG viewBox
 */
function calculateBoundingBox(elements, padding = 40) {
  if (!elements || elements.length === 0) {
    return { width: 800, height: 600 };
  }
  
  let minX = Infinity, minY = Infinity;
  let maxX = -Infinity, maxY = -Infinity;
  
  for (const el of elements) {
    if (typeof el.x !== 'number' || typeof el.y !== 'number') continue;
    
    const elWidth = el.width || 0;
    const elHeight = el.height || 0;
    
    minX = Math.min(minX, el.x);
    minY = Math.min(minY, el.y);
    maxX = Math.max(maxX, el.x + elWidth);
    maxY = Math.max(maxY, el.y + elHeight);
    
    // For arrows, also consider the points
    if (el.points && Array.isArray(el.points)) {
      for (const pt of el.points) {
        if (Array.isArray(pt) && pt.length >= 2) {
          minX = Math.min(minX, el.x + pt[0]);
          minY = Math.min(minY, el.y + pt[1]);
          maxX = Math.max(maxX, el.x + pt[0]);
          maxY = Math.max(maxY, el.y + pt[1]);
        }
      }
    }
  }
  
  // Handle edge cases
  if (!isFinite(minX)) minX = 0;
  if (!isFinite(minY)) minY = 0;
  if (!isFinite(maxX)) maxX = 800;
  if (!isFinite(maxY)) maxY = 600;
  
  const width = Math.ceil(maxX - minX + padding * 2);
  const height = Math.ceil(maxY - minY + padding * 2);
  
  return {
    width: Math.max(width, 200),  // Minimum 200px wide
    height: Math.max(height, 150), // Minimum 150px tall
    minX,
    minY
  };
}

/**
 * Convert Excalidraw JSON content to PNG
 * @param {string|object} content - Excalidraw JSON string or object
 * @param {string} outputFile - Output PNG file path
 * @param {object} options - Optional settings
 * @param {boolean} options.silent - Suppress console output
 * @returns {Promise<Buffer>} PNG buffer
 */
export async function convertJsonToPng(content, outputFile, options = {}) {
  const jsonObj = typeof content === 'string' ? JSON.parse(content) : content;
  const jsonContent = typeof content === 'string' ? content : JSON.stringify(content);
  
  // Calculate bounding box from elements BEFORE calling Kroki
  // This is the key fix - we don't trust Kroki's viewBox
  const bbox = calculateBoundingBox(jsonObj.elements);
  
  if (!options.silent) {
    console.log(`Calculated bounds: ${bbox.width}x${bbox.height}`);
    console.log('Requesting SVG from Kroki.io...');
  }
  
  // Kroki.io API - get SVG (only format supported for excalidraw)
  const response = await fetch('https://kroki.io/excalidraw/svg', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      diagram_source: jsonContent,
    }),
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Kroki API error: ${response.status} - ${errorText}`);
  }
  
  let svgContent = await response.text();
  
  if (!options.silent) {
    console.log('Converting SVG to PNG with Puppeteer...');
  }
  
  // Override the SVG's viewBox and dimensions with our calculated values
  // This fixes Kroki's broken viewBox calculations
  const newViewBox = `0 0 ${bbox.width} ${bbox.height}`;
  svgContent = svgContent.replace(/viewBox="[^"]*"/, `viewBox="${newViewBox}"`);
  svgContent = svgContent.replace(/width="[^"]*"/, `width="${bbox.width}"`);
  svgContent = svgContent.replace(/height="[^"]*"/, `height="${bbox.height}"`);
  
  // Scale up for better quality (2x)
  const scale = 2;
  const width = bbox.width;
  const height = bbox.height;
  
  // Create HTML wrapper with the SVG
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        * { margin: 0; padding: 0; }
        html, body { 
          width: ${width}px;
          height: ${height}px;
          background: transparent;
          overflow: hidden;
        }
        svg { 
          display: block;
          width: ${width}px;
          height: ${height}px;
        }
      </style>
    </head>
    <body>
      ${svgContent}
    </body>
    </html>
  `;
  
  // Use Puppeteer to render
  const browser = await getBrowser();
  const page = await browser.newPage();
  
  await page.setViewport({
    width: width,
    height: height,
    deviceScaleFactor: scale
  });
  
  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  // Wait a bit for fonts to load
  await new Promise(r => setTimeout(r, 100));
  
  // Take screenshot of the full viewport
  const pngBuffer = await page.screenshot({
    type: 'png',
    omitBackground: true
  });
  
  await page.close();
  
  // Write to file if output path provided
  if (outputFile) {
    // Ensure output directory exists
    const outputDir = path.dirname(outputFile);
    if (outputDir && outputDir !== '.') {
      await fs.mkdir(outputDir, { recursive: true });
    }
    
    await fs.writeFile(outputFile, pngBuffer);
    
    if (!options.silent) {
      console.log(`✅ Exported: ${outputFile} (${Math.round(pngBuffer.length / 1024)}KB, ${width * scale}x${height * scale})`);
    }
  }
  
  return pngBuffer;
}

/**
 * Convert an Excalidraw file to PNG
 * @param {string} inputFile - Input .excalidraw file path
 * @param {string} outputFile - Output PNG file path (defaults to same name with .png)
 * @param {object} options - Optional settings
 * @returns {Promise<Buffer>} PNG buffer
 */
export async function convertToPng(inputFile, outputFile = null, options = {}) {
  const content = await fs.readFile(inputFile, 'utf-8');
  const output = outputFile || inputFile.replace('.excalidraw', '.png');
  return convertJsonToPng(content, output, options);
}

// CLI execution
const isMainModule = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/^file:\/\//, ''));

if (isMainModule || process.argv[1]?.endsWith('excalidraw_to_png.mjs')) {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3] || (inputFile ? inputFile.replace('.excalidraw', '.png') : null);
  
  if (!inputFile) {
    console.error('Usage: node excalidraw_to_png.mjs input.excalidraw [output.png]');
    console.error('');
    console.error('Converts Excalidraw JSON to PNG using Kroki.io and Puppeteer.');
    console.error('Properly renders embedded Virgil (hand-drawn) font.');
    process.exit(1);
  }
  
  convertToPng(inputFile, outputFile)
    .then(() => closeBrowser())
    .catch(err => {
      console.error('Error:', err.message);
      closeBrowser();
      process.exit(1);
    });
}

export default { convertToPng, convertJsonToPng, closeBrowser };
