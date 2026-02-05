---
title: Excel Data Visualization Items 14-25
output: html_document
description: Multiple choice items covering Excel chart best practices and PivotCharts
---

## Avoiding 3D Charts

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A colleague has created a 3D column chart showing quarterly sales by region. When reviewing the visualization, you notice that some values are difficult to read accurately, and the perspective makes it challenging to compare regions.

What is the primary reason to avoid using 3D charts in data visualization?

`@options1`
- [They create perspective distortion that confuses interpretation]
- They require more processing power than 2D charts
- They cannot display multiple data series simultaneously
- They are incompatible with Excel's latest version features

---

## Y-Axis Starting Point

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're reviewing a line chart showing monthly revenue trends. The Y-axis starts at 45,000 instead of zero, making a 5% increase appear much more dramatic than it actually is.

What best practice should be followed for the Y-axis in this scenario?

`@options1`
- [Set the axis minimum to start at zero]
- Set the axis maximum to match the highest value
- Use logarithmic scaling to compress the range
- Remove the Y-axis labels entirely

---

## Strategic Color Usage

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A bar chart displays profit by product category, with each bar colored differently using a rainbow palette. The colors don't convey any meaningful information about the data.

What approach should be taken when using color in this chart?

`@options1`
- Apply red, amber, and green to indicate performance levels
- Use a different color for each category to improve readability
- [Apply uniform color or highlight only key data points]
- Match colors to company brand guidelines exactly

---

## Removing Chart Clutter

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A chart contains redundant elements: the axis title repeats information already in the chart title, the legend shows only one series, and gridlines overlap with data labels.

What principle should guide the removal of chart elements?

`@options1`
- Keep all elements to ensure maximum information density
- Remove elements based on personal design preferences
- [Evaluate whether each element contributes to understanding]
- Maintain all default Excel formatting options

---

## Dynamic Chart Titles

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want the chart title to automatically update when you change the text in cell B2, which contains a summary statement about the data.

How should you create a chart title that references this cell?

`@options1`
- Type the cell reference directly into the title text box
- Copy and paste the cell value into the title
- [Use a formula with an equal sign to reference the cell]
- Format the title to match the cell font style

---

## Formatting Axis Display Units

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A chart's Y-axis shows values like 50,000, 100,000, and 150,000, making the axis labels crowded and difficult to read.

What approach should be used to simplify these axis labels?

`@options1`
- Manually edit each label to remove trailing zeros
- [Change display units to thousands and format as "K"]
- Increase the font size of the axis labels
- Rotate the axis labels to a vertical orientation

---

## PivotCharts from Disaggregated Data

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have a dataset containing individual sales transactions with thousands of rows. Each row represents one order with details like date, product, region, and amount.

What is the most effective way to visualize insights from this disaggregated data?

`@options1`
- Create separate aggregated tables for each analysis view
- Insert a standard chart directly from raw transaction data
- [Use PivotCharts to dynamically aggregate and visualize data]
- Export the data to another tool for visualization

---

## PivotTable and PivotChart Relationship

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You modify a PivotTable by adding a new field to the rows, and notice that the associated PivotChart updates automatically to reflect this change.

What describes the relationship between PivotTables and PivotCharts?

`@options1`
- PivotCharts must be manually updated when tables change
- [PivotCharts are dynamically linked to underlying PivotTables]
- PivotTables are created automatically from chart selections
- Changes to one do not affect the other tables

---

## Adding Slicers to PivotCharts

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to add an interactive filter to a PivotChart that allows users to filter the visualization by product category.

What element should be added to enable this interactive filtering?

`@options1`
- [A slicer based on the Category field]
- A dropdown list in a separate worksheet cell
- A conditional formatting rule applied to the chart
- A data validation list linked to the chart

---

## Adding Timelines to PivotCharts

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to add a date-based filter to a PivotChart that allows users to select a time period using a visual calendar interface.

What interactive element should be added for date filtering?

`@options1`
- A slicer based on a date field formatted as text
- A manual date input cell with a formula reference
- A dropdown list containing all available date values
- [A timeline based on the date field in the PivotTable]

---

## Connecting Slicers to Multiple PivotTables

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A dashboard contains three PivotCharts, each based on a different PivotTable. You've added a slicer, but it only filters one of the charts.

How should the slicer be configured to filter all three visualizations?

`@options1`
- Create separate slicers for each PivotChart
- Copy the slicer three times and connect each to one chart
- Manually update each PivotTable when slicer changes
- [Use Report Connections to link slicer to all PivotTables]

---

## Print Configuration for Charts

```yaml
type: MultipleChoiceChallenge
key:
unit: data-visualization-in-excel
subskill: data-visualization
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to print a dashboard containing multiple charts arranged horizontally. The default print settings would split the dashboard across multiple pages.

What print configuration should be used to fit everything on one page?

`@options1`
- [Set orientation to landscape and use "Fit Sheet on One Page"]
- Set orientation to portrait and reduce chart sizes manually
- Print each chart separately and combine them afterward
- Export the charts as images and insert them into a document
