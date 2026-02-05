#!/usr/bin/env python3
"""
R Iterative (Bullet) Exercise Validator

Validates the complete exercise markdown structure for R iterative exercises.
These exercises have a parent BulletExercise with multiple NormalExercise children.
Each step is INDEPENDENT - code does NOT accumulate across steps.

Usage:
    python r_iterative_validator.py <exercise_markdown_file>
    python r_iterative_validator.py /tmp/exercise_to_validate.md

R-specific rules:
- Uses 3 underscores (___) for scaffolding
- Uses ```{r} or ```r code blocks
- Follows tidyverse style guide (<- for assignment, %>% for pipes)
"""

import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================================
# CONSTANTS
# ============================================================================

# Structural constraints (will break production if violated)
MIN_STEPS = 2
MAX_STEPS = 4
EXPECTED_TOTAL_XP = 100

# Content guidelines (optional, for information only)
GUIDELINE_MAX_CONTEXT_LENGTH = 550
GUIDELINE_RECOMMENDED_CONTEXT_LENGTH = 300
GUIDELINE_MAX_TITLE_LENGTH = 25
GUIDELINE_RECOMMENDED_INSTRUCTION_LENGTH = 60


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class StepData:
    """Data for a single exercise step."""
    index: int
    yaml_block: Optional[str] = None
    xp: Optional[int] = None
    instructions: Optional[str] = None
    hint: Optional[str] = None
    sample_code: Optional[str] = None
    solution: Optional[str] = None
    sct: Optional[str] = None


