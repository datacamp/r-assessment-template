#!/usr/bin/env python3
"""
BlanksChallenge Preview Generator

Generates rich HTML previews for BlanksChallenge items with course content references.

Features:
- Parses BlanksChallenge markdown items
- Extracts relevant video script excerpts
- Extracts relevant exercise code snippets
- Generates styled HTML preview

Usage:
    python generate_blanks_preview.py <items_file> [--scripts <scripts_dir>] [--exercises <exercises_dir>]
    python generate_blanks_preview.py .cursor/tmp_items/items.md --scripts ~/Downloads/scripts --exercises ~/Downloads

Example:
    python generate_blanks_preview.py .cursor/tmp_items/evaluation_metrics_items.md \
        --scripts /Users/martine.holland/Downloads/scripts \
        --exercises /Users/martine.holland/Downloads
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
class BlanksItem:
    """A single BlanksChallenge item."""
    title: str
    unit: str
    subskill: str
    context: str
    code1: str
    pre_challenge_code: str
    variables: Dict[str, str]
    item_number: int
    blank_count: int = 0
    course_section: str = ""  # Optional: explicit course section reference
    teaching_point: str = ""  # Optional: key concept being tested


@dataclass
class CourseReference:
    """Reference to course content."""
    source: str  # e.g., "Video 3.2" or "chapter3.md"
    excerpt: str  # The relevant text
    code_snippet: Optional[str] = None


@dataclass 
class EnrichedItem:
    """Item with course references."""
    item: BlanksItem
    video_refs: List[CourseReference] = field(default_factory=list)
    exercise_refs: List[CourseReference] = field(default_factory=list)


# ============================================================================
# PARSERS
# ============================================================================

def parse_items_file(content: str) -> Tuple[str, List[BlanksItem]]:
    """Parse BlanksChallenge items from markdown."""
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


def parse_single_item(content: str, item_number: int) -> Optional[BlanksItem]:
    """Parse a single item block."""
    # Extract title
    title_match = re.search(r'##\s+\[([^\]]+)\]', content)
    if not title_match:
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
    
    # Extract sections - support Python, R, and SQL code blocks
    # Language tags: python/{python}, r/{r}, sql/{sql}
    context_match = re.search(r'`@context`\s*\n(.*?)(?=`@|\Z)', content, re.DOTALL)
    code1_match = re.search(r'`@code1`\s*\n```(?:python|\{python\}|r|\{r\}|sql|\{sql\})\s*\n(.*?)```', content, re.DOTALL)
    pre_code_match = re.search(r'`@pre_challenge_code`\s*\n```(?:python|\{python\}|r|\{r\})\s*\n(.*?)```', content, re.DOTALL)
    variables_match = re.search(r'`@variables`\s*\n```yaml\s*\n(.*?)```', content, re.DOTALL)
    
    context = context_match.group(1).strip() if context_match else ""
    code1 = code1_match.group(1).strip() if code1_match else ""
    pre_code = pre_code_match.group(1).strip() if pre_code_match else ""
    
    # Parse variables
    variables = {}
    if variables_match:
        var_content = variables_match.group(1)
        var_blocks = re.findall(r'(expr\d+):\s*\n\s*-\s*(.+)', var_content)
        for var_name, var_value in var_blocks:
            variables[var_name] = var_value.strip().strip("'\"")
    
    # Count blanks
    blank_count = len(re.findall(r'\{\{_expr\d+\}\}', code1))
    
    return BlanksItem(
        title=title,
        unit=unit,
        subskill=subskill,
        context=context,
        code1=code1,
        pre_challenge_code=pre_code,
        variables=variables,
        item_number=item_number,
        blank_count=blank_count,
        course_section=course_section,
        teaching_point=teaching_point
    )


def parse_video_scripts(scripts_dir: Path) -> Dict[str, str]:
    """Parse video scripts from directory."""
    scripts = {}
    
    if not scripts_dir.exists():
        return scripts
    
    for script_file in scripts_dir.glob("*.txt"):
        content = script_file.read_text()
        # Split by video headers
        videos = re.split(r'# Video (\d+)', content)
        
        chapter_match = re.search(r'chapter_(\d+)', script_file.name)
        chapter_num = chapter_match.group(1) if chapter_match else "?"
        
        for i in range(1, len(videos), 2):
            if i + 1 < len(videos):
                video_num = videos[i]
                video_content = videos[i + 1].strip()
                key = f"Video {chapter_num}.{video_num}"
                scripts[key] = video_content
    
    return scripts


def parse_exercises(exercises_dir: Path) -> Dict[str, List[Dict]]:
    """Parse exercise files from directory."""
    exercises = {}
    
    if not exercises_dir.exists():
        return exercises
    
    for ex_file in exercises_dir.glob("chapter*.md"):
        content = ex_file.read_text()
        chapter_name = ex_file.stem
        
        # Extract exercise blocks - support Python, R, and SQL
        ex_blocks = re.findall(
            r'## ([^\n]+)\n.*?`@solution`\s*\n```(?:python|\{python\}|r|\{r\}|sql|\{sql\})\s*\n(.*?)```',
            content, re.DOTALL
        )
        
        exercises[chapter_name] = [
            {"title": title.strip(), "code": code.strip()}
            for title, code in ex_blocks
        ]
    
    return exercises


# ============================================================================
# MATCHING ENGINE
# ============================================================================

def extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text."""
    # Common terms across Python, R, and SQL exercises
    common_terms = {
        # Python/ML evaluation terms
        'accuracy', 'precision', 'recall', 'f1', 'bleu', 'rouge', 'meteor',
        'perplexity', 'toxicity', 'evaluate', 'metric', 'compute', 'load',
        'predictions', 'references', 'score', 'classification', 'summarization',
        'translation', 'generation', 'pipeline', 'model', 'tokenizer',
        # scikit-learn / supervised learning terms
        'fit', 'predict', 'train', 'test', 'split', 'training', 'testing',
        'knn', 'neighbors', 'classifier', 'regression', 'linear', 'logistic',
        'ridge', 'lasso', 'alpha', 'regularization', 'regularized',
        'cross_validation', 'cross_val', 'kfold', 'gridsearch', 'gridsearchcv',
        'hyperparameter', 'tuning', 'overfitting', 'underfitting',
        'confusion', 'matrix', 'roc', 'auc', 'rmse', 'r_squared', 'r2',
        'dummy', 'dummies', 'categorical', 'encoding', 'impute', 'imputer',
        'scale', 'scaler', 'standardscaler', 'preprocessing', 'preprocess',
        'features', 'target', 'labels', 'supervised', 'unsupervised',
        # MLflow terms
        'mlflow', 'experiment', 'experiments', 'tracking', 'run', 'runs',
        'artifact', 'artifacts', 'autolog', 'log_metric', 'log_param',
        'log_artifact', 'log_model', 'start_run', 'end_run', 'search_runs',
        'register_model', 'registry', 'registered', 'version', 'stage',
        'staging', 'production', 'archived', 'transition', 'flavor', 'flavors',
        'sklearn', 'pyfunc', 'projects', 'mlproject', 'entry_point', 'workflow',
        'serve', 'deploy', 'deployment', 'invocations', 'client',
        # R/tidyverse terms
        'filter', 'select', 'mutate', 'summarize', 'summarise', 'group_by',
        'arrange', 'dplyr', 'ggplot', 'tidyr', 'tibble', 'pipe', 'dataframe',
        'geom_point', 'geom_bar', 'geom_line', 'aes', 'facet',
        # SQL terms
        'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'outer',
        'group', 'order', 'having', 'count', 'sum', 'avg', 'max', 'min',
        'aggregate', 'subquery', 'table', 'column', 'query'
    }
    
    # Extract words and filter
    words = set(re.findall(r'\b[a-z_]+\b', text.lower()))
    return words & common_terms


