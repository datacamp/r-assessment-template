#!/usr/bin/env python3
"""
Web Page to Markdown Converter using Trafilatura

Extracts main content from web pages (articles, documentation, etc.)
and converts to clean Markdown.

Usage:
    python convert_webpage.py <url> [-o output.md]
    
Example:
    python .cursor/utilities/converters/convert_webpage.py "https://r4ds.hadley.nz/missing-values.html" -o context/context-final/missing-values.md
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def url_to_filename(url: str) -> str:
    """Generate a filename from a URL."""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    
    if path:
        # Use the last part of the path
        name = path.split('/')[-1]
        # Remove extension if present
        name = re.sub(r'\.[^.]+$', '', name)
    else:
        # Use domain name
        name = parsed.netloc.replace('.', '_')
    
    # Clean up the name
    name = re.sub(r'[^\w\-]', '_', name)
    name = re.sub(r'_+', '_', name)
    
    return f"{name}.md"


def convert_webpage_to_markdown(url: str, output_path: str = None) -> str:
    """Convert a web page to Markdown using Trafilatura."""
    
    # Import here to allow script to show help even if not installed
    try:
        import trafilatura
    except ImportError:
        print("Error: trafilatura not installed.")
        print("Run: pip install trafilatura")
        sys.exit(1)
    
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    
    # Set default output path
    if output_path is None:
        output_path = url_to_filename(url)
    
    output_file = Path(output_path)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Fetching: {url}")
    
    try:
        # Download the page
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is None:
            print(f"Error: Could not fetch URL: {url}")
            sys.exit(1)
        
        # Extract main content as markdown
        markdown_content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_links=True,
            include_images=False,  # Skip images for cleaner output
            include_tables=True,
            include_comments=False,
            favor_precision=True,  # Prefer precision over recall
        )
        
        if markdown_content is None:
            print("Error: Could not extract content from page")
            sys.exit(1)
        
        # Add source URL header
        header = f"# Web Page Content\n\n**Source:** {url}\n\n---\n\n"
        full_content = header + markdown_content
        
        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        
        print(f"✓ Content saved: {output_path}")
        return full_content
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert web page to Markdown using Trafilatura"
    )
    parser.add_argument(
        "url",
        help="URL of the web page to convert"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output Markdown file (default: generated from URL)"
    )
    
    args = parser.parse_args()
    convert_webpage_to_markdown(args.url, args.output)


if __name__ == "__main__":
    main()