@dataclass
class ExerciseData:
    """Data for the complete iterative exercise."""
    title: Optional[str] = None
    yaml_block: Optional[str] = None
    context: Optional[str] = None
    pre_exercise_code: Optional[str] = None
    steps: List[StepData] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of validation."""
    valid: bool
    message: str
    title: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ============================================================================
# PARSER
# ============================================================================

def parse_iterative_exercise(content: str) -> Tuple[ExerciseData, List[str]]:
    """
    Parse the iterative exercise markdown to extract components.
    
    Returns:
        Tuple of (ExerciseData, parse_errors)
    """
    errors = []
    content = content.strip()
    
    # Remove leading --- separator if present
    content = re.sub(r'^---\s*\n', '', content).strip()
    
    exercise = ExerciseData()
    
    # Extract title from heading
    title_match = re.match(r'^##\s+(.+?)(?:\n|$)', content)
    if not title_match:
        errors.append("Missing markdown heading (must start with '## ')")
    else:
        exercise.title = title_match.group(1).strip()
    
    # Split into parent and steps using *** separator
    parts = re.split(r'\n\*\*\*\s*\n', content)
    
    if len(parts) < 2:
        errors.append("No step separators (***) found. Iterative exercises need at least 2 steps.")
        return exercise, errors
    
    parent_section = parts[0]
    step_sections = parts[1:]
    
    # Parse parent section
    exercise = parse_parent_section(parent_section, exercise, errors)
    
    # Parse each step
    for i, step_content in enumerate(step_sections):
        step = parse_step_section(step_content, i + 1, errors)
        exercise.steps.append(step)
    
    return exercise, errors


def parse_parent_section(content: str, exercise: ExerciseData, errors: List[str]) -> ExerciseData:
    """Parse the parent BulletExercise section."""
    
    # Extract YAML metadata block
    yaml_match = re.search(r'```yaml\s*\n(.*?)```', content, re.DOTALL)
    if yaml_match:
        exercise.yaml_block = yaml_match.group(1).strip()
    else:
        errors.append("Missing ```yaml metadata block in parent section")
    
    # Extract pre_exercise_code (R uses ```{r} or ```r)
    pre_code_match = re.search(r'`@pre_exercise_code`\s*\n```\{r\}\s*\n(.*?)```', content, re.DOTALL)
    if pre_code_match:
        exercise.pre_exercise_code = pre_code_match.group(1).strip()
    else:
        # Try alternative syntax without curly braces
        pre_code_match = re.search(r'`@pre_exercise_code`\s*\n```r\s*\n(.*?)```', content, re.DOTALL)
        if pre_code_match:
            exercise.pre_exercise_code = pre_code_match.group(1).strip()
    
    # Extract context (text between yaml block and @pre_exercise_code or first ***)
    yaml_end_match = re.search(r'```yaml.*?```\s*\n', content, re.DOTALL)
    if yaml_end_match:
        after_yaml = content[yaml_end_match.end():]
        pre_code_start = after_yaml.find('`@pre_exercise_code`')
        if pre_code_start > 0:
            exercise.context = after_yaml[:pre_code_start].strip()
        else:
            exercise.context = after_yaml.strip()
    
    return exercise


def parse_step_section(content: str, step_index: int, errors: List[str]) -> StepData:
    """Parse a single step (NormalExercise) section."""
    
    step = StepData(index=step_index)
    
    # Extract YAML metadata block
    yaml_match = re.search(r'```yaml\s*\n(.*?)```', content, re.DOTALL)
    if yaml_match:
        step.yaml_block = yaml_match.group(1).strip()
        # Extract XP
        xp_match = re.search(r'xp:\s*(\d+)', step.yaml_block)
        if xp_match:
            step.xp = int(xp_match.group(1))
    else:
        errors.append(f"Step {step_index}: Missing ```yaml metadata block")
    
    # Extract text sections
    sections = {
        "instructions": r'`@instructions`\s*\n(.*?)(?=`@|\Z)',
        "hint": r'`@hint`\s*\n(.*?)(?=`@|\Z)',
    }
    
    # Extract code sections (R uses ```{r} or ```r)
    code_sections = {
        "sample_code": r'`@sample_code`\s*\n```\{r\}\s*\n(.*?)```',
        "solution": r'`@solution`\s*\n```\{r\}\s*\n(.*?)```',
        "sct": r'`@sct`\s*\n```\{r\}\s*\n(.*?)```',
    }
    
    # Fallback patterns without curly braces
    code_sections_fallback = {
        "sample_code": r'`@sample_code`\s*\n```r\s*\n(.*?)```',
        "solution": r'`@solution`\s*\n```r\s*\n(.*?)```',
        "sct": r'`@sct`\s*\n```r\s*\n(.*?)```',
    }
    
    for section_name, pattern in sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            setattr(step, section_name, match.group(1).strip())
    
    for section_name, pattern in code_sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            setattr(step, section_name, match.group(1).strip())
        else:
            # Try fallback
            fallback_pattern = code_sections_fallback.get(section_name)
            if fallback_pattern:
                match = re.search(fallback_pattern, content, re.DOTALL)
                if match:
                    setattr(step, section_name, match.group(1).strip())
    
    return step


# ============================================================================
# VALIDATORS
# ============================================================================

def validate_parent_yaml(yaml_content: str) -> Tuple[List[str], List[str]]:
    """Validate the parent YAML metadata block."""
    errors = []
    warnings = []
    
    if not yaml_content:
        errors.append("Parent YAML block is empty")
        return errors, warnings
    
    # Check for required type
    if "type:" not in yaml_content:
        errors.append("Missing 'type:' in parent YAML block")
    elif "BulletExercise" not in yaml_content:
        errors.append("Parent type must be 'BulletExercise' (not TabExercise)")
    
    # Check for XP
    if "xp:" not in yaml_content:
        errors.append("Missing 'xp:' in parent YAML block")
    else:
        xp_match = re.search(r'xp:\s*(\d+)', yaml_content)
        if xp_match and int(xp_match.group(1)) != EXPECTED_TOTAL_XP:
            errors.append(f"Parent xp should be {EXPECTED_TOTAL_XP}, found {xp_match.group(1)}")
    
    return errors, warnings


def validate_step_yaml(step: StepData) -> Tuple[List[str], List[str]]:
    """Validate a step's YAML metadata block."""
    errors = []
    warnings = []
    
    if not step.yaml_block:
        errors.append(f"Step {step.index}: YAML block is empty")
        return errors, warnings
    
    # Check for required type
    if "type:" not in step.yaml_block:
        errors.append(f"Step {step.index}: Missing 'type:' in YAML block")
    elif "NormalExercise" not in step.yaml_block:
        errors.append(f"Step {step.index}: Type must be 'NormalExercise'")
    
    # Check for XP
    if "xp:" not in step.yaml_block:
        errors.append(f"Step {step.index}: Missing 'xp:' in YAML block")
    
    return errors, warnings


