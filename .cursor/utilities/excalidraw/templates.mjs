/**
 * Excalidraw Diagram Templates
 * 
 * Reusable templates for generating common diagram patterns.
 * All diagrams use transparent background and Poppins-compatible font.
 */

// =============================================================================
// GLOBAL DEFAULTS
// =============================================================================

export const DEFAULTS = {
  appState: {
    viewBackgroundColor: "transparent",
    gridSize: null
  },
  // fontFamily: 1 = Virgil (hand-drawn), 2 = Helvetica, 3 = Cascadia (monospace)
  fontFamily: 1,
  fontSize: 16,
  smallFontSize: 12,
  strokeWidth: 2,
  roughness: 1,
  fillStyle: "hachure",
  // Text/sizing constraints
  maxLabelChars: 30,        // Max characters before truncation
  charWidth: 9,             // Approximate width per character (for Poppins 16px)
  minBoxWidth: 80,          // Minimum box width
  maxBoxWidth: 200,         // Maximum box width
  boxPadding: 24            // Horizontal padding inside boxes
};

/**
 * Calculate appropriate box width based on label text
 * @param {string} label - The text label
 * @returns {number} - Calculated width
 */
export function calcWidth(label) {
  if (!label) return DEFAULTS.minBoxWidth;
  const textWidth = label.length * DEFAULTS.charWidth + DEFAULTS.boxPadding;
  return Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, textWidth));
}

/**
 * Truncate label if it exceeds max characters (legacy - prefer wrapText)
 * @param {string} label - The text label
 * @param {number} maxChars - Maximum characters (default from DEFAULTS)
 * @returns {string} - Truncated label with ellipsis if needed
 */
export function truncateLabel(label, maxChars = DEFAULTS.maxLabelChars) {
  if (!label || label.length <= maxChars) return label;
  return label.substring(0, maxChars - 1) + '…';
}

/**
 * Wrap text into multiple lines instead of truncating
 * Splits on word boundaries (spaces, hyphens) when possible
 * @param {string} label - The text label
 * @param {number} maxCharsPerLine - Max characters per line before wrapping
 * @returns {Object} - { text: string with \n, lines: number of lines, maxLineLength: longest line }
 */
export function wrapText(label, maxCharsPerLine = 22) {
  if (!label) return { text: '', lines: 1, maxLineLength: 0 };
  if (label.length <= maxCharsPerLine) return { text: label, lines: 1, maxLineLength: label.length };
  
  // Split on spaces and hyphens, keeping the delimiters
  const words = label.split(/(\s+|-)/);
  const lines = [];
  let currentLine = '';
  
  words.forEach(word => {
    const testLine = currentLine + word;
    if (testLine.length <= maxCharsPerLine) {
      currentLine = testLine;
    } else {
      // Current line is full, start new line
      if (currentLine.trim()) {
        lines.push(currentLine.trim());
      }
      currentLine = word.trimStart();
    }
  });
  
  // Don't forget the last line
  if (currentLine.trim()) {
    lines.push(currentLine.trim());
  }
  
  // Handle edge case where single word is longer than max
  if (lines.length === 0) {
    lines.push(label);
  }
  
  const maxLineLength = Math.max(...lines.map(l => l.length));
  
  return {
    text: lines.join('\n'),
    lines: lines.length,
    maxLineLength
  };
}

// Color palette
export const COLORS = {
  blue: { stroke: "#1971c2", fill: "#a5d8ff" },
  green: { stroke: "#2f9e44", fill: "#b2f2bb" },
  orange: { stroke: "#e8590c", fill: "#ffc078" },
  pink: { stroke: "#9c36b5", fill: "#eebefa" },
  gray: { stroke: "#495057", fill: "#dee2e6" },
  yellow: { stroke: "#e67700", fill: "#ffe066" },
  red: { stroke: "#c92a2a", fill: "#ffc9c9" },
  teal: { stroke: "#0c8599", fill: "#99e9f2" }
};

// =============================================================================
// ELEMENT FACTORIES
// =============================================================================

let seedCounter = 1;
function nextSeed() {
  return seedCounter++;
}

/**
 * Reset seed counter (call before generating a new diagram)
 */
export function resetSeeds() {
  seedCounter = 1;
}

/**
 * Create base element properties
 */
function baseElement(id, type, x, y) {
  return {
    id,
    type,
    x,
    y,
    strokeColor: "#1e1e1e",
    backgroundColor: "transparent",
    fillStyle: DEFAULTS.fillStyle,
    strokeWidth: DEFAULTS.strokeWidth,
    roughness: DEFAULTS.roughness,
    opacity: 100,
    angle: 0,
    seed: nextSeed(),
    version: 1,
    versionNonce: nextSeed(),
    isDeleted: false,
    boundElements: null,
    updated: Date.now(),
    link: null,
    locked: false
  };
}

/**
 * Create a rectangle shape with adaptive width and height (text wrapping)
 * @param {string} id - Element ID
 * @param {number} x - X position
 * @param {number} y - Y position
 * @param {number|null} width - Width (null = auto-calculate from label)
 * @param {number|null} height - Height (null = auto-calculate from wrapped text)
 * @param {string} color - Color name from palette
 * @param {string} label - Text label (will wrap if too long)
 * @param {Object} options - {maxCharsPerLine: number} for custom wrapping
 * @returns {Object} - { elements: Array, height: number } for downstream calculations
 */
export function rectangle(id, x, y, width, height, color = "blue", label = null, options = {}) {
  const elements = [];
  const colorScheme = COLORS[color] || COLORS.blue;
  const maxCharsPerLine = options.maxCharsPerLine || 18;
  const lineHeight = 22;
  const baseHeight = 50;
  
  // Wrap label instead of truncating
  const wrapped = label ? wrapText(label, maxCharsPerLine) : { text: '', lines: 1, maxLineLength: 0 };
  
  // Auto-calculate width based on longest line
  const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding;
  const autoWidth = Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, textWidth));
  const finalWidth = width === null ? autoWidth : Math.max(width, autoWidth);
  
  // Auto-calculate height based on number of lines
  const autoHeight = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
  const finalHeight = height === null ? autoHeight : Math.max(height, autoHeight);
  
  elements.push({
    ...baseElement(id, "rectangle", x, y),
    width: finalWidth,
    height: finalHeight,
    strokeColor: colorScheme.stroke,
    backgroundColor: colorScheme.fill,
    roundness: { type: 3 }
  });
  
  if (wrapped.text) {
    const labelWidth = wrapped.maxLineLength * DEFAULTS.charWidth;
    const labelHeight = wrapped.lines * (DEFAULTS.fontSize + 4);
    elements.push({
      ...baseElement(`${id}-text`, "text", x + finalWidth/2 - labelWidth/2, y + finalHeight/2 - labelHeight/2),
      width: labelWidth,
      height: labelHeight,
      text: wrapped.text,
      fontSize: DEFAULTS.fontSize,
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "middle",
      strokeColor: "#1e1e1e",
      backgroundColor: "transparent"
    });
  }
  
  // Return elements AND computed height for templates that need it
  elements.computedHeight = finalHeight;
  elements.computedWidth = finalWidth;
  return elements;
}

/**
 * Create an ellipse/oval shape with adaptive width and height (text wrapping)
 */
