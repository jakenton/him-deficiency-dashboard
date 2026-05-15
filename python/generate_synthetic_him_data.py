# %%
"""
generate_synthetic_him_data.py

Purpose: Generate a fully synthetic HIM deficiency dataset for a healthcare analytics portfolio project.

This dataset does NOT contain real patient data, employer data, Epic data, or PHI. It is designed only to simulate realistic hospital HIM deficiency tracking workflows.
"""

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

facilities = [
    "Central Valley Medical Center",
    "North Hills Hospital",
    "Rio Grande Regional",
    "Sunrise Community Hospital",
    "Desert Peaks Medical Center",
]

departments = [
    "Emergency Department",
    "Surgery",
    "ICU",
    "Telemetry",
    "Behavioral Health",
    "Women's Services",
    "Cardiology",
    "Orthopedics",
    "Medical/Surgical",
    "Observation",
]

deficiency_types = [
    "History & Physical",
    "Operative Note",
    "Discharge Summary",
    "Progress Note",
    "Verbal Order Authentication",
    "Procedure Documentation",
    "Consult Note",
    "Pathology",
    "ED Provider",
    "Transfer Summary",
]

provider_types = ["MD", "DO", "NP", "PA"]

statuses = ["Completed", "Open", "Suspended"]

comments = [
    "Awaiting provider signature",
    "Provider suspended pending completion",
    "Reassigned to covering provider",
    "Coding review in progress",
    "Incomplete operative note",
    "Provider not currently due",
    "No provider assigned",
    "Completed by provider",
    "Escalated to department leadership",
    "Pending review by HIM analyst",
]

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
    
def generate_status():
    """
    Create a realistic status distribution:
    - Most deficiencies are completed
    - Some remain open
    - A smaller number are suspended
    """
    return random.choices(
        statuses,
        weights=[0.60, 0.30, 0.10],
        k=1
    )[0]

# %%
# -----------------------------
# Generate synthetic rows
# -----------------------------

rows = []

for i in range(1, NUM_ROWS + 1):
    deficiency_id = f"DFI{i:06d}"
    patient_encounter_id = f"ENC{random.randint(1000000, 9999999)}"
    mrn = f"MRN{random.randint(100000, 999999)}"

    patient_name = fake.name()

    facility_name = random.choice(facilities)

    # Weight departments so some areas naturally generate more deficiencies.
    department_name = random.choices(
        departments,
        weights=[18, 16, 12, 8, 6, 8, 8, 8, 12, 4],
        k=1
    )[0]

    provider_name = f"Dr. {fake.last_name()}"
    provider_type = random.choice(provider_types)

    deficiency_type = random.choices(
        deficiency_types,
        weights=[14, 16, 18, 10, 12, 8, 6, 5, 8, 3],
        k=1
    )[0]

    status = generate_status()

    priority_flag = random.choices(
        ["Normal", "High"],
        weights=[0.85, 0.15],
        k=1
    )[0]

    # Open dates are within the last 180 days.
    open_date = datetime.today() - timedelta(days=random.randint(0, 180))

    # Delinquency date is usually 14-30 days after opening.
    delinquency_date = open_date + timedelta(days=random.randint(14, 30))

    if status == "Completed":
        completion_date = open_date + timedelta(days=random.randint(1, 45))
        days_open = (completion_date - open_date).days
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

    comment = random.choice(comments)

    rows.append({
        "deficiency_id": deficiency_id,
        "patient_encounter_id": patient_encounter_id,
        "mrn": mrn,
        "patient_name": patient_name,
        "facility_name": facility_name,
        "department_name": department_name,
        "provider_name": provider_name,
        "provider_type": provider_type,
        "deficiency_type": deficiency_type,
        "priority_flag": priority_flag,
        "open_date": open_date,
        "delinquency_date": delinquency_date.date(),
        "completion_date": completion_date.date() if completion_date else None,
        "status": status,
        "reassigned_flag": reassigned_flag,
        "coding_hold_flag": coding_hold_flag,
        "days_open": days_open,
        "aging_bucket": aging_bucket,
        "comments": comment
    })

# %%
# -----------------------------
# Create dataframe
# -----------------------------

df = pd.DataFrame(rows)

print("Dataset created successfully!")

print(f"\nTotal rows": {len(df)}")
      
# %%
# -----------------------------
# Preview the dataframe
# -----------------------------

df.head()

# %%
# -----------------------------
# Quick validation checks
# -----------------------------

print("\nStatus distribution:")
print(df["status"].value_counts())

print("\nDepartment distribution:")
print(df["department_name"].value_counts())

# %%
# -----------------------------
# Export dataset to CSV
# -----------------------------

df.to_csv(OUTPUT_PATH, index=False)

print(f"\nCSV exported successfully!")

print(f"\nOutput location:")
print(OUTPUT_PATH)