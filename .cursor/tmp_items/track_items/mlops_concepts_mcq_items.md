---
title: MLOps Concepts Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–4 of MLOps Concepts.
---

## Defining MLOps

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your team is spending time on deployment pipelines and monitoring instead of just training a better model in a notebook. A stakeholder asks what value this extra work provides.

What does MLOps aim to achieve?

`@options1`
- [Reliable deployment and maintenance in production]
- Automatic hyperparameter tuning in notebooks
- A dashboard for reporting model accuracy
- A technique for training on streaming data

---

## Cross-functional ML engineer

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need a role that can work across the full ML lifecycle, overlapping with data engineering and data science, and helping with deployment and system integration.

Which role best matches that description?

`@options1`
- The data analyst
- [The machine learning engineer]
- The backend engineer
- The data scientist

---

## Data quality dimensions

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your customer dataset has some records where ages are recorded as 18 when the actual age is 32. You're checking the data before training.

Which data quality dimension does this problem violate?

`@options1`
- Completeness
- Consistency
- [Accuracy]
- Timeliness

---

## Feature store purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Multiple teams in your company keep rebuilding the same features for their ML projects. You want a centralized system where features can be defined once and reused.

What tool addresses this need?

`@options1`
- An experiment tracker
- A model registry
- A data lake
- [A feature store]

---

## Experiment tracking value

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your team ran dozens of model experiments last month. Now you need to find which hyperparameters produced the best result so you can reproduce it.

What practice helps with this?

`@options1`
- [Experiment tracking]
- Data version control
- Feature engineering
- Model containerization

---

## Container benefits

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A model works perfectly on the data scientist's laptop but fails in production because the Python version and library versions differ between environments.

What technique helps prevent this?

`@options1`
- Using a feature store for inputs
- [Packaging the model in a container]
- Switching to a simpler algorithm
- Retraining on production data

---

## Microservices architecture

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your company's application has the ML model, payment service, and inventory service all bundled together. When the model fails, the entire application goes down.

What architecture change could isolate failures?

`@options1`
- Combining all services into one codebase
- Adding a load balancer in front
- Switching to a different cloud provider
- [Deploying each service independently]

---

## Canary deployment

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to deploy a new model version to production but limit the risk if it performs poorly. You decide to route only a small percentage of traffic to the new model at first.

Which deployment strategy is this?

`@options1`
- Basic deployment
- Shadow deployment
- [Canary deployment]
- Blue-green deployment

---

## Statistical monitoring

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter4
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your deployed model's predictions are being tracked to see if the distribution of predicted probabilities has changed over time.

Which type of monitoring is this?

`@options1`
- Computational monitoring
- [Statistical monitoring]
- Infrastructure monitoring
- Network monitoring

---

## MLOps maturity levels

```yaml
type: MultipleChoiceChallenge
key:
unit: mlops-concepts
subskill: chapter4
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A company has automated both model development and deployment. They have a full CI/CD pipeline, close collaboration between teams, and automatic retraining when drift is detected.

Which MLOps maturity level does this describe?

`@options1`
- The lowest level: all processes manual
- Mid-level: development automated only
- [The highest level: full CI/CD automation]
- Entry level: ad-hoc experimentation
