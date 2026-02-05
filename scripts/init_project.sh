#!/bin/bash

# Initialize assessment project structure for chosen mode
# Usage: ./scripts/init_project.sh [chapter|track|standalone]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Get mode from argument or prompt
if [ -n "$1" ]; then
    MODE="$1"
else
    echo "Select assessment mode:"
    echo "  1) chapter    - Single course chapter assessments"
    echo "  2) track      - Multi-course track assessments"
    echo "  3) standalone - Certification pools (new or existing repos)"
    echo ""
    read -p "Enter mode (chapter/track/standalone) or number (1/2/3): " MODE
    
    # Convert numbers to mode names
    case $MODE in
        1) MODE="chapter" ;;
        2) MODE="track" ;;
        3) MODE="standalone" ;;
    esac
fi

# Validate mode
if [[ ! "$MODE" =~ ^(chapter|track|standalone)$ ]]; then
    echo "Error: Invalid mode '$MODE'. Use: chapter, track, or standalone"
    exit 1
fi

echo ""
echo "Initializing $MODE mode..."
echo ""

case $MODE in
    chapter)
        mkdir -p "$REPO_ROOT/context/slides"
        mkdir -p "$REPO_ROOT/context/exercises"
        
        # Create project.yaml
        cat > "$REPO_ROOT/.cursor/project.yaml" << 'YAML'
mode: chapter

chapter:
  course_repo: ""  # Add your course repo here
  chapters: [1, 2, 3, 4]
YAML
        
        print_success "Created context/slides/"
        print_success "Created context/exercises/"
        print_success "Created .cursor/project.yaml"
        echo ""
        print_info "Next steps:"
        echo "  1. Copy video scripts to context/slides/chapter_X.md"
        echo "  2. Copy exercise files to context/exercises/chapterX.md"
        echo "  3. Update .cursor/project.yaml with your course repo"
        echo "  4. Start generating: 'Create MCQs for Chapter 1 based on @context/slides/chapter_1.md'"
        ;;
        
    track)
        mkdir -p "$REPO_ROOT/context"
        
        # Create project.yaml
        cat > "$REPO_ROOT/.cursor/project.yaml" << 'YAML'
mode: track

track:
  track_name: ""  # Add your track name
  courses: []     # Add courses as shown in project.yaml.example
YAML
        
        # Create track_los.md template
        cat > "$REPO_ROOT/context/track_los.md" << 'MD'
# Track Learning Objectives

## Track Name: [Your Track Name]

### Course 1: [Course Name]
- LO 1.1: ...
- LO 1.2: ...

### Course 2: [Course Name]
- LO 2.1: ...
- LO 2.2: ...

## Cross-Course Themes
- Theme 1: Covered in courses X, Y
- Theme 2: Covered in courses Y, Z
MD
        
        print_success "Created context/"
        print_success "Created context/track_los.md template"
        print_success "Created .cursor/project.yaml"
        echo ""
        print_info "Next steps:"
        echo "  1. Download course content from DataCamp Teach for each course"
        echo "  2. Create folders: context/{course_name}/ for each course"
        echo "  3. Copy slides and exercises into each course folder"
        echo "  4. Update .cursor/project.yaml with course list"
        echo "  5. Fill in context/track_los.md with track objectives"
        echo "  6. Start generating: 'Create items covering [topic] across the track'"
        ;;
        
    standalone)
        mkdir -p "$REPO_ROOT/context/existing_items"
        mkdir -p "$REPO_ROOT/context/reference_docs"
        
        # Create project.yaml
        cat > "$REPO_ROOT/.cursor/project.yaml" << 'YAML'
mode: standalone

standalone:
  pool_name: ""  # Add your pool name
  reference_items: "context/existing_items/"
  reference_docs: "context/reference_docs/"
YAML
        
        # Create item_coverage.md template
        cat > "$REPO_ROOT/context/item_coverage.md" << 'MD'
# Item Coverage Tracker

## Pool Name: [Your Pool Name]

### Topics Covered
Track which topics/skills are already covered by existing items.

| Topic | # Items | Item IDs/Files | Notes |
|-------|---------|----------------|-------|
| Example: pandas basics | 5 | pool_v1.md #1-5 | Good coverage |
| Example: SQL joins | 2 | pool_v2.md #1-2 | Need more items |

### Topics Needed
- [ ] Topic A - need X items
- [ ] Topic B - need Y items

### Duplication Notes
Track any overlap or near-duplicates to avoid.
MD
        
        print_success "Created context/existing_items/"
        print_success "Created context/reference_docs/"
        print_success "Created context/item_coverage.md template"
        print_success "Created .cursor/project.yaml"
        echo ""
        print_info "Next steps:"
        echo "  1. Copy existing pool items to context/existing_items/"
        echo "  2. Add any reference docs to context/reference_docs/"
        echo "  3. Fill in context/item_coverage.md with current coverage"
        echo "  4. Update .cursor/project.yaml with pool name"
        echo "  5. Start generating: 'Create 5 MCQs on [topic] avoiding duplicates with @context/existing_items/'"
        ;;
esac

echo ""
print_success "Project initialized in $MODE mode!"