def validate_title(title: str) -> Tuple[List[str], List[str]]:
    """Validate exercise title (structural check only)."""
    errors = []
    warnings = []
    
    if not title:
        errors.append("Missing exercise title")
    
    return errors, warnings


def validate_context(context: str) -> Tuple[List[str], List[str]]:
    """Validate exercise context (structural check only)."""
    errors = []
    warnings = []
    
    if not context:
        warnings.append("Missing context (narrative explaining the scenario)")
    
    return errors, warnings


def validate_step_count(steps: List[StepData]) -> Tuple[List[str], List[str]]:
    """Validate the number of steps (structural check)."""
    errors = []
    warnings = []
    
    step_count = len(steps)
    
    if step_count < MIN_STEPS:
        errors.append(f"Too few steps: {step_count}. Minimum is {MIN_STEPS}")
    elif step_count > MAX_STEPS:
        errors.append(f"Too many steps: {step_count}. Maximum is {MAX_STEPS}")
    
    return errors, warnings


def validate_xp_distribution(steps: List[StepData]) -> Tuple[List[str], List[str]]:
    """Validate that XP values sum to expected total."""
    errors = []
    warnings = []
    
    total_xp = 0
    missing_xp = []
    
    for step in steps:
        if step.xp is not None:
            total_xp += step.xp
        else:
            missing_xp.append(step.index)
    
    if missing_xp:
        errors.append(f"Steps missing XP values: {missing_xp}")
    elif total_xp != EXPECTED_TOTAL_XP:
        errors.append(f"XP values sum to {total_xp}, expected {EXPECTED_TOTAL_XP}")
    
    return errors, warnings


def validate_step_sections(step: StepData) -> Tuple[List[str], List[str]]:
    """Validate that a step has all required sections."""
    errors = []
    warnings = []
    
    required_sections = [
        ("instructions", "`@instructions`"),
        ("hint", "`@hint`"),
        ("sample_code", "`@sample_code`"),
        ("solution", "`@solution`"),
        ("sct", "`@sct`"),
    ]
    
    for section_key, section_name in required_sections:
        if not getattr(step, section_key, None):
            errors.append(f"Step {step.index}: Missing required section {section_name}")
    
    return errors, warnings


def validate_instruction_presence(step: StepData) -> Tuple[List[str], List[str]]:
    """Validate that step has instruction content (structural check only)."""
    errors = []
    warnings = []
    
    if not step.instructions:
        return errors, warnings
    
    instruction_text = step.instructions.strip()
    if not instruction_text:
        warnings.append(f"Step {step.index}: Instructions section is empty")
    
    return errors, warnings


def validate_scaffolding(step: StepData) -> Tuple[List[str], List[str]]:
    """Validate scaffolding in sample code (R uses 3 underscores)."""
    errors = []
    warnings = []
    
    if not step.sample_code:
        return errors, warnings
    
    # Check for 3-underscore scaffolding (R uses 3, not 4)
    three_underscores = re.findall(r'(?<!_)___(?!_)', step.sample_code)
    four_underscores = re.findall(r'____', step.sample_code)
    
    if four_underscores:
        errors.append(
            f"Step {step.index}: Found {len(four_underscores)} instances of 4 underscores (____). "
            f"R uses 3 underscores (___)"
        )
    
    if not three_underscores:
        warnings.append(f"Step {step.index}: No scaffolding (___) found in sample code")
    
    return errors, warnings