export function ellipse(id, x, y, width, height, color = "green", label = null, options = {}) {
  const elements = [];
  const colorScheme = COLORS[color] || COLORS.green;
  const maxCharsPerLine = options.maxCharsPerLine || 16;
  const lineHeight = 22;
  const baseHeight = 60;
  
  // Wrap label instead of truncating
  const wrapped = label ? wrapText(label, maxCharsPerLine) : { text: '', lines: 1, maxLineLength: 0 };
  
  // Auto-calculate width based on longest line (ellipses need more padding)
  const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding + 20;
  const autoWidth = Math.max(DEFAULTS.minBoxWidth + 20, Math.min(DEFAULTS.maxBoxWidth + 40, textWidth));
  const finalWidth = width === null ? autoWidth : Math.max(width, autoWidth);
  
  // Auto-calculate height based on number of lines
  const autoHeight = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
  const finalHeight = height === null ? autoHeight : Math.max(height, autoHeight);
  
  elements.push({
    ...baseElement(id, "ellipse", x, y),
    width: finalWidth,
    height: finalHeight,
    strokeColor: colorScheme.stroke,
    backgroundColor: colorScheme.fill
  });
  
  if (wrapped.text) {
    const labelWidth = wrapped.maxLineLength * DEFAULTS.charWidth;
    const labelHeight = wrapped.lines * (DEFAULTS.fontSize + 4);
    elements.push({
      ...baseElement(`${id}-text`, "text", x + finalWidth/2 - labelWidth/2, y + finalHeight/2 - labelHeight/2),
      width: labelWidth,
      height: labelHeight,
      text: wrapped.text,
      fontSize: DEFAULTS.fontSize,
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "middle",
      strokeColor: "#1e1e1e",
      backgroundColor: "transparent"
    });
  }
  
  elements.computedHeight = finalHeight;
  elements.computedWidth = finalWidth;
  return elements;
}

/**
 * Create a diamond shape with adaptive width and height (text wrapping)
 * Diamonds have less usable space due to their shape, so use shorter lines
 */
export function diamond(id, x, y, width, height, color = "pink", label = null, options = {}) {
  const elements = [];
  const colorScheme = COLORS[color] || COLORS.pink;
  const maxCharsPerLine = options.maxCharsPerLine || 12;  // Shorter lines for diamonds
  const lineHeight = 18;
  const baseHeight = 70;
  
  // Wrap label instead of truncating
  const wrapped = label ? wrapText(label, maxCharsPerLine) : { text: '', lines: 1, maxLineLength: 0 };
  
  // Auto-calculate width based on longest line (diamonds need more padding due to shape)
  const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding + 40;
  const autoWidth = Math.max(DEFAULTS.minBoxWidth + 20, Math.min(DEFAULTS.maxBoxWidth + 60, textWidth));
  const finalWidth = width === null ? autoWidth : Math.max(width, autoWidth);
  
  // Auto-calculate height based on number of lines (diamonds need extra height)
  const autoHeight = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
  const finalHeight = height === null ? autoHeight : Math.max(height, autoHeight);
  
  elements.push({
    ...baseElement(id, "diamond", x, y),
    width: finalWidth,
    height: finalHeight,
    strokeColor: colorScheme.stroke,
    backgroundColor: colorScheme.fill
  });
  
  if (wrapped.text) {
    const labelWidth = wrapped.maxLineLength * DEFAULTS.charWidth;
    const labelHeight = wrapped.lines * (DEFAULTS.smallFontSize + 6);
    elements.push({
      ...baseElement(`${id}-text`, "text", x + finalWidth/2 - labelWidth/2, y + finalHeight/2 - labelHeight/2),
      width: labelWidth,
      height: labelHeight,
      text: wrapped.text,
      fontSize: DEFAULTS.smallFontSize + 2,
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "middle",
      strokeColor: "#1e1e1e",
      backgroundColor: "transparent"
    });
  }
  
  elements.computedHeight = finalHeight;
  elements.computedWidth = finalWidth;
  return elements;
}

/**
 * Create an arrow between two points
 */
export function arrow(id, startX, startY, endX, endY, bidirectional = false) {
  const width = endX - startX;
  const height = endY - startY;
  
  return [{
    ...baseElement(id, "arrow", startX, startY),
    width: Math.abs(width),
    height: Math.abs(height),
    points: [[0, 0], [width, height]],
    lastCommittedPoint: null,
    startBinding: null,
    endBinding: null,
    startArrowhead: bidirectional ? "arrow" : null,
    endArrowhead: "arrow"
  }];
}

/**
 * Create a text label
 */
export function text(id, x, y, content, fontSize = DEFAULTS.fontSize, color = "#1e1e1e") {
  const lines = content.split('\n');
  const maxLineLength = Math.max(...lines.map(l => l.length));
  
  return [{
    ...baseElement(id, "text", x, y),
    width: maxLineLength * (fontSize * 0.6),
    height: lines.length * (fontSize + 4),
    text: content,
    fontSize,
    fontFamily: DEFAULTS.fontFamily,
    textAlign: "left",
    verticalAlign: "top",
    strokeColor: color,
    backgroundColor: "transparent"
  }];
}

// =============================================================================
// HIGH-LEVEL TEMPLATES
// =============================================================================

/**
 * Create a linear flowchart (left to right) with adaptive widths
 * 
 * SIMPLE API: Just pass an array of labels!
 * @param {Array<string>|Array<Object>} nodes - Array of labels OR {id, label, color, shape} objects
 * @example flowchartLR(['Input', 'Process', 'Output'])
 * @example flowchartLR([{label: 'Start', shape: 'ellipse'}, {label: 'End'}])
 */
export function flowchartLR(nodes) {
  resetSeeds();
  const elements = [];
  
  // Normalize input - accept simple strings or objects
  const normalizedNodes = nodes.map((node, i) => {
    if (typeof node === 'string') {
      return { id: `node-${i}`, label: node };
    }
    return { id: node.id || `node-${i}`, ...node };
  });
  
  const nodeHeight = 60;
  const gap = 60;
  const startX = 50;
  const startY = 80;
  
  // First pass: calculate widths for each node
  const nodeWidths = normalizedNodes.map(node => {
    const displayLabel = truncateLabel(node.label);
    return calcWidth(displayLabel);
  });
  
  // Second pass: create elements with proper positioning
  let currentX = startX;
  
  normalizedNodes.forEach((node, i) => {
    const nodeWidth = nodeWidths[i];
    const shape = node.shape || "rectangle";
    const color = node.color || ["blue", "green", "orange", "teal"][i % 4];
    
    if (shape === "ellipse") {
      elements.push(...ellipse(node.id, currentX, startY, nodeWidth, nodeHeight, color, node.label));
    } else if (shape === "diamond") {
      elements.push(...diamond(node.id, currentX, startY - 10, nodeWidth, nodeHeight + 20, color, node.label));
    } else {
      elements.push(...rectangle(node.id, currentX, startY, nodeWidth, nodeHeight, color, node.label));
    }
    
    // Add arrow to next node
    if (i < normalizedNodes.length - 1) {
      const nextNodeX = currentX + nodeWidth + gap;
      elements.push(...arrow(
        `arrow-${i}`,
        currentX + nodeWidth + 5,
        startY + nodeHeight / 2,
        nextNodeX - 5,
        startY + nodeHeight / 2
      ));
    }
    
    currentX += nodeWidth + gap;
  });
  
  return wrapScene(elements);
}

/**
 * Create a vertical flowchart (top to bottom)
 * @param {Array} nodes - Array of {id, label, color, shape} objects
 */
