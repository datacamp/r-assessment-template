#!/bin/bash
# Verification script for DataCamp Curriculum Assistant
# Run this to verify all services are working correctly
#
# Uses the project's virtual environment (.venv/) for Python checks.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
SKIPPED=0

# Get directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/../.."
VENV_DIR="$PROJECT_DIR/.venv"

# Use virtual environment Python if available
if [ -f "$VENV_DIR/bin/python" ]; then
    PYTHON="$VENV_DIR/bin/python"
    source "$VENV_DIR/bin/activate" 2>/dev/null
else
    PYTHON="python3"
fi

# Temp directory for test outputs (cleaned up on exit)
TEST_DIR="/tmp/datacamp_verify_$$"
mkdir -p "$TEST_DIR"
trap "rm -rf $TEST_DIR" EXIT

echo ""
echo "=========================================="
echo "  DataCamp Curriculum Assistant"
echo "  Setup Verification"
echo "=========================================="
echo ""

pass() { echo -e "   ${GREEN}✓${NC} $1"; ((PASSED++)); }
fail() { echo -e "   ${RED}✗${NC} $1"; ((FAILED++)); }
skip() { echo -e "   ${YELLOW}○${NC} $1 (skipped)"; ((SKIPPED++)); }

# 1. DEPENDENCIES
echo -e "${BLUE}1. Checking Dependencies${NC}"
echo ""
if [ -f "$VENV_DIR/bin/python" ]; then
    pass "Python venv ($($PYTHON --version 2>&1))"
elif command -v python3 &>/dev/null; then
    pass "Python 3 ($(python3 --version 2>&1)) - Note: Run setup.sh to create .venv"
else
    fail "Python 3 not found"
fi
if command -v node &>/dev/null; then
    pass "Node.js ($(node --version))"
else
    fail "Node.js not found"
fi
if command -v npm &>/dev/null; then
    pass "npm (v$(npm --version))"
else
    fail "npm not found"
fi
echo ""

# 2. PYTHON PACKAGES
echo -e "${BLUE}2. Checking Python Packages${NC}"
echo ""
if [ ! -f "$VENV_DIR/bin/python" ]; then
    fail "Virtual environment not found - run setup.sh first"
else
    $PYTHON -c "import datalab_sdk" 2>/dev/null && pass "datalab-python-sdk" || fail "datalab-python-sdk"
    $PYTHON -c "import docling" 2>/dev/null && pass "docling" || fail "docling"
    $PYTHON -c "import youtube_transcript_api" 2>/dev/null && pass "youtube-transcript-api" || fail "youtube-transcript-api"
    $PYTHON -c "import trafilatura" 2>/dev/null && pass "trafilatura" || fail "trafilatura"
    $PYTHON -c "import dotenv" 2>/dev/null && pass "python-dotenv" || fail "python-dotenv"
    $PYTHON -c "import brotli" 2>/dev/null && pass "brotli" || fail "brotli"
fi
echo ""

# 3. NODE.JS PACKAGES
echo -e "${BLUE}3. Checking Node.js Packages${NC}"
echo ""
cd "$PROJECT_DIR"
node -e "require('puppeteer')" 2>/dev/null && pass "puppeteer" || fail "puppeteer (run: npm install)"
node -e "require('sharp')" 2>/dev/null && pass "sharp" || fail "sharp (run: npm install)"
echo ""

# 4. API KEYS & CONFIGURATION
echo -e "${BLUE}4. Checking API Configuration${NC}"
echo ""
ENV_FILE="$SCRIPT_DIR/../.env"
HAS_API_KEY=false
HAS_DCT=false
HAS_REPO=false

if [ -f "$ENV_FILE" ]; then
    if grep -q "DATALAB_API_KEY=" "$ENV_FILE" 2>/dev/null; then
        pass "DATALAB_API_KEY configured (PDF conversion)"
        HAS_API_KEY=true
    else
        skip "DATALAB_API_KEY not set (PDF conversion disabled)"
    fi
    
    if grep -q "DATACAMP_DCT=" "$ENV_FILE" 2>/dev/null; then
        pass "DATACAMP_DCT configured (asset upload)"
        HAS_DCT=true
    else
        fail "DATACAMP_DCT not set (required for asset upload)"
    fi
    
    if grep -q "DATACAMP_REPO=" "$ENV_FILE" 2>/dev/null; then
        pass "DATACAMP_REPO configured (asset upload)"
        HAS_REPO=true
    else
        fail "DATACAMP_REPO not set (required for asset upload)"
    fi