def find_relevant_video_content(item: BlanksItem, scripts: Dict[str, str], max_refs: int = 2) -> List[CourseReference]:
    """Find relevant video script excerpts for an item.
    
    Uses multiple strategies:
    1. Explicit teaching_point field (highest priority)
    2. Explicit course_section field
    3. Keyword and code pattern matching (fallback)
    """
    refs = []
    
    # Strategy 1: If teaching_point is specified, use that directly
    if item.teaching_point:
        source = "📍 Teaching Point"
        if item.course_section:
            source += f" ({item.course_section})"
        refs.append(CourseReference(source=source, excerpt=item.teaching_point))
        if len(refs) >= max_refs:
            return refs
    
    # Strategy 2: If course_section is specified, find that exact section
    if item.course_section:
        for video_key, video_content in scripts.items():
            if item.course_section.lower() in video_key.lower():
                item_keywords = extract_keywords(f"{item.title} {item.context} {item.code1}")
                excerpt = extract_relevant_excerpt(video_content, item_keywords)
                if excerpt:
                    refs.append(CourseReference(source=video_key, excerpt=excerpt))
                    if len(refs) >= max_refs:
                        return refs
    
    # Strategy 3: Keyword and code pattern matching
    item_text = f"{item.title} {item.context} {item.code1}"
    item_keywords = extract_keywords(item_text)
    
    # Also check for specific function/method names
    code_terms = set(re.findall(r'[a-z_]+', item.code1.lower()))
    
    scored_refs = []
    
    for video_key, video_content in scripts.items():
        # Score based on keyword overlap
        video_keywords = extract_keywords(video_content)
        overlap = len(item_keywords & video_keywords)
        
        # Bonus for code term matches
        video_lower = video_content.lower()
        code_matches = sum(1 for term in code_terms if term in video_lower and len(term) > 3)
        
        # Bonus for MLflow-specific patterns
        mlflow_patterns = ['mlflow.', 'start_run', 'log_metric', 'log_param', 'autolog', 
                          'register_model', 'search_runs', 'projects.run']
        for pattern in mlflow_patterns:
            if pattern in item.code1.lower() and pattern in video_lower:
                code_matches += 5
        
        score = overlap + code_matches
        
        if score > 0:
            # Extract relevant paragraph
            excerpt = extract_relevant_excerpt(video_content, item_keywords | code_terms)
            if excerpt:
                scored_refs.append((score, video_key, excerpt))
    
    # Sort by score and take top refs
    scored_refs.sort(key=lambda x: x[0], reverse=True)
    
    remaining_slots = max_refs - len(refs)
    for score, video_key, excerpt in scored_refs[:remaining_slots]:
        refs.append(CourseReference(source=video_key, excerpt=excerpt))
    
    return refs