def validate_code_structure(step: StepData) -> Tuple[List[str], List[str]]:
    """
    Validate that sample and solution code are identical except for scaffolding.
    
    This is a critical structural check - sample code should be the solution
    with ___ placeholders where learners fill in answers.
    """
    errors = []
    warnings = []
    
    if not step.sample_code or not step.solution:
        return errors, warnings
    
    sample_normalized = step.sample_code.strip()
    solution_normalized = step.solution.strip()
    
    # First check: line counts must match
    sample_lines = sample_normalized.split('\n')
    solution_lines = solution_normalized.split('\n')
    
    if len(sample_lines) != len(solution_lines):
        errors.append(
            f"Step {step.index}: Line count mismatch - sample has {len(sample_lines)} lines, "
            f"solution has {len(solution_lines)} lines"
        )
        return errors, warnings
    
    # Second check: each line must match when scaffolding is accounted for
    for i, (sample_line, solution_line) in enumerate(zip(sample_lines, solution_lines), 1):
        # Check if lines match (sample line with ___ replaced by regex pattern)
        if '___' in sample_line:
            # Build pattern: escape everything except ___ which becomes .+
            parts = sample_line.split('___')
            escaped_parts = [re.escape(p) for p in parts]
            line_pattern = '.+'.join(escaped_parts)
            
            if not re.fullmatch(line_pattern, solution_line):
                errors.append(
                    f"Step {step.index}: Line {i} structure mismatch - "
                    f"sample and solution differ beyond scaffolding"
                )
        else:
            # No scaffolding on this line - must be identical
            if sample_line != solution_line:
                errors.append(
                    f"Step {step.index}: Line {i} mismatch - "
                    f"lines must be identical (no scaffolding on this line)"
                )
    
    return errors, warnings


def validate_r_style(step: StepData) -> Tuple[List[str], List[str]]:
    """Validate R-specific style conventions (tidyverse guidelines)."""
    warnings = []
    errors = []
    
    if not step.solution:
        return errors, warnings
    
    # Check for = assignment (should use <-)
    lines = step.solution.split('\n')
    for i, line in enumerate(lines, 1):
        # Skip comments and lines inside function calls
        if line.strip().startswith('#'):
            continue
        # Check for = assignment pattern at start of line (not inside function)
        if re.search(r'^\s*\w+\s*=\s*[^=]', line) and '(' not in line.split('=')[0]:
            warnings.append(
                f"Step {step.index}, Line {i}: Consider using '<-' for assignment instead of '='"
            )
    
    return errors, warnings


def validate_success_message(steps: List[StepData]) -> Tuple[List[str], List[str]]:
    """Validate that success_msg is only in the last step."""
    errors = []
    warnings = []
    
    for i, step in enumerate(steps):
        if not step.sct:
            continue
        
        has_success_msg = 'success_msg(' in step.sct
        is_last_step = (i == len(steps) - 1)
        
        if has_success_msg and not is_last_step:
            warnings.append(f"Step {step.index}: success_msg() should only be in the last step")
        
        if is_last_step and not has_success_msg:
            warnings.append(f"Step {step.index} (last step): Missing success_msg() in SCT")
    
    return errors, warnings


def validate_pre_exercise_code(pre_exercise_code: str) -> Tuple[List[str], List[str]]:
    """Validate pre-exercise code exists."""
    errors = []
    warnings = []
    
    if not pre_exercise_code:
        warnings.append("Missing `@pre_exercise_code` section in parent (may be intentional)")
    
    return errors, warnings


# ============================================================================
# MAIN VALIDATOR
# ============================================================================

