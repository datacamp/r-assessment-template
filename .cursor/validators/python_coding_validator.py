#!/usr/bin/env python3
"""
Python BlanksChallenge Validator

Validates BlanksChallenge exercise markdown structure for Python coding items.

Usage:
    python python_coding_validator.py <exercise_markdown_file>
    python python_coding_validator.py /tmp/exercise_to_validate.md
"""

import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# VALIDATION MODELS
# ============================================================================

@dataclass
class ItemValidationResult:
    """Result of validating a single item."""
    valid: bool
    title: str
    item_number: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    blank_count: int = 0


@dataclass
class DocumentValidationResult:
    """Result of validating the entire document."""
    valid: bool
    message: str
    document_title: Optional[str] = None
    item_count: int = 0
    items: List[ItemValidationResult] = field(default_factory=list)
    document_errors: List[str] = field(default_factory=list)


# ============================================================================
# PARSER
# ============================================================================

def parse_document_header(content: str) -> Tuple[dict, str]:
    """
    Parse the document header (title, output, description).
    
    Returns:
        Tuple of (header_data, remaining_content)
    """
    header = {}
    
    # Check for YAML front matter
    front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if front_matter_match:
        front_matter = front_matter_match.group(1)
        
        # Extract title
        title_match = re.search(r'title:\s*(.+)', front_matter)
        if title_match:
            header["title"] = title_match.group(1).strip()
        
        # Extract output
        output_match = re.search(r'output:\s*(.+)', front_matter)
        if output_match:
            header["output"] = output_match.group(1).strip()
        
        # Extract description
        desc_match = re.search(r'description:\s*(.+)', front_matter)
        if desc_match:
            header["description"] = desc_match.group(1).strip()
        
        remaining = content[front_matter_match.end():]
    else:
        remaining = content
    
    return header, remaining


def split_items(content: str) -> List[str]:
    """
    Split content into individual items by --- separator.
    
    Returns:
        List of item content strings
    """
    # Split by --- on its own line (item separator)
    items = re.split(r'\n---\s*\n', content)
    
    # Filter out empty items
    items = [item.strip() for item in items if item.strip()]
    
    return items


def parse_single_item(content: str) -> Tuple[dict, List[str]]:
    """
    Parse a single BlanksChallenge item.
    
    Returns:
        Tuple of (parsed_data, errors)
    """
    errors = []
    
    parsed = {
        "title": None,
        "yaml_block": None,
        "context": None,
        "code1": None,
        "pre_challenge_code": None,
        "variables": None,
        "distractors": None,
    }
    
    # Extract title from heading (## [Title] format)
    title_match = re.search(r'^##\s+\[([^\]]+)\]', content, re.MULTILINE)
    if not title_match:
        # Try without brackets
        title_match = re.search(r'^##\s+(.+?)(?:\n|$)', content, re.MULTILINE)
    
    if not title_match:
        errors.append("Missing item heading (must have '## [Title]' or '## Title')")
    else:
        parsed["title"] = title_match.group(1).strip()
    
    # Extract YAML metadata block
    yaml_match = re.search(r'```yaml\s*\n(.*?)```', content, re.DOTALL)
    if yaml_match:
        parsed["yaml_block"] = yaml_match.group(1).strip()
    else:
        errors.append("Missing ```yaml metadata block")
    
    # Extract sections - support both ```python and ```{python}
    sections = {
        "context": r'`@context`\s*\n(.*?)(?=`@|\Z)',
        "code1": r'`@code1`\s*\n```(?:python|\{python\})\s*\n(.*?)```',
        "pre_challenge_code": r'`@pre_challenge_code`\s*\n```(?:python|\{python\})\s*\n(.*?)```',
        "variables": r'`@variables`\s*\n```yaml\s*\n(.*?)```',
        "distractors": r'`@distractors`\s*\n```yaml\s*\n(.*?)```',
    }
    
    for section_name, pattern in sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            parsed[section_name] = match.group(1).strip()
    
    return parsed, errors


# ============================================================================
# VALIDATORS
# ============================================================================

