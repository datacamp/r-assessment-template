#!/usr/bin/env python3
"""
Generate Exercise Preview

Reads the HTML template and injects exercise YAML to create a preview.

Usage:
    python generate_preview.py <exercise_markdown_file>
    python generate_preview.py .cursor/tmp_items/exercise_to_validate.md
"""

import sys
import re
from pathlib import Path


def extract_title_and_yaml(markdown_content: str) -> tuple[str, str]:
    """Extract the exercise title and YAML content from markdown."""
    # Extract title from heading
    title_match = re.search(r'^##\s+(.+?)$', markdown_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Exercise"
    
    # Extract YAML from code block
    yaml_match = re.search(r'```yaml\s*\n(.*?)```', markdown_content, re.DOTALL)
    yaml_content = yaml_match.group(1).strip() if yaml_match else ""
    
    return title, yaml_content


def generate_preview(exercise_file: Path, output_file: Path = None) -> Path:
    """
    Generate an HTML preview from an exercise markdown file.
    
    Args:
        exercise_file: Path to the exercise markdown file
        output_file: Path for output HTML (default: .cursor/tmp_items/exercise_preview.html)
    
    Returns:
        Path to the generated preview file
    """
    if output_file is None:
        output_file = Path(".cursor/tmp_items/exercise_preview.html")
    
    # Find the template
    script_dir = Path(__file__).parent
    template_file = script_dir / "drag_drop_classify_preview.html"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    if not exercise_file.exists():
        raise FileNotFoundError(f"Exercise file not found: {exercise_file}")
    
    # Read template and exercise
    template = template_file.read_text()
    exercise_content = exercise_file.read_text()
    
    # Extract title and YAML
    title, yaml_content = extract_title_and_yaml(exercise_content)
    
    # Add title to YAML
    yaml_with_title = f"title: {title}\n{yaml_content}"
    
    # Inject into template
    preview_html = template.replace("__EXERCISE_YAML__", yaml_with_title)
    
    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(preview_html)
    
    return output_file


def main():
    if len(sys.argv) < 2:
        print("Generate Exercise Preview")
        print("")
        print("Usage:")
        print("  python generate_preview.py <exercise_markdown_file>")
        print("")
        print("Example:")
        print("  python generate_preview.py .cursor/tmp_items/exercise_to_validate.md")
        sys.exit(1)
    
    exercise_file = Path(sys.argv[1])
    
    try:
        output = generate_preview(exercise_file)
        print(f"✅ Preview generated: {output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

