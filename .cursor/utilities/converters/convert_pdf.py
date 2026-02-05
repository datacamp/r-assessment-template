#!/usr/bin/env python3
"""
PDF to Markdown Converter using Datalab API

Usage:
    python convert_pdf.py <input_pdf> [-o output.md]
    
Example:
    python .cursor/utilities/converters/convert_pdf.py context/document.pdf -o context/context-final/document.md

Reference: https://documentation.datalab.to/docs/welcome/sdk/conversion
"""

import argparse
import os
import sys
from pathlib import Path

# Load environment variables from .cursor/.env
from dotenv import load_dotenv

# Find the .cursor directory relative to this script
script_dir = Path(__file__).parent.parent
env_path = script_dir / ".env"
load_dotenv(env_path)

def convert_pdf_to_markdown(input_path: str, output_path: str = None) -> str:
    """Convert a PDF file to Markdown using Datalab API."""
    
    # Import here to allow script to show help even if SDK not installed
    try:
        from datalab_sdk import DatalabClient, ConvertOptions
    except ImportError:
        print("Error: datalab-python-sdk not installed.")
        print("Run: pip install datalab-python-sdk")
        sys.exit(1)
    
    # Check for API key
    api_key = os.getenv("DATALAB_API_KEY")
    if not api_key:
        print("Error: DATALAB_API_KEY not found.")
        print(f"Please add your API key to {env_path}")
        sys.exit(1)
    
    # Set the environment variable for the SDK
    os.environ["DATALAB_API_KEY"] = api_key
    
    # Verify input file exists
    input_file = Path(input_path).resolve()  # Use absolute path
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    if not input_file.suffix.lower() == ".pdf":
        print(f"Warning: File may not be a PDF: {input_path}")
    
    # Set default output path
    if output_path is None:
        output_path = input_file.with_suffix(".md")
    
    output_file = Path(output_path)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {input_file}")
    print(f"Output: {output_path}")
    
    try:
        # Initialize client (uses DATALAB_API_KEY env var)
        client = DatalabClient()
        
        # Set conversion options
        options = ConvertOptions(
            output_format="markdown",
            mode="balanced",
        )
        
        # Convert the PDF
        result = client.convert(str(input_file), options=options)
        
        if not result.success:
            print(f"Error: Conversion failed - {result.error}")
            sys.exit(1)
        
        # Write markdown output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        
        print(f"✓ Conversion complete: {output_path}")
        print(f"  Pages processed: {result.page_count}")
        print(f"  Quality score: {result.parse_quality_score}")
        return result.markdown
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown using Datalab API"
    )
    parser.add_argument(
        "input",
        help="Path to input PDF file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output Markdown file (default: same name with .md extension)"
    )
    
    args = parser.parse_args()
    convert_pdf_to_markdown(args.input, args.output)


if __name__ == "__main__":
    main()
