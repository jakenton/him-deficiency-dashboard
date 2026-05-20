# &#128211; HIM Deficiency Dashboard Project

## &#128506; Project Overview

**Purpose:**
Simulate a healthcare Health Information Management (HIM) deficiency tracking workflow using synthetic data to demonstrate data generation, validation, SQL analysis, and dashboard reporting.

This project contains no PHI and uses entirely synthetic data.

--

## &#128269; Business Problem

Hospitals monitor incomplete clinical documentation to support:

- medical record completeness
- provider compliance
- regulatory requirements
- delinquency tacking
- operational performance

Manual workflows often involve spreadsheets and repeated review processes.

This project simulates a more structured analytics workflow.

---

## &#128187; Technology Stack

Python
- pandas
- Faker

SQL Server
- T-SQL

Power BI
- Dashboard visualization

Git/GitHub
- Version control

---

## &#128640; Project Pipeline

```text
Synthetic Dataset Generation
        ↓
Data Cleaning / Validation
        ↓
SQL Loading / Staging
        ↓
Analytics Queries
        ↓
Power BI Dashboard
```

## &#128295; Current Features

&#10003; Synthetic provider metadata
&#10003; Department-specific deficiency logic
&#10003; Risk-based provider behavior
&#10003; Cleaning and validation pipeline
&#10003; Reporting flags
&#10003; SQL starter queries

---

## &#128198; Planned Features

- [ ] SQL staging workflow
- [ ] Power BI dashboard
- [ ] Provider performance metrics
- [ ] Aging analysis
- [ ] Monthly trends
- [ ] Documentation compliance KPIs

---

## &#127970; Repository Structure

```text
him-deficiency-dashboard/

├── README.md
├── data/
│   ├── raw/
│   │   └── him_deficiencies_raw.csv
│   │
│   └── cleaned/
│       └── him_deficiencies_cleaned.csv
│
├── python/
│   ├── README.md
│   ├── generate_synthetic_him_data.py
│   └── clean_him_deficiency_data.py
│
├── sql/
│   ├── README.md
│   ├── 01_create_tables.sql
│   ├── 02_validation_queries.sql
│   └── 03_analytics_queries.sql
│
└── docs/
    ├── data_dictionary.md
    ├── build_guide.md
    └── assumptions_and_limitations.md
```

---

## &#128506; Notes

All data are simulated and intended only for demonstration and educational purposes.