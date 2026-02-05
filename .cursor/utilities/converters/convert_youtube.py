#!/usr/bin/env python3
"""
YouTube Transcript to Markdown Converter

Usage:
    python convert_youtube.py <youtube_url> [-o output.md]
    
Example:
    python .cursor/utilities/converters/convert_youtube.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o context/context-final/video.md
"""

import argparse
import re
import sys
from pathlib import Path


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/watch\?.*v=)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Maybe it's already just the video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    return None


def convert_youtube_to_markdown(url: str, output_path: str = None) -> str:
    """Convert YouTube video transcript to Markdown."""
    
    # Import here to allow script to show help even if not installed
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Error: youtube-transcript-api not installed.")
        print("Run: pip install youtube-transcript-api")
        sys.exit(1)
    
    # Extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Error: Could not extract video ID from URL: {url}")
        sys.exit(1)
    
    print(f"Video ID: {video_id}")
    
    # Set default output path
    if output_path is None:
        output_path = f"youtube_{video_id}.md"
    
    output_file = Path(output_path)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Fetching transcript...")
    
    try:
        # New API (v1.0+): use fetch() method
        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id)
        language = 'en'
        
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        sys.exit(1)
    
    # Build markdown content (plain text, no timestamps)
    lines = []
    lines.append(f"# YouTube Video Transcript")
    lines.append(f"")
    lines.append(f"**Video URL:** https://www.youtube.com/watch?v={video_id}")
    lines.append(f"**Language:** {language}")
    lines.append(f"")
    lines.append("---")
    lines.append("")
    
    # Combine transcript segments into paragraphs
    current_paragraph = []
    for entry in transcript_data:
        text = entry.text.strip() if hasattr(entry, 'text') else entry.get('text', '').strip()
        if text:
            current_paragraph.append(text)
            # Start new paragraph after sentences ending with period
            if text.endswith('.') or text.endswith('?') or text.endswith('!'):
                lines.append(' '.join(current_paragraph))
                lines.append("")
                current_paragraph = []
    
    # Add any remaining text
    if current_paragraph:
        lines.append(' '.join(current_paragraph))
    
    markdown_content = '\n'.join(lines)
    
    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"✓ Transcript saved: {output_path}")
    return markdown_content


def main():
    parser = argparse.ArgumentParser(
        description="Convert YouTube video transcript to Markdown"
    )
    parser.add_argument(
        "url",
        help="YouTube video URL or video ID"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output Markdown file (default: youtube_<video_id>.md)"
    )
    
    args = parser.parse_args()
    convert_youtube_to_markdown(args.url, args.output)


if __name__ == "__main__":
    main()
