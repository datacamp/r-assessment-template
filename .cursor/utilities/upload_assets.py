#!/usr/bin/env python3
"""
DataCamp Asset Upload Script

Uploads local images from markdown files to DataCamp's asset system
and updates the markdown with public URLs.

Usage:
    # Upload all images referenced in a markdown file (uses DATACAMP_REPO from .env)
    python .cursor/utilities/upload_assets.py slides/chapter_1.md --update
    
    # Or override with explicit repo
    python .cursor/utilities/upload_assets.py slides/chapter_1.md --repo https://github.com/datacamp/courses-example --update
    
    # Preview changes without writing (dry run)
    python .cursor/utilities/upload_assets.py slides/chapter_1.md

Environment (.cursor/.env):
    DATACAMP_DCT: Your DataCamp _dct cookie value (required)
    DATACAMP_REPO: GitHub URL or repository ID (required for video workflow)
"""

import requests
import os
import sys
import re
import argparse
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

DOMAIN = 'datacamp.com'


def load_env():
    """Load environment variables from .cursor/.env file"""
    script_dir = Path(__file__).parent.parent  # .cursor directory
    env_path = script_dir / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)


def load_dct_cookie():
    """
    Load DCT cookie from .cursor/.env file
    
    Returns:
        str: The DCT cookie value
    
    Raises:
        ValueError: If DATACAMP_DCT is not set
    """
    load_env()
    
    dct = os.getenv('DATACAMP_DCT')
    if not dct:
        raise ValueError(
            "DATACAMP_DCT environment variable not set.\n"
            "Add DATACAMP_DCT=your_cookie_value to .cursor/.env"
        )
    return dct


def load_repo():
    """
    Load repository from .cursor/.env file
    
    Returns:
        str: The repository URL or ID, or None if not set
    """
    load_env()
    return os.getenv('DATACAMP_REPO')


