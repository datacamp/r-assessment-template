#!/usr/bin/env python3
"""
MultipleChoiceChallenge Preview Generator

Generates rich HTML previews for MultipleChoiceChallenge items with course content references.

Features:
- Parses MultipleChoiceChallenge markdown items
- Extracts relevant video script excerpts
- Shows option lengths and validation status
- Highlights correct answers

Usage:
    python generate_mc_preview.py <items_file> [--scripts <scripts_dir>]
    python generate_mc_preview.py .cursor/tmp_items/mc_items.md --scripts ~/Downloads/scripts

Example:
    python generate_mc_preview.py .cursor/tmp_items/mc_items.md \
        --scripts /Users/martine.holland/Downloads/scripts
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import html


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class MCOption:
    """A single option."""
    text: str
    length: int
    is_correct: bool


@dataclass
class MCItem:
    """A single MultipleChoiceChallenge item."""
    title: str
    unit: str
    subskill: str
    assignment: str  # stem/question
    options: List[MCOption]
    correct_position: int  # 1-based
    item_number: int
    course_section: str = ""  # Optional: explicit course section reference
    teaching_point: str = ""  # Optional: key concept being tested
    course_content_reference: str = ""  # AI-extracted verbatim passages from course materials

@dataclass
class CourseReference:
    """Reference to course content."""
    source: str  # e.g., "Video 3.2"
    excerpt: str  # The relevant text


@dataclass 
class EnrichedItem:
    """Item with course references and validation."""
    item: MCItem
    embedded_refs: List[CourseReference] = field(default_factory=list)  # From course_content_reference
    video_refs: List[CourseReference] = field(default_factory=list)
    curated_refs: List[CourseReference] = field(default_factory=list)  # Definitional snippets
    length_valid: bool = True
    length_warnings: List[str] = field(default_factory=list)


# ============================================================================
# PARSERS
# ============================================================================

def parse_items_file(content: str) -> Tuple[str, List[MCItem]]:
    """Parse MultipleChoiceChallenge items from markdown."""
    items = []
    
    # Extract document title
    title_match = re.search(r'title:\s*(.+)', content)
    doc_title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Remove front matter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Split into items
    item_blocks = re.split(r'\n---\s*\n', content)
    
    for i, block in enumerate(item_blocks, start=1):
        if not block.strip():
            continue
            
        item = parse_single_item(block, i)
        if item:
            items.append(item)
    
    return doc_title, items


def parse_single_item(content: str, item_number: int) -> Optional[MCItem]:
    """Parse a single item block."""
    # Extract title
    title_match = re.search(r'##\s+(.+?)(?:\n|$)', content)
    title = title_match.group(1).strip() if title_match else f"Item {item_number}"
    
    # Extract YAML fields
    unit_match = re.search(r'unit:\s*(.+)', content)
    subskill_match = re.search(r'subskill:\s*(.+)', content)
    course_section_match = re.search(r'course_section:\s*["\']?([^"\']+)["\']?', content)
    teaching_point_match = re.search(r'teaching_point:\s*["\']?([^"\']+)["\']?', content)
    
    unit = unit_match.group(1).strip() if unit_match else ""
    subskill = subskill_match.group(1).strip() if subskill_match else ""
    course_section = course_section_match.group(1).strip() if course_section_match else ""
    teaching_point = teaching_point_match.group(1).strip() if teaching_point_match else ""
    
    # Extract course_content_reference (multi-line YAML block)
    course_content_reference = ""
    ccr_match = re.search(r'#\s*course_content_reference:\s*\|?\s*\n((?:#.*\n)*)', content)
    if ccr_match:
        ccr_lines = ccr_match.group(1)
        course_content_reference = re.sub(r'^#\s?', '', ccr_lines, flags=re.MULTILINE).strip()

    # Extract assignment (stem)
    assignment_match = re.search(r'`@assignment1`\s*\n(.*?)(?=`@|\Z)', content, re.DOTALL)
    assignment = assignment_match.group(1).strip() if assignment_match else ""
    
    # Extract options
    options = []
    correct_position = 0
    
    options_match = re.search(r'`@options1`\s*\n(.*?)(?=`@|\Z|---)', content, re.DOTALL)
    if options_match:
        options_text = options_match.group(1).strip()
        option_lines = re.findall(r'^-\s*(.+)$', options_text, re.MULTILINE)
        
        for i, opt in enumerate(option_lines):
            opt = opt.strip()
            is_correct = opt.startswith('[') and opt.endswith(']')
            
            if is_correct:
                correct_position = i + 1
                opt_text = opt[1:-1]  # Remove brackets
            else:
                opt_text = opt
            
            options.append(MCOption(
                text=opt_text,
                length=len(opt_text),
                is_correct=is_correct
            ))
    
    if not options:
        return None
    
    return MCItem(
        title=title,
        unit=unit,
        subskill=subskill,
        assignment=assignment,
        options=options,
        correct_position=correct_position,
        item_number=item_number,
        course_section=course_section,
        teaching_point=teaching_point,
        course_content_reference=course_content_reference
    )


def parse_video_scripts(scripts_dir: Path) -> Dict[str, str]:
    """Parse video/course scripts from directory.
    
    Supports multiple formats:
    - .txt files with '# Video N' headers (e.g., chapter_1_scripts.txt)
    - .md files with '## Section Title' headers (e.g., chapter1.md)
    """
    scripts = {}
    
    if not scripts_dir.exists():
        return scripts
    
    # Parse .txt files (original format: chapter_1_scripts.txt with # Video N headers)
    for script_file in scripts_dir.glob("*.txt"):
        content = script_file.read_text()
        
        # Extract chapter number from filename
        chapter_match = re.search(r'chapter[_-]?(\d+)', script_file.name, re.IGNORECASE)
        chapter_num = chapter_match.group(1) if chapter_match else "?"
        
        # Split by video headers
        videos = re.split(r'# Video (\d+)', content)
        
        for i in range(1, len(videos), 2):
            if i + 1 < len(videos):
                video_num = videos[i]
                video_content = videos[i + 1].strip()
                key = f"Chapter {chapter_num}, Video {video_num}"
                scripts[key] = video_content
    
    # Parse .md files (course exercise format: chapter1.md with ## Section headers)
    for md_file in scripts_dir.glob("*.md"):
        # Skip non-chapter files
        chapter_match = re.search(r'chapter[_-]?(\d+)', md_file.name, re.IGNORECASE)
        if not chapter_match:
            continue
            
        chapter_num = chapter_match.group(1)
        content = md_file.read_text()
        
        # Split by ## section headers
        sections = re.split(r'\n##\s+', content)
        
        for i, section in enumerate(sections[1:], start=1):  # Skip content before first ##
            # Extract section title (first line)
            lines = section.split('\n', 1)
            section_title = lines[0].strip()
            section_content = lines[1] if len(lines) > 1 else ""
            
            # Extract teaching content (text before @instructions or @possible_answers)
            teaching_match = re.match(r'(.*?)(?:`@instructions`|`@possible_answers`|\Z)', 
                                     section_content, re.DOTALL)
            if teaching_match:
                teaching_content = teaching_match.group(1).strip()
                # Clean up: remove yaml blocks and code solution blocks
                teaching_content = re.sub(r'```yaml.*?```', '', teaching_content, flags=re.DOTALL)
                teaching_content = re.sub(r'`@solution`.*?```', '', teaching_content, flags=re.DOTALL)
                teaching_content = re.sub(r'`@sct`.*?```', '', teaching_content, flags=re.DOTALL)
                teaching_content = re.sub(r'`@pre_exercise_code`.*?```', '', teaching_content, flags=re.DOTALL)
                teaching_content = re.sub(r'`@hint`.*?(?=\n\n|\Z)', '', teaching_content, flags=re.DOTALL)
                
                if len(teaching_content) > 50:  # Only include substantial content
                    key = f"Chapter {chapter_num}: {section_title}"
                    scripts[key] = teaching_content
    
    return scripts


# ============================================================================
# CURATED SNIPPETS - Definitional passages for key concepts
# ============================================================================

CURATED_SNIPPETS = {
    # ==========================================================================
    # SHELL / UNIX CONCEPTS (Introduction to Shell course)
    # ==========================================================================
    
    # Chapter 1 - Navigating files and directories
    "absolute path": {
        "source": "Shell Chapter 1",
        "excerpt": 'An **absolute path** starts from the root directory `/` and describes the complete location. A **relative path** starts from the current directory. For example, `/home/user/data.csv` is absolute, while `data/sales.csv` is relative to wherever you currently are.'
    },
    "relative path": {
        "source": "Shell Chapter 1", 
        "excerpt": 'A **relative path** specifies a location starting from your current working directory. The path `data/sales.csv` means "look for data folder here, then sales.csv inside it". If you change directories, the same relative path points to a different location.'
    },
    "cd command": {
        "source": "Shell Chapter 1",
        "excerpt": 'The `cd` command changes your current working directory. `cd data` moves into a subdirectory called data. `cd ..` moves up one level. `cd ~` goes to your home directory. `cd /path` goes to an absolute path.'
    },
    "copy move": {
        "source": "Shell Chapter 1",
        "excerpt": '`cp` copies files: `cp original.txt backup.txt` creates a copy. `mv` moves or renames files: `mv old.txt new.txt` renames, `mv file.txt folder/` moves. The key difference: **cp keeps the original, mv removes it**.'
    },
    "rmdir directory": {
        "source": "Shell Chapter 1",
        "excerpt": '`rmdir` removes **empty directories only**. If a directory contains files, rmdir fails with an error. You must first delete the files inside, then remove the directory. Use `rm -r` to remove directories with contents (carefully!).'
    },
    
    # Chapter 2 - Manipulating data
    "head tail": {
        "source": "Shell Chapter 2",
        "excerpt": '`head` shows the **first** lines of a file (default 10). `tail` shows the **last** lines. Use `-n` to specify how many: `head -n 5 file.csv` shows first 5 lines. `tail -n +7` shows everything from line 7 onward.'
    },
    "cut command": {
        "source": "Shell Chapter 2",
        "excerpt": '`cut` selects **columns** from a file. Use `-d` for delimiter and `-f` for fields: `cut -d , -f 2 data.csv` extracts the second column from a comma-separated file. You can select multiple columns: `-f 1,3` or `-f 2-5`.'
    },
    "grep command": {
        "source": "Shell Chapter 2",
        "excerpt": '`grep` selects **lines** containing a pattern. Common flags: `-c` counts matches, `-v` inverts (shows non-matching lines), `-i` ignores case, `-n` shows line numbers. Example: `grep -v error log.txt` shows lines WITHOUT "error".'
    },
    "history command": {
        "source": "Shell Chapter 2",
        "excerpt": '`history` shows commands you have run. Re-run command 55 with `!55`. Re-run the most recent grep with `!grep`. The exclamation mark followed by a command name re-runs the most recent use of that command.'
    },
    
    # Chapter 3 - Combining tools
    "redirection": {
        "source": "Shell Chapter 3",
        "excerpt": 'The `>` operator **redirects output to a file** instead of the screen. `head -n 5 data.csv > sample.csv` saves the first 5 lines to sample.csv. Nothing appears on screen—output goes to the file. `>>` appends instead of overwriting.'
    },
    "pipe": {
        "source": "Shell Chapter 3",
        "excerpt": 'The **pipe** `|` sends the output of one command as input to another. `grep error log.txt | wc -l` counts error lines. No intermediate files needed. You can chain many commands: `cut | grep | sort | uniq`.'
    },
    "wildcard": {
        "source": "Shell Chapter 3",
        "excerpt": 'The `*` **wildcard** matches zero or more characters. `*.csv` matches all CSV files. `data*` matches anything starting with "data". Wildcards are expanded by the shell before the command runs.'
    },
    "sort uniq": {
        "source": "Shell Chapter 3",
        "excerpt": '`sort` orders lines alphabetically (or numerically with `-n`). `uniq` removes **adjacent** duplicates only. To remove all duplicates, **sort first**: `sort data.txt | uniq`. Use `uniq -c` to count occurrences.'
    },
    
    # Chapter 4 - Batch processing
    "shell variable": {
        "source": "Shell Chapter 4",
        "excerpt": 'Create a variable with `name=value` (**no spaces** around =). Access its value with `$name`. Example: `datafile=report.csv` then `cat $datafile`. Without the `$`, you get the literal text "datafile".'
    },
    "for loop": {
        "source": "Shell Chapter 4",
        "excerpt": 'Loop structure: `for var in list; do commands; done`. Example: `for f in *.csv; do head $f; done` shows first lines of all CSV files. The variable `$f` takes each filename in turn. Use `$var` to access the value.'
    },
    "script argument": {
        "source": "Shell Chapter 5",
        "excerpt": 'In scripts, `$1` is the first argument, `$2` the second, etc. `$@` means all arguments. If script.sh contains `head $1`, then `bash script.sh data.csv` runs `head data.csv`.'
    },
    
    # ==========================================================================
    # MLOPS CONCEPTS (MLOps Concepts course)
    # ==========================================================================
    
    # Chapter 1 concepts
    "mlops purpose": {
        "source": "MLOps Chapter 1, Video 1",
        "excerpt": 'MLOps is the abbreviation for Machine Learning Operations, and it describes the set of practices to **design, deploy and maintain machine learning in production continuously, reliably, and efficiently**. MLOps also facilitates **monitoring of model performance**, which helps to maintain accuracy and reliability over time.'
    },
    "mlops principles": {
        "source": "Chapter 1, Video 1",
        "excerpt": 'Through MLOps principles we can **automate the deployment of models**, which reduces manual errors and speeds up the process of getting models from development to production. Inherent to MLOps is that it aims to **bridge the gap between machine learning and operations teams**, which enhances collaboration.'
    },
    "design phase": {
        "source": "Chapter 1, Video 2",
        "excerpt": 'In the **design phase**, we clarify the context of the problem and assess the added value of using machine learning. **Gathering clear business requirements** helps us define success, while establishing key metrics allows us to track progress effectively.'
    },
    "development phase": {
        "source": "Chapter 1, Video 2",
        "excerpt": 'In the **development phase**, the real magic happens. This is where we dive deep into creating our machine learning model. We experiment with various combinations of data, algorithms, and hyperparameters, testing different approaches to find the best fit.'
    },
    "deployment phase": {
        "source": "Chapter 1, Video 2",
        "excerpt": 'In the **deployment phase**, our model meets the real world. We focus on integrating our model into existing business processes, ensuring it operates seamlessly within the larger system. Setting up monitoring systems is crucial here.'
    },
    "subject matter expert": {
        "source": "Chapter 1, Video 3",
        "excerpt": 'The **subject matter expert** has **domain knowledge about the problem** that we are trying to solve. The subject matter expert is involved throughout the lifecycle because **they can assist the more technical roles with interpreting the data and results** at each step.'
    },
    "data scientist": {
        "source": "Chapter 1, Video 3",
        "excerpt": 'The **data scientist** is responsible for data analysis and model training and evaluation. The evaluation includes monitoring the model once it has been deployed to ensure that the model predictions are valid.'
    },
    "data engineer": {
        "source": "Chapter 1, Video 3",
        "excerpt": 'The **data engineer** is responsible for the collecting, storing, and processing of data. This also means that the data engineer should check the data quality and include tests such that the quality is maintained throughout the process.'
    },
    "business stakeholder": {
        "source": "Chapter 1, Video 3",
        "excerpt": 'The **business stakeholder**, or product owner, is a managerial staff member making budget decisions and ensuring the machine learning project aligns with the company\'s vision. They are involved throughout the lifecycle.'
    },
    "ml engineer": {
        "source": "Chapter 1, Video 3",
        "excerpt": 'The **machine learning engineer** is a relatively new role that is quite versatile and designed specifically to have expertise over the entire machine learning lifecycle. It is a cross-functional role that overlaps with the other technical roles.'
    },
    
    # Chapter 2 concepts
    "stakeholder metrics": {
        "source": "Chapter 2, Video 1",
        "excerpt": 'The roles involved in MLOps processes are multidisciplinary and thus also have **their own way of tracking performance**. The data scientist looks at the **accuracy** of a model... The **subject matter expert** is interested in the model\'s **impact on the business**... The **business stakeholder** is more interested in the **monetary value** of the model.'
    },
    "accuracy": {
        "source": "Chapter 2, Video 2",
        "excerpt": 'An example of **accuracy** would be whether the data correctly describes the customer. It could be that the data states that a customer is 18, but the customer is actually 32. That would be inaccurate.'
    },
    "completeness": {
        "source": "Chapter 2, Video 2",
        "excerpt": 'For **completeness**, we mainly look at missing data, for instance, whether we are missing last names of customers.'
    },
    "consistency": {
        "source": "Chapter 2, Video 2",
        "excerpt": 'With **consistency**, we investigate whether the definition of a customer is **consistent throughout the organization**. It could be that one department has a **different definition of an active customer than another**, which makes the data inconsistent.'
    },
    "timeliness": {
        "source": "Chapter 2, Video 2",
        "excerpt": 'If we look at **timeliness**, we are interested in the availability of data. For instance, when the customer orders are synchronized daily, they are not available in real-time.'
    },
    "feature engineering": {
        "source": "Chapter 2, Video 3",
        "excerpt": '**Feature engineering** is the process of selecting, manipulating, and transforming raw data into features. A feature is a variable, such as a column in a table. The goal is to enhance model performance by identifying the most informative features.'
    },
    "feature store": {
        "source": "Chapter 2, Video 3",
        "excerpt": 'A **feature store** is a **centralized repository for features**, allowing data scientists to **discover, define, and reuse features** across projects. Feature stores are essential in large teams where multiple projects need **consistent and reusable features**.'
    },
    "experiment tracking": {
        "source": "Chapter 2, Video 4",
        "excerpt": 'Why is tracking all of this so crucial? Well, it helps us **compare results, reproduce past experiments**, collaborate with our team, and report findings to stakeholders. Before starting the training, we establish our experiment tracking to **log every detail meticulously**.'
    },
    
    # Chapter 3 concepts
    "container": {
        "source": "Chapter 3, Video 1",
        "excerpt": 'A **container** is like a special box that holds a computer program along with everything it needs to run, such as certain tools and settings. This makes it easier to move programs around and ensures they don\'t break when they\'re used on different computers.'
    },
    "containerization": {
        "source": "Chapter 3, Video 1",
        "excerpt": 'A **container** is like a special box that holds everything our model needs to run—code, libraries, and settings. **Containerization** packages applications with their dependencies, ensuring consistent runtime environments across development, testing, and production.'
    },
    "microservices": {
        "source": "Chapter 3, Video 1",
        "excerpt": '**Microservices architecture** deploys applications as a collection of independent services. Each service handles a specific function and communicates through APIs, enabling scalability and independent deployment.'
    },
    "api": {
        "source": "Chapter 3, Video 1",
        "excerpt": 'An **API** (Application Programming Interface) enables communication between services. In ML deployment, APIs allow other applications to send data to the model and receive predictions.'
    },
    "ci/cd": {
        "source": "Chapter 3, Video 2",
        "excerpt": '**CI/CD pipelines** (Continuous Integration/Continuous Deployment) automate the build, test, and deployment process. This allows multiple developers to work on the same code and helps in automating the development and deployment process.'
    },
    "basic deployment": {
        "source": "Chapter 3, Video 2",
        "excerpt": 'In **basic deployment**, we simply replace the old model with the new one. This is straightforward but risky—if the new model has issues, all users are affected immediately.'
    },
    "shadow deployment": {
        "source": "Chapter 3, Video 2",
        "excerpt": 'In **shadow deployment**, the new model runs alongside the old one, receiving the same inputs. We compare outputs without affecting users, allowing safe validation of the new model.'
    },
    "canary deployment": {
        "source": "Chapter 3, Video 2",
        "excerpt": 'In **canary deployment**, we gradually roll out the new model to a small percentage of users first. If metrics look good, we increase the percentage until full deployment.'
    },
    
    # Chapter 4 concepts
    "data drift": {
        "source": "Chapter 4, Video 1",
        "excerpt": '**Data drift** occurs when the input data distribution changes over time. The model was trained on historical data, but the real-world data it now receives has different characteristics.'
    },
    "concept drift": {
        "source": "Chapter 4, Video 1",
        "excerpt": '**Concept drift** occurs when the relationship between input data and the target variable changes. Even if the input data looks the same, what constitutes a correct prediction has shifted.'
    },
    "statistical monitoring": {
        "source": "Chapter 4, Video 1",
        "excerpt": '**Statistical monitoring** tracks the distribution of input data and model predictions over time. This helps detect data drift and concept drift before they significantly impact model performance.'
    },
    "computational monitoring": {
        "source": "Chapter 4, Video 1",
        "excerpt": '**Computational monitoring** tracks technical metrics like request latency, network usage, and resource consumption. This ensures the model infrastructure remains healthy and responsive.'
    },
    "mlops maturity": {
        "source": "Chapter 4, Video 2",
        "excerpt": '**MLOps maturity levels** describe the degree of automation, collaboration, and monitoring in an organization\'s ML practices. Higher maturity means more automated pipelines, better governance, and proactive monitoring.'
    },
}


def find_curated_snippet(item: 'MCItem') -> Optional[CourseReference]:
    """Find a curated definitional snippet for this item.
    
    Priority:
    1. If teaching_point is specified, return that directly
    2. Match against curated snippets database
    """
    # If teaching_point is explicitly provided, use that
    if item.teaching_point:
        source = f"📍 Teaching Point"
        if item.course_section:
            source += f" ({item.course_section})"
        return CourseReference(
            source=source,
            excerpt=item.teaching_point
        )
    
    # Otherwise, match against curated snippets
    item_text = f"{item.title} {item.assignment}".lower()
    correct_answer = next((opt.text.lower() for opt in item.options if opt.is_correct), "")
    
    # Also check unit name
    unit_text = item.unit.replace('-', ' ').replace('_', ' ').lower()
    
    # Priority matching based on concept keywords
    match_scores = []
    
    for concept_key, snippet_data in CURATED_SNIPPETS.items():
        score = 0
        concept_words = concept_key.split()
        
        # Check if concept appears in title, stem, or correct answer
        for word in concept_words:
            if word in item.title.lower():
                score += 10
            if word in item_text:
                score += 5
            if word in correct_answer:
                score += 8
            if word in unit_text:
                score += 12  # Strong signal from unit name
        
        # Bonus for multi-word concept matches
        if concept_key in item_text or concept_key in correct_answer:
            score += 15
        if concept_key in unit_text:
            score += 20
        
        if score > 0:
            match_scores.append((score, concept_key, snippet_data))
    
    if not match_scores:
        return None
    
    # Return highest scoring match
    match_scores.sort(key=lambda x: x[0], reverse=True)
    best = match_scores[0]
    
    return CourseReference(
        source=f"📖 {best[1].title()} — {best[2]['source']}",
        excerpt=best[2]['excerpt']
    )


# ============================================================================
# MATCHING ENGINE
# ============================================================================

def extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text."""
    # Common conceptual terms for MC items
    concept_terms = {
        # Shell/Unix commands and concepts
        'command', 'shell', 'bash', 'terminal', 'console',
        'directory', 'folder', 'file', 'path', 'filename',
        'absolute', 'relative', 'root', 'home', 'parent', 'current',
        'copy', 'move', 'remove', 'delete', 'rename', 'create', 'mkdir', 'rmdir',
        'cd', 'ls', 'pwd', 'cat', 'head', 'tail', 'less', 'more',
        'cut', 'grep', 'sort', 'uniq', 'wc', 'echo', 'history',
        'pipe', 'redirect', 'redirection', 'output', 'input', 'stdin', 'stdout',
        'wildcard', 'glob', 'pattern', 'match',
        'loop', 'for', 'variable', 'script', 'argument', 'parameter',
        'flag', 'option', 'delimiter', 'separator', 'column', 'field', 'line',
        'duplicate', 'unique', 'count', 'filter', 'select', 'extract',
        
        # General tech/programming
        'container', 'docker', 'kubernetes', 'microservice', 'api', 'database',
        'function', 'class', 'method', 'iteration', 'recursion', 'algorithm',
        
        # Data science
        'model', 'training', 'prediction', 'accuracy', 'precision', 'recall',
        'dataset', 'feature', 'label', 'classification', 'regression',
        'neural', 'network', 'layer', 'optimizer', 'gradient',
        
        # ML/AI specific
        'agent', 'agentic', 'llm', 'prompt', 'token', 'embedding',
        'transformer', 'attention', 'inference',
        'pipeline', 'workflow', 'orchestration', 'automation',
        
        # Software engineering
        'modularity', 'scalability', 'maintainability', 'testing',
        'deployment', 'infrastructure', 'logging', 'monitoring',
        'version', 'control', 'git', 'branch', 'merge',
    }
    
    # Extract words and filter
    words = set(re.findall(r'\b[a-z_]+\b', text.lower()))
    return words & concept_terms


