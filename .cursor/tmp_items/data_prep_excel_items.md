---
title: Data Preparation in Excel
output: html_document
description: >-
  Assessment items covering data preparation concepts in Excel including importing,
  cleaning, text/date functions, logical formulas, lookups, and PivotTables.
---

## Data Preparation Steps

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.1"
# course_content_reference: |
#   "Data preparation involves cleaning, transforming, and organizing any raw 
#   data you will use to perform data analysis. To provide good quality analysis, 
#   you must ensure your data is high quality and 'clean'. This will ensure that 
#   your final results and outcomes are accurate."
```

`@assignment1`
A marketing analyst receives raw customer data with inconsistent formatting, duplicate entries, and some missing values. Before analyzing purchasing patterns, the analyst needs to prepare the data properly.

What is the primary goal of data preparation in this scenario?

`@options1`
- To create visualizations that communicate purchasing trends clearly
- To build formulas that automatically calculate marketing metrics
- [To ensure the data is clean and accurate for reliable analysis]
- To share the dataset with colleagues in a standardized format

---

## Importing External Data

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.2"
# course_content_reference: |
#   "To import data into our Excel file, we go to the Data menu, and under the 
#   Get & Transform Data section, we click on From Text/CSV. A new window appears 
#   that allows us to select the file we want to load into the file."
```

`@assignment1`
A data analyst needs to bring customer information stored in a CSV file into an Excel workbook for further processing. The file contains thousands of records that would be impractical to enter manually.

Where should the analyst navigate to import this CSV file into Excel?

`@options1`
- Navigate to Home menu then Insert section and select Import CSV
- [Navigate to Data menu then Get & Transform Data and From Text/CSV]
- Navigate to File menu then Open section and Browse for CSV files
- Navigate to Review menu then Data Connections and select New Source

---

## Removing Duplicate Records

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.2"
# course_content_reference: |
#   "Removing duplicates is an important part of cleaning raw data. Excel has a 
#   feature that lets you do this with great ease. You can identify and select 
#   the columns to remove duplicates from your data."
```

`@assignment1`
An inventory manager discovers that the product database contains rows that were accidentally entered multiple times during data entry. Each product should only appear once in the database.

What step should the manager take to address this issue efficiently?

`@options1`
- Sort data alphabetically then manually delete similar rows
- [Use the Remove Duplicates feature found in the Data menu]
- Use Find & Replace to locate and remove matching entries
- Create a filter and hide rows containing repeated IDs

---

## Using Flash Fill

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.2"
# course_content_reference: |
#   "So let's select a cell in Column D, click on Data at the top, and click 
#   Flash-fill. Flash fill lets you easily fill your data when it senses a 
#   pattern. This works best when there is existing data so that Excel can 
#   identify patterns easier."
```

`@assignment1`
A sales coordinator has a column containing full customer names like "Smith, John" and needs to create a separate column showing only the last names. The dataset has over 500 rows.

After manually typing the last name for the first two rows, what feature would automatically complete the remaining cells?

`@options1`
- [Flash Fill, which detects patterns from the examples provided]
- AutoComplete, which suggests text based on previous entries
- Fill Down, which copies the formula from the cell above
- Format Painter, which applies consistent formatting to cells

---

## Using Fill Series for Dates

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 1.2 / Chapter 1 Exercise"
# course_content_reference: |
#   "More advanced Fill Series features allow you to select either rows or columns 
#   to fill, the type of data, and even the intervals between the values. For 
#   example, you can enter the date in the first cell of a new column and then use 
#   Fill Series to populate the whole column with weekdays up to your desired end date."
```

`@assignment1`
A project manager needs to create a date lookup sheet showing every calendar day from January 1, 2024 through December 31, 2024. Manually typing 366 dates would be time-consuming.

What Excel feature allows populating a column with consecutive dates using a specified start and end date?

`@options1`
- [Fill Series with Type set to Date and a Stop value]
- Flash Fill with date pattern recognition enabled
- AutoFill by dragging the cell corner down the column
- SEQUENCE function with date formatting applied

---

## LEN Function for Data Quality

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1"
# course_content_reference: |
#   "The LEN function allows you to count how many characters are in a text string, 
#   including the spaces and special characters. For data preparation, it is a great 
#   way to help you identify if there are trailing spaces in your cells or identify 
#   anomalies in the data."
```