def validate_exercise(content: str) -> ValidationResult:
    """
    Validate a complete R iterative exercise.
    
    Args:
        content: Full markdown content
        
    Returns:
        ValidationResult with validation status and details
    """
    all_errors = []
    all_warnings = []
    
    # Step 1: Parse the markdown
    exercise, parse_errors = parse_iterative_exercise(content)
    all_errors.extend(parse_errors)
    
    title = exercise.title or "Unknown"
    
    # If parsing failed badly, return early
    if len(exercise.steps) == 0 and parse_errors:
        return ValidationResult(
            valid=False,
            message=f"❌ Parsing failed: \"{title}\"",
            title=title,
            errors=all_errors,
            warnings=all_warnings
        )
    
    # Step 2: Validate title
    title_errors, title_warnings = validate_title(exercise.title)
    all_errors.extend(title_errors)
    all_warnings.extend(title_warnings)
    
    # Step 3: Validate parent YAML block
    if exercise.yaml_block:
        yaml_errors, yaml_warnings = validate_parent_yaml(exercise.yaml_block)
        all_errors.extend(yaml_errors)
        all_warnings.extend(yaml_warnings)
    
    # Step 4: Validate context
    context_errors, context_warnings = validate_context(exercise.context)
    all_errors.extend(context_errors)
    all_warnings.extend(context_warnings)
    
    # Step 5: Validate pre-exercise code
    pre_errors, pre_warnings = validate_pre_exercise_code(exercise.pre_exercise_code)
    all_errors.extend(pre_errors)
    all_warnings.extend(pre_warnings)
    
    # Step 6: Validate step count
    step_count_errors, step_count_warnings = validate_step_count(exercise.steps)
    all_errors.extend(step_count_errors)
    all_warnings.extend(step_count_warnings)
    
    # Step 7: Validate XP distribution
    xp_errors, xp_warnings = validate_xp_distribution(exercise.steps)
    all_errors.extend(xp_errors)
    all_warnings.extend(xp_warnings)
    
    # Step 8: Validate each step
    for step in exercise.steps:
        # Step YAML
        step_yaml_errors, step_yaml_warnings = validate_step_yaml(step)
        all_errors.extend(step_yaml_errors)
        all_warnings.extend(step_yaml_warnings)
        
        # Required sections
        section_errors, section_warnings = validate_step_sections(step)
        all_errors.extend(section_errors)
        all_warnings.extend(section_warnings)
        
        # Instruction presence
        inst_errors, inst_warnings = validate_instruction_presence(step)
        all_errors.extend(inst_errors)
        all_warnings.extend(inst_warnings)
        
        # Scaffolding (R uses 3 underscores)
        scaffold_errors, scaffold_warnings = validate_scaffolding(step)
        all_errors.extend(scaffold_errors)
        all_warnings.extend(scaffold_warnings)
        
        # Code structure
        struct_errors, struct_warnings = validate_code_structure(step)
        all_errors.extend(struct_errors)
        all_warnings.extend(struct_warnings)
        
        # R style (tidyverse guidelines)
        style_errors, style_warnings = validate_r_style(step)
        all_errors.extend(style_errors)
        all_warnings.extend(style_warnings)
    
    # Step 9: Validate success message placement
    success_errors, success_warnings = validate_success_message(exercise.steps)
    all_errors.extend(success_errors)
    all_warnings.extend(success_warnings)
    
    # Build result
    if all_errors:
        return ValidationResult(
            valid=False,
            message=f"❌ Validation failed: \"{title}\"",
            title=title,
            errors=all_errors,
            warnings=all_warnings
        )
    
    # Count total scaffolding
    total_scaffolds = 0
    for step in exercise.steps:
        if step.sample_code:
            total_scaffolds += len(re.findall(r'(?<!_)___(?!_)', step.sample_code))
    
    return ValidationResult(
        valid=True,
        message=f"✅ Validation passed: \"{title}\" — {len(exercise.steps)} steps, {total_scaffolds} scaffolding points",
        title=title,
        warnings=all_warnings
    )


# ============================================================================
# CLI
# ============================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("R Iterative Exercise Validator")
        print("")
        print("Usage:")
        print("  python r_iterative_validator.py <markdown_file>")
        print("")
        print("Example:")
        print("  python r_iterative_validator.py /tmp/exercise_to_validate.md")
        print("")
        print("Validates:")
        print("  - Parent structure (BulletExercise)")
        print("  - Step count (2-4 steps)")
        print("  - XP distribution (sums to 100)")
        print("  - Required sections per step")
        print("  - Scaffolding (3 underscores for R)")
        print("  - Code structure matching")
        print("  - R style (tidyverse: <- assignment, %>% pipes)")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    content = file_path.read_text()
    
    # Validate
    result = validate_exercise(content)
    
    # Output
    print(result.message)
    
    if result.errors:
        print("")
        print("🚨 Errors (must fix):")
        for error in result.errors:
            print(f"  ❌ {error}")
    
    if result.warnings:
        print("")
        print("💡 Warnings (suggestions):")
        for warning in result.warnings:
            print(f"  ⚠️  {warning}")
    
    # Summary
    print("")
    if result.valid:
        print(f"Summary: Exercise is valid with {len(result.warnings)} warning(s)")
    else:
        print(f"Summary: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