def find_relevant_video_content(item: MCItem, scripts: Dict[str, str], max_refs: int = 2) -> List[CourseReference]:
    """Find relevant video script excerpts for an item.
    
    Uses multiple strategies:
    1. Explicit course_section field (highest priority)
    2. Unit name matching to section titles
    3. Teaching pattern extraction
    4. Keyword overlap (fallback)
    """
    refs = []
    
    # Strategy 1: If course_section is specified, find that exact section
    if item.course_section:
        for video_key, video_content in scripts.items():
            if item.course_section.lower() in video_key.lower():
                excerpt = extract_teaching_excerpt(video_content, item)
                if excerpt:
                    refs.append(CourseReference(
                        source=f"📍 {video_key} (explicit match)",
                        excerpt=excerpt
                    ))
                    return refs  # Return immediately - this is the definitive source
    
    # Strategy 2: Match unit name to section titles
    unit_words = set(item.unit.replace('-', ' ').replace('_', ' ').lower().split())
    for video_key, video_content in scripts.items():
        key_words = set(video_key.lower().split())
        if len(unit_words & key_words) >= 2:  # At least 2 words match
            excerpt = extract_teaching_excerpt(video_content, item)
            if excerpt:
                refs.append(CourseReference(
                    source=f"📍 {video_key} (unit match)",
                    excerpt=excerpt
                ))
                if len(refs) >= max_refs:
                    return refs
    
    # Strategy 3 & 4: Keyword matching with teaching pattern bonus
    item_text = f"{item.title} {item.assignment}"
    for opt in item.options:
        item_text += f" {opt.text}"
    
    item_keywords = extract_keywords(item_text)
    
    scored_refs = []
    
    for video_key, video_content in scripts.items():
        # Skip if already added via unit match
        if any(video_key in ref.source for ref in refs):
            continue
            
        # Score based on keyword overlap
        video_keywords = extract_keywords(video_content)
        overlap = len(item_keywords & video_keywords)
        
        # Bonus for direct term matches
        video_lower = video_content.lower()
        direct_matches = sum(1 for kw in item_keywords if kw in video_lower)
        
        # Bonus for teaching patterns
        teaching_bonus = score_teaching_patterns(video_content, item_keywords)
        
        score = overlap * 2 + direct_matches + teaching_bonus * 3
        
        if score > 5:  # Minimum threshold
            excerpt = extract_teaching_excerpt(video_content, item)
            if excerpt:
                scored_refs.append((score, video_key, excerpt))
    
    # Sort by score and take top refs
    scored_refs.sort(key=lambda x: x[0], reverse=True)
    
    remaining_slots = max_refs - len(refs)
    for score, video_key, excerpt in scored_refs[:remaining_slots]:
        refs.append(CourseReference(source=f"🔍 {video_key}", excerpt=excerpt))
    
    return refs


