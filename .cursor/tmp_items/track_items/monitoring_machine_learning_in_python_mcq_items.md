---
title: Monitoring Machine Learning in Python Assessment Items (MCQ)
output: html_document
description: Four MultipleChoiceChallenge items aligned to Monitoring Machine Learning in Python (conceptual topics).
---

## What NannyML helps with

```yaml
type: MultipleChoiceChallenge
key:
unit: nannyml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your team deploys a model, but labels are delayed and you cannot compute real-time accuracy. You still need to understand whether performance is likely dropping and what might be causing it.

Which capability is NannyML designed to provide in this setting?

`@options1`
- Building new models with automated hyperparameter tuning
- [Estimating performance and linking issues to data changes]
- Packaging models into Docker images for deployment
- Replacing feature engineering with end-to-end deep learning

---

## Reference versus analysis data

```yaml
type: MultipleChoiceChallenge
key:
unit: nannyml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You prepare data for production monitoring. One dataset represents a period where the model is known to behave well and includes ground truth labels. Another dataset represents more recent production data where labels may be missing.

What is the correct interpretation of reference versus analysis data?

`@options1`
- The analysis set must include `y_true` labels for every observation
- The reference set must always be newer in time than the analysis set
- Both sets must have the same columns, but values differ by period
- [The reference set is a baseline; labels may be missing in analysis]

---

## Choosing CBPE versus DLE

```yaml
type: MultipleChoiceChallenge
key:
unit: nannyml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to estimate performance for a model in production without having ground truth labels yet. The model predicts a continuous number (like a tip amount).

Which estimator type is intended for this task?

`@options1`
- [DLE (for regression tasks)]
- CBPE (for classification tasks)
- PSI (drift detection metric)
- KS test (drift detection test)

---

## Chunking results

```yaml
type: MultipleChoiceChallenge
key:
unit: nannyml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You configure a NannyML estimator with `chunk_period='d'` so results aggregate over time windows.

What does a “chunk” represent in the monitoring output?

`@options1`
- A fixed batch of observations summarized into one result point
- A single raw record from the production data stream
- [A time window of observations aggregated into one result point]
- A single feature category from dummy-variable encoding