def find_relevant_exercises(item: BlanksItem, exercises: Dict[str, List[Dict]], max_refs: int = 2) -> List[CourseReference]:
    """Find relevant exercise code for an item.
    
    Prioritizes exercises that contain the actual blank answer in their code.
    """
    refs = []
    
    # Get the actual blank answers - these should appear in matched exercises
    blank_answers = [v.lower() for v in item.variables.values()]
    
    # Extract specific code patterns from item
    item_code = item.code1.lower()
    
    # Look for library/module usage patterns
    code_patterns = []
    
    # Python: Extract function calls like evaluate.load, evaluate.compute
    func_calls = re.findall(r'(\w+)\.(\w+)\s*\(', item.code1)
    for obj, method in func_calls:
        code_patterns.append(f"{obj}.{method}")
        code_patterns.append(obj)
        code_patterns.append(method)
    
    # Extract standalone function calls (works for Python, R, SQL functions)
    standalone = re.findall(r'\b(\w+)\s*\(', item.code1)
    code_patterns.extend(standalone)
    
    # R: Extract pipe chain functions (data %>% filter() %>% select())
    pipe_funcs = re.findall(r'%>%\s*(\w+)\s*\(', item.code1)
    code_patterns.extend(pipe_funcs)
    
    # R: Extract ggplot geoms (geom_point, geom_bar, etc.)
    geoms = re.findall(r'\b(geom_\w+)\b', item.code1)
    code_patterns.extend(geoms)
    
    # SQL: Extract SQL keywords and clauses
    sql_keywords = re.findall(r'\b(SELECT|FROM|WHERE|JOIN|GROUP BY|ORDER BY|HAVING|COUNT|SUM|AVG|MAX|MIN)\b', item.code1, re.IGNORECASE)
    code_patterns.extend([kw.upper() for kw in sql_keywords])
    
    # Extract variable names that look like metrics or common concepts
    metric_names = re.findall(r'\b(accuracy|precision|recall|f1|bleu|rouge|meteor|perplexity|toxicity|exact_match)\b', item_code)
    code_patterns.extend(metric_names)
    
    # R: dplyr verbs
    dplyr_verbs = re.findall(r'\b(filter|select|mutate|summarize|summarise|group_by|arrange|slice|rename)\b', item_code)
    code_patterns.extend(dplyr_verbs)
    
    scored_refs = []
    
    for chapter, ex_list in exercises.items():
        for ex in ex_list:
            ex_code = ex['code'].lower()
            score = 0
            
            # CRITICAL: Massive bonus if exercise contains the actual blank answer
            answer_found = False
            for answer in blank_answers:
                if answer in ex_code:
                    score += 100  # Ensure this exercise is prioritized
                    answer_found = True
            
            # If this exercise doesn't contain any blank answer, it's less useful
            # but still might provide context
            if not answer_found:
                score -= 50  # Penalize exercises without the answer
            
            # High score for matching library patterns (e.g., evaluate.load)
            for pattern in code_patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in ex_code:
                    # Higher weight for compound patterns like "evaluate.load"
                    if '.' in pattern:
                        score += 10
                    elif pattern_lower in ('filter', 'select', 'mutate', 'summarize', 'group_by'):
                        score += 8  # dplyr verbs
                    elif len(pattern) > 4:
                        score += 3
                    else:
                        score += 1
            
            # Python: Bonus for matching the exact library (evaluate)
            if 'evaluate' in item_code and 'evaluate' in ex_code:
                score += 15
            
            # Python: Bonus for matching compute/load patterns
            if '.compute(' in item_code and '.compute(' in ex_code:
                score += 10
            if '.load(' in item_code and 'load(' in ex_code:
                score += 5
            
            # scikit-learn: Bonus for fit/predict patterns
            if '.fit(' in item_code and '.fit(' in ex_code:
                score += 12
            if '.predict(' in item_code and '.predict(' in ex_code:
                score += 12
            if '.score(' in item_code and '.score(' in ex_code:
                score += 10
            if 'train_test_split' in item_code and 'train_test_split' in ex_code:
                score += 15
            
            # scikit-learn: Model types
            if 'kneighbors' in item_code and 'kneighbors' in ex_code:
                score += 12
            if 'linearregression' in item_code and 'linearregression' in ex_code:
                score += 12
            if 'ridge' in item_code and 'ridge' in ex_code:
                score += 12
            if 'lasso' in item_code and 'lasso' in ex_code:
                score += 12
            if 'logisticregression' in item_code and 'logisticregression' in ex_code:
                score += 12
            if 'gridsearchcv' in item_code and 'gridsearchcv' in ex_code:
                score += 15
            
            # scikit-learn: Preprocessing
            if 'get_dummies' in item_code and 'get_dummies' in ex_code:
                score += 15
            if 'pipeline' in item_code and 'pipeline' in ex_code:
                score += 12
            if 'simpleimputer' in item_code and 'simpleimputer' in ex_code:
                score += 12
            if 'standardscaler' in item_code and 'standardscaler' in ex_code:
                score += 12
            
            # Metrics
            if 'classification_report' in item_code and 'classification_report' in ex_code:
                score += 15
            if 'confusion_matrix' in item_code and 'confusion_matrix' in ex_code:
                score += 12
            
            # R: Bonus for pipe operator usage
            if '%>%' in item.code1 and '%>%' in ex['code']:
                score += 8
            if '|>' in item.code1 and '|>' in ex['code']:
                score += 8
            
            # R: ggplot matching
            if 'ggplot' in item_code and 'ggplot' in ex_code:
                score += 10
            
            # SQL: JOIN matching
            if 'join' in item_code and 'join' in ex_code:
                score += 8
            
            # MLflow: Experiment and tracking patterns
            if 'mlflow' in item_code and 'mlflow' in ex_code:
                score += 15
            if 'create_experiment' in item_code and 'create_experiment' in ex_code:
                score += 20
            if 'set_experiment' in item_code and 'set_experiment' in ex_code:
                score += 15
            if 'set_experiment_tag' in item_code and 'set_experiment_tag' in ex_code:
                score += 20
            if 'start_run' in item_code and 'start_run' in ex_code:
                score += 15
            if 'log_metric' in item_code and 'log_metric' in ex_code:
                score += 20
            if 'log_param' in item_code and 'log_param' in ex_code:
                score += 20
            if 'log_artifact' in item_code and 'log_artifact' in ex_code:
                score += 15
            if 'search_runs' in item_code and 'search_runs' in ex_code:
                score += 20
            
            # MLflow: Models and flavors
            if 'autolog' in item_code and 'autolog' in ex_code:
                score += 20
            if 'save_model' in item_code and 'save_model' in ex_code:
                score += 15
            if 'load_model' in item_code and 'load_model' in ex_code:
                score += 15
            if 'log_model' in item_code and 'log_model' in ex_code:
                score += 20
            if 'last_active_run' in item_code and 'last_active_run' in ex_code:
                score += 15
            if 'mlflow.sklearn' in item_code and 'mlflow.sklearn' in ex_code:
                score += 20
            if 'mlflow.pyfunc' in item_code and 'mlflow.pyfunc' in ex_code:
                score += 20
            
            # MLflow: Model Registry
            if 'register_model' in item_code and 'register_model' in ex_code:
                score += 20
            if 'mlflowclient' in item_code and 'mlflowclient' in ex_code:
                score += 15
            if 'create_registered_model' in item_code and 'create_registered_model' in ex_code:
                score += 20
            if 'search_registered_models' in item_code and 'search_registered_models' in ex_code:
                score += 15
            if 'transition_model_version_stage' in item_code and 'transition_model_version_stage' in ex_code:
                score += 20
            if 'models:/' in item_code and 'models:/' in ex_code:
                score += 15
            
            # MLflow: Projects
            if 'mlflow.projects' in item_code and 'mlflow.projects' in ex_code:
                score += 20
            if 'projects.run' in item_code and 'projects.run' in ex_code:
                score += 20
            if 'entry_point' in item_code and 'entry_point' in ex_code:
                score += 15
            if 'mlproject' in item_code.lower() and 'mlproject' in ex_code.lower():
                score += 10
            
            if score > 0:  # Only include exercises with positive score (ideally with the answer)
                scored_refs.append((score, chapter, ex))
    
    scored_refs.sort(key=lambda x: x[0], reverse=True)
    
    for score, chapter, ex in scored_refs[:max_refs]:
        refs.append(CourseReference(
            source=f"{chapter}: {ex['title']}",
            excerpt="",
            code_snippet=ex['code'][:400] + ("..." if len(ex['code']) > 400 else "")
        ))
    
    return refs