def score_teaching_patterns(content: str, keywords: set) -> int:
    """Score content based on presence of teaching patterns near keywords."""
    score = 0
    content_lower = content.lower()
    
    # Teaching pattern indicators
    teaching_patterns = [
        r'`([^`]+)`\s+(is|means|does|removes|creates|shows|displays|prints|selects|extracts)',
        r'the\s+`([^`]+)`\s+(command|operator|symbol|flag)',
        r'to\s+\w+[^.]*,?\s+you\s+(must|can|should|use|need)',
        r'this\s+(is|means|allows|enables|lets)',
        r'because\s+',
        r'the\s+reason\s+is',
        r'in\s+order\s+to',
        r'\*\*[^*]+\*\*',  # Bold text often indicates definitions
    ]
    
    for pattern in teaching_patterns:
        matches = re.findall(pattern, content_lower)
        # Extra points if the match is near a keyword
        for match in matches:
            match_text = match if isinstance(match, str) else ' '.join(match)
            for kw in keywords:
                if kw in match_text or kw in content_lower[max(0, content_lower.find(match_text)-50):content_lower.find(match_text)+50]:
                    score += 2
                    break
            else:
                score += 1
    
    return min(score, 10)  # Cap the bonus


def extract_teaching_excerpt(content: str, item: MCItem) -> str:
    """Extract the most relevant teaching passage from content.
    
    Prioritizes:
    1. Sentences containing teaching patterns
    2. Sentences containing item keywords
    3. Sentences with command definitions
    """
    # Get keywords from item
    item_text = f"{item.title} {item.assignment}"
    for opt in item.options:
        item_text += f" {opt.text}"
    keywords = extract_keywords(item_text)
    
    # Also include command names from item (backtick content)
    commands = set(re.findall(r'`([^`]+)`', item_text))
    
    # Split into sentences/paragraphs
    paragraphs = re.split(r'\n\n+', content)
    
    best_score = 0
    best_excerpt = ""
    
    for para in paragraphs:
        if len(para) < 30 or len(para) > 500:  # Skip too short or too long
            continue
            
        score = 0
        para_lower = para.lower()
        
        # Score keyword presence
        for kw in keywords:
            if kw in para_lower:
                score += 2
        
        # Score command mention
        for cmd in commands:
            if cmd.lower() in para_lower or f'`{cmd}`' in para:
                score += 5
        
        # Bonus for teaching language
        teaching_indicators = [
            'is used to', 'allows you to', 'means', 'will print', 'will display',
            'tells the shell', 'removes', 'creates', 'selects', 'extracts',
            'the command', 'the operator', 'the symbol', 'for example',
            'you can use', 'you must', 'notice that', 'this is because'
        ]
        for indicator in teaching_indicators:
            if indicator in para_lower:
                score += 3
        
        # Bonus for bold/emphasis (definitions)
        if '**' in para:
            score += 4
        
        # Bonus for code examples
        if '`' in para:
            score += 2
        
        if score > best_score:
            best_score = score
            best_excerpt = para
    
    # Clean up and truncate
    if best_excerpt:
        # Remove markdown code block markers
        best_excerpt = re.sub(r'```\w*\n?', '', best_excerpt)
        best_excerpt = best_excerpt.strip()
        
        if len(best_excerpt) > 400:
            best_excerpt = best_excerpt[:400] + "..."
    
    return best_excerpt




