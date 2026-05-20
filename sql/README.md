# <img src="C:\Data-Analytics-Projects\him-deficiency-dashboard\images\sql-logo" alt="SQL logo"> SQL Workflow

**Purpose:**


The SQL scripts in this folder load, validate, and analyze the cleaned HIM deficiency dataset.

The SQL layer represents the transition from raw data processing to structured analytics workflows.

---

## &#128194; Files

### *01_create_tables.sql*

Purpose:

Create SQL Server tables for the HIM Deficiency Dashboard project.

Features:

- Defines table strcuture
- Assigns column data types
- Creates the cleaned HIM deficiency table

Run first.

---

### *02_validation_queries.sql*

Purpose:

Confirm that imported data loaded correctly.

Features:

- Row counts
- Status distribution
- Provider distributions
- Date validation checks
- Missing value checkes

Run second.

---

### *03_analytics_queries.sql*

Purpose:

Generate initial business metrics and KPIs

Features:

- Overall KPI calculations
- Deficiencies by department
- Provider performance summaries
- Deficiency type summaries
- Monthly trend analysis

Run third.

---

## Loading data into SQL Server

Current method:

1. Open SQL Server Management Studio

2. Right-click database

3. Select:

```text
Tasks
    → Import Flat File

4. Select:

```text
data/cleaned/him_deficiencies_cleaned.csv
```

5. Import into:

```text
dbo.him_deficiencies_cleaned
```

---

## SQL Workflow

```textRaw synthetic data
        ↓

Cleaned reporting dataset
        ↓

SQL table creation
        ↓

Validation queries
        ↓

Analytics queries
        ↓

Power BI dashboard
```

---

## &#128506; Notes

This project uses SQL Server and T-SQL syntax.

All data are synthetic and used for demonstration purposes only.