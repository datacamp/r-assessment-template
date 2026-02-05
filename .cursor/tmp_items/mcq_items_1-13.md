---
title: Data Analysis in Excel - Items 1-13
output: html_document
description: Multiple choice items covering EDA, PivotTables, and logical functions
---

## EDA Definition

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A marketing team receives a new customer dataset with purchase history, demographics, and engagement metrics. Before building predictive models, they need to understand the data's structure, identify patterns, and generate insights about customer behavior.

What process describes this initial data investigation phase?

`@options1`
- [Exploratory data analysis]
- Data validation and cleaning
- Statistical hypothesis testing
- Model training and evaluation

---

## EDA Process Steps

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A data analyst has collected sales transaction data from multiple sources. The raw data contains missing values, inconsistent date formats, and duplicate records. Before exploring relationships between sales and customer segments, what should the analyst do first?

`@options1`
- Generate sales hypotheses
- Compute summary statistics
- [Prepare and clean the data]
- Visualize correlations

---

## Summary Statistics Overview

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A retail analyst examines monthly sales figures: $12,000, $15,000, $15,000, $18,000, $20,000. The most frequently occurring value is $15,000, the middle value is $15,000, and the average is $16,000.

Which summary statistic represents the middle value when data is sorted?

`@options1`
- Mean
- [Median]
- Mode
- Range

---

## PivotTables for Exploration

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales manager needs to quickly summarize revenue by product category and region. The dataset contains thousands of transactions with columns for category, region, and revenue amount.

Which Excel tool allows aggregating and reorganizing this data without writing formulas?

`@options1`
- [PivotTables]
- Conditional formatting
- Data validation
- Chart recommendations

---

## Calculated Fields Usage

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A PivotTable shows total sales and total units sold. The analyst wants to display revenue per unit as a new column in the same PivotTable without modifying the source data.

Which PivotTable feature creates this calculated column?

`@options1`
- Custom grouping
- Value field settings
- [Calculated fields]
- Slicer filters

---

## Custom Grouping Feature

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A PivotTable displays individual product names in rows. The analyst wants to compare performance between "Premium" products (Product A, Product B, Product C) and "Standard" products (Product D, Product E) without changing the source data.

Which PivotTable feature combines multiple row items into custom categories?

`@options1`
- Calculated fields
- [Custom grouping]
- Timeline filters
- Value formatting

---

## Slicers for Filtering

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst creates a PivotTable showing sales by region. They frequently need to filter by different subscription types while keeping the filter options visible and easy to change.

Which PivotTable feature provides visible, interactive filter buttons?

`@options1`
- [Slicers]
- Timeline filter tools
- Calculated field tools
- Custom grouping tools

---

## Timeline Filters Purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A PivotTable contains sales data with date columns. The analyst wants to filter sales by quarters and years using an interactive calendar interface rather than dropdown menus.

Which PivotTable feature provides date-based filtering with a visual timeline?

`@options1`
- Slicer tools
- Custom grouping tools
- Calculated field tools
- [Timeline filters]

---

## IFS Function Syntax

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales analyst needs to categorize transactions into "High", "Medium", or "Low" based on sales amounts: over $10,000 is High, $5,000-$10,000 is Medium, and under $5,000 is Low. They want a single formula that evaluates multiple conditions in order.

Which function evaluates multiple logical tests sequentially and returns the first matching value?

`@options1`
- SWITCH
- COUNTIF
- SUMIF
- [IFS]

---

## SWITCH Function Usage

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A dataset contains subscription type codes: "B" for Basic, "P" for Premium, "E" for Enterprise. The analyst needs to convert these single-letter codes into full subscription names in a new column.

Which function maps a cell's value against a list and returns the corresponding result?

`@options1`
- IFS
- COUNTIF
- AVERAGEIF
- [SWITCH]

---

## COUNTIF Function Purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A customer service manager has a list of support tickets with status values. They need to count how many tickets have a status of "Open" across the entire dataset.

Which function counts cells in a range that meet a specific condition?

`@options1`
- SUMIF
- AVERAGEIF
- SWITCH
- [COUNTIF]

---

## SUMIF Function Application

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A financial analyst has sales data with regions in one column and revenue amounts in another. They need to calculate the total revenue for only the "North" region without creating a PivotTable.

Which function sums values in a range where corresponding cells meet a specified condition?

`@options1`
- COUNTIF
- AVERAGEIF
- IFS
- [SUMIF]

---

## AVERAGEIF Function Usage

```yaml
type: MultipleChoiceChallenge
key:
unit: data-analysis-in-excel
subskill: data-analysis
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A product manager analyzes customer satisfaction scores. The dataset contains product categories and satisfaction ratings. They need to find the average satisfaction score for only the "Electronics" category.

Which function calculates the average of values in a range where corresponding cells meet a specified condition?

`@options1`
- COUNTIF
- SUMIF
- SWITCH
- [AVERAGEIF]
