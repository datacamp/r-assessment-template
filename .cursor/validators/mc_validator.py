#!/usr/bin/env python3
"""
MultipleChoiceChallenge Validator

Validates MultipleChoiceChallenge item markdown structure.

Usage:
    python mc_validator.py <items_markdown_file>
    python mc_validator.py /tmp/mc_items.md
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
    correct_position: int  # 1-4, or 0 if not found
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    option_lengths: List[int] = field(default_factory=list)


@dataclass
class DocumentValidationResult:
    """Result of validating the entire document."""
    valid: bool
    message: str
    document_title: Optional[str] = None
    item_count: int = 0
    items: List[ItemValidationResult] = field(default_factory=list)
    document_errors: List[str] = field(default_factory=list)
    document_warnings: List[str] = field(default_factory=list)


# ============================================================================
# VAGUE STEM PATTERNS
# ============================================================================

VAGUE_STEM_PATTERNS = [
    r'\bwhich of the following\b',
    r'\bwhich option\b',
    r'\bwhich statement\b',
    r'\bhow would you best describe\b',
    r'\bwhich best describes\b',
    r'\bwhich is true\b',
    r'\bwhich is false\b',
    r'\bwhich is correct\b',
    r'\bwhich is incorrect\b',
    r'\ball of the above\b',
    r'\bnone of the above\b',
]


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
    Parse a single MultipleChoiceChallenge item.
    
    Returns:
        Tuple of (parsed_data, errors)
    """
    errors = []
    
    parsed = {
        "title": None,
        "yaml_block": None,
        "assignment": None,
        "options": [],
        "correct_index": -1,  # 0-based index of correct answer
        "correct_answer": None,
    }
    
    # Extract title from heading (## Title format)
    title_match = re.search(r'^##\s+(.+?)(?:\n|$)', content, re.MULTILINE)
    if not title_match:
        errors.append("Missing item heading (must have '## Title')")
    else:
        parsed["title"] = title_match.group(1).strip()
    
    # Extract YAML metadata block
    yaml_match = re.search(r'```yaml\s*\n(.*?)```', content, re.DOTALL)
    if yaml_match:
        parsed["yaml_block"] = yaml_match.group(1).strip()
    else:
        errors.append("Missing ```yaml metadata block")
    
    # Extract assignment (stem/question)
    assignment_match = re.search(r'`@assignment1`\s*\n(.*?)(?=`@|\Z)', content, re.DOTALL)
    if assignment_match:
        parsed["assignment"] = assignment_match.group(1).strip()
    else:
        errors.append("Missing `@assignment1` section")
    
    # Extract options
    options_match = re.search(r'`@options1`\s*\n(.*?)(?=`@|\Z|---)', content, re.DOTALL)
    if options_match:
        options_text = options_match.group(1).strip()
        
        # Parse options - look for lines starting with -
        option_lines = re.findall(r'^-\s*(.+)$', options_text, re.MULTILINE)
        
        for i, opt in enumerate(option_lines):
            opt = opt.strip()
            # Check if this is the correct answer (wrapped in [...])
            if opt.startswith('[') and opt.endswith(']'):
                parsed["correct_index"] = i
                parsed["correct_answer"] = opt[1:-1]  # Remove brackets
                parsed["options"].append(opt[1:-1])
            else:
                parsed["options"].append(opt)
    else:
        errors.append("Missing `@options1` section")
    
    return parsed, errors


# ============================================================================
# VALIDATORS
# ============================================================================

def validate_yaml_block(yaml_content: str) -> Tuple[List[str], List[str]]:
    """Validate the YAML metadata block for MultipleChoiceChallenge."""
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
    
    # Validate type is MultipleChoiceChallenge
    if "type:" in yaml_content and "MultipleChoiceChallenge" not in yaml_content:
        errors.append("type must be 'MultipleChoiceChallenge'")
    
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
            warnings.append(f"unit '{unit_value}' should be kebab-case (e.g., 'container-basics')")
    
    return errors, warnings


def validate_options(options: List[str], correct_index: int) -> Tuple[List[str], List[str]]:
    """Validate option structure and length rules."""
    errors = []
    warnings = []
    
    # Check option count
    if len(options) != 4:
        errors.append(f"Must have exactly 4 options, found {len(options)}")
        return errors, warnings
    
    # Check for correct answer
    if correct_index < 0:
        errors.append("No correct answer marked with [...] brackets")
        return errors, warnings
    
    # Calculate lengths
    lengths = [len(opt) for opt in options]
    correct_length = lengths[correct_index]
    
    # Check ±8 character rule
    min_len = min(lengths)
    max_len = max(lengths)
    
    if max_len - min_len > 16:  # ±8 means max difference of 16
        errors.append(f"Option lengths vary too much: {min_len}-{max_len} chars (max allowed difference: 16)")
    
    # Check each option is within ±8 of others
    for i, length in enumerate(lengths):
        for j, other_length in enumerate(lengths):
            if i != j and abs(length - other_length) > 8:
                warnings.append(f"Option {i+1} ({length} chars) and option {j+1} ({other_length} chars) differ by more than 8 characters")
                break  # Only warn once per pair
    
    # Check correct answer is not longest
    if correct_length > max(lengths[i] for i in range(len(lengths)) if i != correct_index):
        # Correct is longest
        if correct_length > min(lengths[i] for i in range(len(lengths)) if i != correct_index):
            warnings.append(f"Correct answer ({correct_length} chars) is longer than some distractors")
    
    # Check for "All of the above" / "None of the above"
    for opt in options:
        opt_lower = opt.lower()
        if 'all of the above' in opt_lower or 'none of the above' in opt_lower:
            errors.append("Options should not include 'All of the above' or 'None of the above'")
            break
    
    return errors, warnings


