---
title: Monitoring Machine Learning in Python Assessment Items (Coding)
output: html_document
description: Six BlanksChallenge items aligned to Monitoring Machine Learning in Python (NannyML workflows).
---

## Calculating realized performance

```yaml
type: BlanksChallenge
key:
unit: performance-calculation
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
Ground truth labels have arrived for your production data. Initialize the appropriate module to compute actual performance metrics and obtain results on the analysis set.

`@code1`
```{python}
calculator = nannyml.{{_expr1}}(
    problem_type='regression',
    y_pred='y_pred',
    y_true='tip_amount',
    metrics=['mae'],
    timestamp_column_name='timestamp',
    chunk_period='d'
)
calculator.fit(reference)
results = calculator.{{_expr2}}(analysis)
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()

reference, analysis, _ = nannyml.load_synthetic_car_price_dataset()
```

`@variables`
```yaml
expr1:
  - 'PerformanceCalculator'
expr2:
  - 'calculate'
```

`@distractors`
```yaml
```

---

## Initializing a CBPE estimator

```yaml
type: BlanksChallenge
key:
unit: performance-estimation
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're monitoring a binary classifier without immediate labels. Initialize the appropriate estimator for classification performance estimation.

`@code1`
```{python}
estimator = nannyml.{{_expr1}}(
    problem_type='classification_binary',
    y_pred_proba='predicted_probability',
    y_pred='prediction',
    y_true='employed',
    chunk_size=5000,
    metrics=['roc_auc'],
)
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()
```

`@variables`
```yaml
expr1:
  - 'CBPE'
```

`@distractors`
```yaml
```

---

## Initializing a DLE estimator

```yaml
type: BlanksChallenge
key:
unit: performance-estimation
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're estimating regression model performance without ground truth labels. Initialize the appropriate estimator and fit it to the reference data.

`@code1`
```{python}
estimator = nannyml.{{_expr1}}(
    y_pred='y_pred',
    y_true='tip_amount',
    feature_column_names=features,
    metrics=['mse'],
)
estimator = estimator.{{_expr2}}(reference)
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()

reference, analysis, _ = nannyml.load_synthetic_car_price_dataset()
features = ['car_age', 'km_driven', 'fuel_type']
```

`@variables`
```yaml
expr1:
  - 'DLE'
expr2:
  - 'fit'
```

`@distractors`
```yaml
```

---

## Estimating performance on new data

```yaml
type: BlanksChallenge
key:
unit: performance-estimation
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You've fit an estimator on a reference period and now want to estimate performance for the latest production period stored in `analysis`.

`@code1`
```{python}
results = estimator.{{_expr1}}(analysis)
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()

reference, analysis, _ = nannyml.load_us_census_ma_employment_data()
estimator = nannyml.DLE(
    y_pred='predicted_probability',
    feature_column_names=['age', 'education', 'marital_status'],
    chunk_size=5000,
    y_true='employed',
    metrics=['mse'],
)
estimator = estimator.fit(reference)
```

`@variables`
```yaml
expr1:
  - 'estimate'
```

`@distractors`
```yaml
```

---

## Narrowing results for a specific period

```yaml
type: BlanksChallenge
key:
unit: results-analysis
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're exploring monitoring outputs. Narrow down results to the analysis period before visualizing or exporting them.

`@code1`
```{python}
analysis_results = estimated_results.{{_expr1}}(period='analysis')
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()

reference, analysis, analysis_gt = nannyml.load_us_census_ma_employment_data()

cbpe = nannyml.CBPE(
    problem_type='classification_binary',
    y_pred_proba='predicted_probability',
    y_pred='prediction',
    y_true='employed',
    chunk_size=5000,
    metrics=['roc_auc', 'accuracy'],
)
cbpe = cbpe.fit(reference)
estimated_results = cbpe.estimate(analysis)
```

`@variables`
```yaml
expr1:
  - 'filter'
```

`@distractors`
```yaml
```

---

## Converting results to a DataFrame

```yaml
type: BlanksChallenge
key:
unit: results-analysis
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You want to inspect estimated metrics as tabular data. Convert filtered results into a pandas-friendly format.

`@code1`
```{python}
df = estimated_results.filter(metrics=['roc_auc']).{{_expr1}}()
print(df.head(3))
```

`@pre_challenge_code`
```{python}
import nannyml
nannyml.disable_usage_logging()

reference, analysis, analysis_gt = nannyml.load_us_census_ma_employment_data()

cbpe = nannyml.CBPE(
    problem_type='classification_binary',
    y_pred_proba='predicted_probability',
    y_pred='prediction',
    y_true='employed',
    chunk_size=5000,
    metrics=['roc_auc'],
)
cbpe = cbpe.fit(reference)
estimated_results = cbpe.estimate(analysis)
```

`@variables`
```yaml
expr1:
  - 'to_df'
```

`@distractors`
```yaml
```