`@assignment1`
A database administrator notices that some state abbreviation codes in the Customer State column appear to have extra spaces. All valid state codes should be exactly 2 characters.

Which function would help identify cells containing invalid state codes with trailing spaces?

`@options1`
- TRIM() to automatically remove any unwanted space characters
- FIND() to locate the position of spaces within each cell
- [LEN() to count characters and flag values not equal to 2]
- CLEAN() to remove non-printable characters from the data

---

## TRIM Function for Cleaning Text

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Chapter 2 Exercise"
# course_content_reference: |
#   "Using the new column, remove all unwanted spaces from the values in 
#   Customer State. The function TRIM() will come in handy."
```

`@assignment1`
After checking the length of state abbreviation values, a data analyst confirms some cells contain trailing spaces (e.g., "CA  " instead of "CA"). The analyst needs to clean these values.

Which function removes the extra spaces while keeping the text content intact?

`@options1`
- CLEAN() removes all whitespace characters from the text string
- SUBSTITUTE() replaces specific characters with different values
- [TRIM() removes leading, trailing, and excess internal spaces]
- LEN() calculates the length of the text after spaces removed

---

## TEXTJOIN Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1"
# course_content_reference: |
#   "TEXTJOIN is similar to CONCAT. It combines text in the same way, but it also 
#   allows you to specify the delimiter of your choice between each value and 
#   include cells in the output if they are empty."
```

`@assignment1`
A logistics coordinator needs to create a full address column by combining Street, City, and Zip Code columns. Each component should be separated by a comma and space, and empty cells should still be included in the result.

Which function accomplishes this with a specified delimiter?

`@options1`
- CONCAT() combines text and allows delimiter specification
- [TEXTJOIN() combines text with a specified delimiter option]
- CONCATENATE() merges cells with automatic comma separation
- SUBSTITUTE() replaces cell references with combined text

---

## WEEKDAY Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 / Video 2.2"
# course_content_reference: |
#   "Next is WEEKDAY, a function that will give you an integer for the day of the 
#   week based on an inputted date. You can adjust the start of the week so that 
#   your output suits your definition of a week. We will use Monday as the start 
#   of the week, so we will enter two for the second variable of the formula."
```

`@assignment1`
A sales analyst wants to determine which day of the week each order was placed. The Order Date column contains dates, and the analyst needs a new column showing the weekday as a number (1 for Monday through 7 for Sunday).

What formula extracts the weekday number with Monday as day 1?

`@options1`
- =DAY(A2) returns the day portion of any date value
- =WEEKDAY(A2) returns weekday with Sunday as day one
- [=WEEKDAY(A2,2) returns weekday with Monday as day one]
- =DATEPART(A2,"weekday") extracts the day component

---

## WORKDAY Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 2.1 / Chapter 2 Exercise"
# course_content_reference: |
#   "Finally, WORKDAY will help you calculate the date based on the number of 
#   working days before or after a starting date. You are also able to exclude 
#   holiday dates from the calculation. It is useful for project planning."
```

`@assignment1`
A shipping coordinator needs to calculate delivery dates based on the order date and the number of business days required for shipment. Deliveries only occur on weekdays, not weekends.

Which function calculates a future date based on working days from a start date?

`@options1`
- =DATE(A2+B2) adds the number of days to the start date
- =EDATE(A2,B2) adds a specified number of months to a date
- =NETWORKDAYS(A2,B2) counts working days between two dates
- [=WORKDAY(A2,B2) returns the date after specified working days]

---

