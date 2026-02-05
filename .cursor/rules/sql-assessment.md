# SQL BlanksChallenge Exercises - Complete Reference

SQL-specific guidance for generating BlanksChallenge coding items. This supplements the generic `coding-exercise.md` with SQL-focused rules.

---

## Type Identifier

**Type Name:** `BlanksChallenge`

**Used For:**
- Fill-in-the-blank SQL query challenges
- Database querying and manipulation
- Data analysis with SQL
- Joins, aggregations, subqueries

---

## SQL SCAFFOLDING RULES

**Use `{{_exprN}}` placeholders for SQL BlanksChallenge items.**

### What to Scaffold
- Entire clauses: `SELECT {{_expr1}}`
- Column selections: `SELECT {{_expr1}}, {{_expr2}} FROM table`
- Table names: `FROM {{_expr1}}`
- Conditions: `WHERE {{_expr1}}`
- Aggregations: `{{_expr1}}(column)`
- Join conditions: `ON {{_expr1}}`
- Keywords: `{{_expr1}} JOIN table ON ...`

### What NOT to Scaffold
- Semicolons
- Comments
- Basic punctuation (commas, parentheses)

---

## SQL CODE STYLE (Holywell + DataCamp)

### Capitalization (CRITICAL)
- **ALL SQL keywords UPPERCASE:** `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `HAVING`, `JOIN`, `ON`, `AS`, `AND`, `OR`, `NOT`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, `DISTINCT`, `UNION`, `LIMIT`
- **ALL functions UPPERCASE:** `SUM()`, `COUNT()`, `AVG()`, `MAX()`, `MIN()`, `ROUND()`, `COALESCE()`, `CASE`
- **Table and column names lowercase:** `cities`, `country_name`, `population`

### Commas (DataCamp Standard)
- **Commas at END of columns** (not beginning)
- Include space after comma when on same line

```sql
-- Good (DataCamp standard)
SELECT
    name,
    population,
    country
FROM cities;
```

### Indentation
- **4 spaces** for indentation (not tabs)
- Indent columns under `SELECT`
- Indent conditions under `WHERE`
- Indent subqueries

### Aliasing
- **Always use `AS` keyword**
- Good: `SELECT name AS city_name`
- Bad: `SELECT name city_name`

### Comments
- **Use `--` for SQL comments** (not `#`)
- Comments should NOT appear in `@code1`

---

## CODE BLOCK SYNTAX (IMPORTANT)

SQL exercises use **mixed language blocks**:

| Section | Language Tag | Purpose |
|---------|--------------|---------|
| `@code1` | `` ```{sql} `` | Student code with blanks |
| `@pre_challenge_code` | `` ```{python} `` | Database setup |

**Note:** Uses curly braces `{sql}` and `{python}`, not plain `sql` or `python`.

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
```{sql}
SELECT
    {{_expr1}},
    COUNT(*) AS total
FROM orders
{{_expr2}} category
ORDER BY total DESC;
```

`@pre_challenge_code`
```{python}
# Database connection pre-configured
# Tables available: orders (id, category, amount, date)
```

`@variables`
```yaml
expr1:
  - 'category'
expr2:
  - 'GROUP BY'
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
- ✅ Use imperative verbs: "Query", "Join", "Aggregate", "Filter"

**Role-Based Framing:** Put the user IN the scenario as a team member.

| ❌ Bad | ✅ Good |
|--------|---------|
| "You're querying a database. You need to join two tables." | "You're a database analyst on a finance team preparing quarterly reports. Join the transactions and accounts tables to calculate total balances." |

**Pattern:**
```
❌ "You're querying [thing]. You need to [action]."
✅ "You're a [role] on a team [doing X]. [Imperative action]."
```

---

## SECTION REQUIREMENTS

| Section | Required | Description |
|---------|----------|-------------|
| `@context` | Yes | 1-4 lines; role-based scenario with imperative action |
| `@code1` | Yes | SQL query with `{{_exprN}}` placeholders; use `{sql}` tag |
| `@pre_challenge_code` | No | Setup code; use `{python}` tag |
| `@variables` | Yes | Maps each `exprN` to solution (single-element list) |
| `@distractors` | No | Optional incorrect choices |

---

## COMPLETE EXAMPLE

### Example: Aggregating with GROUP BY

**Given pool.yml:**
```yaml
title: "SQL Fundamentals"
subskill: sql-aggregations
```

**Generated item:**

~~~markdown
---
title: SQL Fundamentals
output: html_document
---

## [Counting Orders by Category]

```yaml
type: BlanksChallenge
key:
unit: sql-aggregations
subskill: sql-aggregations
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're a data analyst on an e-commerce team reviewing product performance. Count the number of orders in each category and sort by the most popular categories first.

