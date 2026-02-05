# Multiple Choice Challenge - Item Writing Guide

Generate high-quality multiple-choice items that test genuine understanding through application.

---

## ⚡ QUICK START: 6 Non-Negotiable Rules

Before writing ANY item, internalize these:

| Rule | What It Means |
|------|---------------|
| **1. Stem stands alone** | Question makes sense and is answerable WITHOUT seeing options |
| **2. No answer cueing** | Stem doesn't telegraph the correct answer through keywords or opposites |
| **3. Sufficient context** | Candidate can REASON to the answer from information in the stem |
| **4. Test application** | Ask what to DO with knowledge, not just classify or label |
| **5. Plausible distractors** | Each wrong answer tempts someone with a real misconception |
| **6. Balanced options** | Same length (±8 chars), same structure, same technical register |

---

## 🎯 CORE PRINCIPLES

### 1. Standalone Clarity

**Every question must make complete sense without the options.**

A knowledgeable test-taker should begin formulating an answer before seeing choices.

| ✅ Good Stem | ❌ Bad Stem |
|--------------|-------------|
| "Why is containerization suitable for deploying microservices?" | "Which of the following is true about containerization?" |
| "What change should the company make to increase its MLOps maturity?" | "Which option best describes how to improve this company?" |

### 2. No Answer Cueing

**The stem must NOT telegraph the correct answer.**

| Cueing Problem | Example | Fix |
|----------------|---------|-----|
| **Opposite mapping** | Stem lists anti-patterns → Answer is their opposite | Describe symptoms/outcomes instead |
| **Keyword matching** | Stem uses words that appear only in correct answer | Use keyword in 3+ options or none |
| **Single-factor decision** | Only one factor mentioned → obviously the trigger | Present multiple factors |

### 3. Application Over Recall

**Questions should test what to DO with knowledge, not just classify.**

| ❌ Recall/Classification | ✅ Application |
|--------------------------|----------------|
| "Which maturity level is this?" | "What change would increase the maturity level?" |
| "What type of drift is this?" | "What action would address this drift?" |
| "Which role is responsible?" | "What should this role do next?" |

**When classification is acceptable:** When the scenario requires genuine interpretation, not just label-matching.

### 4. Sufficient Context

**The candidate must be able to reason to the answer from information provided in the stem.**

| ❌ Insufficient | ✅ Sufficient |
|-----------------|---------------|
| "What does `$@` represent?" (pure recall) | "When you run the script with two files, both are processed. What happens with one file?" (can reason from behavior) |
| "Which command navigates directories?" | "You are in `/home/user/projects` and need to reach the `data` subdirectory." |

**Test:** Before finalizing, ask: "Could a learner who understands the concept but hasn't memorized definitions answer this from the information given?"

### 5. Code-Related Items in MCQ Format

**Where possible, test code using Blanks/Coding items, not MCQ.**

When MCQ is required for code-related concepts, follow these guidelines:

#### ✅ DO: Test Understanding of What Commands DO

**Approach A — Predict the outcome:**
> **Stem:** You run the command `mv report.txt summary.txt archive` from your current directory. The `archive` directory already exists.
>
> **Question:** What is the result of this command?
>
> **Options:**
> - Both files are copied to archive and remain in the current directory
> - [Both files are moved to archive and removed from current directory]
> - Only the first file is moved; the second overwrites it in archive
> - The command fails because mv requires files to be moved one at a time

**Approach B — Choose the right tool for a goal:**
> **Stem:** You need to organize project files. You want `data.csv` and `config.txt` placed into a `backup` folder while keeping the originals in your current directory for ongoing work.
>
> **Question:** Which command accomplishes this goal?
>
> **Options:**
> - `mv data.csv config.txt backup`
> - [`cp data.csv config.txt backup`]
> - `mv backup data.csv config.txt`
> - `rm data.csv config.txt backup`

**Approach C — Explain why something fails:**
> **Stem:** A script contains `cat data/sales.csv` and runs correctly from `/home/user`. When run from `/home/user/projects`, it fails with "No such file or directory." The file still exists and has not changed.
>
> **Question:** Why does the script fail when run from the different directory?

*(Tests understanding of underlying concepts, not syntax)*

**Approach D — Identify the error/problem:**
> **Stem:** A colleague runs `rm -r projects` expecting to delete only empty directories, but all files inside are also deleted.
>
> **Question:** What caused this unexpected result?

