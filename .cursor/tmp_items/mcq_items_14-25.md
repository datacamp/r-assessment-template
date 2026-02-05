---
title: Excel Data Preparation Assessment Items 14-25
output: html_document
description: Multiple choice items covering logical functions, references, lookups, and PivotTables
---

## Multiple Conditions AND

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A sales manager wants to flag orders that meet two criteria: the order quantity exceeds 10 units and the product category is "Electronics". 

Which formula correctly identifies these orders?

`@options1`
- [=AND(E2>10,F2="Electronics")]
- `=OR(E2>10,F2="Electronics")`
- `=IF(E2>10,F2="Electronics")`
- `=NOT(E2<=10,F2<>"Electronics")`

---

## At Least One OR

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to identify customers who either live in California or have made purchases exceeding $500. 

What formula returns TRUE when at least one of these conditions is met?

`@options1`
- `=AND(A2="California",B2>500)`
- `=IF(A2="California",B2>500)`
- [=OR(A2="California",B2>500)]
- `=NOT(A2<>"California",B2<=500)`

---

## Opposite NOT Logic

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A product manager wants to flag items where the price is NOT above $100. The current formula tests if price exceeds $100.

Which function returns the opposite result of the condition test?

`@options1`
- `=AND(price>100)`
- `=OR(price>100)`
- [=NOT(price>100)]
- `=IF(price>100)`

---

## Conditional IF Outcomes

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to categorize orders based on delivery status. If an order is marked "Delivered", display "Complete"; otherwise, display "Pending".

Which function structure handles this conditional logic?

`@options1`
- `=AND(A2="Delivered","Complete","Pending")`
- `=OR(A2="Delivered","Complete","Pending")`
- `=NOT(A2="Delivered","Complete","Pending")`
- [=IF(A2="Delivered","Complete","Pending")]

---

## Nested IF Multiple Outcomes

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A finance team needs three payment categories: "High Priority" for amounts over $500, "Medium Priority" for amounts $200-$500, and "Low Priority" for amounts under $200.

What formula structure creates these three outcomes?

`@options1`
- [=IF(A2>500,"High",IF(A2>=200,"Medium","Low"))]
- `=IF(A2>500,"High",IF(A2>=200,"Medium"))`
- `=IF(A2>500,"High",AND(A2>=200,"Medium"))`
- `=OR(A2>500,"High",IF(A2<200,"Low"))`

---

## IF Combined AND

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to label orders as "Priority" only when the shipping mode is "Express" AND the order value exceeds $300. All other orders should be labeled "Standard".

Which formula achieves this?

`@options1`
- `=AND(IF(A2="Express",B2>300),"Priority","Standard")`
- `=IF(OR(A2="Express",B2>300),"Priority","Standard")`
- [=IF(AND(A2="Express",B2>300),"Priority","Standard")]
- `=IF(A2="Express",IF(B2>300,"Priority","Standard"))`

---

## Fixed Cell Reference

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're calculating commission rates where each row must compare sales to a benchmark value in cell H3. When you copy the formula down, you want H3 to remain fixed while other references change.

How do you fix the reference to cell H3?

`@options1`
- `=A2*H3`
- `=A2*H$3`
- `=$A2*H3`
- [=$H$3*A2]

---

## VLOOKUP Required Arguments

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to retrieve product names from a lookup table using product IDs. The VLOOKUP function requires specific arguments to locate and return values.

Which three arguments are required for VLOOKUP?

`@options1`
- lookup_value, table_array, range_lookup
- lookup_value, col_index_num, range_lookup
- [lookup_value, table_array, col_index_num]
- table_array, col_index_num, range_lookup

---

## Exact Match VLOOKUP

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're looking up customer names using customer IDs. You need an exact match because IDs are unique identifiers that must match precisely.

What value should the range_lookup parameter be set to for exact matches?

`@options1`
- TRUE
- 1
- [FALSE]
- 0

---

## Horizontal Lookup Function

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your data has years as column headers (2015, 2016, 2017) and product names as row headers. You need to find sales for a specific product in a specific year.

Which lookup function searches horizontally across rows?

`@options1`
- VLOOKUP
- XLOOKUP
- INDEX
- [HLOOKUP]

---

## Summarize Data PivotTable

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have a dataset with thousands of sales records. You need to quickly transform this raw data into a summary table showing total sales by region.

Which Excel feature creates dynamic summary tables from large datasets?

`@options1`
- Filter
- VLOOKUP
- [PivotTable]
- Sort

---

## PivotTable Aggregation Methods

```yaml
type: MultipleChoiceChallenge
key:
unit: data-preparation-in-excel
subskill: data-preparation
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
In a PivotTable, you've added the "Order Quantity" field to Values. By default, Excel sums these values, but you need to see the average quantity instead.

Where can you change the aggregation method from Sum to Average?

`@options1`
- Fields pane
- Filter menu
- Sort menu
- [Field Settings]
