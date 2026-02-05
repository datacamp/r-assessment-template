---
title: Supervised Learning with scikit-learn Assessment Items (Coding)
output: html_document
description: Six BlanksChallenge items aligned to Supervised Learning with scikit-learn (coding topics).
---

## Instantiating a KNN classifier

```yaml
type: BlanksChallenge
key:
unit: sklearn-classification
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're prototyping a churn model. Choose a classifier that predicts labels based on the majority vote of nearby observations.

`@code1`
```{python}
knn = {{_expr1}}(n_neighbors=5)
```

`@pre_challenge_code`
```{python}
from sklearn.neighbors import KNeighborsClassifier
```

`@variables`
```yaml
expr1:
  - 'KNeighborsClassifier'
```

`@distractors`
```yaml
```

---

## Splitting data for evaluation

```yaml
type: BlanksChallenge
key:
unit: model-evaluation
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're evaluating a classifier. Divide the data so both resulting sets preserve the original label proportions.

`@code1`
```{python}
X_train, X_test, y_train, y_test = {{_expr1}}(
    X, y, test_size=0.3, random_state=7, stratify=y
)
```

`@pre_challenge_code`
```{python}
import numpy as np
from sklearn.model_selection import train_test_split

X = np.array([[1.0, 2.0], [2.0, 1.0], [1.5, 1.2], [3.2, 3.1], [2.8, 2.9]])
y = np.array([0, 0, 0, 1, 1])
```

`@variables`
```yaml
expr1:
  - 'train_test_split'
```

`@distractors`
```yaml
```

---

## Reshaping a single feature

```yaml
type: BlanksChallenge
key:
unit: regression-basics
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're fitting a regression model using a single feature. Convert a 1D feature array into the 2D shape scikit-learn expects.

`@code1`
```{python}
X_bmi_2d = X_bmi.{{_expr1}}(-1, 1)
```

`@pre_challenge_code`
```{python}
import numpy as np

X_bmi = np.array([22.0, 27.5, 31.2, 18.9, 25.0])
```

`@variables`
```yaml
expr1:
  - 'reshape'
```

`@distractors`
```yaml
```

---

## Building a linear regression model

```yaml
type: BlanksChallenge
key:
unit: regression-basics
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're modeling a continuous outcome. Choose the standard scikit-learn estimator that minimizes the residual sum of squares without any regularization penalty.

`@code1`
```{python}
reg = {{_expr1}}()
```

`@pre_challenge_code`
```{python}
from sklearn.linear_model import LinearRegression
```

`@variables`
```yaml
expr1:
  - 'LinearRegression'
```

`@distractors`
```yaml
```

---

## Computing RMSE

```yaml
type: BlanksChallenge
key:
unit: model-evaluation
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're assessing a regression model that predicts house prices in dollars. You want an error metric in dollars that penalizes larger prediction errors more heavily than smaller ones.

`@code1`
```{python}
error = {{_expr1}}(y_test, y_pred)
print(round(error, 2))
```

`@pre_challenge_code`
```{python}
import numpy as np
from sklearn.metrics import root_mean_squared_error

y_test = np.array([3.0, 2.5, 4.1, 5.0])
y_pred = np.array([2.7, 2.8, 3.9, 5.2])
```

`@variables`
```yaml
expr1:
  - 'root_mean_squared_error'
```

`@distractors`
```yaml
```

---

## Encoding categories with dummy variables

```yaml
type: BlanksChallenge
key:
unit: categorical-encoding
subskill: chapter4
initial_difficulty: 0
item_writer_id: '999999999'
```

`@context`
You're encoding the `genre` column as dummy variables. Without any adjustments, `get_dummies()` produces:

|    | popularity | genre_Jazz | genre_Rap | genre_Rock |
|----|------------|------------|-----------|------------|
| 0  | 55         | 1          | 0         | 0          |
| 1  | 73         | 0          | 0         | 1          |
| 2  | 68         | 0          | 1         | 0          |

Notice that if a row has 0 in both `genre_Jazz` and `genre_Rap`, it must be Rock. Adjust the call to remove this redundancy.

`@code1`
```{python}
dummies = pd.get_dummies(music_df, {{_expr1}}=True)
print(dummies.sort_index(axis=1).head(3))
```

`@pre_challenge_code`
```{python}
import pandas as pd

music_df = pd.DataFrame(
    {"genre": ["Jazz", "Rock", "Rap"], "popularity": [55, 73, 68]}
)
```

`@variables`
```yaml
expr1:
  - 'drop_first'
```

`@distractors`
```yaml
```
