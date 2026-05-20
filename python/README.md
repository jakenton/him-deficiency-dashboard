# <img src="C:\Data-Analytics-Projects\him-deficiency-dashboard\images\python-logo-only" alt="Python logo"> Python Workflow

**Purpose:**

The Python scripts in this folder generate and prepare synthetic healthcare Health Information Management (HIM) deficiency data for analysis.

The workflow is designed to simulate a realistic healthcare analytics pipeline while using fully synthetic data (no PHI or employer data).

---

## &#128194; Files

### *generate_synthetic_him_data.py*

Purpose:

Generate a raw synthetic HIM deficiency dataset.

Features:

- Creates synthetic patient encounters
- Generates provider metadata
- Simulates provider specialties and departments
- Applies provider risk levels
- Produces realistic deficiency types
- Creates operational fields such as:
    - status
    - aging buckets
    - completion timing
    - comments

Inputs:

None

Output:

```text
data/raw/him_deficiencies_raw.csv
```

How to run:

1. Open VSCode
2. Open the project folder
3. Activate the project virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

4. Opens:

```text
generate_synthetic_him_data.py
```

5. Run all cells

Expected result:

```text
Raw dataset generated successfully
```

---

### clean_him_deficiency_data.py

Purpose:

Load the raw synthetic dataset and prepare a reporting-ready dataset.

Features:

- Validates required columns
- Converts dates
- Creates reporting flags
- Generates trend fields
- Performs quality checks
- Creates provider summaries

Input:

```text
data/raw/him_deficiencies_raw.py
```

Output:

```text
data/cleaned/him_deficiencies_cleaned.py
```

How to run:

1. Open:

```text
clean_him_deficiency_data.py
```

2. Run all cells

Expected result:

```text
Cleaned dataset exported successfully
```

---

## Python Packages

Required libraries:

- pandas
- Faker
- Jupyter

Install:

```powershell
pip install pandas faker jupyter
```

---

## &#128506; Notes

All datasets are synthetic.

No protected health information (PHI) is used.