---
title: DVC Fundamentals Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–3 of the DVC course.
---

## Reproducing results

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A teammate reruns last week's model training and gets different accuracy than the report you shared. You confirm the script is identical and the dataset file has the same name, but you cannot explain the discrepancy.

Which factor, besides code and data, must also be versioned to ensure reproducible results?

`@options1`
- The operating system and hardware configuration used during training
- [The hyperparameters that control model behavior during training]
- The random seed printed in the training log
- The file path where the trained model artifact was saved

---

## Understanding .dvc files

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
After running `dvc add weather.csv`, DVC creates a file called `weather.csv.dvc`. You open this file and see a small YAML structure with fields like `md5`, `size`, and `path`.

What is the purpose of the `md5` field in this `.dvc` file?

`@options1`
- It stores the file contents in a compressed text format
- It records the timestamp when the file was last modified
- [It stores a checksum that uniquely identifies the file version]
- It contains the remote URL where the file should be uploaded

---

## Using .dvcignore

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your project folder contains thousands of temporary files generated during preprocessing. DVC operations have become noticeably slow because DVC traverses every file in the directory tree.

What is the purpose of the `.dvcignore` file in addressing this problem?

`@options1`
- It prevents specified files from being uploaded to DVC remote
- It removes specified files from the Git staging area on commit
- [It tells DVC to skip specified files when traversing the project]
- It compresses specified files automatically to reduce disk usage

---

## Using DVC remotes

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team stores their code on GitHub, but their model artifacts and datasets are too large to store comfortably in the Git repository. They want a central place where teammates can upload and download those large DVC-tracked artifacts.

What is the primary role of a DVC remote in this setup?

`@options1`
- Replace Git for code versioning so all files live in one place
- Store the `.dvc` metadata files so Git does not need to track them
- Run pipeline stages on cloud infrastructure instead of locally
- [Sync cached data and models externally without Git storage limits]

---

## Downloading to cache

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have just cloned a repository and want to download the DVC-tracked data into your cache. You do not want the files placed in your working directory yet because you plan to check out a different branch first.

Which command downloads data to the cache without updating the workspace?

`@options1`
- `dvc pull`
- `dvc checkout`
- [`dvc fetch`]
- `dvc get`

---

## Downloading from external repos

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A colleague shares a public GitHub repository that contains a large dataset tracked by DVC. You only need the dataset file for your own project — you do not want to clone the entire repository or set up DVC tracking locally.

Which command downloads a DVC-tracked file from an external repository?

`@options1`
- `dvc pull`
- `dvc fetch`
- `dvc checkout`
- [`dvc get`]

---

## Parameter dependencies

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your pipeline has a training stage that reads hyperparameters from `params.yaml`. You want DVC to automatically rerun this stage whenever any hyperparameter value changes, even if the code files are unchanged.

How does DVC track parameter changes differently from code file changes?

`@options1`
- DVC monitors file modification timestamps for both types of changes
- DVC requires you to manually run `dvc commit` after any param edit
- [DVC hashes specific parameter keys, not just the whole file content]
- DVC ignores parameter files entirely and only tracks code changes

---

## Overwriting a stage

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You already have a `preprocess` stage in `dvc.yaml`. You rerun `dvc stage add -n preprocess ...` to update the dependencies and outputs, but DVC errors because the stage already exists.

What should you do to overwrite the existing stage definition?

`@options1`
- Delete the existing stage from `dvc.yaml` manually before rerunning
- Edit `dvc.yaml` directly instead of using the `dvc stage add` command
- Run `dvc remove preprocess` first to clear the stage from the file
- [Add `--force` so DVC overwrites the existing stage in `dvc.yaml` file]

---

## Skipping unchanged stages

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You run `dvc repro` twice in a row. The second time, the terminal output shows that multiple stages are skipped and their cached results are reused.

Why is DVC skipping those stage executions?

`@options1`
- [The stage dependencies did not change, so cached outputs are reused]
- The remote is unreachable, so DVC cannot download the missing outputs
- The `dvc.lock` file is missing, so DVC has no record of prior runs
- You accidentally ran `dvc repro --dry`, which skips actual execution

---

## Tracking metrics in Git

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your pipeline produces a small JSON file containing accuracy and loss values. You want this file versioned in Git so you can easily diff it in pull requests, rather than storing it in the DVC cache.

Why would you set `cache: false` for this metrics file in `dvc.yaml`?

`@options1`
- It prevents DVC from running the stage that produces the file
- It allows multiple stages to write to the same output file
- It tells DVC to compress the file before storing it remotely
- [It keeps the file in Git instead of moving it to the DVC cache]