export function flowchartTB(nodes, startX = 150, startY = 50) {
  resetSeeds();
  const elements = [];
  const nodeWidth = 140;
  const nodeHeight = 50;
  const gap = 60;
  
  nodes.forEach((node, i) => {
    const y = startY + i * (nodeHeight + gap);
    const shape = node.shape || "rectangle";
    const color = node.color || "blue";
    
    if (shape === "ellipse") {
      elements.push(...ellipse(node.id, startX, y, nodeWidth, nodeHeight, color, node.label));
    } else if (shape === "diamond") {
      elements.push(...diamond(node.id, startX + 10, y - 10, nodeWidth - 20, nodeHeight + 20, color, node.label));
    } else {
      elements.push(...rectangle(node.id, startX, y, nodeWidth, nodeHeight, color, node.label));
    }
    
    // Add arrow to next node
    if (i < nodes.length - 1) {
      elements.push(...arrow(
        `arrow-${i}`,
        startX + nodeWidth / 2,
        y + nodeHeight + 5,
        startX + nodeWidth / 2,
        y + nodeHeight + gap - 5
      ));
    }
  });
  
  return wrapScene(elements);
}

/**
 * Create an architecture diagram with a central component and surrounding services
 * @param {Object} config - {center: {label, color}, services: [{label, color}]}
 */
export function architecture(config) {
  resetSeeds();
  const elements = [];
  const centerX = 250;
  const centerY = 150;
  const centerWidth = 160;
  const centerHeight = 80;
  const serviceWidth = 100;
  const serviceHeight = 50;
  const radius = 180;
  
  // Central component
  const centerColor = config.center?.color || "green";
  elements.push(...ellipse("center", centerX, centerY, centerWidth, centerHeight, centerColor, config.center?.label || "Core"));
  
  // Surrounding services
  const services = config.services || [];
  const angleStep = (2 * Math.PI) / services.length;
  
  services.forEach((service, i) => {
    const angle = -Math.PI / 2 + i * angleStep; // Start from top
    const x = centerX + centerWidth/2 - serviceWidth/2 + radius * Math.cos(angle);
    const y = centerY + centerHeight/2 - serviceHeight/2 + radius * Math.sin(angle);
    
    elements.push(...rectangle(service.id || `service-${i}`, x, y, serviceWidth, serviceHeight, service.color || "blue", service.label));
    
    // Arrow to center
    const arrowStartX = x + serviceWidth/2;
    const arrowStartY = y + serviceHeight/2;
    const arrowEndX = centerX + centerWidth/2;
    const arrowEndY = centerY + centerHeight/2;
    
    // Shorten arrow to not overlap shapes
    const dx = arrowEndX - arrowStartX;
    const dy = arrowEndY - arrowStartY;
    const len = Math.sqrt(dx*dx + dy*dy);
    const shortenStart = 35;
    const shortenEnd = 50;
    
    elements.push(...arrow(
      `arrow-${i}`,
      arrowStartX + (dx/len) * shortenStart,
      arrowStartY + (dy/len) * shortenStart,
      arrowEndX - (dx/len) * shortenEnd,
      arrowEndY - (dy/len) * shortenEnd
    ));
  });
  
  return wrapScene(elements);
}

/**
 * Create a process/pipeline diagram
 * @param {Array} steps - Array of {label, color, description} objects
 */
export function process(steps, startX = 50, startY = 100) {
  resetSeeds();
  const elements = [];
  const stepWidth = 120;
  const stepHeight = 60;
  const gap = 60;
  
  steps.forEach((step, i) => {
    const x = startX + i * (stepWidth + gap);
    const color = step.color || ["blue", "green", "orange", "teal"][i % 4];
    
    elements.push(...rectangle(step.id || `step-${i}`, x, startY, stepWidth, stepHeight, color, step.label));
    
    // Add description below if provided
    if (step.description) {
      elements.push(...text(
        `desc-${i}`,
        x,
        startY + stepHeight + 10,
        step.description,
        DEFAULTS.smallFontSize,
        "#868e96"
      ));
    }
    
    // Add arrow to next step
    if (i < steps.length - 1) {
      elements.push(...arrow(
        `arrow-${i}`,
        x + stepWidth + 5,
        startY + stepHeight / 2,
        x + stepWidth + gap - 5,
        startY + stepHeight / 2
      ));
    }
  });
  
  return wrapScene(elements);
}

/**
 * Create a comparison diagram (two columns)
 * @param {Object} left - {title, items: [string]}
 * @param {Object} right - {title, items: [string]}
 */
export function comparison(left, right) {
  resetSeeds();
  const elements = [];
  const colWidth = 180;
  const titleHeight = 50;
  const itemHeight = 35;
  const gap = 100;
  const startX = 50;
  const startY = 50;
  
  // Left column
  elements.push(...rectangle("left-title", startX, startY, colWidth, titleHeight, left.color || "blue", left.title));
  
  (left.items || []).forEach((item, i) => {
    const y = startY + titleHeight + 20 + i * (itemHeight + 10);
    elements.push(...rectangle(`left-item-${i}`, startX, y, colWidth, itemHeight, "gray", item));
  });
  
  // Right column
  const rightX = startX + colWidth + gap;
  elements.push(...rectangle("right-title", rightX, startY, colWidth, titleHeight, right.color || "green", right.title));
  
  (right.items || []).forEach((item, i) => {
    const y = startY + titleHeight + 20 + i * (itemHeight + 10);
    elements.push(...rectangle(`right-item-${i}`, rightX, y, colWidth, itemHeight, "gray", item));
  });
  
  // VS text in the middle
  elements.push(...text("vs", startX + colWidth + gap/2 - 15, startY + titleHeight/2 - 10, "vs", 20, "#868e96"));
  
  return wrapScene(elements);
}

/**
 * Create a simple box diagram with labeled components
 * @param {Array} boxes - Array of {id, label, x, y, width, height, color} objects
 * @param {Array} arrows - Array of {from, to, bidirectional} objects
 */
export function custom(boxes, connections = []) {
  resetSeeds();
  const elements = [];
  const boxMap = {};
  
  // Create boxes
  boxes.forEach(box => {
    const width = box.width || 120;
    const height = box.height || 60;
    const shape = box.shape || "rectangle";
    
    boxMap[box.id] = { x: box.x, y: box.y, width, height };
    
    if (shape === "ellipse") {
      elements.push(...ellipse(box.id, box.x, box.y, width, height, box.color || "blue", box.label));
    } else if (shape === "diamond") {
      elements.push(...diamond(box.id, box.x, box.y, width, height, box.color || "pink", box.label));
    } else {
      elements.push(...rectangle(box.id, box.x, box.y, width, height, box.color || "blue", box.label));
    }
  });
  
  // Create connections
  connections.forEach((conn, i) => {
    const from = boxMap[conn.from];
    const to = boxMap[conn.to];
    
    if (from && to) {
      // Calculate connection points (center to center, shortened)
      const fromCenterX = from.x + from.width / 2;
      const fromCenterY = from.y + from.height / 2;
      const toCenterX = to.x + to.width / 2;
      const toCenterY = to.y + to.height / 2;
      
      const dx = toCenterX - fromCenterX;
      const dy = toCenterY - fromCenterY;
      const len = Math.sqrt(dx*dx + dy*dy);
      
      const startOffset = Math.min(from.width, from.height) / 2 + 5;
      const endOffset = Math.min(to.width, to.height) / 2 + 5;
      
      elements.push(...arrow(
        conn.id || `conn-${i}`,
        fromCenterX + (dx/len) * startOffset,
        fromCenterY + (dy/len) * startOffset,
        toCenterX - (dx/len) * endOffset,
        toCenterY - (dy/len) * endOffset,
        conn.bidirectional || false
      ));
    }
  });
  
  return wrapScene(elements);
}

// =============================================================================
// CREATIVE TEMPLATES (NEW)
// =============================================================================