def validate_yaml_block(yaml_content: str) -> Tuple[List[str], List[str]]:
    """Validate the YAML metadata block for BlanksChallenge."""
    errors = []
    warnings = []
    
    if not yaml_content:
        errors.append("YAML block is empty")
        return errors, warnings
    
    # Check for required fields
    required_fields = [
        ("type:", "type"),
        ("key:", "key"),
        ("unit:", "unit"),
        ("subskill:", "subskill"),
        ("initial_difficulty:", "initial_difficulty"),
        ("item_writer_id:", "item_writer_id"),
    ]
    
    for field_pattern, field_name in required_fields:
        if field_pattern not in yaml_content:
            errors.append(f"Missing '{field_name}' in YAML block")
    
    # Validate type is BlanksChallenge
    if "type:" in yaml_content and "BlanksChallenge" not in yaml_content:
        errors.append("type must be 'BlanksChallenge'")
    
    # Validate item_writer_id is 999999999
    writer_match = re.search(r"item_writer_id:\s*['\"]?(\d+)['\"]?", yaml_content)
    if writer_match:
        if writer_match.group(1) != "999999999":
            warnings.append(f"item_writer_id should be '999999999', found '{writer_match.group(1)}'")
    
    # Check unit format (should be kebab-case, 2-4 words)
    unit_match = re.search(r'unit:\s*([^\n]+)', yaml_content)
    if unit_match:
        unit_value = unit_match.group(1).strip()
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+){1,3}$', unit_value):
            warnings.append(f"unit '{unit_value}' should be kebab-case (e.g., 'llm-metrics', 'llm-tasks-hf-tools')")
    
    return errors, warnings


def validate_required_sections(parsed: dict) -> List[str]:
    """Validate that all required sections are present."""
    errors = []
    
    required_sections = [
        ("context", "`@context`"),
        ("code1", "`@code1`"),
        ("variables", "`@variables`"),
    ]
    
    for section_key, section_name in required_sections:
        if not parsed.get(section_key):
            errors.append(f"Missing required section: {section_name}")
    
    return errors


def validate_blanks(code1: str, variables: str) -> Tuple[List[str], List[str]]:
    """Validate {{_exprN}} placeholders in code1 match variables."""
    errors = []
    warnings = []
    
    if not code1:
        return errors, warnings
    
    # Find all {{_exprN}} placeholders in code1
    blanks = re.findall(r'\{\{_expr(\d+)\}\}', code1)
    blank_numbers = sorted(set(int(b) for b in blanks))
    
    if not blank_numbers:
        errors.append("No {{_exprN}} blanks found in @code1")
        return errors, warnings
    
    # Check for consecutive numbering starting at 1
    expected = list(range(1, len(blank_numbers) + 1))
    if blank_numbers != expected:
        errors.append(f"Blank numbers should be consecutive starting at 1. Found: {blank_numbers}")
    
    # Validate variables section has matching entries
    if variables:
        for num in blank_numbers:
            expr_pattern = f"expr{num}:"
            if expr_pattern not in variables:
                errors.append(f"Missing 'expr{num}:' in @variables for {{{{_expr{num}}}}}")
        
        # Check for extra variables not in code
        var_matches = re.findall(r'expr(\d+):', variables)
        for var_num in var_matches:
            if int(var_num) not in blank_numbers:
                warnings.append(f"Variable 'expr{var_num}' defined but not used in @code1")
    
    return errors, warnings


def validate_code1_content(code1: str) -> Tuple[List[str], List[str]]:
    """Validate code1 content (no comments, etc.)."""
    errors = []
    warnings = []
    
    if not code1:
        return errors, warnings
    
    # Check for comments (should not be in @code1)
    comments = re.findall(r'#.*$', code1, re.MULTILINE)
    if comments:
        errors.append(f"@code1 should not contain comments. Found {len(comments)} comment(s)")
    
    # Check for string blanks (answers shouldn't be string literals in certain cases)
    # This is a warning, not an error, as sometimes strings are valid
    
    return errors, warnings


def validate_variables_format(variables: str) -> Tuple[List[str], List[str]]:
    """Validate variables section format."""
    errors = []
    warnings = []
    
    if not variables:
        return errors, warnings
    
    # Check each variable has a list with exactly one answer
    var_blocks = re.findall(r'(expr\d+):\s*\n\s*-\s*(.+)', variables)
    
    for var_name, answer in var_blocks:
        # Check answer is quoted
        if not (answer.startswith("'") or answer.startswith('"')):
            warnings.append(f"{var_name} answer should be quoted: '{answer}'")
    
    return errors, warnings


