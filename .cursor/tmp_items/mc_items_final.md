---
title: Data Quality Concepts — Item Set
output: html_document
description: >-
  Ten MultipleChoiceChallenge items covering data quality definitions,
  dimensions, rules, metadata, lineage, remediation, monitoring, and thresholds.
---

## Definition of Data Quality

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team is evaluating whether their customer dataset meets the organization's data quality standards.

What does "data quality" measure?

`@options1`
- Whether the dataset uses the latest storage technology
- Whether the dataset follows the company's naming conventions
- [Whether the dataset is fit for its intended business use]
- Whether the dataset is stored in multiple backup locations

---

## Valid Values Check

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team maintains a customer table with an `AccountStatus` column. The business says the only allowed values are `Open`, `Closed`, or `Pending`.

A rule flags any record whose `AccountStatus` is not one of those values. Which data quality dimension is the rule measuring?

`@options1`
- Completeness
- Accuracy
- Timeliness
- [Validity]

---

## Rule Scope Choice

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
An analytics team receives a daily customer extract. They want to ensure the extract is complete before analysts use it.

Which rule is a dataset-level data quality rule?

`@options1`
- [A rule that compares source and loaded record counts]
- A rule that checks a column is populated on every row
- A rule that enforces allowed values in one column
- A rule that validates a date format in one column

---

## Profiling Limits

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A data profile shows that `CustomerAccountType` contains the values `Loan`, `Deposit`, `Loan and Deposit`, and `Credit Card`. A colleague proposes a validity rule that only allows these four values.

Why might business knowledge input still be needed before implementing this rule?

`@options1`
- A profile cannot detect whether a column contains text or numbers
- A profile cannot measure how many records have missing values
- [A profile shows current values but not whether they are all valid]
- A profile cannot identify duplicates in a primary key column

---

## Lineage for Triage

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A completeness rule flags missing values in a report column. The analyst confirms that the source table has no missing values, so the issue must have been introduced somewhere downstream.

What information would help the analyst identify where the issue was introduced?

`@options1`
- A catalog entry describing the column's business meaning
- A log showing who last modified the report definition
- A schedule showing when each table refresh job runs
- [A map of each transformation between source and report]

---

## Fix Location Choice

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A team finds an invalid `AccountStatus` value that appears on three downstream reports. They could either correct the value in the source table or add override logic to each report.

Why does best practice recommend correcting the issue near the source?

`@options1`
- It guarantees faster query performance on all reports
- It eliminates the need for any downstream validation
- [It avoids repeating the same fix in multiple places]
- It assigns ownership of the issue to the report team

---

## Prevent or Detect

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A bank discovers that 40% of rows in a daily extract have a missing value for `CurrentBalance`, a field used by multiple customer-facing processes. The data producer believes the issue is caused by a bad file transfer and can be corrected quickly.

What type of rule behavior fits this situation?

`@options1`
- Load the data and create a weekly quality summary
- [Stop the load and alert for rapid remediation]
- Load the data and only track the issue manually
- Stop the load and ignore the producer response

---

## Completing the Remediation

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A detective rule flags invalid customer birth dates. The data producer investigates and corrects the values in the source table. However, the same bad values still appear in reports the next morning.

What step was most likely missed?

`@options1`
- Notifying the data governance team of the correction
- Updating the rule to exclude the corrected records
- Documenting the root cause in the issue tracking log
- [Reloading the downstream tables that feed the reports]

---

## Monitoring at Scale

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A company has 500 tables used in customer decisioning models. Writing and maintaining explicit rules for every column is not practical, but the team still wants to catch unexpected changes.

Which approach addresses this challenge?

`@options1`
- Implement row-level audit triggers on each source table
- Deploy schema validation checks at the ingestion layer
- [Use anomaly detection to learn patterns and flag outliers]
- Run nightly checksums to verify table row counts match

---

## Critical Field Threshold

```yaml
type: MultipleChoiceChallenge
key:
unit: data-quality-concepts
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A bank classifies `CustomerID` as a critical field because missing values would break multiple downstream processes and regulatory reports.

According to best practice, what threshold should be set for a completeness rule on this field?

`@options1`
- 75%, with a warning sent to the producer for review
- 90%, with an alert and a one-week remediation window
- 95%, with data loaded while issues are being fixed
- [100%, with data blocked from loading until corrected]