/**
 * Create a cycle/loop diagram (circular flow)
 * Perfect for feedback loops, ReAct patterns, iterative processes
 * 
 * SIMPLE API: Just pass an array of labels!
 * @param {Array<string>|Array<Object>} nodes - Array of labels OR {id, label, color, shape} objects
 * @example cycle(['Observe', 'Think', 'Act'])
 * @example cycle([{label: 'Step 1', color: 'blue'}, {label: 'Step 2', color: 'green'}])
 */
export function cycle(nodes) {
  resetSeeds();
  const elements = [];
  
  // Normalize input - accept simple strings or objects
  const normalizedNodes = nodes.map((node, i) => {
    if (typeof node === 'string') {
      return { id: `node-${i}`, label: node };
    }
    return { id: node.id || `node-${i}`, ...node };
  });
  
  const nodeCount = normalizedNodes.length;
  
  // First pass: pre-calculate actual dimensions using wrapText (matching what rectangle() does)
  const nodeDimensions = normalizedNodes.map(node => {
    const wrapped = wrapText(node.label, 18);  // Same maxCharsPerLine as rectangle()
    const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding;
    const width = Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, textWidth));
    const baseHeight = 50;
    const lineHeight = 22;
    const height = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
    return { width, height };
  });
  
  const maxWidth = Math.max(...nodeDimensions.map(d => d.width));
  const maxHeight = Math.max(...nodeDimensions.map(d => d.height));
  
  // Calculate radius based on actual dimensions - tighter spacing for compact layout
  const baseRadius = 70 + Math.min(nodeCount, 6) * 14;  // Reduced by ~30%
  const radius = baseRadius + maxWidth / 2;
  
  // Center position ensuring all nodes have positive coordinates
  const centerX = radius + maxWidth / 2 + 60;
  const centerY = radius + maxHeight / 2 + 60;
  
  // Place nodes in a circle (clockwise from top)
  const angleStep = (2 * Math.PI) / nodeCount;
  const nodePositions = [];
  
  normalizedNodes.forEach((node, i) => {
    // Start from top, go clockwise
    const angle = -Math.PI / 2 + i * angleStep;
    const dims = nodeDimensions[i];
    
    // Position node center on the circle
    const nodeCenterX = centerX + radius * Math.cos(angle);
    const nodeCenterY = centerY + radius * Math.sin(angle);
    
    // Top-left corner for shape placement
    const x = nodeCenterX - dims.width / 2;
    const y = nodeCenterY - dims.height / 2;
    
    const shape = node.shape || "rectangle";
    const color = node.color || ["blue", "green", "orange", "teal", "pink", "yellow"][i % 6];
    
    let shapeElements;
    if (shape === "ellipse") {
      shapeElements = ellipse(node.id, x, y, dims.width, dims.height, color, node.label);
    } else if (shape === "diamond") {
      shapeElements = diamond(node.id, x, y, dims.width, dims.height, color, node.label);
    } else {
      shapeElements = rectangle(node.id, x, y, dims.width, dims.height, color, node.label);
    }
    
    // Use actual computed dimensions from shape factory
    const actualWidth = shapeElements.computedWidth || dims.width;
    const actualHeight = shapeElements.computedHeight || dims.height;
    
    // Recalculate center based on actual dimensions
    const actualCenterX = x + actualWidth / 2;
    const actualCenterY = y + actualHeight / 2;
    
    nodePositions.push({ 
      cx: actualCenterX, 
      cy: actualCenterY, 
      x, 
      y, 
      angle,
      width: actualWidth,
      height: actualHeight
    });
    
    elements.push(...shapeElements);
  });
  
  // Create arrows between consecutive nodes (clockwise: node -> next node)
  for (let i = 0; i < nodeCount; i++) {
    const from = nodePositions[i];
    const to = nodePositions[(i + 1) % nodeCount];
    
    // Calculate direction from this node to next node
    const dx = to.cx - from.cx;
    const dy = to.cy - from.cy;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const ux = dx / dist; // unit vector x
    const uy = dy / dist; // unit vector y
    
    // Calculate intersection with box edges (ray-box intersection)
    // For 'from' box: find where ray exits
    const fromHalfW = from.width / 2;
    const fromHalfH = from.height / 2;
    const tFromX = Math.abs(ux) > 0.001 ? fromHalfW / Math.abs(ux) : Infinity;
    const tFromY = Math.abs(uy) > 0.001 ? fromHalfH / Math.abs(uy) : Infinity;
    const fromOffset = Math.min(tFromX, tFromY);
    
    // For 'to' box: find where ray enters (from opposite direction)
    const toHalfW = to.width / 2;
    const toHalfH = to.height / 2;
    const tToX = Math.abs(ux) > 0.001 ? toHalfW / Math.abs(ux) : Infinity;
    const tToY = Math.abs(uy) > 0.001 ? toHalfH / Math.abs(uy) : Infinity;
    const toOffset = Math.min(tToX, tToY);
    
    // Arrow endpoints at box edges with small gap (reduced for tighter spacing)
    const gap = 5;
    const startX = from.cx + ux * (fromOffset + gap);
    const startY = from.cy + uy * (fromOffset + gap);
    const endX = to.cx - ux * (toOffset + gap);
    const endY = to.cy - uy * (toOffset + gap);
    
    elements.push(...arrow(
      `arrow-${i}`,
      startX,
      startY,
      endX,
      endY
    ));
  }
  
  return wrapScene(elements);
}

/**
 * Create a radial/hub-and-spoke diagram
 * Perfect for showing a central concept with related components
 * 
 * SIMPLE API: Pass center label and array of satellite labels!
 * @param {string|Object} center - Center label OR {label, color, shape} object
 * @param {Array<string>|Array<Object>} satellites - Array of labels OR {id, label, color, shape} objects
 * @param {Object} options - {arrowDirection: "inward"|"outward"|"both"}
 * @example radial('Core', ['Feature 1', 'Feature 2', 'Feature 3'])
 */