def find_repository_by_github_url(github_url, dct):
    """
    Find DataCamp repository ID by GitHub repository URL
    
    Args:
        github_url (str): GitHub repository URL
        dct (str): DCT cookie value
    
    Returns:
        int: Repository ID from DataCamp
    """
    # Parse GitHub URL to extract owner/repo
    parsed_url = urlparse(github_url)
    if parsed_url.hostname not in ['github.com', 'www.github.com']:
        raise ValueError(f"Invalid GitHub URL: {github_url}")
    
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GitHub repository URL format: {github_url}")
    
    repo_name = f"{path_parts[0]}/{path_parts[1]}"
    
    # Search for repository using teach-api
    search_url = f"https://teach-api.{DOMAIN}/teach-browser/repositories/course"
    params = {
        'limit': 10,
        'search': repo_name,
        'datacampOnly': 0,
        'offset': 0
    }
    
    headers = {'accept': 'application/json'}
    cookies = {'_dct': dct}
    
    response = requests.get(
        search_url,
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    
    for repo in data.get('repositories', []):
        if repo.get('githubRepoName') == repo_name:
            return repo['id']
    
    raise ValueError(f"Repository '{repo_name}' not found in DataCamp")


def is_github_url(url_or_id):
    """Check if the input is a GitHub URL or a repository ID"""
    return url_or_id.startswith(('http://', 'https://')) and 'github.com' in url_or_id


def upload_asset(file_path, output_filename, repository_id, dct):
    """
    Upload an asset file to DataCamp teach editor
    
    Args:
        file_path (str): Path to the file to upload
        output_filename (str): Output filename
        repository_id (str): Repository ID
        dct (str): DCT cookie value
    
    Returns:
        dict: Response containing 'id' and 'public_url'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    url = f"https://www.{DOMAIN}/teach/editor/repositories/{repository_id}/branches/master/create_dataset"
    
    headers = {
        'accept': 'application/json',
        'origin': f'https://www.{DOMAIN}',
    }
    
    cookies = {'_dct': dct}
    
    with open(file_path, 'rb') as f:
        files = {
            'outputFileName': (None, output_filename),
            'file': (output_filename, f, 'application/octet-stream')
        }
        
        response = requests.post(
            url,
            headers=headers,
            cookies=cookies,
            files=files,
            timeout=60
        )
    
    response.raise_for_status()
    return response.json()


def find_local_images(markdown_content):
    """
    Find all local image references in markdown content
    
    Matches patterns like:
    - ![alt](images/lesson_1_1/lesson_1_1_image_1_description.png)
    - ![flowchart: ...](images/lesson_1_1/lesson_1_1_image_1_flowchart_a_b_c.png)
    
    Args:
        markdown_content (str): The markdown content to parse
    
    Returns:
        list: List of tuples (full_match, alt_text, local_path)
    """
    # Match markdown images with local paths (not http/https URLs)
    pattern = r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg))\)'
    matches = []
    
    for match in re.finditer(pattern, markdown_content, re.IGNORECASE):
        full_match = match.group(0)
        alt_text = match.group(1)
        path = match.group(2)
        
        # Skip if it's already a URL
        if path.startswith(('http://', 'https://')):
            continue
        
        matches.append((full_match, alt_text, path))
    
    return matches


def process_markdown_file(markdown_path, repository_id, dct, update=False):
    """
    Process a markdown file, upload local images, and optionally update the file
    
    Args:
        markdown_path (str): Path to the markdown file
        repository_id (str): DataCamp repository ID
        dct (str): DCT cookie value
        update (bool): Whether to write changes back to the file
    
    Returns:
        tuple: (updated_content, upload_results)
    """
    markdown_path = Path(markdown_path)
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    
    content = markdown_path.read_text(encoding='utf-8')
    images = find_local_images(content)
    
    if not images:
        print("No local images found in markdown file.")
        return content, []
    
    print(f"Found {len(images)} local image(s) to upload:\n")
    
    results = []
    updated_content = content
    
    for full_match, alt_text, local_path in images:
        # Resolve the image path relative to the markdown file
        image_path = markdown_path.parent / local_path
        
        if not image_path.exists():
            # Try from workspace root
            image_path = Path(local_path)
        
        if not image_path.exists():
            print(f"  ⚠️  Skipping (not found): {local_path}")
            continue
        
        output_filename = image_path.name
        print(f"  📤 Uploading: {local_path}")
        
        try:
            result = upload_asset(
                str(image_path),
                output_filename,
                repository_id,
                dct
            )
            
            public_url = result.get('public_url')
            if public_url:
                # Ensure URL has https:// prefix
                if not public_url.startswith(('http://', 'https://')):
                    public_url = f"https://{public_url}"
                
                # Replace local path with public URL
                new_image = f"![{alt_text}]({public_url})"
                updated_content = updated_content.replace(full_match, new_image)
                
                results.append({
                    'local_path': local_path,
                    'public_url': public_url,
                    'asset_id': result.get('id')
                })
                
                print(f"     ✅ Uploaded: {public_url}")
            else:
                print(f"     ❌ No public URL returned")
                
        except Exception as e:
            print(f"     ❌ Failed: {str(e)}")
    
    if update and results:
        markdown_path.write_text(updated_content, encoding='utf-8')
        print(f"\n✅ Updated {markdown_path} with {len(results)} new URL(s)")
    elif results:
        print(f"\n📋 Dry run complete. Use --update to write changes.")
    
    return updated_content, results


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(
        description='Upload local images from markdown to DataCamp assets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload images using DATACAMP_REPO from .env
  python upload_assets.py slides/chapter_1.md --update
  
  # Override repo with explicit URL
  python upload_assets.py slides/chapter_1.md --repo https://github.com/datacamp/courses-example --update
  
  # Preview what would be uploaded (dry run)
  python upload_assets.py slides/chapter_1.md
  
  # Upload a single image file
  python upload_assets.py --file images/diagram.png --name my-diagram.png
"""
    )
    
    parser.add_argument(
        'markdown_file',
        nargs='?',
        help='Markdown file to process for local images'
    )
    
    parser.add_argument(
        '--repo', '-r',
        help='GitHub URL or DataCamp repository ID (default: DATACAMP_REPO from .env)'
    )
    
    parser.add_argument(
        '--update', '-u',
        action='store_true',
        help='Update the markdown file with uploaded URLs'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Single file to upload (instead of processing markdown)'
    )
    
    parser.add_argument(
        '--name', '-n',
        help='Output filename for single file upload (default: original filename)'
    )
    
    args = parser.parse_args()
    
    if not args.markdown_file and not args.file:
        parser.error("Either markdown_file or --file must be provided")
    
    try:
        # Load DCT cookie
        print("Loading credentials...")
        dct = load_dct_cookie()
        
        # Resolve repository - from args or env
        repo = args.repo or load_repo()
        if not repo:
            print("❌ Repository not specified.")
            print("   Either provide --repo or set DATACAMP_REPO in .cursor/.env")
            sys.exit(1)
        
        # Resolve repository ID
        if is_github_url(repo):
            print(f"Looking up repository: {repo}")
            repository_id = find_repository_by_github_url(repo, dct)
            print(f"Found repository ID: {repository_id}\n")
        else:
            repository_id = repo
            print(f"Using repository ID: {repository_id}\n")
        
        if args.file:
            # Single file upload mode
            file_path = args.file
            output_name = args.name or Path(file_path).name
            
            print(f"Uploading: {file_path}")
            result = upload_asset(file_path, output_name, repository_id, dct)
            
            print("\n✅ Upload successful!")
            print(f"Asset ID: {result.get('id')}")
            print(f"Public URL: {result.get('public_url')}")
            
        else:
            # Markdown processing mode
            print(f"Processing: {args.markdown_file}")
            process_markdown_file(
                args.markdown_file,
                repository_id,
                dct,
                update=args.update
            )
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ API error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
