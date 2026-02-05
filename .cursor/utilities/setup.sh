#!/bin/bash
# Setup script for DataCamp Curriculum Assistant
# Run this once to install all dependencies
#
# Creates a project-local virtual environment (.venv/) to ensure
# consistent Python package management across all machines.

set -e  # Exit on error

echo "=========================================="
echo "DataCamp Curriculum Assistant Setup"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/../.."
VENV_DIR="$PROJECT_DIR/.venv"

# =============================================================================
# PYTHON VIRTUAL ENVIRONMENT SETUP
# =============================================================================

echo "📦 Setting up Python environment..."
echo ""

# Find best Python (prefer 3.10+ for full compatibility)
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd -c 'import sys; print(sys.version_info.minor)')
        if [ "$VERSION" -ge 10 ] 2>/dev/null; then
            PYTHON_CMD=$cmd
            break
        elif [ -z "$PYTHON_CMD" ]; then
            PYTHON_CMD=$cmd  # Fallback to any python3
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo "   Using: $PYTHON_CMD ($PYTHON_VERSION)"

# Check version and warn if too old
MINOR_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
if [ "$MINOR_VERSION" -lt 10 ]; then
    echo "   ⚠️  Warning: Python 3.10+ recommended for full functionality"
    echo "      Some packages (datalab-python-sdk) require Python 3.10+"
    echo "      PDF conversion may not be available."
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "   Creating virtual environment at .venv/..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment exists at .venv/"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "   ✅ Virtual environment activated"

# Upgrade pip
echo "   Upgrading pip..."
pip install --upgrade pip -q

# Install Python dependencies
if [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
    echo "   Installing Python packages..."
    
    # Install core packages (work on Python 3.9+)
    pip install -q trafilatura youtube-transcript-api python-dotenv brotli 2>/dev/null && \
        echo "   ✅ Core packages installed (trafilatura, youtube-transcript-api, etc.)"
    
    # Install packages requiring Python 3.10+ (may fail on older Python)
    if [ "$MINOR_VERSION" -ge 10 ]; then
        pip install -q datalab-python-sdk docling 2>/dev/null && \
            echo "   ✅ Advanced packages installed (datalab-python-sdk, docling)"
    else
        echo "   ⚠️  Skipped: datalab-python-sdk, docling (require Python 3.10+)"
    fi
fi

echo ""

# =============================================================================
# NODE.JS SETUP
# =============================================================================

echo "📦 Setting up Node.js dependencies..."
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is required but not installed."
    echo "   Install from: https://nodejs.org/"
    exit 1
fi

echo "   Node version: $(node --version)"
echo "   npm version: $(npm --version)"

# Install Node.js dependencies
cd "$PROJECT_DIR"
if [ -f "package.json" ]; then
    echo "   Installing Node.js packages..."
    npm install --silent
    echo "   ✅ Node.js dependencies installed (puppeteer, sharp)"
fi

echo ""

# =============================================================================
# VERIFY INSTALLATION
# =============================================================================

echo "🔍 Verifying installation..."
echo ""

# Check Python converters
if [ -f "$SCRIPT_DIR/converters/convert_pdf.py" ]; then
    echo "   ✅ Python converters found"
else
    echo "   ⚠️  Python converters not found at $SCRIPT_DIR/converters/"
fi

# Check Excalidraw tools
if [ -f "$SCRIPT_DIR/excalidraw/from_script.mjs" ]; then
    echo "   ✅ Excalidraw tools found"
else
    echo "   ⚠️  Excalidraw tools not found at $SCRIPT_DIR/excalidraw/"
fi

# Test puppeteer installation
cd "$PROJECT_DIR"
if node -e "require('puppeteer')" 2>/dev/null; then
    echo "   ✅ Puppeteer installed correctly"
else
    echo "   ⚠️  Puppeteer not installed - run 'npm install' in project root"
fi

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Folder Structure:"
echo ""
echo "  .cursor/utilities/"
echo "  ├── converters/           # Python content converters"
echo "  │   ├── convert_pdf.py"
echo "  │   ├── convert_html.py"
echo "  │   ├── convert_webpage.py"
echo "  │   └── convert_youtube.py"
echo "  ├── excalidraw/           # Diagram generation (Node.js)"
echo "  │   ├── from_script.mjs   # Main CLI tool"
echo "  │   ├── templates.mjs     # Diagram templates"
echo "  │   └── to_png.mjs        # PNG conversion"
echo "  └── setup.sh              # This script"
echo ""
echo "Available Commands:"
echo ""
echo "  📝 Content Converters:"
echo "     python $SCRIPT_DIR/converters/convert_pdf.py <file.pdf>"
echo "     python $SCRIPT_DIR/converters/convert_html.py <file.html>"
echo "     python $SCRIPT_DIR/converters/convert_youtube.py <url>"
echo "     python $SCRIPT_DIR/converters/convert_webpage.py <url>"
echo ""
echo "  🎨 Excalidraw Diagram Generator:"
echo "     node $SCRIPT_DIR/excalidraw/from_script.mjs <script.md> --chapter N --lesson M"
echo ""
echo "     Or use npm script (from project root):"
echo "     npm run excalidraw -- <script.md> --chapter N --lesson M --update"
echo ""
echo "Available Templates:"
echo "     flowchart, cycle, radial, hierarchy, layers,"
echo "     timeline (year|desc, // breaks), funnel, mindmap,"
echo "     matrix, comparison, architecture"
echo ""
echo "Notes:"
echo "  - PDF conversion requires DATALAB_API_KEY in .cursor/.env"
echo "  - Asset upload requires DATACAMP_DCT and DATACAMP_REPO in .cursor/.env"
echo "  - Diagrams use Virgil (hand-drawn) font with transparent backgrounds"
echo "  - Use --update flag to auto-replace placeholders in source file"
echo "  - All templates support dynamic text wrapping for long labels"
echo ""
echo "Verify Setup:"
echo "  Run .cursor/utilities/verify_setup.sh to test all services"
echo ""