## AND Function for Multiple Conditions

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1"
# course_content_reference: |
#   "The AND function tests whether one or more conditions are true. If the 
#   logical tests are all true, the result is TRUE; otherwise, FALSE is returned."
```

`@assignment1`
A finance analyst needs to flag orders where the payment type is "CASH" and the order total exceeds $200. Both conditions must be true for the flag to show TRUE.

Which function tests that both conditions are met simultaneously?

`@options1`
- =OR(A2="CASH",B2>200) returns TRUE if either condition is met
- =IF(A2="CASH",B2>200) checks conditions in sequential order
- [=AND(A2="CASH",B2>200) returns TRUE only if both are true]
- =NOT(A2="CASH",B2>200) inverts the result of both conditions

---

## NOT Function for Opposite Conditions

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1 / Video 3.2"
# course_content_reference: |
#   "The NOT function is different as it only takes one logical argument. In 
#   addition, the function's output will also be the opposite of the condition 
#   set. Excel will look if the outcome of the condition is TRUE or FALSE, 
#   and then give the opposite outcome."
```

`@assignment1`
A product manager wants to flag products priced at or below the average price. The average price is stored in cell H3. The manager considers testing if the price is greater than the average.

How can the NOT function create a TRUE flag for products at or below average?

`@options1`
- =NOT(E2=H3) returns TRUE when price does not equal average
- =NOT(E2>H3,E2<H3) tests multiple conditions simultaneously
- [=NOT(E2>$H$3) returns TRUE when price is not above average]
- =NOT(E2) returns TRUE when the cell contains no value

---

## IF with AND Combined

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 3.1 / Chapter 3 Exercise"
# course_content_reference: |
#   "To do this in Excel, we can combine logical functions like AND, OR, and NOT 
#   with our IF function to create nested formulas that can test multiple conditions."
```

`@assignment1`
An operations analyst needs to categorize orders as "Same Day - On Time" when the shipping mode is "Same Day" AND the late delivery risk is 0. All other orders should be labeled "Other".

Which formula correctly combines IF and AND for this categorization?

`@options1`
- =IF(E2="Same Day",F2=0,"Same Day - On Time","Other")
- =AND(IF(E2=0,F2="Same Day"),"Same Day - On Time","Other")
- =IF(OR(E2=0,F2="Same Day"),"Same Day - On Time","Other")
- [=IF(AND(E2=0,F2="Same Day"),"Same Day - On Time","Other")]

---

## VLOOKUP Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 4.1"
# course_content_reference: |
#   "VLOOKUP searches the data vertically, so across columns. The function requires 
#   a lookup_value, the table_array is where you will look for the value, and the 
#   col_index_num is the column number containing the value to return. The optional 
#   range_lookup is set to FALSE for an exact match."
```

`@assignment1`
An analyst needs to pull product names from a Products sheet into the Orders sheet using the Product Id as the lookup value. The Products sheet has Product Id in column A and Product Name in column B.

What formula retrieves the product name for the ID in cell T2?

`@options1`
- =VLOOKUP(T2,Products!A:B,1,FALSE) returns the first column value
- =VLOOKUP(Products!A:B,T2,2,FALSE) places the table first in syntax
- =VLOOKUP(T2,Products!A:B,2,TRUE) finds an approximate match value
- [=VLOOKUP(T2,Products!A:B,2,FALSE) returns exact match from column 2]

---

## PivotTable Creation and Use

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
# course_section: "Video 4.1 / Video 4.2"
# course_content_reference: |
#   "We now have some values, but by default, the aggregation type is sum. To change 
#   this, click the down arrow next to the Sum of Price, then select Value Field 
#   Settings. Here we can choose which summarization method is applied."
```

`@assignment1`
A sales manager creates a PivotTable showing total order quantities by market region. By default, the values show as "Sum of Order Quantity" but the manager needs to display the average instead.

How does the manager change the aggregation method from Sum to Average?

`@options1`
- Right-click the PivotTable and then select Change Summary Type
- Edit the source data to calculate averages before the PivotTable
- [Click the field dropdown in Values then select Value Field Settings]
- Use the PivotTable Design menu to then modify calculation options
