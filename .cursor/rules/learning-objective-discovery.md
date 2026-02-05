# Learning Objective Discovery - Complete Reference

Systematically discover and structure learning objectives from course content before generating assessment items.

---

## Type Identifier

**Skill Name:** `learning_objective_discovery`

**Used For:**
- Identifying main learning objectives from video scripts and slides
- Breaking down main LOs into assessable sub-LOs (one per item)
- Determining appropriate item type for each sub-LO
- Ensuring LO wording matches what the item type can actually test
- Validating alignment between LOs and course content

---

## WHEN TO USE THIS SKILL

Trigger LO discovery:
- Before generating multiple assessment items for a chapter
- When starting work on a new course section
- When explicitly requested ("discover learning objectives", "what are the LOs")
- Before batch item generation

---

## LO DISCOVERY PROCESS

```
Course Content → Main LOs → Sub-LOs → [Per sub-LO: analyze content → determine item type → word appropriately] → Validate
```

### Step 1: Main LO Identification (by Chapter)

Analyze video scripts and slides for each chapter to extract main learning objectives.

**How to identify main LOs:**
- Look for explicit statements: "By the end of this lesson, you will be able to..."
- Identify the core skills being taught in each video/lesson
- Focus on what learners should be able to DO (not just know)

**Main LO format:** Action verb + concept + context

**Examples:**
- "Use `.groupby()` to aggregate data by categories"
- "Apply machine learning models to predict customer churn"
- "Write SQL queries to join multiple tables"

**Guidelines:**
- Extract 3-5 main LOs per chapter
- Each main LO should represent a significant capability
- Main LOs can be broad (they will be broken into sub-LOs)

---

### Step 2: Sub-LO Decomposition (per Item)

Break each main LO into granular, assessable sub-LOs. Each sub-LO becomes ONE assessment item.

**Sub-LO requirements:**
- Specific enough to test in a single item
- References specific course content (video timestamp, slide number)
- Distinct from other sub-LOs (no overlap)
- One sub-LO = one assessment item

**Example decomposition:**

| Main LO | Sub-LOs |
|---------|---------|
| Use `.groupby()` to aggregate data | 1. Apply `.groupby()` with a single column<br>2. Chain `.groupby()` with aggregation methods<br>3. Identify when to use `.groupby()` vs `.pivot_table()` |

---

### Step 3: Item Type Analysis (per Sub-LO)

**For EACH sub-LO**, analyze the specific course content it references to determine the appropriate item type.

| Content Type | Indicators | Recommended Item Type |
|--------------|------------|----------------------|
| **Conceptual** | Definitions, explanations, comparisons, "why" discussions, decision criteria, trade-offs | **MCQ** |
| **Coding/Procedural** | Code examples, syntax demonstrations, step-by-step procedures, "how to" content | **BlanksChallenge** |

**Important:** A single main LO can have sub-LOs of different types.

**Example:**
```
Main LO: "Use `.groupby()` for data aggregation"

Sub-LO 1: "Apply `.groupby()` syntax"
  → References: Code example at Video 1.2, 03:45
  → Content type: Coding (syntax demo)
  → Item type: BlanksChallenge

Sub-LO 2: "Identify when `.groupby()` is more appropriate than `.pivot_table()`"
  → References: Comparison discussion at Video 1.2, 05:30
  → Content type: Conceptual (comparison)
  → Item type: MCQ
```

#### Analysis Signals for MCQ (Conceptual Content)

Look for these patterns in the referenced content:
- "X is defined as..."
- "The difference between X and Y is..."
- "You should use X when..."
- "X is important because..."
- Comparison tables
- Decision trees or flowcharts
- Best practices discussions
- Trade-off explanations
- "Why" questions answered

#### Analysis Signals for BlanksChallenge (Coding Content)

Look for these patterns in the referenced content:
- Code blocks with syntax examples
- "To do X, use the following code..."
- Method/function demonstrations
- Step-by-step coding workflows
- "How to" instructions with code
- Syntax patterns being taught
- Parameter usage examples

---

### Step 4: LO Wording by Item Type (per Sub-LO)

**Critical: The action verb must be testable by the chosen item type.**

| Item Type | Cognitive Level | Recommended Action Verbs | Verbs to AVOID |
|-----------|-----------------|--------------------------|----------------|
| **BlanksChallenge** | Application/Structure | Apply, Use, Complete, Implement, Construct, Write, Execute | Explain, Describe, Compare, Identify (not testable by filling in code) |
| **MCQ** | Understanding/Reasoning | Explain, Identify, Select, Determine, Predict, Distinguish, Compare, Recognize | Apply, Implement, Write, Execute, Complete (requires actual coding) |

#### Why This Matters

- **BlanksChallenge** tests whether learners can write/complete code correctly
- **MCQ** tests whether learners understand concepts and can make decisions
- Using the wrong verb creates an untestable LO

#### Examples of Properly Matched LO Wording

| Sub-LO Content Reference | Item Type | Good LO Wording | Bad LO Wording |
|--------------------------|-----------|-----------------|----------------|
| Code example of `.groupby()` syntax | BlanksChallenge | "Apply `.groupby()` to aggregate DataFrame columns" | "Explain what `.groupby()` does" |
| Discussion of when to use inner vs outer join | MCQ | "Identify when to use an inner join versus an outer join" | "Implement an inner join query" |
| Comparison of `fit()` vs `fit_transform()` | MCQ | "Distinguish between `fit()` and `fit_transform()` methods" | "Use `fit_transform()` on training data" |
| Code walkthrough of method chaining | BlanksChallenge | "Complete a pandas method chain for data transformation" | "Describe the purpose of method chaining" |
| Explanation of why normalization matters | MCQ | "Explain why feature normalization improves model performance" | "Apply normalization to a dataset" |