export function radial(center, satellites, options = {}) {
  resetSeeds();
  const elements = [];
  
  // Normalize center - accept string or object
  const normalizedCenter = typeof center === 'string' 
    ? { label: center } 
    : center;
  
  // Normalize satellites - accept strings or objects
  const normalizedSatellites = satellites.map((sat, i) => {
    if (typeof sat === 'string') {
      return { id: `sat-${i}`, label: sat };
    }
    return { id: sat.id || `sat-${i}`, ...sat };
  });
  
  // DYNAMIC SIZING: Calculate widths based on text content
  const centerLabel = truncateLabel(normalizedCenter.label);
  const centerWidth = Math.max(120, calcWidth(centerLabel) + 20); // Extra padding for ellipse
  const centerHeight = 70;
  
  // Calculate width for each satellite
  const satelliteWidths = normalizedSatellites.map(sat => {
    const label = truncateLabel(sat.label);
    return calcWidth(label);
  });
  const maxSatelliteWidth = Math.max(...satelliteWidths, 100);
  const satelliteHeight = 50;
  
  // Adjust radius based on content size to prevent overlaps
  const baseRadius = 140;
  const radius = baseRadius + Math.max(0, (maxSatelliteWidth - 100) / 2) + Math.max(0, (centerWidth - 120) / 2);
  
  // Position center to ensure all satellites have positive coordinates
  const padding = 60;
  const centerX = radius + maxSatelliteWidth / 2 + padding;
  const centerY = radius + satelliteHeight / 2 + padding;
  const arrowDirection = options.arrowDirection || "inward";
  
  // Central node (ellipse by default for visual distinction)
  const centerColor = normalizedCenter.color || "green";
  const centerShape = normalizedCenter.shape || "ellipse";
  
  if (centerShape === "rectangle") {
    elements.push(...rectangle("center", centerX - centerWidth/2, centerY - centerHeight/2, centerWidth, centerHeight, centerColor, normalizedCenter.label));
  } else {
    elements.push(...ellipse("center", centerX - centerWidth/2, centerY - centerHeight/2, centerWidth, centerHeight, centerColor, normalizedCenter.label));
  }
  
  // Surrounding satellites
  const angleStep = (2 * Math.PI) / normalizedSatellites.length;
  
  normalizedSatellites.forEach((sat, i) => {
    const satWidth = maxSatelliteWidth;
    const angle = -Math.PI / 2 + i * angleStep; // Start from top
    const x = centerX + radius * Math.cos(angle) - satWidth / 2;
    const y = centerY + radius * Math.sin(angle) - satelliteHeight / 2;
    
    const color = sat.color || ["blue", "orange", "teal", "pink", "yellow", "red"][i % 6];
    const shape = sat.shape || "rectangle";
    
    if (shape === "ellipse") {
      elements.push(...ellipse(sat.id || `sat-${i}`, x, y, satWidth, satelliteHeight, color, sat.label));
    } else if (shape === "diamond") {
      elements.push(...diamond(sat.id || `sat-${i}`, x, y, satWidth, satelliteHeight, color, sat.label));
    } else {
      elements.push(...rectangle(sat.id || `sat-${i}`, x, y, satWidth, satelliteHeight, color, sat.label));
    }
    
    // Arrow between satellite and center - PROPER CENTER-TO-CENTER alignment
    const satCenterX = x + satWidth / 2;
    const satCenterY = y + satelliteHeight / 2;
    
    // Direction vector from satellite center to main center
    const dx = centerX - satCenterX;
    const dy = centerY - satCenterY;
    const len = Math.sqrt(dx * dx + dy * dy);
    const ux = dx / len;  // unit vector x
    const uy = dy / len;  // unit vector y
    
    // Calculate edge intersections using ray-box intersection
    // For satellite (rectangle): find where ray exits the box
    const satHalfW = satWidth / 2;
    const satHalfH = satelliteHeight / 2;
    const tSatX = Math.abs(ux) > 0.001 ? satHalfW / Math.abs(ux) : Infinity;
    const tSatY = Math.abs(uy) > 0.001 ? satHalfH / Math.abs(uy) : Infinity;
    const satOffset = Math.min(tSatX, tSatY);
    
    // For center (ellipse): use ellipse intersection formula
    const centerHalfW = centerWidth / 2;
    const centerHalfH = centerHeight / 2;
    // Ellipse parametric: find t where (ux*t/a)^2 + (uy*t/b)^2 = 1
    const centerOffset = 1 / Math.sqrt((ux * ux) / (centerHalfW * centerHalfW) + (uy * uy) / (centerHalfH * centerHalfH));
    
    // Calculate edge points
    const satEdgeX = satCenterX + ux * satOffset;
    const satEdgeY = satCenterY + uy * satOffset;
    const centerEdgeX = centerX - ux * centerOffset;
    const centerEdgeY = centerY - uy * centerOffset;
    
    // Add consistent gap for arrowheads (increased to prevent bleeding)
    const arrowGap = 12;  // Gap from satellite edge
    const centerGapVal = 14;  // Gap from center edge
    const satGapX = satEdgeX + ux * arrowGap;
    const satGapY = satEdgeY + uy * arrowGap;
    const centerGapX = centerEdgeX - ux * centerGapVal;
    const centerGapY = centerEdgeY - uy * centerGapVal;
    
    const isBidirectional = arrowDirection === "both";
    
    // Determine arrow start/end based on direction
    const arrowStartX = arrowDirection === "outward" ? centerGapX : satGapX;
    const arrowStartY = arrowDirection === "outward" ? centerGapY : satGapY;
    const arrowEndX = arrowDirection === "outward" ? satGapX : centerGapX;
    const arrowEndY = arrowDirection === "outward" ? satGapY : centerGapY;
    
    // Use standard arrow construction: base at start point, relative endpoint
    elements.push(...arrow(
      `arrow-${i}`,
      arrowStartX,
      arrowStartY,
      arrowEndX,
      arrowEndY,
      isBidirectional
    ));
  });
  
  return wrapScene(elements);
}

/**
 * Create a hierarchy/tree diagram (top-down)
 * Perfect for org charts, taxonomies, decision trees
 * 
 * SIMPLE API: Pass root label and array of child labels!
 * @param {string|Object} root - Root label OR {label, color, shape} for root node
 * @param {Array<string>|Array<Object>} children - Array of labels OR {label, color, shape, children?} objects
 * @example hierarchy('Parent', ['Child 1', 'Child 2', 'Child 3'])
 */
export function hierarchy(root, children) {
  resetSeeds();
  const elements = [];
  const baseNodeWidth = 120;
  const baseNodeHeight = 50;
  const horizontalGap = 60;  // Gap between siblings
  const verticalGap = 80;
  const startY = 50;
  const maxCharsPerLine = 18;  // Match rectangle() default
  const lineHeight = 22;
  
  // Normalize root - accept string or object
  const normalizedRoot = typeof root === 'string' 
    ? { label: root } 
    : root;
  
  // Normalize children - accept strings or objects
  const normalizedChildren = children.map(child => {
    if (typeof child === 'string') {
      return { label: child };
    }
    return child;
  });
  
  // Pre-calculate dimensions for a node using wrapText (matching rectangle() logic)
  function calcNodeDimensions(label) {
    const wrapped = wrapText(label, maxCharsPerLine);
    const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding;
    const width = Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, textWidth));
    const height = baseNodeHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
    return { width, height, wrapped };
  }
  
  // Pre-calculate all dimensions
  const rootDims = calcNodeDimensions(normalizedRoot.label);
  const childDims = normalizedChildren.map(child => calcNodeDimensions(child.label));
  
  // Calculate total width needed for children (sum of widths + gaps)
  const totalChildrenWidth = childDims.reduce((sum, d) => sum + d.width, 0) + 
                             (childDims.length - 1) * horizontalGap;
  
  // Starting X position for children (centered layout)
  const startX = 50;
  
  // Root node - centered above children
  const rootX = startX + totalChildrenWidth / 2 - rootDims.width / 2;
  const rootY = startY;
  const rootColor = normalizedRoot.color || "green";
  
  if (normalizedRoot.shape === "ellipse") {
    elements.push(...ellipse("root", rootX, rootY, rootDims.width, rootDims.height, rootColor, normalizedRoot.label));
  } else {
    elements.push(...rectangle("root", rootX, rootY, rootDims.width, rootDims.height, rootColor, normalizedRoot.label));
  }
  
  // Render children with proper spacing based on actual widths
  let currentX = startX;
  const childY = startY + rootDims.height + verticalGap;
  
  normalizedChildren.forEach((node, i) => {
    const dims = childDims[i];
    const nodeId = `root-${i}`;
    const color = node.color || ["blue", "orange", "teal", "pink"][i % 4];
    
    let shapeElements;
    if (node.shape === "ellipse") {
      shapeElements = ellipse(nodeId, currentX, childY, dims.width, dims.height, color, node.label);
    } else if (node.shape === "diamond") {
      shapeElements = diamond(nodeId, currentX, childY, dims.width, dims.height, color, node.label);
    } else {
      shapeElements = rectangle(nodeId, currentX, childY, dims.width, dims.height, color, node.label);
    }
    
    // Use actual dimensions from shape factory
    const actualWidth = shapeElements.computedWidth || dims.width;
    const actualHeight = shapeElements.computedHeight || dims.height;
    
    elements.push(...shapeElements);
    
    // Arrow from root CENTER bottom to child CENTER top
    const rootCenterX = rootX + rootDims.width / 2;
    const childCenterX = currentX + actualWidth / 2;
    
    elements.push(...arrow(
      `arrow-${nodeId}`,
      rootCenterX,
      rootY + rootDims.height + 5,
      childCenterX,
      childY - 5
    ));
    
    // Move to next position
    currentX += actualWidth + horizontalGap;
  });
  
  return wrapScene(elements);
}

