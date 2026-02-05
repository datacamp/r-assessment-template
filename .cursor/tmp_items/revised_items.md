---
title: Data Preparation in Excel - Revised Items
output: html_document
description: Revised MCQ items addressing review feedback
---

## Order Entry Workflow

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You just started as an analyst at a supply chain company. Your manager hands you three raw data files from different systems and asks you to prepare them for the quarterly sales analysis. You've never worked with this data before.

What should you do first?

`@options1`
- [Consolidate files into one workbook]
- Remove any duplicate rows found
- Apply formatting to all columns
- Create summary calculations now

---

## External Data Import

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your IT department sends you customer records stored in a comma-separated file. You need to bring this data into your Excel workbook while preserving all columns and maintaining data integrity. The file contains 50,000 records.

What is the recommended approach to bring this external file into Excel?

`@options1`
- Copy raw contents and paste into a new worksheet
- [Use Get & Transform Data from the Data tab menu]
- Open the file separately and recreate structure
- Create a new workbook and type records in manually

---

## Cleaning Repeated Records

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
After importing product data, you notice that some products appear multiple times with identical information in every column. Your analysis requires each product to appear only once. You select all columns in your dataset.

What happens when you use the Remove Duplicates feature with all columns selected?

`@options1`
- Excel highlights duplicate rows but keeps all data
- [Excel deletes rows where all column values match]
- Excel removes rows with any repeated cell value
- Excel creates a sheet listing duplicates found

---

## Pattern-Based Column Population

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your customer database has "First Name" in column A and "Last Name" in column B. You need to create a "Full Name" column combining them with a space. You type "John Smith" in C2 and "Maria Garcia" in C3 to establish a pattern.

Which feature will automatically complete the remaining 5,000 rows based on this pattern?

`@options1`
- AutoComplete
- [Flash Fill]
- Fill Series
- Copy Special

---

## Combining Address Components

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have customer addresses split across three columns: Street (A2), City (B2), and State (C2). You need to create a single address column where each component is separated by a comma and space, like "123 Main St, Seattle, WA".

Which function lets you specify what character separates each component when combining them?

`@options1`
- CONCAT()
- CONCATENATE()
- [TEXTJOIN()]
- COMBINE()

---

## Dynamic Date Display

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You create a sales report that colleagues will open on different days throughout the month. You want cell A1 to always display the current date when anyone opens the workbook, so they know when they're viewing the calculations.

Which function automatically updates to show the current date each time the workbook opens?

`@options1`
- [TODAY()]
- DATE()
- NOW()
- CURRENT()

---

## Controlling Worksheet Access

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You've finished preparing the customer data and need to share the workbook with colleagues. You want to prevent anyone from accidentally deleting columns or changing formulas, but they should still be able to view and filter the data.

Where do you configure these restrictions for a single sheet?

`@options1`
- File > Info > Permissions
- [Review > Protect Sheet]
- Home > Format > Lock Cells
- Data > Data Validation

---

## Reversing a Logical Test

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have a formula that tests whether each product price exceeds $100, returning TRUE or FALSE. Your manager now wants the opposite: flag products that are $100 or less as TRUE instead.

Which function wraps around your existing test to reverse the TRUE/FALSE output?

`@options1`
- AND()
- [NOT()]
- OR()
- XOR()

---

## Two-Outcome Conditional Labels

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your order tracking sheet has a Status column with values like "Shipped" and "Processing". You need a new column that displays "Complete" for shipped orders and "Pending" for everything else.

Which function tests a condition and returns different values based on whether the test is TRUE or FALSE?

`@options1`
- [IF()]
- AND()
- OR()
- NOT()

---

## Three-Category Classification

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your finance team needs to categorize invoice amounts: "High" for over $500, "Medium" for $200-$500, and "Low" for under $200. A single TRUE/FALSE test cannot produce three different labels.

What technique allows you to create three distinct category labels from one formula?

`@options1`
- Using AND() with three conditions in a single function call
- [Nesting one IF() function inside another IF() function]
- Using OR() to test each price threshold one at a time
- Combining AND() and OR() together in the same formula

---

## Multi-Condition Category Assignment

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to label orders as "Priority" only when TWO conditions are both true: shipping mode is "Express" AND order value exceeds $300. Orders meeting only one condition or neither should be labeled "Standard".

Which approach tests both conditions together and then assigns the appropriate label?

`@options1`
- Use OR() inside IF() to check either condition is met
- Use two separate IF() formulas placed in two columns
- [Use AND() inside IF() requiring both for "Priority"]
- Use NOT() to reverse the logic of one condition test

---

## Preserving Cell References When Copying

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're calculating commission by multiplying each salesperson's revenue (column A) by a rate stored in cell H3. When you copy the formula from row 2 to row 100, the revenue reference should change (A2, A3, A4...) but the rate cell must always stay H3.

How do you ensure the rate cell reference doesn't change when copying?

`@options1`
- Type the cell address using uppercase letters
- [Add dollar signs before column and row ($H$3)]
- Name the cell "Rate" and use it in formula
- Place the rate value directly in the formula

---

## Lookup Function Components

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to pull product names from a reference table using product IDs. The VLOOKUP function requires you to specify: what you're searching for, where to search, and which column contains the value to return.

What is the third required argument that tells VLOOKUP which column holds the return value?

`@options1`
- [The col_index_num specifying return column position]
- The range_lookup setting for match type (TRUE/FALSE)
- The lookup_value specifying what to search for
- The table_array range defining where to search

---

## Requiring Precise Matches

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're using VLOOKUP to find customer names by their unique ID numbers. Customer ID "1001" must match exactly—returning data for ID "1002" or "10010" would cause errors in your report.

What value do you enter for the range_lookup argument to require an exact match?

`@options1`
- TRUE
- [FALSE]
- EXACT
- MATCH

---

## Row-Based Data Lookup

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your sales data has years as column headers (2020, 2021, 2022, 2023) across the top row, with product names down the first column. You need to find the sales figure for "Laptops" in 2022 by searching horizontally across the year headers.

Which lookup function searches across rows rather than down columns?

`@options1`
- VLOOKUP
- [HLOOKUP]
- XLOOKUP
- INDEXMATCH

