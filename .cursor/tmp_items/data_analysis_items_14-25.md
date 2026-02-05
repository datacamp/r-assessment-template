---
title: Data Analysis Items 14-25
output: html_document
description: Multiple choice items covering COUNTIFS, SUMIFS, what-if analysis, and forecasting
---

## COUNTIFS Multiple Criteria

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales analyst needs to count how many Premium subscription customers made purchases in June 2021. The data includes columns for `Sales Month`, `Subscription Type`, and `Sales Amount`.

Which function should the analyst use to count rows where both conditions are true?

`@options1`
- COUNTIF with nested IF statements
- [COUNTIFS with multiple criteria ranges]
- SUMIFS with a count aggregation
- AVERAGEIFS with conditional counting

---

## SUMIFS Multiple Criteria

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A financial analyst wants to calculate total sales revenue for Enterprise customers in the last quarter. The data table has `Sales Month`, `Subscription Type`, and `Sales Amount` columns.

What function calculates the sum when multiple conditions must be met?

`@options1`
- SUMIF with multiple nested functions
- [SUMIFS with range and criteria pairs]
- COUNTIFS converted to sum values
- AVERAGEIFS multiplied by count

---

## What-If Analysis Concept

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A business manager wants to understand how changing the growth rate would impact projected revenue. They need to explore different assumptions about future performance.

What type of analysis asks "what would this be if that" to evaluate outcomes?

`@options1`
- Historical trend analysis only
- Descriptive statistics summary
- [What-if analysis using scenarios]
- Data validation checking

---

## Scenario vs Sensitivity Analysis

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst needs to evaluate how projected sales change across a wide range of price points and elasticity values. They want to see all possible combinations in one table.

Which analysis type evaluates a dependent variable across a range of input values?

`@options1`
- Scenario analysis with fixed inputs
- [Sensitivity analysis with varying ranges]
- Goal Seek with single target value
- Manual calculation for each case

---

## Goal Seek Tool

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales team knows their target revenue is $100,000 next month. They have a formula that calculates revenue based on growth rate, but they need to find what growth rate achieves this target.

Which Excel tool finds the input value needed to reach a specific output?

`@options1`
- [Goal Seek for reverse calculation]
- Scenario Manager for multiple cases
- Data Table for sensitivity ranges
- Forecast Sheet for predictions

---

## Scenario Manager Tool

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A pricing analyst wants to compare how three different pricing strategies affect projected sales. They need to organize multiple scenarios and generate a summary report comparing all outcomes.

Which Excel tool manages and compares multiple what-if scenarios?

`@options1`
- Goal Seek for single target finding
- [Scenario Manager for multiple scenarios]
- Data Table for sensitivity analysis
- Forecast Sheet for time series

---

## One-Variable Data Table

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst wants to see how projected sales change when Premium license prices vary from $12.50 to $25.00. They need a table showing sales at each price point automatically.

Which tool creates a table showing how one input variable affects the output?

`@options1`
- Scenario Manager with multiple scenarios
- [Data Table with one input variable]
- Goal Seek for target finding
- Forecast Sheet for predictions

---

## Two-Variable Data Table

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A pricing strategist needs to analyze how both price changes and demand elasticity together impact projected sales. They want to see all combinations in a single table format.

Which Data Table configuration evaluates two input variables simultaneously?

`@options1`
- One-variable table with nested formulas
- [Two-variable table with row and column inputs]
- Scenario Manager with two scenarios
- Goal Seek with two constraints

---

## Forecasting Fundamentals

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A business analyst needs to predict next quarter's sales based on historical monthly data. They understand that forecasts are estimates, not guarantees, and want to use statistical techniques.

What process predicts future outcomes using historical data patterns?

`@options1`
- Goal Seek for target values
- Scenario analysis for fixed cases
- [Forecasting with statistical methods]
- Data validation for accuracy checks

---

## Simple Moving Average

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst wants to forecast next month's sales by averaging the previous three months. Each historical month should contribute equally to the prediction.

Which forecasting method uses equal weights for previous periods?

`@options1`
- Weighted moving average with different weights
- [Simple moving average with equal weights]
- Exponential smoothing with decay factors
- Trendline regression with slope methods

---

## Weighted Moving Average

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales forecaster wants to predict next month's revenue by giving more importance to recent months. They assign 15% to the oldest month, 35% to the middle month, and 50% to the most recent month.

Which method applies different importance weights to historical periods?

`@options1`
- Simple moving average with equal treatment
- [Weighted moving average with assigned weights]
- Goal Seek for target calculation
- Scenario Manager for fixed cases

---

## FORECAST.ETS Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst needs to create a sophisticated forecast that accounts for seasonality patterns and provides confidence intervals. They want Excel to automatically detect trends and seasonal variations.

Which function provides advanced forecasting with seasonality detection?

`@options1`
- AVERAGE for simple calculations
- [FORECAST.ETS for advanced predictions]
- SUMIFS for conditional sums
- COUNTIFS for counting with criteria