/**
 * Create a timeline diagram with numbered steps
 * Perfect for sequences, processes with clear phases
 * 
 * SIMPLE API: Just pass an array of labels!
 * @param {Array<string>|Array<Object>} steps - Array of labels OR {label, description?, color} objects
 * @example timeline(['Step 1', 'Step 2', 'Step 3'])
 * @example timeline([{label: 'Start', color: 'green'}, {label: 'End', color: 'blue'}])
 */
export function timeline(steps) {
  resetSeeds();
  const elements = [];
  
  // Normalize input - accept simple strings or objects
  // Supports: "label", "year|description", "text // with // linebreaks"
  const normalizedSteps = steps.map((step, i) => {
    if (typeof step === 'string') {
      // Check for year|description format
      if (step.includes('|')) {
        const pipeIndex = step.indexOf('|');
        const year = step.substring(0, pipeIndex).trim();
        const description = step.substring(pipeIndex + 1).trim();
        return { year, label: description };
      }
      return { label: step };
    }
    return step;
  });
  
  const circleSize = 50;
  const gap = 100;
  const startX = 60;
  const startY = 60;
  const lineY = startY + circleSize / 2;
  
  // Draw connecting line first (background)
  if (normalizedSteps.length > 1) {
    const lineStartX = startX + circleSize / 2;
    const lineEndX = startX + (normalizedSteps.length - 1) * (circleSize + gap) + circleSize / 2;
    
    elements.push({
      ...baseElement("timeline-line", "line", lineStartX, lineY),
      width: lineEndX - lineStartX,
      height: 0,
      points: [[0, 0], [lineEndX - lineStartX, 0]],
      strokeColor: "#868e96",
      strokeWidth: 3
    });
  }
  
  // Draw numbered circles and labels
  normalizedSteps.forEach((step, i) => {
    const x = startX + i * (circleSize + gap);
    const color = step.color || ["blue", "green", "orange", "teal", "pink"][i % 5];
    const colorScheme = COLORS[color] || COLORS.blue;
    
    // Numbered circle
    elements.push({
      ...baseElement(`step-circle-${i}`, "ellipse", x, startY),
      width: circleSize,
      height: circleSize,
      strokeColor: colorScheme.stroke,
      backgroundColor: colorScheme.fill
    });
    
    // Content inside circle: year if provided, otherwise step number
    const circleText = step.year || String(i + 1);
    const circleTextWidth = circleText.length * 8;  // Approximate width
    elements.push({
      ...baseElement(`step-num-${i}`, "text", x + circleSize / 2 - circleTextWidth / 2, startY + circleSize / 2 - 12),
      width: circleTextWidth,
      height: 24,
      text: circleText,
      fontSize: step.year ? 14 : 20,  // Smaller font for years
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "middle",
      strokeColor: "#1e1e1e"
    });
    
    // Label below - support // as explicit line breaks, then wrap remaining text
    // Convert // to newlines first, then wrap each segment
    const labelWithBreaks = step.label.replace(/\s*\/\/\s*/g, '\n');
    const segments = labelWithBreaks.split('\n');
    const wrappedSegments = segments.map(seg => wrapText(seg, 12).text);
    const finalText = wrappedSegments.join('\n');
    const lines = finalText.split('\n');
    const maxLineLength = Math.max(...lines.map(l => l.length));
    
    const labelWidth = maxLineLength * DEFAULTS.charWidth;
    const labelHeight = lines.length * (DEFAULTS.fontSize + 4);
    elements.push({
      ...baseElement(`step-label-${i}`, "text", x + circleSize / 2 - labelWidth / 2, startY + circleSize + 15),
      width: labelWidth,
      height: labelHeight,
      text: finalText,
      fontSize: DEFAULTS.fontSize,
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "top",
      strokeColor: "#1e1e1e",
      backgroundColor: "transparent"
    });
    
    // Description if provided (below the wrapped label)
    if (step.description) {
      const descWrapped = wrapText(step.description, 15);
      const descWidth = descWrapped.maxLineLength * (DEFAULTS.smallFontSize * 0.6);
      const descHeight = descWrapped.lines * (DEFAULTS.smallFontSize + 4);
      elements.push({
        ...baseElement(`step-desc-${i}`, "text", x + circleSize / 2 - descWidth / 2, startY + circleSize + 15 + labelHeight + 5),
        width: descWidth,
        height: descHeight,
        text: descWrapped.text,
        fontSize: DEFAULTS.smallFontSize,
        fontFamily: DEFAULTS.fontFamily,
        textAlign: "center",
        verticalAlign: "top",
        strokeColor: "#868e96",
        backgroundColor: "transparent"
      });
    }
  });
  
  return wrapScene(elements);
}

/**
 * Create a 2x2 matrix/quadrant diagram
 * Perfect for comparisons, priority matrices, categorizations
 * @param {Object} config - {topLeft, topRight, bottomLeft, bottomRight, xAxis?, yAxis?}
 */
export function matrix(config) {
  resetSeeds();
  const elements = [];
  const cellWidth = 180;
  const cellHeight = 120;
  const startX = 80;
  const startY = 60;
  const axisOffset = 40;
  
  const quadrants = [
    { pos: "topLeft", x: startX, y: startY },
    { pos: "topRight", x: startX + cellWidth + 20, y: startY },
    { pos: "bottomLeft", x: startX, y: startY + cellHeight + 20 },
    { pos: "bottomRight", x: startX + cellWidth + 20, y: startY + cellHeight + 20 }
  ];
  
  const defaultColors = ["blue", "green", "orange", "teal"];
  
  // Draw quadrant boxes
  quadrants.forEach((q, i) => {
    const data = config[q.pos] || {};
    const color = data.color || defaultColors[i];
    
    elements.push(...rectangle(
      `quad-${q.pos}`,
      q.x, q.y,
      cellWidth, cellHeight,
      color,
      data.label || q.pos
    ));
    
    // Add items if provided
    if (data.items && data.items.length > 0) {
      const itemsText = data.items.slice(0, 3).join("\n");
      elements.push(...text(
        `items-${q.pos}`,
        q.x + 10,
        q.y + 45,
        itemsText,
        DEFAULTS.smallFontSize,
        "#495057"
      ));
    }
  });
  
  // Axis labels if provided
  if (config.xAxis) {
    elements.push(...text(
      "x-axis",
      startX + cellWidth,
      startY + 2 * cellHeight + 50,
      config.xAxis,
      DEFAULTS.fontSize,
      "#495057"
    ));
    
    // X-axis arrow
    elements.push({
      ...baseElement("x-arrow", "arrow", startX - 20, startY + 2 * cellHeight + 35),
      width: 2 * cellWidth + 60,
      height: 0,
      points: [[0, 0], [2 * cellWidth + 60, 0]],
      strokeColor: "#868e96",
      startArrowhead: null,
      endArrowhead: "arrow"
    });
  }
  
  if (config.yAxis) {
    elements.push(...text(
      "y-axis",
      startX - 60,
      startY + cellHeight - 10,
      config.yAxis,
      DEFAULTS.fontSize,
      "#495057"
    ));
    
    // Y-axis arrow
    elements.push({
      ...baseElement("y-arrow", "arrow", startX - 20, startY + 2 * cellHeight + 30),
      width: 0,
      height: 2 * cellHeight + 30,
      points: [[0, 0], [0, -(2 * cellHeight + 30)]],
      strokeColor: "#868e96",
      startArrowhead: null,
      endArrowhead: "arrow"
    });
  }
  
  return wrapScene(elements);
}