def extract_relevant_excerpt(content: str, keywords: set, context_lines: int = 4) -> str:
    """Extract the most relevant paragraph from content.
    
    Prioritizes lines that contain specific function/method names (with underscores)
    over lines with generic keywords.
    """
    lines = content.split('\n')
    best_score = 0
    best_start = 0
    
    # Identify "specific" keywords (function names with underscores or dots)
    specific_keywords = {kw for kw in keywords if '_' in kw or '.' in kw}
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        line_keywords = extract_keywords(line)
        
        # Base score from keyword overlap
        overlap = line_keywords & keywords
        score = len(overlap)
        
        # BONUS: Extra points for specific function names found in the line text
        for specific in specific_keywords:
            if specific in line_lower:
                score += 5  # Strong bonus for exact function match
        
        if score > best_score:
            best_score = score
            best_start = max(0, i - 1)
    
    if best_score == 0:
        return ""
    
    # Get surrounding context
    excerpt_lines = lines[best_start:best_start + context_lines]
    excerpt = ' '.join(line.strip() for line in excerpt_lines if line.strip())
    
    # Truncate if too long
    if len(excerpt) > 400:
        excerpt = excerpt[:400] + "..."
    
    return excerpt


def enrich_items(items: List[BlanksItem], scripts: Dict[str, str], exercises: Dict[str, List[Dict]]) -> List[EnrichedItem]:
    """Add course references to items."""
    enriched = []
    
    for item in items:
        video_refs = find_relevant_video_content(item, scripts)
        exercise_refs = find_relevant_exercises(item, exercises)
        
        enriched.append(EnrichedItem(
            item=item,
            video_refs=video_refs,
            exercise_refs=exercise_refs
        ))
    
    return enriched