*(Tests understanding of what flags/options actually do)*

**Approach E — Single-token completion:**
> **Stem:** You want to copy a file while keeping the original in place. Complete the command:
>
> ```
> ___ report.txt backup/report.txt
> ```
>
> **Question:** Which command completes this correctly?
>
> **Options:**
> - `cp`
> - `mv`
> - `rm`
> - `cat`

*(Tests command selection with minimal syntax noise — options are single tokens)*

**Approach F — Compare two approaches:**
> **Stem:** You need to process all `.csv` files in a directory.
>
> **Question:** What is the difference between using `*.csv` and listing each file individually?

*(Tests understanding of wildcards/patterns and when to use them)*

**Approach G — Single blank in code line (in stem):**
> **Stem:** You need to count how many lines in `server.log` contain the word "error". You want to do this without creating intermediate files.
>
> Complete the command: `grep error server.log ___ wc -l`
>
> **Options:**
> - `|`
> - `>`
> - `+`
> - `&`

*(The full command is in the stem; options are ONLY the single token to fill the blank. This avoids spot-the-difference by testing just the key decision point.)*

#### ❌ DON'T: Test Spot-the-Difference Syntax

| Approach | Problem |
|----------|---------|
| **Minor syntax variations** | `./archive` vs `archive` vs `/archive` — tests typo-spotting, not understanding |
| **Flag memorization** | `-n 5` vs `-5` vs `--lines=5` — tests syntax recall, not concept |
| **Path permutations** | Options differ only by `/`, `./`, `~`, `..` — wordspot-prone |
| **Full command variations** | Options are full commands differing by one symbol — use Approach G instead |
| **Hidden differences** | Showing two similar commands without highlighting what differs — make it explicit |

#### When Showing Code Differences: Make Them Explicit

If the stem compares two commands or shows an error, **state the difference explicitly** rather than requiring candidates to spot it:

| ❌ Hidden Difference | ✅ Explicit Difference |
|---------------------|------------------------|
| "You type `head -n 5 \| tail -n 3 data.csv` instead of `head -n 5 data.csv \| tail -n 3`" | "You type `head -n 5 \| tail -n 3 data.csv` — notice that `head` has no filename" |
| "Compare `for f in files` vs `for f in $files`" | "The loop uses `files` without a `$` prefix" |

#### Why This Matters

Syntax precision is better tested in interactive coding environments where:
- The learner types the command themselves
- Error messages provide feedback
- Partial credit can be given

MCQ should test whether the learner **understands what tools do and when to use them**, not whether they can spot a missing character.

---

## ✍️ WRITING THE STEM

### Structure
1. **Context** (1-3 sentences): Real-world scenario
2. **Question** (1 sentence): Clear, direct question

### Requirements
- State the central idea in the stem, not hidden in options
- Use positive phrasing (avoid "not" or "except")
- Keep wording concise (grade-8 readability)
- Test ONE concept aligned to ONE learning objective

### Forbidden Language

| ❌ Avoid | Why | ✅ Use Instead |
|----------|-----|----------------|
| "best" | Implies multiple partial answers | "What change would..." |
| "most appropriate" | Implies degrees of correctness | "Which role should..." |
| "most likely" | Ambiguous | "What does X indicate?" |
| "Which of the following" | Option-dependent | Direct question |

### Stem-Option Grammatical Parallelism

**The stem's framing must work grammatically with ALL options.**

Certain verbs in the stem cue certain types of answers:

| Cue Word | Cues Answer Type | Risk |
|----------|------------------|------|
| "represent" | Symbolic/variable interpretations | Distractors describing effects sound wrong |
| "cause" | Effects/outcomes | Distractors describing states sound wrong |
| "prevent" | Blocking actions | Distractors describing enablers sound wrong |

**Rule:** Read each option as a completion of the stem. If some options sound grammatically awkward:
- Reword the stem to be neutral, OR
- Reword all options to match the stem's framing

### Multi-Factor Decision Scenarios

**For decision-based items, present multiple factors where only ONE indicates the correct action.**