`@code1`
```{sql}
SELECT
    category,
    {{_expr1}} AS order_count
FROM orders
GROUP BY {{_expr2}}
ORDER BY order_count DESC;
```

`@pre_challenge_code`
```{python}
# Database connection pre-configured
# Table: orders (id, category, amount, order_date)
```

`@variables`
```yaml
expr1:
  - 'COUNT(*)'
expr2:
  - 'category'
```

`@distractors`
```yaml
```
~~~

---

## COMMON SQL PATTERNS

### Basic SELECT
```sql
SELECT
    name,
    population,
    country
FROM cities;
```

### Filtering with WHERE
```sql
SELECT
    name,
    population
FROM cities
WHERE population > 1000000
    AND country = 'USA';
```

### Aggregations
```sql
SELECT
    country,
    COUNT(*) AS city_count,
    AVG(population) AS avg_population
FROM cities
GROUP BY country
HAVING COUNT(*) > 5
ORDER BY avg_population DESC;
```

### JOINs
```sql
SELECT
    c.name AS city_name,
    co.name AS country_name
FROM cities AS c
INNER JOIN countries AS co
    ON c.country_id = co.id
WHERE co.continent = 'Europe';
```

---

## BEST PRACTICES

### 1. Uppercase Keywords
- Always capitalize SQL keywords and functions
- This is DataCamp standard and improves readability

### 2. Strategic Scaffolding
- Focus on the learning objective
- Don't scaffold keywords that are obvious from context
- Each `{{_expr}}` should test understanding

### 3. Readable Formatting
- One column per line for 3+ columns
- Indent subqueries and CASE statements
- Keep lines under 60 characters

### 4. Always Use AS
- Every alias must include `AS`
- Tables: `FROM cities AS c`
- Columns: `COUNT(*) AS city_count`

### 5. No Comments in @code1
- Comments should NOT appear in the `@code1` section
- Keep SQL minimal and focused on the tested concept

---

## COMMON PITFALLS TO AVOID

1. **Wrong placeholder format**: Using `___` instead of `{{_exprN}}`
2. **Lowercase keywords**: `select` instead of `SELECT`
3. **Missing AS**: `SELECT name city_name` instead of `SELECT name AS city_name`
4. **Wrong code block tags**: `sql` instead of `{sql}`
5. **Wrong comment style**: `#` instead of `--`
6. **GROUP BY numbers**: `GROUP BY 1` instead of `GROUP BY country`
7. **Comments in @code1**: Code section should have no comments
8. **String blanks**: Making the answer a text string value
9. **Missing semicolon**: SQL queries should end with `;`

---

## QUALITY CHECKLIST

Before finalizing a SQL BlanksChallenge item, verify:

- ✅ Placeholders use `{{_exprN}}` format
- ✅ All SQL keywords are UPPERCASE
- ✅ All functions are UPPERCASE
- ✅ Table/column names are lowercase
- ✅ Aliases always use `AS`
- ✅ Each `{{_expr}}` has matching entry in `@variables`
- ✅ No comments in `@code1`
- ✅ Context uses role-based framing with imperative action
- ✅ `@code1` uses `` ```{sql} `` tag
- ✅ `@pre_challenge_code` uses `` ```{python} `` tag
- ✅ `type: BlanksChallenge` in YAML
- ✅ `item_writer_id: '999999999'`
- ✅ Query ends with semicolon

---

## AUTOMATIC VALIDATION

After generating the exercise, validate it:

```bash
python .cursor/validators/sql_coding_validator.py /tmp/exercise_to_validate.md
```

---

## PREVIEW

Generate a visual preview with course content matching:

```bash
python .cursor/preview/generate_blanks_preview.py /tmp/items.md \
    --scripts <scripts_dir> \
    --exercises <exercises_dir>
```
