"""
generate_synthetic_him_data.py

Purpose: Generate a fully synthetic HIM deficiency dataset for a healthcare analytics portfolio project.

This dataset does NOT contain real patient data, employer data, Epic data, or PHI. It is designed only to simulate realistic hospital HIM deficiency tracking workflows.
"""

# %%
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

# %%
# -----------------------------
# Basic setup
# -----------------------------

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_ROWS = 1000

OUTPUT_PATH = "../data/raw/him_deficiencies_raw.csv"

# %%
# -----------------------------
# Reference values
# -----------------------------

providers = [
    {
        "provider_id": "1598463",
        "provider_name": "SMITH,JOHN",
        "provider_type": "MD",
        "specialty": "GENERAL SURGERY",
        "home_department": "SURGERY",
        "deficiency_risk": "HIGH",
    },
    {
        "provider_id": "1594984",
        "provider_name": "PATEL,MAYA",
        "provider_type": "DO",
        "specialty": "CARDIOLOGY",
        "home_department": "CARDIOLOGY",
        "deficiency_risk": "LOW",
    },
    {
        "provider_id": "1591652",
        "provider_name": "GARCIA,BRITTANY",
        "provider_type": "PA",
        "specialty": "EMERGENCY MEDICINE",
        "home_department": "SURGERY",
        "deficiency_risk": "MEDIUM",
    },
    {
        "provider_id": "1591234",
        "provider_name": "JOHNSON,EMILY",
        "provider_type": "CNM",
        "specialty": "OBGYN",
        "home_department": "OBSTETRICS/GYNECOLOGY",
        "deficiency_risk": "MEDIUM",
    },
    {
        "provider_id": "1598498",
        "provider_name": "NG,DAVID",
        "provider_type": "MD",
        "specialty": "ORTHOPEDICS",
        "home_department": "ORTHOPEDICS",
        "deficiency_risk": "HIGH",
    },
    {
        "provider_id": "1596443",
        "provider_name": "MARTINEZ,SOFIA",
        "provider_type": "MD",
        "specialty": "PSYCHIATRY",
        "home_department": "BEHAVIORAL HEALTH",
        "deficiency_risk": "LOW",
    },
    {
        "provider_id": "1597165",
        "provider_name": "BROWN,JAMES",
        "provider_type": "PA",
        "specialty": "OBGYN",
        "home_department": "OBSTETRICS/GYNECOLOGY",
        "deficiency_risk": "LOW",
    },
    {
        "provider_id": "1592314",
        "provider_name": "LEE,GRACE",
        "provider_type": "MD",
        "specialty": "GENERAL SURGERY",
        "home_department": "SURGERY",
        "deficiency_risk": "MEDIUM",
    },
    {
        "provider_id": "1590961",
        "provider_name": "WILSON,MICHAEL",
        "provider_type": "MD",
        "specialty": "ORTHOPEDICS",
        "home_department": "ORTHOPEDICS",
        "deficiency_risk": "MEDIUM",
    },
    {
        "provider_id": "1590354",
        "provider_name": "ANDERSON,SARA",
        "provider_type": "MD",
        "specialty": "PSYCHIATRY",
        "home_department": "BEHAVIORAL HEALTH",
        "deficiency_risk": "LOW",
    },

]

facilities = [
    "Central Valley Medical Center",
    "North Hills Hospital",
    "Rio Grande Regional",
    "Sunrise Community Hospital",
    "Desert Peaks Medical Center",
]

deficiency_types_by_department = {
    "SURGERY": [
        "History & Physical",
        "Operative Note",
        "Procedure Documentation",
        "Discharge Summary",
    ],
    "CARDIOLOGY": [
        "Progress Note",
        "Consult Note",
        "History & Physical",
        "Discharge Note",
    ],
    "OBSTETRICS/GYNECOLOGY": [
        "History & Physical",
        "OB Triage Note",
        "Progress Note",
        "Discharge Summary",
    ],
    "ORTHOPEDICS": [
        "Operative Note",
        "Procedure Documentation",
        "Progress Note",
        "Discharge Summary",
    ],
    "BEHAVIORAL HEALTH": [
        "History & Physical",
        "Progress Note",
        "Consult Note",
        "Discharge Summary",
    ],
}

statuses = ["Completed", "Open", "Suspended"]

# %%
# -----------------------------
# Helper functions
# -----------------------------

def assign_aging_bucket(days_open):
    """
    Assign a simple aging bucket based on how long the deficiency has been open.
    This will later support dashboard visuals and SQL CASE logic.
    """
    if days_open <= 7:
        return "0-7 days"
    elif days_open <= 30:
        return "8-30 days"
    else:
        return ">30 days"
    
def generate_status(provider_risk):
    """
    Generate deficiency status using provider risk.

    The statuses list is defined in the reference values section so that status categories have a single source of truth.
    """
    if provider_risk == "HIGH":
        weights = [0.45, 0.40, 0.15]

    elif provider_risk == "MEDIUM":
        weights = [0.60, 0.30, .10]

    else:
        weights = [0.75, 0.20, 0.05]

    return random.choices(
        statuses,
        weights=weights,
        k=1
    )[0]