**Structure:**
1. Describe 3-4 relevant factors from the course
2. Make 2-3 factors neutral (don't suggest action)
3. Make exactly ONE factor clearly indicate the correct action
4. Distractors reference the other factors

| ❌ Single-Factor | ✅ Multi-Factor |
|------------------|-----------------|
| "Accuracy dropped below 90%." | "Business is stable, costs are high, but accuracy dropped below threshold." |

---

## 🧠 WRITING THE OPTIONS

### Structure Requirements
- **Exactly 4 options** per item
- **Exactly 1 correct answer**
- **3 plausible distractors**

### Length Rule (CRITICAL)
- All options **within ±8 characters** of each other
- Correct answer **NOT longer** than any distractor

**Exception — Terminology-only options:** When all options are standard technical terms (e.g., "Concept drift", "Covariate shift", "Batch prediction"), length imbalance is acceptable. These are fixed terms that cannot be adjusted, and the imbalance does not create cueing.

### Parallel Structure
All options must share:
- Same grammatical form (all actions, all principles, all roles)
- Same structural complexity (if one has a list, all do)
- Same technical register (all technical OR all conceptual)

**Default:** Simplify the correct answer to match distractor complexity.

### Simple Label Rule

When testing **known, finite categories** (phases, roles, strategies), use labels only:

| ❌ With Description | ✅ Label Only |
|--------------------|---------------|
| "The design phase, where requirements are gathered" | "The design phase" |
| "The data engineer, who builds pipelines" | "The data engineer" |

### Keyword Consistency (Anti-Wordspotting)

If a distinctive keyword appears in the stem/context:

| Distribution | Status |
|--------------|--------|
| ALL 4 options | ✅ Ideal |
| 3 of 4 options | ✅ Acceptable |
| 1-2 options only | ❌ Creates elimination cue |
| NO options | ✅ Acceptable (rephrase all) |

---

## 🎭 DISTRACTOR QUALITY

### Definition

> A **plausible distractor** is an incorrect option that a learner with incomplete understanding would reasonably select because it appears relevant and defensible.

### The Plausibility Test

> "Would a learner who doesn't fully understand the concept reasonably choose this?"

### Types of Plausible Distractors

| Type | Description | Example |
|------|-------------|---------|
| **Common misconception** | What learners often wrongly believe | "Feature stores replace data pipelines" |
| **Partial truth** | Correct elsewhere, wrong here | "Add more training data" |
| **Related concept confusion** | Mixing up similar concepts | Confusing data drift with concept drift |
| **Reasonable but insufficient** | Addresses symptom, not cause | "Add staging testing" when CI/CD is needed |

### Distractor Rules

| Rule | Requirement |
|------|-------------|
| **Technical Register** | Match the complexity of the correct answer |
| **Course-Aligned Vocabulary** | Use terms the learner has seen in the course |
| **Context-Rooted** | Reference information explicitly stated in the stem |
| **Scenario-Relevant** | Address the problem described |

### Red Flags: Implausible Distractors

| ❌ Red Flag | Why It Fails |
|-------------|--------------|
| Obviously absurd | "Delete all code and start over" |
| Unrelated to scenario | Problem is slow deploys / Option is "hire more analysts" |
| Wrong technical register | Key is technical / Distractor is generic |
| Unrooted | References info not in the stem |

### Distractor Evaluation Checklist

For each distractor, verify:

- [ ] A learner could actually believe this (common misconception)
- [ ] It's clearly wrong based on how the command/concept WORKS (not data-dependent)
- [ ] It doesn't require seeing specific data to evaluate
- [ ] It's not a potential double key (could also be correct)
- [ ] It matches the stem's grammatical framing

### Distractor Iteration Process

When distractors aren't working:

1. **Generate 5+ alternatives** with rationales
2. **Present to reviewer:**
   ```
   **1. "[Distractor text]"** (XX chars)
   - *Why plausible:* [Misconception it represents]
   - *Why wrong:* [Why it doesn't address the concept]
   ```
3. **Reviewer selects 3**
4. **Balance lengths** after selection
5. **Check keyword consistency**

---

## 🔄 ANSWER POSITION ROTATION

- Distribute correct answers across positions 1, 2, 3, 4
- Never same position more than 2x in a row
- Over 8+ items, each position appears at least once

---

## 📝 MARKDOWN FORMAT

~~~markdown
---
title: <Course Title>
output: html_document
description: <1–2 line description>
---

## <3–4 Word Item Title>

```yaml
type: MultipleChoiceChallenge
key:
unit: <kebab-case-unit>
subskill: <from pool.yml>
initial_difficulty: 0
item_writer_id: '999999999'
# DEVELOPMENT FIELDS (remove before finalizing):
# course_section: "Video 1.1"
# course_content_reference: |
#   **From Video 1.1:**
#   "Verbatim passage from video script that teaches this concept..."
#
#   **From chapter1.md:**
#   "Verbatim passage from chapter file if relevant..."
```

`@assignment1`
<Context: 1-3 sentences>

<Question: Single clear question>

`@options1`
- <Distractor A>
- [<Correct answer>]
- <Distractor B>
- <Distractor C>
~~~

### Development Fields (Temporary)

During item creation, you MUST include these fields to ensure accurate course alignment in previews:

| Field | Purpose | Example |
|-------|---------|---------|
| `course_section` | Source location (Video number or Chapter) | `"Video 1.1"` or `"Chapter 2 - Data Quality"` |
| `course_content_reference` | Verbatim passage(s) from course that teach the concept (1-2 paragraphs) | See example below |

**These fields help verify course alignment but MUST be removed before finalizing items.**

#### Course Content Reference Format

When creating items, extract the EXACT verbatim passage(s) from course materials that teach the concept being tested. Include content from **both** `.txt` (video scripts) and `.md` (chapter files) when relevant:

```yaml
# course_section: "Video 1.1"
# course_content_reference: |
#   **From Video 1.1 (video script):**
#   "Of course, most organizations start playing with ML without the Ops,
#   manually executing all workflows and monitoring models only ad hoc.
#   Many, unfortunately, don't evolve much further than that, paying dearly
#   down the line. This causes the accumulation of so-called technical debt
#   which Wikipedia defines as: the implied cost of additional rework caused
#   by choosing an easy (limited) solution now instead of using a better
#   approach that would take longer."
#
#   "Implementing MLOps tools and practices will, on the other hand, make
#   your processes automated, fast, reproducible, and explainable – producing
#   the highest quality of service and earning the trust of your customers."
#
#   **From chapter1.md:**
#   "Technical debt accumulates when teams skip proper MLOps practices,
#   leading to models that are difficult to update, monitor, or reproduce."
```

**Requirements:**
- Include 1-2 paragraphs that directly teach the concept
- Label each passage with its source (video script vs chapter file)
- Use verbatim quotes — do not paraphrase
- Include content from multiple sources when both cover the concept

#### Stripping Development Fields

To remove development fields before finalizing, use this Python snippet:
```bash
python3 -c "
import re
with open('/tmp/mc_items.md', 'r') as f:
    content = f.read()
# Remove course_content_reference block (commented multi-line YAML)
content = re.sub(r'# course_content_reference:.*?(?=\n[^#\n]|\n\\\`\\\`\\\`|\Z)', '', content, flags=re.DOTALL)
# Remove other development fields
content = re.sub(r'# course_section:.*\n', '', content)
content = re.sub(r'# teaching_point:.*\n', '', content)
content = re.sub(r'# DEVELOPMENT FIELDS.*\n', '', content)
with open('/tmp/mc_items.md', 'w') as f:
    f.write(content)
"
```

---

## ✅ PRE-GENERATION CHECKLIST

Before writing each item:

- [ ] I know the ONE concept being tested
- [ ] I have the course extract that teaches this concept
- [ ] I can write a scenario requiring APPLICATION (not recall)
- [ ] The candidate can REASON to the answer from information I'll provide
- [ ] The question type matches what I'll put in options

---

## ✅ POST-GENERATION CHECKLIST

### Stem Quality
- [ ] Question stands alone without options
- [ ] No comparative language ("best," "most")
- [ ] Does not cue the answer (no opposite mapping, no keyword matching)
- [ ] Provides sufficient context to reason to the answer
- [ ] Tests application, not just classification
- [ ] Decision scenarios have multiple factors (only one decisive)
- [ ] Code differences are explicit (not hidden for candidate to spot)

### Option Quality
- [ ] All 4 options within ±8 characters
- [ ] Correct answer NOT longer than distractors
- [ ] All distractors are plausible misconceptions
- [ ] Options are parallel (same type, structure, register)
- [ ] Keywords appear in 3+ options or none
- [ ] Each distractor references something in the stem
- [ ] Classification uses simple labels only

### Format
- [ ] Correct YAML with all required fields
- [ ] Correct answer in brackets `[...]`
- [ ] Position rotation maintained

---

## ❗ COMMON ERRORS

### Stem Errors

| Error | Example | Fix |
|-------|---------|-----|
| Vague stem | "Which is true about X?" | Ask specific question |
| Comparative language | "What is the best approach?" | "What approach addresses this?" |
| Opposite mapping | Lists anti-patterns → answer is opposite | Describe symptoms instead |
| Single-factor decision | Only triggering factor mentioned | Present multiple factors |
| Recall-only question | "Which level is this?" | "What change would increase the level?" |
| Insufficient context | "What does `$@` do?" | Add scenario showing behavior to reason from |
| Hidden code differences | Two commands differ subtly | State the difference explicitly in the stem |

### Option Errors

| Error | Example | Fix |
|-------|---------|-----|
| Semantic mismatch | Q: "What problem?" / Options: solutions | Align question to options |
| Implausible distractor | "Delete all code" | Use common misconceptions |
| Unrooted distractor | References info not in stem | Add context OR change distractor |
| Length giveaway | Correct: 90 chars / Distractors: 40 | Balance within ±8 chars |
| Wordspotting | Keyword in only 1-2 options | Use in 3+ or none |
| Register mismatch | Key: technical / Distractor: generic | Match complexity |
| Non-course vocabulary | Unfamiliar jargon | Use course terms |

---

## 🔧 VALIDATION & PREVIEW

### Validate Structure
```bash
python3 .cursor/validators/mc_validator.py /tmp/mc_items.md
```

### Generate Preview
```bash
python3 .cursor/preview/generate_mc_preview.py /tmp/mc_items.md --scripts <scripts_dir>
```

**Note:** The `--scripts` argument is required for course reference matching. Point it to the directory containing video script files (e.g., `chapter_1_scripts.txt`). Course content may include code snippets in both `.txt` and `.md` files.

---

## 📚 COURSE ALIGNMENT

### Required: Extract Course Content Reference

When creating items, you MUST search both `.txt` (video scripts) and `.md` (chapter files) to find and extract the relevant teaching passages.

**Step 1: Identify the concept being tested**
- What specific knowledge or skill does this item assess?

**Step 2: Search course materials for teaching content**
- Search `.txt` files (video scripts) for passages that teach this concept
- Search `.md` files (chapter content) for related explanations
- Look for definitions, explanations, examples, and key principles

**Step 3: Extract verbatim passages**
- Copy the EXACT text (1-2 paragraphs) that teaches the concept
- Include source attribution (e.g., "Video 1.1" or "chapter2.md")
- If both file types contain relevant content, include passages from each

**Step 4: Add to `course_content_reference` field**
- Place in the YAML block as a commented multi-line field
- Label each passage with its source

### Alignment Principles

**Good alignment:** Tests whether learner can APPLY what was taught
**Bad alignment:** Tests whether learner REMEMBERS exact wording

1. **Create a NEW scenario** that applies (not restates) the concept
2. **Verify the item tests what the passage TEACHES** (not adjacent content)
3. **If the item tests something from a different section:**
   - Reassign to the correct subskill, OR
   - Revise to test the intended content

| ❌ Misalignment | ✅ Alignment |
|-----------------|-------------|
| Course section teaches wildcards; item tests loop syntax | Course section teaches loop syntax; item tests loop syntax |
| Course section is Chapter 4; concept is from Chapter 5 | Concept matches the chapter specified in pool.yml |

---

## EXAMPLE: Well-Constructed Item

~~~markdown
## MLOps Core Purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-fundamentals
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A data science team has developed a promising customer churn model. However, models often break when moved to production, updates take weeks to deploy, and no one monitors whether predictions remain accurate over time.

What is the primary purpose of MLOps in addressing these challenges?

`@options1`
- To optimize training pipelines so that new models are developed more quickly
- [To enable reliable, continuous deployment and monitoring of ML systems]
- To create documentation and checklists that speed up deployment approvals
- To establish accuracy thresholds that models must pass before any release
~~~

**Why this works:**
- ✅ Stem describes symptoms (not anti-patterns)
- ✅ Question type matches options (purpose → purposes)
- ✅ All distractors are plausible improvements
- ✅ Balanced lengths and structure
- ✅ Tests application to new scenario