# ============================================================================
# HTML GENERATOR
# ============================================================================

def generate_html(doc_title: str, enriched_items: List[EnrichedItem], subskill: str = "") -> str:
    """Generate HTML preview."""
    
    items_html = ""
    for ei in enriched_items:
        item = ei.item
        
        # Format code with blanks highlighted
        code_html = html.escape(item.code1)
        code_html = re.sub(
            r'\{\{(_expr\d+)\}\}',
            r'<span class="blank">{{\1}}</span>',
            code_html
        )
        
        # Format variables
        vars_html = ""
        for var_name, var_value in item.variables.items():
            vars_html += f'''
                <div class="variable-chip">
                    <div class="var-name">{var_name}</div>
                    <div class="var-value">'{html.escape(var_value)}'</div>
                </div>'''
        
        # Get the blank answers for highlighting
        blank_answers = list(item.variables.values())
        
        def highlight_answers(text: str, answers: list, is_code: bool = False) -> str:
            """Highlight blank answers in text."""
            result = html.escape(text)
            for answer in answers:
                # Escape the answer for regex
                escaped_answer = html.escape(answer)
                # Use word boundaries for non-code, more flexible for code
                if is_code:
                    # In code, highlight the function/method name
                    result = re.sub(
                        rf'(\b{re.escape(escaped_answer)}\b)',
                        r'<span class="answer-highlight">\1</span>',
                        result
                    )
                else:
                    # In text, also match with underscores converted to spaces
                    result = re.sub(
                        rf'(\b{re.escape(escaped_answer)}\b)',
                        r'<span class="answer-highlight">\1</span>',
                        result
                    )
                    # Also try matching the readable form (e.g., "log metric" for "log_metric")
                    readable = answer.replace('_', ' ')
                    if readable != answer:
                        result = re.sub(
                            rf'(\b{re.escape(html.escape(readable))}\b)',
                            r'<span class="answer-highlight">\1</span>',
                            result,
                            flags=re.IGNORECASE
                        )
            return result
        
        # Format video references with highlighting
        video_refs_html = ""
        for ref in ei.video_refs:
            highlighted_excerpt = highlight_answers(ref.excerpt, blank_answers, is_code=False)
            video_refs_html += f'''
            <div class="course-ref video-ref">
                <div class="ref-header">📹 {html.escape(ref.source)}</div>
                <div class="ref-content">{highlighted_excerpt}</div>
            </div>'''
        
        # Format exercise references with highlighting
        exercise_refs_html = ""
        for ref in ei.exercise_refs:
            if ref.code_snippet:
                highlighted_code = highlight_answers(ref.code_snippet, blank_answers, is_code=True)
                code_snippet = f'<pre class="ref-code">{highlighted_code}</pre>'
            else:
                code_snippet = ""
            exercise_refs_html += f'''
            <div class="course-ref exercise-ref">
                <div class="ref-header">📝 {html.escape(ref.source)}</div>
                {code_snippet}
            </div>'''
        
        items_html += f'''
        <div class="item">
            <div class="item-header">
                <span class="item-number">Item {item.item_number}</span>
                <h2 class="item-title">{html.escape(item.title)}</h2>
            </div>
            
            <div class="yaml-block"><span class="yaml-key">type:</span> <span class="yaml-value">BlanksChallenge</span>
<span class="yaml-key">unit:</span> <span class="yaml-value">{html.escape(item.unit)}</span>
<span class="yaml-key">subskill:</span> <span class="yaml-value">{html.escape(item.subskill)}</span></div>
            
            <div class="section-label">📋 Context</div>
            <div class="context-box">{html.escape(item.context)}</div>
            
            <div class="section-label">💻 Code</div>
            <div class="code-block">{code_html}</div>
            
            <div class="section-label">✅ Answers ({item.blank_count} blank{"s" if item.blank_count != 1 else ""})</div>
            <div class="variables-grid{" single-blank" if item.blank_count == 1 else ""}">{vars_html}</div>
            
            <div class="section-label">📚 Course References</div>
            <div class="references-container">
                {video_refs_html if video_refs_html else '<div class="no-refs">No video references found</div>'}
                {exercise_refs_html if exercise_refs_html else '<div class="no-refs">No exercise references found</div>'}
            </div>
        </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlanksChallenge Preview - {html.escape(doc_title)}</title>
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
            color: #00d4aa;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #00d4aa;
            padding-bottom: 0.5rem;
        }}
        .pool-info {{
            background: rgba(0, 212, 170, 0.1);
            border-left: 4px solid #00d4aa;
            padding: 1rem;
            margin-bottom: 2rem;
            border-radius: 0 8px 8px 0;
        }}
        .pool-info code {{
            color: #00d4aa;
            background: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 4px;
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
            background: #00d4aa;
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
        }}
        .context-box {{
            background: rgba(126, 184, 218, 0.1);
            border-left: 3px solid #7eb8da;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        .code-block {{
            background: #0d1520;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            border: 1px solid #2d3f52;
            line-height: 1.5;
            white-space: pre;
        }}
        .blank {{
            background: #ff6b9d;
            color: #1a1a2e;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .answer-highlight {{
            background: rgba(255, 107, 157, 0.3);
            color: #ff6b9d;
            padding: 1px 4px;
            border-radius: 3px;
            font-weight: 600;
            border: 1px solid #ff6b9d;
        }}
        .variables-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }}
        .variables-grid.single-blank {{
            justify-content: center;
        }}
        .variables-grid.single-blank .variable-chip {{
            min-width: 200px;
        }}
        .variable-chip {{
            background: rgba(168, 230, 207, 0.15);
            border: 1px solid #a8e6cf;
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
            text-align: center;
            flex: 1;
            min-width: 150px;
            max-width: 300px;
        }}
        .variable-chip .var-name {{
            color: #ff6b9d;
            font-family: monospace;
            font-size: 0.8rem;
        }}
        .variable-chip .var-value {{
            color: #a8e6cf;
            font-family: monospace;
            font-weight: bold;
            font-size: 0.95rem;
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
        .video-ref {{
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
        }}
        .exercise-ref {{
            background: rgba(156, 39, 176, 0.1);
            border: 1px solid rgba(156, 39, 176, 0.3);
        }}
        .ref-header {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #ffc107;
        }}
        .exercise-ref .ref-header {{
            color: #ce93d8;
        }}
        .ref-content {{
            color: #ccc;
            line-height: 1.5;
        }}
        .ref-code {{
            background: #0d1520;
            padding: 0.75rem;
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.8rem;
            overflow-x: auto;
            margin: 0.5rem 0 0 0;
            color: #a8e6cf;
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
        <h1>🧪 BlanksChallenge Preview</h1>
        
        <div class="pool-info">
            <strong>Document:</strong> {html.escape(doc_title)}<br>
            <strong>Subskill:</strong> <code>{html.escape(subskill or enriched_items[0].item.subskill if enriched_items else "")}</code>
            <div class="stats">
                <span>📝 {len(enriched_items)} items</span>
                <span>🔲 {sum(ei.item.blank_count for ei in enriched_items)} total blanks</span>
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
    parser = argparse.ArgumentParser(description="Generate BlanksChallenge preview with course references")
    parser.add_argument("items_file", type=Path, help="Path to items markdown file")
    parser.add_argument("--scripts", type=Path, help="Directory containing video script files")
    parser.add_argument("--exercises", type=Path, help="Directory containing exercise markdown files")
    parser.add_argument("--output", "-o", type=Path, default=Path(".cursor/tmp_items/blanks_preview.html"), help="Output HTML file")
    
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
    exercises = {}
    
    if args.scripts:
        print(f"📹 Parsing video scripts from {args.scripts}...")
        scripts = parse_video_scripts(args.scripts)
        print(f"   Found {len(scripts)} video sections")
    
    if args.exercises:
        print(f"📝 Parsing exercises from {args.exercises}...")
        exercises = parse_exercises(args.exercises)
        total_ex = sum(len(ex) for ex in exercises.values())
        print(f"   Found {total_ex} exercises across {len(exercises)} chapters")
    
    # Enrich items with course references
    print("🔗 Matching items to course content...")
    enriched = enrich_items(items, scripts, exercises)
    
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
