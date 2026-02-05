#!/usr/bin/env python3
"""
Generate R Coding Exercise Preview

Reads the HTML template and injects exercise data to create a preview.

Usage:
    python generate_r_preview.py <exercise_markdown_file>
    python generate_r_preview.py .cursor/tmp_items/exercise_to_validate.md
"""

import sys
import re
import json
from pathlib import Path


def extract_exercise_data(markdown_content: str) -> dict:
    """Extract exercise components from markdown."""
    content = markdown_content.strip()
    
    # Remove leading --- separator if present
    content = re.sub(r'^---\s*\n', '', content).strip()
    
    data = {
        "title": "Exercise",
        "xp": 100,
        "context": "",
        "instructions": "",
        "hint": "",
        "pre_exercise_code": "",
        "sample_code": "",
        "solution": "",
        "sct": "",
    }
    
    # Extract title from heading
    title_match = re.match(r'^##\s+(.+?)(?:\n|$)', content)
    if title_match:
        data["title"] = title_match.group(1).strip()
    
    # Extract XP from YAML block
    xp_match = re.search(r'xp:\s*(\d+)', content)
    if xp_match:
        data["xp"] = int(xp_match.group(1))
    
    # Extract context (text between yaml block closing and @instructions)
    context_match = re.search(r'```\s*\n\n(.*?)(?=`@instructions`)', content, re.DOTALL)
    if context_match:
        data["context"] = context_match.group(1).strip()
    
    # Extract sections (R uses ```r code blocks)
    sections = {
        "instructions": r'`@instructions`\s*\n(.*?)(?=`@|\Z)',
        "hint": r'`@hint`\s*\n(.*?)(?=`@|\Z)',
        "pre_exercise_code": r'`@pre_exercise_code`\s*\n```r\s*\n(.*?)```',
        "sample_code": r'`@sample_code`\s*\n```r\s*\n(.*?)```',
        "solution": r'`@solution`\s*\n```r\s*\n(.*?)```',
        "sct": r'`@sct`\s*\n```r\s*\n(.*?)```',
    }
    
    for section_name, pattern in sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            data[section_name] = match.group(1).strip()
    
    return data


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
    template_file = script_dir / "r_coding_preview.html"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    if not exercise_file.exists():
        raise FileNotFoundError(f"Exercise file not found: {exercise_file}")
    
    # Read template and exercise
    template = template_file.read_text()
    exercise_content = exercise_file.read_text()
    
    # Extract exercise data
    exercise_data = extract_exercise_data(exercise_content)
    
    # Convert to JSON for injection
    exercise_json = json.dumps(exercise_data, indent=2)
    
    # Inject into template
    preview_html = template.replace("__EXERCISE_DATA__", exercise_json)
    
    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(preview_html)
    
    return output_file


def main():
    if len(sys.argv) < 2:
        print("Generate R Coding Exercise Preview")
        print("")
        print("Usage:")
        print("  python generate_r_preview.py <exercise_markdown_file>")
        print("")
        print("Example:")
        print("  python generate_r_preview.py .cursor/tmp_items/exercise_to_validate.md")
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
