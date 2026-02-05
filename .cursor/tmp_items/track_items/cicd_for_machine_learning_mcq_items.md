---
title: CI/CD for Machine Learning Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–4 of CI/CD for Machine Learning.
---

## SDLC workflow stages

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your team's pipeline has three stages: one compiles the code, one runs unit tests, and one copies artifacts to the production server. A bug appears only after users access the application.

Which stage most likely introduced the issue that testing missed?

`@options1`
- Build
- Test
- [Deploy]
- Document

---

## Continuous integration purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team merges code weekly in large batches. Builds often break, and finding the cause takes hours because many changes landed together.

Which practice would most directly reduce the time spent identifying broken commits?

`@options1`
- [Continuous integration]
- Continuous delivery
- Continuous deployment
- Manual release management

---

## Delivery versus deployment

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A financial services company requires audit sign-off before any production release due to regulatory requirements. They still want automated testing and the ability to release at any time once approved.

Why is continuous delivery more appropriate than continuous deployment for this team?

`@options1`
- [It keeps a manual approval step]
- It automates rollbacks on failure
- It reduces deployment frequency
- It logs all configuration changes

---

## ML-specific versioning needs

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An ML model in production suddenly produces worse predictions. The training code has not changed in two weeks, and no one modified the feature pipeline.

Which versioned artifact would most likely help identify the root cause?

`@options1`
- README documentation
- Deployment environment name
- [Training dataset version]
- Notebook execution logs

---

## YAML indentation rules

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A workflow file fails to parse, and you suspect inconsistent indentation. Your teammate suggests using tabs "so it's easier to align."

What is the correct guidance for YAML indentation?

`@options1`
- Tabs are preferred because they are unambiguous
- Tabs and spaces can be mixed as long as they line up visually
- YAML ignores indentation, so it cannot be the cause
- [Use spaces only; tabs are not allowed in YAML]

---

## YAML boolean values

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A workflow uses `enabled: "true"` in its configuration. The code checks `if config['enabled'] == True` but the condition never triggers.

What change fixes the issue?

`@options1`
- Change the check to `== "True"`
- [Remove the quotes around true]
- Add `bool()` around the config value
- Use `1` instead of `true`

---

## YAML data structures

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to configure three database connections, each with host, port, and credentials. You also need an ordered list of startup commands.

Which YAML structure supports both requirements?

`@options1`
- Scalars nested inside scalars
- [Sequences and mappings]
- Arrays and tokens
- Flow-style strings only

---

## GitHub Actions workflow location

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You added `ci.yml` to the `.github/actions/` folder, but GitHub doesn't detect it as a workflow. Your teammate's workflow runs fine from a different location.

What is the most likely cause?

`@options1`
- The file extension should be `.yaml`
- GitHub Actions is disabled for the repository
- [The file is in the wrong directory]
- The file needs executable permissions

---

## Jobs versus steps

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your workflow has two jobs: `lint` and `test`. Both succeed alone, but when run together, `test` sometimes fails because it starts before `lint` finishes checking out code.

What does this indicate about job behavior?

`@options1`
- Steps share state across jobs
- [Jobs run in parallel by default]
- The runner is handling too many tasks
- Indentation merged the two jobs

---

## What triggers a workflow

```yaml
type: MultipleChoiceChallenge
key:
unit: cicd-for-ml
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want a workflow to run only when someone opens or updates a pull request targeting `main`—not on direct pushes.

Which trigger configuration achieves this?

`@options1`
- `on: push`
- `on: workflow_dispatch`
- [`on: pull_request`]
- `on: schedule`