---

### Step 5: Content Alignment Validation

Before finalizing the LO table, validate alignment:

**For each sub-LO, verify:**
- [ ] Cites specific course content (video timestamp or slide reference)
- [ ] The cited content actually teaches what the sub-LO claims
- [ ] Item type matches the nature of the cited content
- [ ] Action verb is testable by the chosen item type
- [ ] Sub-LO is distinct from other sub-LOs (no duplication)

**Red flags:**
- Sub-LO references content that doesn't exist → Remove or reassign
- Sub-LO tests something not explicitly taught → Flag as out of scope
- Multiple sub-LOs test the same concept → Merge or differentiate

---

## OUTPUT FORMAT

The LO discovery skill produces a structured table:

```markdown
## Chapter X: [Chapter Title]

| Main LO | Sub-LO | Content Type | Item Type | Action Verb | Course Reference |
|---------|--------|--------------|-----------|-------------|------------------|
| [Main objective] | [Specific sub-objective] | [Conceptual/Coding] | [MCQ/BlanksChallenge] | [Verb] | [Video X.Y, MM:SS] |
```

### Complete Example

```markdown
## Chapter 1: Introduction to pandas

| Main LO | Sub-LO | Content Type | Item Type | Action Verb | Course Reference |
|---------|--------|--------------|-----------|-------------|------------------|
| Use `.groupby()` for aggregation | Apply `.groupby()` with a single column | Coding (syntax demo) | BlanksChallenge | Apply | Video 1.2, 03:45 |
| Use `.groupby()` for aggregation | Identify when to use `.groupby()` vs `.pivot_table()` | Conceptual (comparison) | MCQ | Identify | Video 1.2, 05:30 |
| Understand aggregation functions | Distinguish between `sum()`, `mean()`, and `count()` | Conceptual (definitions) | MCQ | Distinguish | Video 1.3, 01:20 |
| Chain pandas methods | Complete a method chain for data transformation | Coding (procedure) | BlanksChallenge | Complete | Video 1.4, 02:15 |
| Chain pandas methods | Predict the output of a method chain | Conceptual (reasoning) | MCQ | Predict | Video 1.4, 04:00 |
```

---

## QUICK REFERENCE: ACTION VERBS

### For BlanksChallenge (Coding Items)
- **Apply** - Use a method/function in context
- **Use** - Employ a specific syntax or pattern
- **Complete** - Fill in missing code to achieve a result
- **Implement** - Write code that accomplishes a task
- **Construct** - Build a data structure or query
- **Write** - Create code from requirements
- **Execute** - Run a sequence of operations

### For MCQ (Conceptual Items)
- **Identify** - Recognize the correct option
- **Select** - Choose the appropriate approach
- **Distinguish** - Tell apart similar concepts
- **Compare** - Evaluate differences between options
- **Explain** - Understand why something works
- **Determine** - Figure out the correct answer
- **Predict** - Anticipate an outcome
- **Recognize** - Spot a pattern or concept

---

## COMMON PITFALLS TO AVOID

1. **Verb mismatch**: Using "Explain" for a BlanksChallenge or "Implement" for an MCQ
2. **Missing citations**: Sub-LOs without specific course content references
3. **Overlapping sub-LOs**: Multiple items testing the same concept
4. **Out-of-scope LOs**: Testing concepts not covered in the referenced content
5. **Wrong item type**: Assigning MCQ to code syntax or BlanksChallenge to conceptual content
6. **Too broad sub-LOs**: Sub-LOs that can't be tested in a single item
7. **Assuming item type from main LO**: Always analyze at the sub-LO level

---

## WORKFLOW INTEGRATION

After discovering LOs, the workflow continues:

1. **LO Discovery** (this skill) → Produces LO table with item types
2. **Read Item Type Rules** → Load rules for the determined item type (MCQ or BlanksChallenge)
3. **Generate Item** → Create item aligned to the sub-LO
4. **Validate** → Check structure
5. **Preview** → Visual review
6. **Iterate** → Refine as needed

---

## EXAMPLE SESSION

**User:** "Discover learning objectives for Chapter 2 based on @slides/chapter_2.md"

**Assistant:**
1. Reads chapter content
2. Extracts main LOs
3. Breaks into sub-LOs
4. For each sub-LO: analyzes referenced content → determines item type → words appropriately
5. Validates alignment
6. Outputs structured LO table

**Output:**
```markdown
## Chapter 2: Data Cleaning with pandas

| Main LO | Sub-LO | Content Type | Item Type | Action Verb | Course Reference |
|---------|--------|--------------|-----------|-------------|------------------|
| Handle missing data | Apply `.fillna()` to replace missing values | Coding (syntax) | BlanksChallenge | Apply | Video 2.1, 02:30 |
| Handle missing data | Identify appropriate strategies for different missing data patterns | Conceptual (decision) | MCQ | Identify | Video 2.1, 05:15 |
| Clean string data | Use `.str` accessor methods for text cleaning | Coding (methods) | BlanksChallenge | Use | Video 2.2, 03:00 |
| Clean string data | Distinguish between `.strip()`, `.lower()`, and `.replace()` | Conceptual (comparison) | MCQ | Distinguish | Video 2.2, 06:45 |
```

**User can then say:** "Generate a BlanksChallenge item for the first sub-LO"

---

This is your complete reference for discovering and structuring learning objectives before assessment item generation.