def validate_option_lengths(options: List[MCOption]) -> Tuple[bool, List[str]]:
    """Validate option lengths and return warnings."""
    warnings = []
    valid = True
    
    lengths = [opt.length for opt in options]
    correct_length = next((opt.length for opt in options if opt.is_correct), 0)
    
    # Check ±8 rule
    for i, opt1 in enumerate(options):
        for j, opt2 in enumerate(options):
            if i < j and abs(opt1.length - opt2.length) > 8:
                warnings.append(f"Options {i+1} and {j+1} differ by {abs(opt1.length - opt2.length)} chars (>8)")
                valid = False
    
    # Check correct not longest
    max_distractor = max((opt.length for opt in options if not opt.is_correct), default=0)
    if correct_length > max_distractor:
        warnings.append(f"Correct answer ({correct_length} chars) is longer than all distractors")
    
    return valid, warnings


def enrich_items(items: List[MCItem], scripts: Dict[str, str]) -> List[EnrichedItem]:
    """Add course references and validation to items."""
    enriched = []
    
    for item in items:
        video_refs = find_relevant_video_content(item, scripts)
        length_valid, length_warnings = validate_option_lengths(item.options)
        
        # Parse embedded course content reference (highest priority)
        embedded_refs = []
        if item.course_content_reference:
            embedded_refs.append(CourseReference(
                source=f"📍 AI-Identified ({item.course_section})" if item.course_section else "📍 AI-Identified Content",
                excerpt=item.course_content_reference
            ))
        
        # Find curated definitional snippet (fallback)
        curated_refs = []
        if not embedded_refs:
            curated = find_curated_snippet(item)
            if curated:
                curated_refs.append(curated)
        
        enriched.append(EnrichedItem(
            item=item,
            embedded_refs=embedded_refs,
            video_refs=video_refs,
            curated_refs=curated_refs,
            length_valid=length_valid,
            length_warnings=length_warnings
        ))
    
    return enriched