def generate_completion_days(provider_risk):
    """
    Generate completion timing.
    
    Higher-risk providers tend to complete deficiencies more slowly.
    """

    if provider_risk == "HIGH":
        return random.randint(10, 60)
    
    if provider_risk == "MEDIUM":
        return random.randint(5, 45)
    
    return random.randint(1,25)
    
def generate_comment(status, reassigned_flag, coding_hold_flag):
    """Generate comments that loosely aligh with operational status."""

    if status == "Suspended":
        return "Provider suspended pending completion"
    
    if reassigned_flag == "Y":
        return "Reassigned to covering provider"
    
    if coding_hold_flag == "Y":
        return "Coding review in progress"
    
    if status == "Completed":
        return "Completed by provider"
    
    return random.choice([
        "Awaiting provider signature",
        "Incomplete documentation",
        "Escalated to department leadership",
        "Pending review by HIM analyst",
        "Provider not currently due",
    ])

# %%
# -----------------------------
# Generate synthetic rows
# -----------------------------

rows = []

for i in range(1, NUM_ROWS + 1):
    deficiency_id = f"{i:06d}"
    patient_encounter_id = f"{random.randint(10000, 9999999)}"
    mrn = f"{random.randint(10000, 9999999)}"

    patient_name = (
        f"{fake.last_name()},"
        f"{fake.first_name()}"
    ).upper()

    facility_name = random.choice(facilities)

    provider = random.choice(providers)

    provider_id = provider["provider_id"]
    provider_name = provider["provider_name"]
    provider_type = provider["provider_types"]
    provider_specialty = provider["specialty"]
    department_name = provider["home_department"]
    provider_risk = provider["deficiency_risk"]

    deficiency_type = random.choice(
        deficiency_types_by_department[department_name]
    )
    
    status = generate_status(provider_risk)

    priority_flag = random.choices(
        ["Normal", "High"],
        weights=[0.85, 0.15],
        k=1
    )[0]

    # Open dates are within the last 180 days.
    open_date = datetime.today() - timedelta(
        days=random.randint(0, 180)
        )

    # Delinquency date is usually 14-30 days after opening.
    delinquency_date = open_date + timedelta(
        days=random.randint(14, 30)
        )

    if status == "Completed":
        completion_days = generate_completion_days(provider_risk)
        completion_date = open_date + timedelta(days=completion_days)
        days_open = completion_days
    
    else:
        completion_date = None
        days_open = (datetime.today() - open_date).days

    aging_bucket = assign_aging_bucket(days_open)

    reassigned_flag = random.choices(
        ["Y", "N"],
        weights=[0.12, 0.88],
        k=1
    )[0]

    coding_hold_flag = random.choices(
        ["Y", "N"],
        weights=[0.10, 0.90],
        k=1
    )[0]

    comment = generate_comment(
        status=status,
        reassigned_flag=reassigned_flag,
        coding_hold_flag=coding_hold_flag,
    )

    rows.append({
        "deficiency_id": deficiency_id,
        "patient_encounter_id": patient_encounter_id,
        "mrn": mrn,
        "patient_name": patient_name,
        "facility_name": facility_name,
        "department_name": department_name,
        "provider_id": provider_id,
        "provider_name": provider_name,
        "provider_type": provider_type,
        "provider_specialty": provider_specialty,
        "provider_risk": provider_risk,
        "deficiency_type": deficiency_type,
        "priority_flag": priority_flag,
        "open_date": open_date,
        "delinquency_date": delinquency_date.date(),
        "completion_date": (
            completion_date.date()
            if completion_date
            else None,
        )
        "status": status,
        "reassigned_flag": reassigned_flag,
        "coding_hold_flag": coding_hold_flag,
        "days_open": days_open,
        "aging_bucket": aging_bucket,
        "comments": comment,
    })

# %%
# -----------------------------
# Create dataframe
# -----------------------------

df = pd.DataFrame(rows)

print("Dataset created successfully!")

print(f"\nTotal rows: {len(df)}")
      
# %%
# -----------------------------
# Preview the dataframe
# -----------------------------

df.head()

# %%
# -----------------------------
# Quick validation checks
# -----------------------------

print("Status distribution:")
print(df["status"].value_counts())

print("\nProvider risk distribution:")
print(df["provider_risk"].value_counts())

print("\nDepartment distribution:")
print(df["department_name"].value_counts())

print("\nDeficiency type distribution:")
print(df["deficiency_type"].value_counts())

print("\nMissing values by column:")
print(df.isna().sum())

# %%
# -----------------------------
# Provider-level QA Check
# -----------------------------

provider_summary = (
    df.groupby([
        "provider_id",
        "provider_name",
        "provider_specialty",
        "department_name",
        "provider_risk",
    ])
    .agg(
        total_deficiencies=("deficiency_id", "count"),
        open_deficiencies=("status", lambda x: (x == "Open").sum()),
        suspended_deficiencies=("status", lambda x: (x == "Suspended").sum()),
        avg_days_open=("days_open", "mean"),
    )
)

provider_summary

# %%
# -----------------------------
# Export dataset to CSV
# -----------------------------

df.to_csv(OUTPUT_PATH, index=False)

print(f"CSV exported successfully!")

print(f"\nOutput location: {OUTPUT_PATH}")