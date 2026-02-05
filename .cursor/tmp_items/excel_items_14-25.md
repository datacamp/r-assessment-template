---
title: Excel Fundamentals Assessment Items 14-25
output: html_document
description: >-
  Multiple choice items covering Excel functions and features.
---

## Calculating Total Sales

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.3 - Aggregate and Arithmetic operations"
# course_content_reference: |
#   **From Video 2.3:**
#   "Finally, we'll look at the sum function, which can be useful for adding together values in a given column."
#   "Similar to our average function, we can use the same types of references for other aggregate functions, including min, max, count, and sum."
```

`@assignment1`
A retail manager has a sales table with item prices in column E. They need to calculate the total revenue from all sales transactions.

Which function should they use to add together all values in the ItemPrice column?

`@options1`
- [SUM()]
- AVERAGE()
- COUNT()
- MIN()

---

## Finding Average Price

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.3 - Aggregate and Arithmetic operations"
# course_content_reference: |
#   **From Video 2.3:**
#   "Average, also known as the arithmetic mean, can express the central or typical value in a set of numbers. It's calculated as the sum of all values divided by the number of records."
```

`@assignment1`
An analyst wants to understand the typical value of house prices in their dataset. They have prices listed in column B from rows 2 to 50.

Which function will calculate the central value of these prices?

`@options1`
- SUM()
- MAX()
- COUNT()
- [AVERAGE()]

---

## Counting Sales Records

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.3 - Aggregate and Arithmetic operations"
# course_content_reference: |
#   **From Video 2.3:**
#   "If we want to determine how many rows of data exist in the data set, we can use the count function, which gives us the number of records in a given column."
```

`@assignment1`
A data analyst needs to verify how many sales transactions are recorded in their spreadsheet. The transaction IDs are stored in column A.

Which function will return the number of records in this column?

`@options1`
- SUM()
- AVERAGE()
- [COUNT()]
- MIN()

---

## Identifying Price Range

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.3 - Aggregate and Arithmetic operations"
# course_content_reference: |
#   **From Video 2.3:**
#   "We can use the min function to get the minimum or smallest value in a column. We can use the max function to get the maximum or largest value in a column."
```

`@assignment1`
A product manager wants to understand the price range of their inventory. They have prices in column D and need to find both the lowest and highest prices.

Which two functions should they use together?

`@options1`
- SUM() and AVERAGE()
- COUNT() and SUM()
- [MIN() and MAX()]
- AVERAGE() and COUNT()

---

## Referencing Named Ranges

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 - Managing and formatting data"
# course_content_reference: |
#   **From Video 2.1:**
#   "By naming a range in your data, it becomes easier to reference that range in formulas in different areas of your spreadsheet, saving you a lot of time."
```

`@assignment1`
A financial analyst frequently uses the same price column in multiple formulas across different sheets. They want to avoid repeatedly searching for the correct cell range.

What Excel feature allows them to assign a name to a cell range for easier reference in formulas?

`@options1`
- [Named ranges]
- Data validation
- Subtotals
- Cell formatting

---

## Grouping Data Summaries

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 - Managing and formatting data"
# course_content_reference: |
#   **From Video 2.1:**
#   "Excel provides a subtotal feature that allows you to use more common aggregation methods, like sum, count, or even average across a specific column in your data. This feature creates a subtotal for the different data points in your chosen column and even adds a grand total for the whole data set."
```

`@assignment1`
A sales manager has data sorted by region and wants to see average sales for each region without manually creating formulas. They need aggregation that automatically groups by region.

Which Excel feature creates summary calculations for each group in sorted data?

`@options1`
- Named ranges
- Data validation
- [Subtotals]
- Cell formatting

---

## Restricting Data Entry

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 - Managing and formatting data"
# course_content_reference: |
#   **From Video 2.1:**
#   "Data validation allows you to control the data or values entered into a cell. This includes the type of data that can be entered. You can add instructions that appear for the user to know what they can enter, while also customizing the error message that will appear if an invalid value is entered."
```

`@assignment1`
A team lead is sharing a workbook where others will enter order quantities. They want to ensure only whole numbers greater than zero can be entered in the quantity column.

Which feature should they use to control what values can be entered in cells?

`@options1`
- Named ranges
- [Data validation]
- Subtotals
- Cell formatting

---

## Highlighting Cell Conditions

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 - Managing and formatting data"
# course_content_reference: |
#   **From Video 2.1:**
#   "This feature allows you to format and highlight cells that meet specific conditions that you can set. This way, you can make patterns or trends more apparent."
```

`@assignment1`
An analyst wants to automatically highlight all cells in a price column that exceed $1000 to quickly identify high-value items.

Which Excel feature formats cells based on specific conditions?

`@options1`
- Data validation
- Named ranges
- [Conditional formatting]
- Subtotals

---

## Extracting Text Characters

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1 - Other functions in Excel"
# course_content_reference: |
#   **From Video 3.1:**
#   "With the left function, we return the first characters in a string based on a specified number of characters. Similarly, the right function follows the same premise, except it returns the last characters in a string."
```

`@assignment1`
A data preparer has product codes in column A where the first 3 characters represent the category. They need to extract just these first 3 characters into a new column.

Which function returns the first characters from a text string?

`@options1`
- [LEFT()]
- RIGHT()
- UPPER()
- COUNT()

---

## Extracting Date Components

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1 - Other functions in Excel"
# course_content_reference: |
#   **From Video 3.1:**
#   "We can use functions such as day and year, which will return the corresponding part of the date you have specified."
```

`@assignment1`
An analyst has order dates in column G and needs to create separate columns showing the year and month of each order for trend analysis.

Which functions extract the year and month from a date value?

`@options1`
- LEFT() and RIGHT()
- SUM() and AVERAGE()
- [YEAR() and MONTH()]
- COUNT() and MIN()

---

## Rounding Numerical Values

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1 - Other functions in Excel"
# course_content_reference: |
#   **From Video 3.1:**
#   "This straightforward function returns a number rounded to the specified number of digits."
```

`@assignment1`
A financial analyst calculates average prices that result in values like $486.093. They want to display these rounded to 2 decimal places for reporting.

Which function rounds a number to a specified number of digits?

`@options1`
- SUM()
- AVERAGE()
- [ROUND()]
- COUNT()

---

## Quick Data Summary

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-excel
subskill: excel-fundamentals
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.1 - Navigating Excel"
# course_content_reference: |
#   **From Video 1.1:**
#   "When you select cells, the status bar at the bottom gives you a quick summary, like the average value or sum. It's a handy tool for a quick data check."
```

`@assignment1`
A user selects a range of sales values and wants to quickly see the average without creating a formula. They need an instant summary that appears automatically.

Where can they view a quick summary like average or sum for selected cells?

`@options1`
- Formula bar
- Ribbon menu
- Name manager
- [Status bar]