# ============================================================================
# HTML GENERATOR
# ============================================================================

def generate_html(doc_title: str, enriched_items: List[EnrichedItem]) -> str:
    """Generate HTML preview."""
    
    items_html = ""
    for ei in enriched_items:
        item = ei.item
        
        # Format options
        options_html = ""
        for i, opt in enumerate(item.options):
            correct_class = "correct" if opt.is_correct else ""
            length_class = ""
            
            # Check if this option violates length rule
            for warning in ei.length_warnings:
                if f"Options {i+1}" in warning or f"and {i+1}" in warning:
                    length_class = "length-warning"
            
            marker = "✓" if opt.is_correct else ""
            options_html += f'''
                <div class="option {correct_class} {length_class}">
                    <span class="option-num">{i+1}</span>
                    <span class="option-text">{html.escape(opt.text)}</span>
                    <span class="option-length">{opt.length} chars</span>
                    <span class="option-marker">{marker}</span>
                </div>'''
        
        # Length validation status
        length_status = "✅ Lengths OK" if ei.length_valid else "⚠️ Length issues"
        length_warnings_html = ""
        if ei.length_warnings:
            for w in ei.length_warnings:
                length_warnings_html += f'<div class="length-warning-text">⚠️ {html.escape(w)}</div>'
        
        # Format embedded course content (highest priority - AI-identified)
        embedded_refs_html = ""
        for ref in ei.embedded_refs:
            excerpt_html = html.escape(ref.excerpt)
            excerpt_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', excerpt_html)
            excerpt_html = excerpt_html.replace('\n', '<br>')
            embedded_refs_html += f'''
            <div class="course-ref embedded-ref">
                <div class="ref-header">{html.escape(ref.source)}</div>
                <div class="ref-content">{excerpt_html}</div>
            </div>'''
        
        # Format curated definitional snippets (fallback if no embedded)
        curated_refs_html = ""
        if not embedded_refs_html:
            for ref in ei.curated_refs:
                excerpt_html = html.escape(ref.excerpt)
                excerpt_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', excerpt_html)
                curated_refs_html += f'''
                <div class="course-ref curated-ref">
                    <div class="ref-header">{html.escape(ref.source)}</div>
                    <div class="ref-content">{excerpt_html}</div>
                </div>'''
        
        # Format video references (keyword-matched)
        video_refs_html = ""
        for ref in ei.video_refs:
            video_refs_html += f'''
            <div class="course-ref video-ref">
                <div class="ref-header">🔍 Keyword Match: {html.escape(ref.source)}</div>
                <div class="ref-content">{html.escape(ref.excerpt)}</div>
            </div>'''
        
        items_html += f'''
        <div class="item">
            <div class="item-header">
                <span class="item-number">Item {item.item_number}</span>
                <h2 class="item-title">{html.escape(item.title)}</h2>
            </div>
            
            <div class="yaml-block"><span class="yaml-key">type:</span> <span class="yaml-value">MultipleChoiceChallenge</span>
<span class="yaml-key">unit:</span> <span class="yaml-value">{html.escape(item.unit)}</span>
<span class="yaml-key">subskill:</span> <span class="yaml-value">{html.escape(item.subskill)}</span></div>
            
            <div class="section-label">📋 Stem (Assignment)</div>
            <div class="stem-box">{html.escape(item.assignment)}</div>
            
            <div class="section-label">🔘 Options <span class="length-status">{length_status}</span></div>
            <div class="options-container">{options_html}</div>
            {length_warnings_html}
            
            <div class="section-label">📚 Course Alignment</div>
            <div class="references-container">
                {embedded_refs_html if embedded_refs_html else curated_refs_html if curated_refs_html else '<div class="no-refs">No course content reference found - add course_content_reference field</div>'}
            </div>
            
            <div class="section-label">🔍 Keyword Matches <span class="ref-note">(automated fallback)</span></div>
            <div class="references-container">
                {video_refs_html if video_refs_html else '<div class="no-refs">No keyword matches found</div>'}
            </div>
        </div>'''
    
    # Calculate rotation info
    positions = [ei.item.correct_position for ei in enriched_items]
    rotation_html = " → ".join(str(p) for p in positions)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MC Preview - {html.escape(doc_title)}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{
            color: #ff6b9d;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #ff6b9d;
            padding-bottom: 0.5rem;
        }}
        .pool-info {{
            background: rgba(255, 107, 157, 0.1);
            border-left: 4px solid #ff6b9d;
            padding: 1rem;
            margin-bottom: 2rem;
            border-radius: 0 8px 8px 0;
        }}
        .pool-info code {{
            color: #ff6b9d;
            background: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .rotation-info {{
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #7eb8da;
        }}
        .item {{
            background: #1e2a3a;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #2d3f52;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .item-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        .item-number {{
            background: #ff6b9d;
            color: #1a1a2e;
            font-weight: bold;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.9rem;
            white-space: nowrap;
        }}
        .item-title {{
            color: #fff;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
        }}
        .yaml-block {{
            background: #0d1520;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.8rem;
            margin-bottom: 1rem;
            border: 1px solid #2d3f52;
            white-space: pre;
        }}
        .yaml-key {{ color: #ff6b9d; }}
        .yaml-value {{ color: #a8e6cf; }}
        .section-label {{
            color: #7eb8da;
            font-weight: 600;
            font-size: 0.85rem;
            margin: 1rem 0 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .length-status {{
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(168, 230, 207, 0.2);
        }}
        .stem-box {{
            background: rgba(126, 184, 218, 0.1);
            border-left: 3px solid #7eb8da;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        .options-container {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .option {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: #0d1520;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid #2d3f52;
        }}
        .option.correct {{
            background: rgba(168, 230, 207, 0.15);
            border-color: #a8e6cf;
        }}
        .option.length-warning {{
            border-color: #ffc107;
        }}
        .option-num {{
            background: #2d3f52;
            color: #7eb8da;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
            flex-shrink: 0;
        }}
        .option.correct .option-num {{
            background: #a8e6cf;
            color: #1a1a2e;
        }}
        .option-text {{
            flex: 1;
            font-size: 0.9rem;
        }}
        .option-length {{
            color: #666;
            font-size: 0.75rem;
            font-family: monospace;
            white-space: nowrap;
        }}
        .option-marker {{
            color: #a8e6cf;
            font-weight: bold;
            width: 20px;
        }}
        .length-warning-text {{
            color: #ffc107;
            font-size: 0.8rem;
            margin-top: 0.5rem;
            padding-left: 1rem;
        }}
        .references-container {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        .course-ref {{
            border-radius: 8px;
            padding: 0.75rem 1rem;
            font-size: 0.85rem;
        }}
        .curated-ref {{
            background: rgba(168, 230, 207, 0.15);
            border: 1px solid rgba(168, 230, 207, 0.4);
        }}
        .curated-ref .ref-header {{
            color: #a8e6cf;
        }}
        .curated-ref .ref-content strong {{
            color: #a8e6cf;
            font-weight: 600;
        }}
        .embedded-ref {{
            background: rgba(100, 200, 255, 0.15);
            border: 1px solid rgba(100, 200, 255, 0.4);
        }}
        .embedded-ref .ref-header {{
            color: #64c8ff;
        }}
        .embedded-ref .ref-content {{
            white-space: pre-wrap;
        }}
        .video-ref {{
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
        }}
        .ref-header {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #ffc107;
        }}
        .ref-content {{
            color: #ccc;
            line-height: 1.5;
        }}
        .ref-note {{
            font-weight: normal;
            font-size: 0.75rem;
            color: #666;
        }}
        .no-refs {{
            color: #666;
            font-style: italic;
            font-size: 0.85rem;
        }}
        .stats {{
            display: flex;
            gap: 2rem;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 MultipleChoiceChallenge Preview</h1>
        
        <div class="pool-info">
            <strong>Document:</strong> {html.escape(doc_title)}<br>
            <strong>Subskill:</strong> <code>{html.escape(enriched_items[0].item.subskill if enriched_items else "")}</code>
            <div class="stats">
                <span>📝 {len(enriched_items)} items</span>
                <span>🔘 4 options each</span>
            </div>
            <div class="rotation-info">
                <strong>Correct answer positions:</strong> {rotation_html}
            </div>
        </div>

        {items_html}
    </div>
</body>
</html>'''


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate MultipleChoiceChallenge preview with course references")
    parser.add_argument("items_file", type=Path, help="Path to items markdown file")
    parser.add_argument("--scripts", type=Path, help="Directory containing video script files")
    parser.add_argument("--output", "-o", type=Path, default=Path(".cursor/tmp_items/mc_preview.html"), help="Output HTML file")
    
    args = parser.parse_args()
    
    if not args.items_file.exists():
        print(f"❌ Items file not found: {args.items_file}")
        sys.exit(1)
    
    # Parse items
    print(f"📄 Parsing items from {args.items_file}...")
    content = args.items_file.read_text()
    doc_title, items = parse_items_file(content)
    print(f"   Found {len(items)} items")
    
    # Parse course content
    scripts = {}
    
    if args.scripts:
        print(f"📹 Parsing video scripts from {args.scripts}...")
        scripts = parse_video_scripts(args.scripts)
        print(f"   Found {len(scripts)} video sections")
    
    # Enrich items with course references
    print("🔗 Matching items to course content...")
    enriched = enrich_items(items, scripts)
    
    # Generate HTML
    print("🎨 Generating HTML preview...")
    html_content = generate_html(doc_title, enriched)
    
    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_content)
    print(f"✅ Preview generated: {args.output}")
    
    # Open in browser
    import subprocess
    subprocess.run(["open", str(args.output)], check=False)


if __name__ == "__main__":
    main()
