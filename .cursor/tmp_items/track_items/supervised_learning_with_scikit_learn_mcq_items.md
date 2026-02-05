---
title: Supervised Learning with scikit-learn Assessment Items (MCQ)
output: html_document
description: Four MultipleChoiceChallenge items aligned to Supervised Learning with scikit-learn (conceptual topics).
---

## Picking a target type

```yaml
type: MultipleChoiceChallenge
key:
unit: supervised-learning-sklearn
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You’re building a supervised learning model, and you need to decide whether the problem is classification or regression based on the target.

Which target variable is best suited for a regression model?

`@options1`
- Whether a customer churned (0 or 1)
- Whether an email is spam (0 or 1)
- Whether a payment is fraudulent (yes or no)
- [The price of a house (in dollars)]

---

## Why stratify a split

```yaml
type: MultipleChoiceChallenge
key:
unit: supervised-learning-sklearn
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You’re splitting a churn dataset into train and test sets. Only about 10% of customers churn, so you want both sets to reflect that same proportion.

Which `train_test_split()` setting helps preserve the label proportions?

`@options1`
- Set `shuffle=False`
- Set `random_state=0`
- [Set `stratify=y`]
- Set `test_size=None`

---

## Accuracy under imbalance

```yaml
type: MultipleChoiceChallenge
key:
unit: supervised-learning-sklearn
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A fraud model sees only 1% fraudulent transactions. A teammate reports 99% accuracy and says the model is “excellent,” but you suspect it may be missing most fraud cases.

Which metric directly reflects how many actual fraud cases were correctly found?

`@options1`
- Precision
- [Recall]
- Accuracy
- Support

---

## What `predict_proba()` returns

```yaml
type: MultipleChoiceChallenge
key:
unit: supervised-learning-sklearn
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to build an ROC curve for a binary classifier. To do that, you need scores that represent how confident the model is that each observation belongs to the positive class.

What does `predict_proba(X_test)` return in scikit-learn?

`@options1`
- A single-column array of predicted class labels
- A 1D array of predicted probabilities for one class
- A dictionary mapping labels to confusion matrix values
- [A 2D array of probabilities for each class]
