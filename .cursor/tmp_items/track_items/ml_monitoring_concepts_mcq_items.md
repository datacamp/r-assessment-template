---
title: Machine Learning Monitoring Concepts Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–3 of the ML Monitoring course.
---

## Why monitoring matters

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A model is still returning predictions in production, but the business has started seeing costly mistakes. There are no obvious system errors or crashes.

Which failure type does monitoring help detect in this situation?

`@options1`
- The input data distribution stayed the same
- The model was retrained too frequently
- [The model's performance silently degrades over time]
- The feature engineering pipeline was updated

---

## Ground truth timing

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You deploy a loan default model. Whether each borrower actually defaults only becomes known after several months of payments and collection processes.

Which category describes the ground truth availability in this scenario?

`@options1`
- Immediately available after each prediction
- [Available only after a significant delay]
- Permanently absent for all predictions
- Available through real-time labeling services

---

## Alert fatigue

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your drift detection system triggers dozens of notifications every week, but only a small fraction correspond to meaningful drops in model performance. The team has started ignoring them entirely.

What is this problem commonly called?

`@options1`
- Covariate shift
- Concept drift
- Distribution mismatch
- [Alert fatigue]

---

## Ideal monitoring workflow

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want a monitoring workflow that reduces false alarms and focuses investigations when something is actually wrong.

What should be the first step in the ideal monitoring workflow?

`@options1`
- Start with drift detection across all input features
- Start with root cause analysis of feature shifts
- [Start by tracking or estimating performance]
- Start by retraining on a fixed calendar schedule

---

## Covariate shift definition

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Production inputs start coming from a different distribution than the training inputs, but the relationship between features and the target has not changed.

What is this phenomenon called?

`@options1`
- Concept drift
- Label shift
- [Covariate shift]
- Target leakage

---

## Concept drift definition

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
The input data distribution looks stable, but the model's predictions become less reliable because the relationship between features and the target has changed in the real world.

What is this phenomenon called?

`@options1`
- Covariate shift
- Label shift
- [Concept drift]
- Data leakage

---

## Why drift-only systems mislead

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your monitoring stack is centered on drift tests. It flags any distribution change, even when the model's performance stays stable.

Why can drift detection create problems for the team?

`@options1`
- It is computationally too expensive to run
- It requires frequent model retraining to work
- It needs immediate ground truth for scoring
- [It can trigger many false alarms over time]

---

## Performance estimation algorithms

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have a classification model and the ground truth labels are delayed. You want an approach that estimates performance using predicted probabilities and an estimated confusion matrix.

Which algorithm matches that goal?

`@options1`
- Direct Loss Estimation (DLE)
- Wasserstein distance test
- [Confidence-Based Performance Estimation]
- Kolmogorov-Smirnov test

---

## DLE use case

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're monitoring a regression model, but the ground truth values are not available in real time. You want to estimate error metrics by training an additional model on reference data.

Which performance estimation approach is designed for this?

`@options1`
- [Direct Loss Estimation (DLE)]
- Confidence-Based Performance Estimation
- ROC curve threshold tuning
- Confusion matrix reconstruction

---

## Assumptions behind CBPE/DLE

```yaml
type: MultipleChoiceChallenge
key:
unit: ml-monitoring
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your colleague warns that performance estimation can break down if production data moves into areas never seen during training, or if the feature-target relationship changes.

Which assumption is being questioned?

`@options1`
- The model outputs calibrated probabilities
- The reference dataset is representative enough
- Labels arrive within a fixed time window
- [No unseen-region shift or concept drift occurs]
