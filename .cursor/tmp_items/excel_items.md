---
title: Introduction to Excel
output: html_document
description: >-
  Assessment items covering Excel fundamentals including navigation, tables, formulas,
  data management, aggregate functions, and data visualization.
---

## Excel Data Limitations

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: excel-basics
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A marketing analyst is planning to consolidate customer transaction data from multiple regional databases into a single Excel workbook. The combined dataset will contain 1.5 million rows of transaction records spanning three years.

What limitation will the analyst encounter when attempting to store all this data in Excel?

`@options1`
- Excel cannot handle workbooks with more than one million columns of data
- [Excel worksheets are limited to approximately 1,048,576 rows of data]
- Excel restricts data imports to files under 500 megabytes in size
- Excel requires all data to be entered manually, row by row

## Cell Reference Identification

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: excel-basics
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An intern is learning to navigate Excel and needs to locate specific data. Their supervisor asks them to find the value at the intersection of column D and row 15.

Which cell reference should the intern look for?

`@options1`
- 15D
- [D15]
- Row15ColD
- Column D Row 15

## Formula Creation

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: excel-basics
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales representative wants to calculate the total cost by adding the values in cells B5 and C5 within their Excel worksheet.

What must the representative type at the beginning of the formula to make Excel perform this calculation?

`@options1`
- A plus sign (+)
- A colon (:)
- [An equal sign (=)]
- A dollar sign ($)

## Structured Reference Benefits

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: tables
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst is building formulas in an Excel table with columns named "Revenue" and "Expenses". They can use either traditional cell references like `E2:E500` or structured references like `[@Revenue]`.

What advantage do structured references provide over traditional cell references?

`@options1`
- Structured references execute calculations significantly faster than cell references
- Structured references prevent users from accidentally deleting table columns
- [Structured references update automatically when data is added or removed]
- Structured references allow formulas to work across multiple workbooks

## Filtering and Sorting Data

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: tables
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A warehouse manager has a large inventory table and needs to find all products from a specific supplier. They want to temporarily hide all other supplier records while keeping the data intact.

Which Excel feature should the manager use to accomplish this task?

`@options1`
- Delete rows that don't match the supplier name
- [Apply a filter to show only the selected supplier]
- Sort the table alphabetically by supplier column
- Create a new worksheet and copy matching rows

## Named Ranges Purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: data-management
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An accountant frequently references the same column of expense data in multiple formulas across different worksheets. They decide to create a named range called "monthly_expenses" for this column.

What benefit does using a named range provide in this situation?

`@options1`
- Named ranges automatically calculate the sum of all values in the column
- Named ranges prevent other users from viewing sensitive expense data
- [Named ranges make formulas easier to read and maintain across worksheets]
- Named ranges convert expense values into different currency formats

## Subtotals for Data Analysis

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: data-management
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A regional manager has sales data sorted by store location and wants to see the average sales amount for each store without creating individual formulas for each location.

Which Excel feature automatically calculates aggregated values at each change in the sorted column?

`@options1`
- Conditional formatting with data bars for each store
- [Subtotals with the average function on the sales column]
- Pivot tables with store names in the row area
- Data validation rules applied to the sales column

## Data Validation Rules

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: data-management
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team lead is creating a shared workbook for tracking project hours. They want to ensure that team members can only enter positive whole numbers in the "Hours Worked" column, and receive an error message if they enter invalid data.

Which Excel feature should the team lead configure to enforce these input requirements?

`@options1`
- Conditional formatting to highlight invalid entries with red fill
- Cell protection to lock the column from any user modifications
- [Data validation to allow only whole numbers greater than zero]
- Custom number format to display values as positive integers

## Order of Operations

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: aggregate-functions
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analyst enters the formula `=10+5*2` into an Excel cell and expects the result to be 30. Instead, Excel returns 20.

Why did Excel return a different result than the analyst expected?

`@options1`
- Excel processes formulas from right to left by default
- Excel rounds all intermediate calculations to whole numbers
- [Excel performs multiplication before addition in calculations]
- Excel requires parentheses around every arithmetic operation

## Aggregate Functions

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: aggregate-functions
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A professor has a column of student test scores and needs to find the typical score achieved by the class. They want to calculate the central value by summing all scores and dividing by the number of students.

Which Excel function should the professor use to calculate this value directly?

`@options1`
- `COUNT()`
- `SUM()`
- [`AVERAGE()`]
- `MAX()`

## Text Functions

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: text-functions
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A data analyst has a column of product codes where some are entered as "ABC123" and others as "abc123". They need all codes to appear in uppercase for consistency before importing the data into another system.

Which Excel function should the analyst use to convert all product codes to uppercase?

`@options1`
- `LEFT()`
- `RIGHT()`
- [`UPPER()`]
- `LOWER()`

## LEFT Function Application

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: text-functions
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A shipping clerk has order numbers in the format "ORD-2024-12345" and needs to extract just the prefix "ORD" for a report. The prefix is always the first three characters.

Which formula would correctly extract only the first three characters from cell A1?

`@options1`
- `=RIGHT(A1, 3)`
- `=MID(A1, 1, 3)`
- [=LEFT(A1, 3)]
- `=UPPER(A1, 3)`

## Date Functions

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: date-functions
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A financial analyst has a column of transaction dates and needs to extract just the year from each date to create a yearly summary report. The dates are stored in standard Excel date format.

Which function should the analyst use to extract the year component from a date cell?

`@options1`
- `DATE()`
- `MONTH()`
- `DAY()`
- [`YEAR()`]

## Data Visualization Purpose

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A business analyst is preparing a presentation for executives who need to quickly understand sales trends and identify unusual patterns in a large dataset containing thousands of records.

Why would creating data visualizations be more effective than presenting the raw data in tables?

`@options1`
- Visualizations reduce the file size of Excel workbooks significantly
- Visualizations automatically correct errors found in the source data
- [Visualizations help identify trends and outliers more easily than tables]
- Visualizations prevent unauthorized users from accessing sensitive data

## Chart Type Selection

```yaml
type: MultipleChoiceChallenge
key:
unit: intro-to-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A project manager has monthly revenue data for the past two years and wants to show how revenue has changed over time. They need to highlight the upward or downward movement between consecutive months.

Which chart type is most appropriate for displaying this time-based trend data?

`@options1`
- A pie chart showing each month as a slice of total revenue
- [A line chart showing revenue progression across time periods]
- A bar chart comparing all months side by side vertically
- A scatter plot with months on both axes of the chart
