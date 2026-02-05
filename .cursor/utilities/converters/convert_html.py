#!/usr/bin/env python3
"""
HTML to Markdown Converter using Docling

Usage:
    python convert_html.py <input_html> [-o output.md]
    
Example:
    python .cursor/utilities/converters/convert_html.py context/page.html -o context/context-final/page.md
"""

import argparse
import sys
from pathlib import Path


def convert_html_to_markdown(input_path: str, output_path: str = None) -> str:
    """Convert an HTML file to Markdown using Docling."""
    
    # Import here to allow script to show help even if not installed
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("Error: docling not installed.")
        print("Run: pip install docling")
        sys.exit(1)
    
    # Verify input file exists
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    # Set default output path
    if output_path is None:
        output_path = input_file.with_suffix(".md")
    
    output_file = Path(output_path)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {input_path}")
    print(f"Output: {output_path}")
    
    try:
        # Initialize converter and convert
        converter = DocumentConverter()
        result = converter.convert(str(input_file))
        
        # Export to markdown
        markdown_content = result.document.export_to_markdown()
        
        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"✓ Conversion complete: {output_path}")
        return markdown_content
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML to Markdown using Docling"
    )
    parser.add_argument(
        "input",
        help="Path to input HTML file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output Markdown file (default: same name with .md extension)"
    )
    
    args = parser.parse_args()
    convert_html_to_markdown(args.input, args.output)


if __name__ == "__main__":
    main()
