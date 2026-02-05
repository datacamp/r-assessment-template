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
A teammate reruns last week’s model training code and gets different accuracy than the report you shared, even though they are “using the same script.” You want your team to be able to reproduce the exact reported result months later.

What should you version to make that reproduction reliable?

`@options1`
- [Version the data, code, and hyperparameters used to train the model]
- Version the code and scripts, but not the data or hyperparameters
- Version the dataset and features, but not the code or hyperparameters
- Version the trained model file, but not the inputs used to create it

---

## Committing DVC tracking

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your repository contains a large `dataset.csv` that you want to track with DVC and share with teammates without bloating your Git repo. After running `dvc add dataset.csv`, you want to make the change available through Git.

What should you commit to Git to enable versioning while keeping the repo lightweight?

`@options1`
- Commit `dataset.csv` so Git preserves every data revision in commit history
- [Commit `dataset.csv.dvc` so Git tracks dataset versions via metadata]
- Commit `.dvc/cache` so teammates download the cached file from Git itself
- Commit `.gitignore` so Git knows to exclude `dataset.csv` from the repo

---

## Writing `.dvcignore`

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your project folder contains thousands of files under `dataset/`, and DVC operations have become slow. You want DVC to ignore everything in `dataset/` except `dataset/myData.csv`, which you still want to track.

What change should you make in `.dvcignore` to achieve that behavior?

`@options1`
- Add `dataset/` and add `!dataset/myData.csv` as the exception rule
- Add `!dataset/` and add `dataset/myData.csv` as a normal ignore rule
- [Add `dataset/*` and add `!dataset/myData.csv` as the exception rule]
- Add `dataset/myData.csv` and add `!dataset/*` as the exception rule

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
You’ve just checked out a new branch and want to download the DVC-tracked data so it’s available in your local cache. However, you do not want DVC to place or update the data file in your working directory yet.

What should you run to download the tracked data into the cache without updating the workspace file?

`@options1`
- [Run `dvc fetch` to download tracked data into the local cache]
- Run `dvc pull` to download data and also update the workspace file
- Run `dvc checkout` to update files from tracked metadata only
- Run `dvc get` to download a file from an external DVC repository

---

## Local remote config

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You’re configuring a DVC remote for a training lab and want the remote URL to stay local to your machine (so it does not get committed and shared with others).

When you use the `--local` flag with `dvc remote add` or `dvc remote modify`, where is that configuration written?

`@options1`
- It writes the remote URL to `.dvc/config` so it can be committed to Git
- [It writes the remote URL to `.dvc/config.local` for local-only config]
- It writes the remote URL to `.git/config` as a Git remote entry
- It writes the remote URL into `dvc.yaml` as part of the pipeline stages

---

## Tracking parameter changes

```yaml
type: MultipleChoiceChallenge
key:
unit: dvc-fundamentals
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your `train_and_evaluate` stage should rerun whenever you change hyperparameters under the `train_and_evaluate` section in `params.yaml`, even if no code files changed.

In `dvc.yaml`, what should you include so DVC treats that section as a tracked parameter dependency?

`@options1`
- Add `params: - params.yaml` to track the full parameter file as one unit
- Add `deps: - params.yaml` so parameters are treated like a code dependency
- [Add `params: - train_and_evaluate` to track that parameter section]
- Add `cmd: --params train_and_evaluate` as an argument to the command

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
Your pipeline produces a small text file called `metrics.json`. You want it tracked by Git (not stored as a cached artifact in the DVC remote), so it is easy to diff and review in pull requests.

How should you configure `dvc.yaml` to track this file appropriately?

`@options1`
- Track `metrics.json` under `outs:` so DVC caches it and pushes it remotely
- [Track `metrics.json` under `metrics:` with `cache: false` to keep it in Git]
- Track `metrics.json` under `deps:` so the stage reruns when metrics change
- Track `metrics.json` under `plots:` so DVC generates visualizations from it