/**
 * Create a layered/stack diagram
 * Perfect for architectures, tech stacks, abstraction layers
 * 
 * SIMPLE API: Just pass an array of labels!
 * @param {Array<string>|Array<Object>} layerList - Array of labels OR {label, color, description?} objects (top to bottom)
 * @example layers(['Presentation', 'Business Logic', 'Data Access', 'Database'])
 */
export function layers(layerList) {
  resetSeeds();
  const elements = [];
  const layerWidth = 300;
  const baseHeight = 50;
  const lineHeight = 22;  // Height per line of wrapped text
  const gap = 15;
  const startX = 100;
  const startY = 50;
  const maxCharsPerLine = 28;  // Chars that fit in layerWidth
  
  // Normalize input - accept simple strings or objects
  const normalizedLayers = layerList.map((layer, i) => {
    if (typeof layer === 'string') {
      return { id: `layer-${i}`, label: layer };
    }
    return { id: layer.id || `layer-${i}`, ...layer };
  });
  
  const colors = ["blue", "green", "orange", "teal", "pink", "yellow"];
  
  // Pre-calculate wrapped text and heights for each layer
  const layerData = normalizedLayers.map(layer => {
    const wrapped = wrapText(layer.label, maxCharsPerLine);
    const height = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
    return { ...layer, wrapped, height };
  });
  
  // Build layers with dynamic heights
  let currentY = startY;
  
  layerData.forEach((layer, i) => {
    const color = layer.color || colors[i % colors.length];
    const colorScheme = COLORS[color] || COLORS.blue;
    
    // Create rectangle manually to handle multiline text
    elements.push({
      ...baseElement(layer.id || `layer-${i}`, "rectangle", startX, currentY),
      width: layerWidth,
      height: layer.height,
      strokeColor: colorScheme.stroke,
      backgroundColor: colorScheme.fill,
      roundness: { type: 3 }
    });
    
    // Add wrapped text centered in the box
    const textWidth = layer.wrapped.maxLineLength * DEFAULTS.charWidth;
    const textHeight = layer.wrapped.lines * (DEFAULTS.fontSize + 4);
    elements.push({
      ...baseElement(`${layer.id}-text`, "text", startX + layerWidth/2 - textWidth/2, currentY + layer.height/2 - textHeight/2),
      width: textWidth,
      height: textHeight,
      text: layer.wrapped.text,
      fontSize: DEFAULTS.fontSize,
      fontFamily: DEFAULTS.fontFamily,
      textAlign: "center",
      verticalAlign: "middle",
      strokeColor: "#1e1e1e",
      backgroundColor: "transparent"
    });
    
    // Description to the right if provided
    if (layer.description) {
      elements.push(...text(
        `layer-desc-${i}`,
        startX + layerWidth + 20,
        currentY + layer.height / 2 - 8,
        layer.description,
        DEFAULTS.smallFontSize,
        "#868e96"
      ));
    }
    
    currentY += layer.height + gap;
  });
  
  return wrapScene(elements);
}

/**
 * Create a funnel diagram (wide to narrow stages)
 * Perfect for marketing funnels, sales pipelines, conversion processes
 * 
 * SIMPLE API: Just pass an array of stage labels!
 * @param {Array<string>} stages - Array of stage labels (top to bottom, wide to narrow)
 * @example funnel(['Awareness', 'Interest', 'Decision', 'Action'])
 */
export function funnel(stages) {
  resetSeeds();
  const elements = [];
  
  // Normalize input
  const normalizedStages = stages.map((stage, i) => {
    if (typeof stage === 'string') {
      return { label: stage };
    }
    return stage;
  });
  
  const stageCount = normalizedStages.length;
  const maxWidth = 300;
  const minWidth = 120;
  const baseHeight = 50;
  const gap = 12;  // Gap between stages
  const startY = 50;
  const maxCharsPerLine = 18;
  const lineHeight = 22;
  
  // Calculate width reduction per stage
  const widthStep = (maxWidth - minWidth) / Math.max(stageCount - 1, 1);
  
  // Pre-calculate dimensions for each stage
  const stageDims = normalizedStages.map((stage, i) => {
    const wrapped = wrapText(stage.label, maxCharsPerLine);
    const height = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
    const width = maxWidth - (i * widthStep);
    return { width, height, wrapped };
  });
  
  // Colors for stages (gradient-like effect)
  const stageColors = ['blue', 'teal', 'green', 'orange', 'pink'];
  
  // Track cumulative Y position for dynamic spacing
  let currentY = startY;
  const stagePositions = [];
  
  normalizedStages.forEach((stage, i) => {
    const dims = stageDims[i];
    const color = stage.color || stageColors[i % stageColors.length];
    
    // Center horizontally based on max width
    const x = (maxWidth - dims.width) / 2 + 50;
    
    // Create rectangle with proper dimensions
    const shapeElements = rectangle(
      `stage-${i}`,
      x,
      currentY,
      dims.width,
      dims.height,
      color,
      stage.label
    );
    
    // Get actual dimensions from shape factory
    const actualWidth = shapeElements.computedWidth || dims.width;
    const actualHeight = shapeElements.computedHeight || dims.height;
    
    // Re-center based on actual width
    const actualX = (maxWidth - actualWidth) / 2 + 50;
    
    // Update x position in elements if different
    if (actualX !== x) {
      shapeElements.forEach(el => {
        if (el.x !== undefined) {
          el.x = el.x - x + actualX;
        }
      });
    }
    
    stagePositions.push({ x: actualX, y: currentY, width: actualWidth, height: actualHeight });
    elements.push(...shapeElements);
    
    // Move to next position
    currentY += actualHeight + gap;
  });
  
  // Add arrows between stages
  for (let i = 0; i < stageCount - 1; i++) {
    const current = stagePositions[i];
    const next = stagePositions[i + 1];
    const arrowX = maxWidth / 2 + 50;
    
    elements.push(...arrow(
      `arrow-${i}`,
      arrowX,
      current.y + current.height + 2,
      arrowX,
      next.y - 2
    ));
  }
  
  return wrapScene(elements);
}

/**
 * Create a mindmap diagram - center topic with branches spreading out
 * First label is the central topic, rest are branches
 * 
 * SIMPLE API: First label = center, rest = branches
 * @param {Array<string>} labels - [center, branch1, branch2, ...]
 * @example mindmap(['Main Topic', 'Branch A', 'Branch B', 'Branch C'])
 */