def validate_stem(assignment: str) -> Tuple[List[str], List[str]]:
    """Validate the stem/question for clarity."""
    errors = []
    warnings = []
    
    if not assignment:
        return errors, warnings
    
    assignment_lower = assignment.lower()
    
    # Check for vague stem patterns
    for pattern in VAGUE_STEM_PATTERNS:
        if re.search(pattern, assignment_lower):
            warnings.append(f"Vague stem detected: '{pattern.replace(chr(92), '').replace('b', '')}' - stems should stand alone without options")
            break
    
    # Check minimum length (should have context + question)
    if len(assignment) < 50:
        warnings.append("Stem seems too short - consider adding context or detail")
    
    return errors, warnings


def validate_single_item(content: str, item_number: int) -> ItemValidationResult:
    """
    Validate a single MultipleChoiceChallenge item.
    
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
    
    # Validate options
    options = parsed.get("options", [])
    correct_index = parsed.get("correct_index", -1)
    
    if options:
        opt_errors, opt_warnings = validate_options(options, correct_index)
        all_errors.extend(opt_errors)
        all_warnings.extend(opt_warnings)
    
    # Validate stem
    if parsed.get("assignment"):
        stem_errors, stem_warnings = validate_stem(parsed["assignment"])
        all_errors.extend(stem_errors)
        all_warnings.extend(stem_warnings)
    
    # Calculate option lengths for reporting
    option_lengths = [len(opt) for opt in options] if options else []
    
    # Correct position (1-based)
    correct_position = correct_index + 1 if correct_index >= 0 else 0
    
    return ItemValidationResult(
        valid=len(all_errors) == 0,
        title=title,
        item_number=item_number,
        correct_position=correct_position,
        errors=all_errors,
        warnings=all_warnings,
        option_lengths=option_lengths
    )


def validate_rotation(items: List[ItemValidationResult]) -> List[str]:
    """Check rotation pattern across items."""
    warnings = []
    
    if len(items) < 3:
        return warnings
    
    positions = [item.correct_position for item in items if item.correct_position > 0]
    
    # Check for same position more than twice in a row
    for i in range(len(positions) - 2):
        if positions[i] == positions[i+1] == positions[i+2]:
            warnings.append(f"Correct answer in position {positions[i]} three times in a row (items {i+1}-{i+3})")
    
    # Check distribution
    if len(positions) >= 8:
        from collections import Counter
        counts = Counter(positions)
        for pos in range(1, 5):
            if counts.get(pos, 0) == 0:
                warnings.append(f"Position {pos} never used for correct answer across {len(positions)} items")
    
    return warnings


# ============================================================================
# MAIN VALIDATOR
# ============================================================================

def validate_document(content: str) -> DocumentValidationResult:
    """
    Validate a complete MultipleChoiceChallenge document with multiple items.
    
    Args:
        content: Full markdown content
        
    Returns:
        DocumentValidationResult
    """
    document_errors = []
    document_warnings = []
    
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
    
    # Validate rotation pattern across items
    rotation_warnings = validate_rotation(item_results)
    document_warnings.extend(rotation_warnings)
    
    # Aggregate results
    all_valid = all(item.valid for item in item_results) and len(document_errors) == 0
    
    if all_valid:
        message = f"✅ Validation passed: {len(item_results)} item(s)"
    else:
        failed_count = sum(1 for item in item_results if not item.valid)
        message = f"❌ Validation failed: {failed_count}/{len(item_results)} item(s) have errors"
    
    return DocumentValidationResult(
        valid=all_valid,
        message=message,
        document_title=document_title,
        item_count=len(item_results),
        items=item_results,
        document_errors=document_errors,
        document_warnings=document_warnings
    )


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("MultipleChoiceChallenge Validator")
        print("")
        print("Usage:")
        print("  python mc_validator.py <markdown_file>")
        print("")
        print("Example:")
        print("  python mc_validator.py /tmp/mc_items.md")
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
    
    # Document-level warnings
    if result.document_warnings:
        print("Document Warnings:")
        for warning in result.document_warnings:
            print(f"  ⚠️  {warning}")
        print("")
    
    # Per-item results
    for item in result.items:
        status = "✅" if item.valid else "❌"
        pos_str = f"correct@{item.correct_position}" if item.correct_position > 0 else "no correct marked"
        lengths_str = f"lengths: {item.option_lengths}" if item.option_lengths else ""
        print(f"{status} Item {item.item_number}: \"{item.title}\" — {pos_str} {lengths_str}")
        
        if item.errors:
            for error in item.errors:
                print(f"     ❌ {error}")
        
        if item.warnings:
            for warning in item.warnings:
                print(f"     ⚠️  {warning}")
    
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