def validate_single_item(content: str, item_number: int) -> ItemValidationResult:
    """
    Validate a single BlanksChallenge item.
    
    Args:
        content: Item markdown content
        item_number: 1-based item number
        
    Returns:
        ItemValidationResult
    """
    all_errors = []
    all_warnings = []
    
    # Parse the item
    parsed, parse_errors = parse_single_item(content)
    all_errors.extend(parse_errors)
    
    title = parsed.get("title", f"Item {item_number}")
    
    # Validate YAML block
    if parsed.get("yaml_block"):
        yaml_errors, yaml_warnings = validate_yaml_block(parsed["yaml_block"])
        all_errors.extend(yaml_errors)
        all_warnings.extend(yaml_warnings)
    
    # Validate required sections
    section_errors = validate_required_sections(parsed)
    all_errors.extend(section_errors)
    
    # Validate blanks
    blank_count = 0
    if parsed.get("code1"):
        blank_errors, blank_warnings = validate_blanks(parsed["code1"], parsed.get("variables"))
        all_errors.extend(blank_errors)
        all_warnings.extend(blank_warnings)
        blank_count = len(re.findall(r'\{\{_expr\d+\}\}', parsed["code1"]))
    
    # Validate code1 content
    if parsed.get("code1"):
        code_errors, code_warnings = validate_code1_content(parsed["code1"])
        all_errors.extend(code_errors)
        all_warnings.extend(code_warnings)
    
    # Validate variables format
    if parsed.get("variables"):
        var_errors, var_warnings = validate_variables_format(parsed["variables"])
        all_errors.extend(var_errors)
        all_warnings.extend(var_warnings)
    
    return ItemValidationResult(
        valid=len(all_errors) == 0,
        title=title,
        item_number=item_number,
        errors=all_errors,
        warnings=all_warnings,
        blank_count=blank_count
    )


# ============================================================================
# MAIN VALIDATOR
# ============================================================================

def validate_document(content: str) -> DocumentValidationResult:
    """
    Validate a complete BlanksChallenge document with multiple items.
    
    Args:
        content: Full markdown content
        
    Returns:
        DocumentValidationResult
    """
    document_errors = []
    
    # Parse document header
    header, remaining_content = parse_document_header(content)
    document_title = header.get("title", "Untitled")
    
    # Check for document header
    if not header.get("title"):
        document_errors.append("Missing document 'title:' in front matter")
    
    # Split into items
    items_content = split_items(remaining_content)
    
    if not items_content:
        document_errors.append("No items found in document")
        return DocumentValidationResult(
            valid=False,
            message="❌ No items found in document",
            document_title=document_title,
            document_errors=document_errors
        )
    
    # Validate each item
    item_results = []
    for i, item_content in enumerate(items_content, start=1):
        result = validate_single_item(item_content, i)
        item_results.append(result)
    
    # Aggregate results
    all_valid = all(item.valid for item in item_results) and len(document_errors) == 0
    total_blanks = sum(item.blank_count for item in item_results)
    
    if all_valid:
        message = f"✅ Validation passed: {len(item_results)} item(s), {total_blanks} total blanks"
    else:
        failed_count = sum(1 for item in item_results if not item.valid)
        message = f"❌ Validation failed: {failed_count}/{len(item_results)} item(s) have errors"
    
    return DocumentValidationResult(
        valid=all_valid,
        message=message,
        document_title=document_title,
        item_count=len(item_results),
        items=item_results,
        document_errors=document_errors
    )


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Python BlanksChallenge Validator")
        print("")
        print("Usage:")
        print("  python python_coding_validator.py <markdown_file>")
        print("")
        print("Example:")
        print("  python python_coding_validator.py /tmp/exercise_to_validate.md")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    content = file_path.read_text()
    
    # Validate
    result = validate_document(content)
    
    # Output
    print(result.message)
    print(f"Document: {result.document_title}")
    print("")
    
    # Document-level errors
    if result.document_errors:
        print("Document Errors:")
        for error in result.document_errors:
            print(f"  ❌ {error}")
        print("")
    
    # Per-item results
    for item in result.items:
        status = "✅" if item.valid else "❌"
        print(f"{status} Item {item.item_number}: \"{item.title}\" — {item.blank_count} blank(s)")
        
        if item.errors:
            for error in item.errors:
                print(f"     ❌ {error}")
        
        if item.warnings:
            for warning in item.warnings:
                print(f"     ⚠️  {warning}")
    
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