else
    fail ".cursor/.env file not found"
fi
echo ""

# 5. CONVERTER TESTS
echo -e "${BLUE}5. Testing Converters${NC}"
echo ""

if [ ! -f "$VENV_DIR/bin/python" ]; then
    skip "Converters (run setup.sh first)"
else
    echo "   Testing webpage converter..."
    if $PYTHON "$SCRIPT_DIR/converters/convert_webpage.py" "https://example.com" -o "$TEST_DIR/web.md" 2>/dev/null && [ -s "$TEST_DIR/web.md" ]; then
        pass "Webpage → Markdown"
    else
        fail "Webpage → Markdown"
    fi

    echo "   Testing YouTube converter..."
    if $PYTHON "$SCRIPT_DIR/converters/convert_youtube.py" "https://www.youtube.com/watch?v=gXwewPgLmkE" -o "$TEST_DIR/yt.md" 2>/dev/null && [ -s "$TEST_DIR/yt.md" ]; then
        pass "YouTube → Transcript"
    else
        fail "YouTube → Transcript"
    fi

    echo "   Testing PDF converter..."
    if [ "$HAS_API_KEY" = true ]; then
        $PYTHON -c "import sys; sys.path.insert(0,'$SCRIPT_DIR/converters'); from convert_pdf import convert_pdf_to_markdown" 2>/dev/null && pass "PDF converter ready" || fail "PDF converter"
    else
        skip "PDF → Markdown (no API key)"
    fi
fi
echo ""

# 6. EXCALIDRAW
echo -e "${BLUE}6. Testing Excalidraw Diagram Generation${NC}"
echo ""
cat > "$TEST_DIR/test.md" << 'EOF'
## Test
`@part1`
![excalidraw: flowchart: A, B, C]()
EOF

echo "   Generating test diagram..."
cd "$PROJECT_DIR"
if node .cursor/utilities/excalidraw/from_script.mjs "$TEST_DIR/test.md" --chapter 999 --lesson 999 --output "$TEST_DIR" 2>/dev/null; then
    # Find any generated PNG (new naming: lesson_999_999_image_1_*.png)
    PNG_FILE=$(find "$TEST_DIR" -name "lesson_999_999_image_1_*.png" -type f 2>/dev/null | head -1)
    if [ -n "$PNG_FILE" ] && [ -f "$PNG_FILE" ]; then
        SIZE=$(wc -c < "$PNG_FILE")
        [ "$SIZE" -gt 1000 ] && pass "Excalidraw PNG (${SIZE} bytes)" || fail "Excalidraw PNG (too small)"
    else
        fail "Excalidraw PNG (no output)"
    fi
else
    fail "Excalidraw PNG (command failed)"
fi
echo ""

# 7. FILE STRUCTURE
echo -e "${BLUE}7. Checking File Structure${NC}"
echo ""
[ -d "$SCRIPT_DIR/converters" ] && pass "converters/" || fail "converters/"
[ -d "$SCRIPT_DIR/excalidraw" ] && pass "excalidraw/" || fail "excalidraw/"
[ -f "$SCRIPT_DIR/excalidraw/from_script.mjs" ] && pass "from_script.mjs" || fail "from_script.mjs"
[ -f "$SCRIPT_DIR/excalidraw/templates.mjs" ] && pass "templates.mjs" || fail "templates.mjs"
echo ""

# SUMMARY
echo "=========================================="
echo "  Summary"
echo "=========================================="
echo ""
echo -e "   ${GREEN}Passed:${NC}  $PASSED"
echo -e "   ${RED}Failed:${NC}  $FAILED"
echo -e "   ${YELLOW}Skipped:${NC} $SKIPPED"
echo ""
if [ $FAILED -eq 0 ]; then
    echo -e "   ${GREEN}All checks passed! Ready for content creation.${NC}"
elif [ "$HAS_DCT" = false ] || [ "$HAS_REPO" = false ]; then
    echo -e "   ${RED}Missing required configuration.${NC}"
    echo "   Add to .cursor/.env:"
    [ "$HAS_DCT" = false ] && echo "     DATACAMP_DCT=your_cookie_value"
    [ "$HAS_REPO" = false ] && echo "     DATACAMP_REPO=https://github.com/datacamp-content/courses-..."
else
    echo -e "   ${RED}Some checks failed.${NC}"
    echo "   Fix: Run .cursor/utilities/setup.sh"
fi
echo ""
echo "=========================================="
exit $FAILED
