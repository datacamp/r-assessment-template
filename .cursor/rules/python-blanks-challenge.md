# Python BlanksChallenge - Language-Specific Reference

Python-specific guidance for generating BlanksChallenge items. This supplements the generic `coding-exercise.md` with Python-focused rules.

---

## Type Identifier

**Type Name:** `BlanksChallenge` (Python)

**Used For:**
- Python programming assessments
- Data manipulation with pandas, numpy
- API integrations (OpenAI, requests)
- Machine learning workflows
- General Python scripting

---

## PYTHON PLACEHOLDER SYNTAX

Use `{{_expr1}}`, `{{_expr2}}`, etc. for blanks in Python code.

### What to Test with Blanks
- Method calls: `data.{{_expr1}}("column")`
- Parameters: `model={{_expr1}}`
- Operators: `x {{_expr1}} y`
- Function names: `{{_expr1}}(data)`
- Indexing: `data[{{_expr1}}]`
- Method chains: `df.{{_expr1}}("col").{{_expr2}}()`
- List comprehension parts: `[x {{_expr1}} 2 for x in numbers]`

### What NOT to Test
- Import statements (unless that's the learning objective)
- Basic syntax keywords (`if`, `for`, `def`, `class`)
- String literals or field names not visible in code
- Variable names that could have multiple valid options
- `if __name__ == "__main__":`

---

## PYTHON CODE STYLE

### PEP 8 Compliance
- 4-space indentation
- `snake_case` for variables and functions
- `PascalCase` for classes
- Line length under 79 characters (soft limit)
- Two blank lines before top-level definitions

### Pythonic Patterns
- List comprehensions over explicit loops when clearer
- F-strings over `.format()` or `%` formatting
- Context managers (`with` statements) for file operations
- Unpacking: `a, b = get_values()`
- Ternary expressions when simple: `x = a if condition else b`

### Method Chaining (pandas)

```python
# Good - clear chain
result = (df
    .groupby("category")
    .agg({"value": "mean"})
    .reset_index())

# Also good - single line for short chains
result = df.groupby("category").mean()
```

---

## CODE BLOCK TAGS

All Python BlanksChallenge items use:

| Section | Tag |
|---------|-----|
| `@code1` | `{python}` |
| `@pre_challenge_code` | `{python}` |

---

## COMPLETE EXAMPLES

### Example 1: pandas groupby

**Context:**
You're analyzing customer orders for an e-commerce platform. Calculate the average order value by customer segment.

**@code1:**
```python
segment_avg = orders.{{_expr1}}("segment")["order_value"].{{_expr2}}()
print(segment_avg.sort_index())
```

**@pre_challenge_code:**
```python
import pandas as pd
orders = pd.DataFrame({
    "segment": ["retail", "wholesale", "retail", "wholesale"],
    "order_value": [150, 500, 200, 450]
})
```

**@variables:**
```yaml
expr1:
  - 'groupby'
expr2:
  - 'mean'
```

---

### Example 2: List comprehension

**Context:**
You're processing a list of temperatures in Celsius. Convert each temperature to Fahrenheit using the formula: F = C × 9/5 + 32.

**@code1:**
```python
fahrenheit = [c {{_expr1}} 9/5 {{_expr2}} 32 for c in celsius]
print(fahrenheit)
```

**@pre_challenge_code:**
```python
celsius = [0, 10, 20, 30]
```

**@variables:**
```yaml
expr1:
  - '*'
expr2:
  - '+'
```

---

### Example 3: Dictionary operations

**Context:**
You're building a configuration system. Access the nested 'timeout' value from the settings dictionary.

**@code1:**
```python
timeout = settings{{_expr1}}"network"{{_expr2}}{{_expr1}}"timeout"{{_expr2}}
print(timeout)
```

**@pre_challenge_code:**
```python
settings = {
    "network": {"timeout": 30, "retries": 3},
    "display": {"theme": "dark"}
}
```

**@variables:**
```yaml
expr1:
  - '['
expr2:
  - ']'
```

---

### Example 4: OpenAI API

**Context:**
You're building a chatbot. Send a completion request to OpenAI's API using the client.

**@code1:**
```python
response = client.chat.completions.{{_expr1}}(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.{{_expr2}})
```

**@pre_challenge_code:**
```python
from openai import OpenAI
client = OpenAI(api_key="test-key")
prompt = "Hello, world!"
```

**@variables:**
```yaml
expr1:
  - 'create'
expr2:
  - 'content'
```

---

### Example 5: pandas filtering

**Context:**
You're cleaning survey data. Filter the DataFrame to keep only rows where the response is complete.

**@code1:**
```python
complete = survey[survey["status"] {{_expr1}} "complete"]
print(complete)
```

**@pre_challenge_code:**
```python
import pandas as pd
survey = pd.DataFrame({
    "respondent_id": [1, 2, 3, 4],
    "status": ["complete", "partial", "complete", "complete"]
})
```

**@variables:**
```yaml
expr1:
  - '=='
```

---

## SKILL ASSESSMENT ITEM DESIGN

When creating multiple BlanksChallenge items for a skill assessment:

### Avoid Duplicate Blanks
- Each item should test a **unique** concept across the assessment
- Track blanks used: don't test `fit` in 5 different items
- Create a blank distribution table before generating items

### Avoid Arbitrary Values
❌ **Bad**: `test_size={{_expr1}}` where answer is `0.2` (arbitrary, not conceptual)
✅ **Good**: `knn.{{_expr1}}(X_test, y_test)` where answer is `score` (tests method knowledge)

### Avoid Wordspotting
The context should NOT contain words that directly cue the answer:
❌ **Bad**: "Perform cross-validated grid search..." → `GridSearchCV`
✅ **Good**: "Systematically test combinations of hyperparameter values..." → `GridSearchCV`

### Context Must Include Imperative Instruction
Every context must include an imperative instruction telling the candidate what to do. Describe the task requirements (not the answer) so the candidate can determine the correct solution.

**Context structure:**
1. **Scenario** (optional): Brief situational setup
2. **Imperative instruction** (required): What the candidate must accomplish
3. **Distinguishing details** (if needed): Information that uniquely identifies the correct answer

❌ **Bad** (no instruction):
> "You're working with a regression model that predicts prices."

✅ **Good** (clear instruction):
> "You're assessing a regression model that predicts house prices in dollars. Choose an error metric that penalizes larger prediction errors more heavily."

❌ **Bad** (instruction names the answer):
> "Instantiate a k-nearest neighbors classifier."

✅ **Good** (instruction describes the requirement):
> "Choose a classifier that predicts labels based on the majority vote of nearby observations."

### Fresh Examples Required
- Never lift code verbatim from course exercises
- Use different:
  - Dataset names (`employee_df` not `music_df`)
  - Variable names
  - Context scenarios
- Same concept, fresh implementation

### Verify Course Coverage
Before creating a blank, verify:
1. The exact function/method name is taught in the course
2. The specific syntax matches what's taught
3. The concept appears in video scripts AND/OR exercises

---

## ENSURING UNAMBIGUOUS ANSWERS

### Single Valid Answer Rule
Each blank must have exactly ONE correct answer. Check for:

| Potential Issue | Example | Solution |
|-----------------|---------|----------|
| Similar methods | `fit` vs `fit_transform` | Add context showing return value usage |
| Similar classes | `GridSearchCV` vs `RandomizedSearchCV` | Use distinguishing parameters (`param_grid=` vs `param_distributions=`) |
| Multiple valid approaches | `.sum()` vs `.agg("sum")` | Restructure to test unambiguous method |

### Distinguishing Multiple Blanks
When an item has 2+ blanks, candidates must be able to tell them apart:

❌ **Bad** (ambiguous):
```python
knn.{{_expr1}}(X_train, y_train)
accuracy = knn.{{_expr2}}(X_test, y_test)
```
Both `fit` and `score` take similar arguments - candidate may guess wrong positions.

✅ **Good** (distinguishable):
```python
knn.{{_expr1}}(X_train, y_train)  
predictions = knn.{{_expr2}}(X_test)  # Returns predictions array
```
`fit` takes X and y; `predict` takes only X - clear distinction.

### Import Placement for Class Names
When testing class names, move imports to `@pre_challenge_code`:

❌ **Bad** (two identical blanks):
```python
from sklearn.linear_model import {{_expr1}}
reg = {{_expr1}}()
```

✅ **Good** (single blank):
```python
# In @pre_challenge_code:
from sklearn.linear_model import LinearRegression

# In @code1:
reg = {{_expr1}}()
```

---

## PREPROCESSING ITEMS

### Show Data Context
When testing preprocessing operations, display the data so candidates understand WHY the operation is needed:

✅ **Good** (shows categorical column):
```python
print(employee_df.head())
employee_dummies = pd.get_dummies(employee_df, {{_expr1}}=True)
```

❌ **Bad** (no data visibility):
```python
employee_dummies = pd.get_dummies(employee_df, {{_expr1}}=True)
```

### Common Preprocessing Blanks
| Concept | Recommended Blank | Avoid |
|---------|-------------------|-------|
| Dummy variables | `drop_first` parameter | `get_dummies` (too easy) |
| Imputation | `strategy="mean"` | `fit_transform` (generic) |
| Scaling | `StandardScaler` class | `fit` (duplicated elsewhere) |

---

## COMMON PYTHON PATTERNS TO TEST

### pandas Operations

| Pattern | Blank Example |
|---------|---------------|
| Grouping | `df.{{_expr}}("column")` |
| Aggregation | `grouped.{{_expr}}()` |
| Filtering | `df[df["col"] {{_expr}} value]` |
| Sorting | `df.{{_expr}}("column")` |
| Merging | `pd.{{_expr}}(df1, df2, on="key")` |
| Selecting | `df{{_expr}}"column"{{_expr}}` |

### String Operations

| Pattern | Blank Example |
|---------|---------------|
| F-string | `f"Hello, {{_expr}}name{{_expr}}"` |
| Method | `text.{{_expr}}()` |
| Join | `" ".{{_expr}}(words)` |

### Control Flow

| Pattern | Blank Example |
|---------|---------------|
| Comparison | `x {{_expr}} y` |
| Membership | `item {{_expr}} collection` |
| Boolean | `a {{_expr}} b` |

### Functions

| Pattern | Blank Example |
|---------|---------------|
| Built-in | `{{_expr}}(iterable)` |
| Method call | `obj.{{_expr}}()` |
| Chained | `obj.{{_expr1}}().{{_expr2}}()` |

---

## DETERMINISTIC OUTPUT (Python-Specific)

Ensure reproducible output:

```python
# ✅ Good - sorted output
print(sorted(my_dict.items()))

# ❌ Bad - dict order may vary in older Python
print(my_dict)

# ✅ Good - fixed seed
import random
random.seed(42)

# ❌ Bad - random output
print(random.random())

# ✅ Good - sorted set
print(sorted(my_set))

# ❌ Bad - set order undefined
print(my_set)
```

---

## QUALITY CHECKLIST (Python)

Before finalizing a Python BlanksChallenge item:

- ✅ Code blocks tagged as `{python}`
- ✅ Follows PEP 8 style
- ✅ Uses Pythonic patterns
- ✅ No comments in `@code1`
- ✅ Deterministic output (sorted collections, fixed seeds)
- ✅ Each blank has exactly one valid Python token
- ✅ Blanks test structure/syntax, not string memorization
- ✅ Pre-challenge code handles all imports and setup
- ✅ DataFrames limited to ≤10 rows

---

## COMMON PITFALLS (Python)

1. **Testing string values**: `name = {{_expr}}` where answer is `"Alice"` — avoid this
2. **Multiple valid methods**: Both `.sum()` and `.aggregate("sum")` would work
3. **Indentation issues**: Blanks inside indented blocks must preserve structure
4. **Import scaffolding**: Never make imports a blank (unless testing class name - then move import to pre_challenge_code)
5. **Operator ambiguity**: `+` could be addition or concatenation — ensure context is clear
6. **Dict/set output**: Always sort before printing
7. **Course verbatim**: Copying exact code/datasets from course exercises — always use fresh examples
8. **Wordspotting**: Context that directly cues the answer (e.g., "grid search" → `GridSearchCV`)
9. **Duplicate blanks**: Same concept tested multiple times across assessment items
10. **Arbitrary values**: Testing memorization of numbers (e.g., `0.2` for test_size) rather than concepts
11. **Ambiguous positioning**: Multiple blanks with similar arguments that could be swapped
12. **Untaught concepts**: Testing functions/syntax not explicitly covered in the course materials
13. **Missing imperative**: Context lacks a clear instruction telling the candidate what to accomplish
14. **Variable name giveaway**: Variable names that reveal the answer (e.g., `rmse = {{_expr}}(...)` for RMSE)

---

This supplements the generic `coding-exercise.md` with Python-specific guidance.