export function mindmap(labels) {
  resetSeeds();
  const elements = [];
  
  if (labels.length === 0) return wrapScene([]);
  
  const centerLabel = labels[0];
  const branches = labels.slice(1);
  
  // Pre-calculate center node dimensions using wrapText
  const centerWrapped = wrapText(centerLabel, 12);
  const centerTextWidth = centerWrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding;
  const centerWidth = Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, centerTextWidth));
  const centerBaseHeight = 60;
  const centerLineHeight = 20;
  const centerHeight = centerBaseHeight + Math.max(0, centerWrapped.lines - 1) * centerLineHeight;
  const centerX = 50;
  const centerY = 150;
  
  elements.push(...ellipse('center', centerX, centerY, centerWidth, centerHeight, 'blue', centerLabel));
  
  if (branches.length === 0) return wrapScene(elements);
  
  // Pre-calculate all branch dimensions for dynamic spacing
  const branchColors = ['green', 'orange', 'teal', 'pink', 'yellow', 'red'];
  const horizontalGap = 80;
  
  // Calculate dimensions for each branch using rectangle's logic
  const branchDims = branches.map(branch => {
    const wrapped = wrapText(branch, 15);
    const textWidth = wrapped.maxLineLength * DEFAULTS.charWidth + DEFAULTS.boxPadding;
    const width = Math.max(DEFAULTS.minBoxWidth, Math.min(DEFAULTS.maxBoxWidth, textWidth));
    const baseHeight = 40;
    const lineHeight = 18;
    const height = baseHeight + Math.max(0, wrapped.lines - 1) * lineHeight;
    return { width, height, wrapped };
  });
  
  // Find max width AND max height for uniform sizing (better symmetry)
  const maxBranchWidth = Math.max(...branchDims.map(d => d.width));
  const maxBranchHeight = Math.max(...branchDims.map(d => d.height));
  
  // Dynamic vertical gap: scales with box height (minimum 20px, ~40% of box height)
  const verticalGap = Math.max(20, Math.round(maxBranchHeight * 0.4));
  
  // Calculate total height for vertical centering using uniform box heights
  const totalBranchHeight = branches.length * maxBranchHeight + (branches.length - 1) * verticalGap;
  
  // Center ellipse center point
  const ellipseCenterX = centerX + centerWidth / 2;
  const ellipseCenterY = centerY + centerHeight / 2;
  const ellipseRx = centerWidth / 2;
  const ellipseRy = centerHeight / 2;
  
  // Position branches vertically centered relative to ellipse center
  let currentY = ellipseCenterY - totalBranchHeight / 2;
  const branchX = centerX + centerWidth + horizontalGap;
  
  branches.forEach((branch, i) => {
    const color = branchColors[i % branchColors.length];
    
    // Use uniform height for all boxes (maxBranchHeight) for better symmetry
    elements.push(...rectangle(`branch-${i}`, branchX, currentY, maxBranchWidth, maxBranchHeight, color, branch));
    
    // Arrow from ellipse edge to branch left edge
    const branchCenterY = currentY + maxBranchHeight / 2;
    
    // Calculate ellipse intersection: direction from ellipse center to branch center
    const dx = branchX - ellipseCenterX;
    const dy = branchCenterY - ellipseCenterY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const ux = dx / dist;
    const uy = dy / dist;
    
    // Ellipse parametric intersection
    const t = 1 / Math.sqrt((ux * ux) / (ellipseRx * ellipseRx) + (uy * uy) / (ellipseRy * ellipseRy));
    const ellipseEdgeX = ellipseCenterX + ux * t;
    const ellipseEdgeY = ellipseCenterY + uy * t;
    
    // Arrow endpoints with gaps
    const gap = 8;
    const arrowStartX = ellipseEdgeX + ux * gap;
    const arrowStartY = ellipseEdgeY + uy * gap;
    const arrowEndX = branchX - gap;
    const arrowEndY = branchCenterY;
    
    elements.push(...arrow(`arrow-${i}`, arrowStartX, arrowStartY, arrowEndX, arrowEndY));
    
    currentY += maxBranchHeight + verticalGap;
  });
  
  return wrapScene(elements);
}

/**
 * Create a pyramid/stack diagram - uniform width boxes stacked vertically
 * Height increases dynamically for long text
 * 
 * SIMPLE API: Labels from top to bottom
 * @param {Array<string>} levels - Level names from top to bottom
 * @example pyramid(['Peak', 'High', 'Medium', 'Foundation'])
 */
export function pyramid(levels) {
  resetSeeds();
  const elements = [];
  
  const levelCount = levels.length;
  if (levelCount === 0) return wrapScene([]);
  
  // Fixed width for all levels
  const boxWidth = 200;
  const baseHeight = 45;
  const gap = 8;
  const startX = 50;
  const startY = 50;
  const colors = ['blue', 'green', 'orange', 'teal', 'pink', 'yellow'];
  
  // Max chars that fit comfortably in one line
  const maxCharsPerLine = 15;
  
  let currentY = startY;
  
  levels.forEach((level, i) => {
    const color = colors[i % colors.length];
    const palette = COLORS[color] || COLORS.blue;
    
    // Calculate if we need extra height for long text
    const needsWrap = level.length > maxCharsPerLine;
    const height = needsWrap ? baseHeight + 25 : baseHeight;
    
    // Create rectangle without embedded label
    elements.push({
      ...baseElement(`level-${i}`, "rectangle", startX, currentY),
      width: boxWidth,
      height: height,
      strokeColor: palette.stroke,
      backgroundColor: palette.fill,
      fillStyle: "hachure",
      roundness: { type: 3 }
    });
    
    // Add text - use smaller font for long text
    const fontSize = needsWrap ? 16 : DEFAULTS.fontSize;
    const textY = currentY + height/2 - fontSize/2;
    
    elements.push({
      ...baseElement(`text-${i}`, "text", startX + boxWidth/2, textY),
      text: level,
      fontSize: fontSize,
      fontFamily: 1,
      textAlign: "center",
      verticalAlign: "middle",
      width: boxWidth - 20,
      height: fontSize + 4
    });
    
    currentY += height + gap;
  });
  
  return wrapScene(elements);
}

// =============================================================================
// SCENE WRAPPER
// =============================================================================

/**
 * Normalize coordinates to ensure all elements have positive x,y values
 * Adds padding to prevent elements from being at the edge
 * @param {Array} elements - Array of Excalidraw elements
 * @param {number} padding - Minimum padding from edge
 * @returns {Array} - Elements with normalized coordinates
 */
function normalizeCoordinates(elements, padding = 20) {
  if (!elements || elements.length === 0) return elements;
  
  // Find minimum x and y across all elements
  let minX = Infinity, minY = Infinity;
  
  elements.forEach(el => {
    if (typeof el.x === 'number') minX = Math.min(minX, el.x);
    if (typeof el.y === 'number') minY = Math.min(minY, el.y);
  });
  
  // Calculate offset needed to make all coordinates positive with padding
  const offsetX = minX < padding ? padding - minX : 0;
  const offsetY = minY < padding ? padding - minY : 0;
  
  // If no offset needed, return as-is
  if (offsetX === 0 && offsetY === 0) return elements;
  
  // Apply offset to all elements
  return elements.map(el => {
    const newEl = { ...el };
    if (typeof newEl.x === 'number') newEl.x += offsetX;
    if (typeof newEl.y === 'number') newEl.y += offsetY;
    return newEl;
  });
}

/**
 * Wrap elements in a complete Excalidraw scene
 */
export function wrapScene(elements) {
  // Normalize coordinates to ensure all are positive
  const normalizedElements = normalizeCoordinates(elements);
  
  return {
    type: "excalidraw",
    version: 2,
    source: "https://excalidraw.com",
    elements: normalizedElements,
    appState: DEFAULTS.appState,
    files: {}
  };
}

// =============================================================================
// EXPORTS
// =============================================================================

export default {
  DEFAULTS,
  COLORS,
  resetSeeds,
  rectangle,
  ellipse,
  diamond,
  arrow,
  text,
  // Original templates
  flowchartLR,
  flowchartTB,
  architecture,
  process,
  comparison,
  custom,
  // New creative templates
  cycle,
  radial,
  hierarchy,
  timeline,
  matrix,
  layers,
  funnel,
  mindmap,
  wrapScene
};
