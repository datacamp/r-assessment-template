# R BlanksChallenge Exercises - Complete Reference

R-specific guidance for generating BlanksChallenge coding items. This supplements the generic `coding-exercise.md` with R-focused rules.

---

## Type Identifier

**Type Name:** `BlanksChallenge`

**Used For:**
- Fill-in-the-blank R coding challenges
- Data manipulation with tidyverse (dplyr, tidyr)
- Data visualization with ggplot2
- Statistical analysis
- General R scripting

---

## R SCAFFOLDING RULES

**Use `{{_exprN}}` placeholders for R BlanksChallenge items.**

### What to Scaffold
- Function calls: `result <- {{_expr1}}(data)`
- Parameters: `filter(data, {{_expr1}})`
- Variable assignments: `filtered_data <- {{_expr1}}`
- Pipe chains: `data %>% {{_expr1}}()`
- ggplot layers: `ggplot(data, aes({{_expr1}})) + {{_expr2}}()`
- Column references: `select(data, {{_expr1}})`

### What NOT to Scaffold
- Library calls (unless that's the learning objective)
- Basic syntax (`if`, `for`, `function` keywords)
- Comments
- Print statements (unless that's the objective)

---

## R CODE STYLE

### Assignment Operator
- **Always use `<-` for assignment** (tidyverse convention)
- Good: `result <- mean(x)`
- Bad: `result = mean(x)`

### Pipe Operators (Default)
- **Use pipe operators (`%>%` or `|>`) unless otherwise specified**
- Break long chains across multiple lines
- Indent continuation lines

```r
# Good - piped chain
result <- data %>%
  filter(year > 2020) %>%
  group_by(region) %>%
  summarize(mean_value = mean(value))

# Also good - single line for short chains
result <- data %>% filter(year > 2020)
```

### tidyverse Style Guide
- snake_case for variables and functions
- Spaces around operators: `x <- 5`, not `x<-5`
- Spaces after commas: `c(1, 2, 3)`, not `c(1,2,3)`
- Line length under 80 characters

### Data Frame Terminology
- Use "data frame" (lowercase, two words) when referring to R data frames
- Good: "The data frame `sales` contains..."
- Bad: "The DataFrame `sales` contains..."

---

## BLANKSCHALLENGE EXPORT FORMAT

~~~markdown
---
title: {{pool.title}}
output: html_document
description: {{pool.description}}
---

## [Learning Objective Title]

```yaml
type: BlanksChallenge
key:
unit: <2-3 word kebab-case phrase>
subskill: {{pool.subskill}}
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
{Role-based scenario: "You're a [role] on a team [doing X]. [Imperative action]."}

`@code1`
```{r}
result <- data %>%
  {{_expr1}}(column > value) %>%
  {{_expr2}}(category)
```

`@pre_challenge_code`
```{r}
library(dplyr)
data <- data.frame(
  category = c("A", "B", "A", "B"),
  value = c(10, 20, 15, 25)
)
```

`@variables`
```yaml
expr1:
  - 'filter'
expr2:
  - 'group_by'
```

`@distractors`
```yaml
```
~~~

---

## CONTEXT GUIDELINES

**Length:** 1-4 lines describing a real-world data task

**Cognitive Level:** Access higher cognitive functions by placing candidates in rich, immersive scenarios—not just describing a task.

**No Explicit Instructions:** Users always see "fill in the blank" automatically, so:
- ❌ Don't write "you need to find" or "your task is to"
- ✅ Use imperative verbs: "Filter", "Summarize", "Calculate", "Create"

**Role-Based Framing:** Put the user IN the scenario as a team member.

| ❌ Bad | ✅ Good |
|--------|---------|
| "You're analyzing data. You need to filter the data frame." | "You're a data analyst on a marketing team reviewing campaign results. Filter the data frame to include only successful campaigns." |

**Pattern:**
```
❌ "You're analyzing [thing]. You need to [action]."
✅ "You're a [role] on a team [doing X]. [Imperative action]."
```

---

## SECTION REQUIREMENTS

| Section | Required | Description |
|---------|----------|-------------|
| `@context` | Yes | 1-4 lines; role-based scenario with imperative action |
| `@code1` | Yes | Minimal, runnable R with `{{_exprN}}` placeholders |
| `@pre_challenge_code` | No | Setup code; data frames ≤10 rows |
| `@variables` | Yes | Maps each `exprN` to solution (single-element list) |
| `@distractors` | No | Optional incorrect choices |

---

## COMPLETE EXAMPLE

### Example: Filtering and Grouping with dplyr

**Given pool.yml:**
```yaml
title: "Data Wrangling with tidyverse"
subskill: dplyr-operations
```

**Generated item:**

~~~markdown
---
title: Data Wrangling with tidyverse
output: html_document
---

## [Filtering and Summarizing Sales Data]

```yaml
type: BlanksChallenge
key:
unit: dplyr-wrangling
subskill: dplyr-operations
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're a data analyst on a retail analytics team investigating regional performance. Filter the sales data for high-value transactions and calculate the average revenue by region.

`@code1`
```{r}
high_value <- sales %>%
  {{_expr1}}(revenue > 1000)

regional_avg <- high_value %>%
  group_by(region) %>%
  {{_expr2}}(avg_revenue = mean(revenue))
```

`@pre_challenge_code`
```{r}
library(dplyr)
sales <- data.frame(
  region = c("North", "South", "North", "East", "South"),
  revenue = c(1200, 800, 1500, 2000, 900)
)
```

`@variables`
```yaml
expr1:
  - 'filter'
expr2:
  - 'summarize'
```

`@distractors`
```yaml
```
~~~

---

## COMMON TIDYVERSE PATTERNS

### dplyr Verbs
```r
# Filtering rows
data %>% filter(column > value)

# Selecting columns
data %>% select(col1, col2, col3)

# Creating new columns
data %>% mutate(new_col = col1 + col2)

# Grouping and summarizing
data %>%
  group_by(category) %>%
  summarize(
    mean_val = mean(value),
    count = n()
  )

# Arranging rows
data %>% arrange(desc(column))
```

### ggplot2 Layers
```r
# Basic plot structure
ggplot(data, aes(x = x_col, y = y_col)) +
  geom_point() +
  labs(title = "Title", x = "X Label", y = "Y Label") +
  theme_minimal()

# Common geoms
geom_point()     # Scatter plot
geom_line()      # Line plot
geom_bar()       # Bar chart
geom_histogram() # Histogram
geom_boxplot()   # Box plot
```

---

## BEST PRACTICES

### 1. Default to Pipes
- Always use `%>%` or `|>` for chaining operations
- Makes code more readable and matches modern R style

### 2. Strategic Scaffolding
- Focus on learning objectives, not busywork
- Don't scaffold every single line
- Each `{{_expr}}` should require understanding, not just typing

### 3. Context Sets the Stage
- Always mention what packages are loaded in pre_challenge_code
- Use "data frame" (not DataFrame) for R
- Use realistic scenarios with role-based framing

### 4. No Comments in @code1
- Comments should NOT appear in the `@code1` section
- Keep code minimal and focused on the tested concept

---

## COMMON PITFALLS TO AVOID

1. **Wrong placeholder format**: Using `___` instead of `{{_exprN}}`
2. **Wrong assignment**: Using `=` instead of `<-`
3. **Wrong terminology**: "DataFrame" instead of "data frame"
4. **Missing pipes**: Not using `%>%` when appropriate
5. **Comments in @code1**: Code section should have no comments
6. **Over-scaffolding**: Every line has `{{_expr}}`
7. **Under-scaffolding**: Key concepts not tested
8. **String blanks**: Making the answer a text string value
9. **Non-deterministic output**: Using randomness without seeds

---

## QUALITY CHECKLIST

Before finalizing an R BlanksChallenge item, verify:

- ✅ Placeholders use `{{_exprN}}` format
- ✅ Assignment uses `<-` operator
- ✅ Pipes (`%>%`) used for chaining
- ✅ Each `{{_expr}}` has matching entry in `@variables`
- ✅ No comments in `@code1`
- ✅ Context uses role-based framing with imperative action
- ✅ Pre-challenge code handles all setup (library calls, data loading)
- ✅ Code follows tidyverse style guide
- ✅ Uses "data frame" terminology (not DataFrame)
- ✅ `type: BlanksChallenge` in YAML
- ✅ `item_writer_id: '999999999'`
- ✅ All code blocks tagged as `{r}`

---

## AUTOMATIC VALIDATION

After generating the exercise, validate it:

```bash
python .cursor/validators/r_coding_validator.py /tmp/exercise_to_validate.md
```

---

## PREVIEW

Generate a visual preview with course content matching:

```bash
python .cursor/preview/generate_blanks_preview.py /tmp/items.md \
    --scripts <scripts_dir> \
    --exercises <exercises_dir>
```
