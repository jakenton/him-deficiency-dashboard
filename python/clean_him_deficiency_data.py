"""
clean_him_deficiency_data.py

Purpose: Load the raw synthetic HIM deficiency dataset, perform basic validation, create repoting-ready flags, and export a clean CSV.

Input:
../data/raw/him_deficiencies_raw.csv

Output:
../data/cleaned/him_deficiences_cleaned.csv
"""

# %%
# -----------------------------------
# Import libraries
# -----------------------------------

import pandas as pd

# %%
# -----------------------------------
# File paths
# -----------------------------------

RAW_PATH = "../data/raw/him_deficiencies_raw.csv"
CLEANED_PATH = "../data/cleaned/him_deficiencies_cleaned.csv"

# %%
# -----------------------------------
# Load raw dataset
# -----------------------------------

df = pd.read_csv(RAW_PATH)

print("Raw dataset loaded successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

# %%
# -----------------------------------
# Preview data
# -----------------------------------

df.head()

# %%
# -----------------------------------
# Confirm expected columns exist
# -----------------------------------

required_columns = [
    "deficiency_id",
    "patient_encounter_id",
    "mrn",
    "patient_name",
    "facility_name",
    "department_name",
    "provider_name",
    "provider_type",
    "provider_specialty",
    "provider_risk",
    "deficiency_type",
    "priority_flag",
    "open_date",
    "delinquency_date",
    "completion_date",
    "status",
    "reassigned_flag",
    "coding_hold_flag",
    "days_open",
    "aging_bucket",
    "comments",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("Missing required columns:")
    print(missing_columns)
else:
    print("All required columns are present.")

# %%
# -----------------------------------
# Convert date columns
# -----------------------------------

date_columns = [
    "open_date",
    "delinquency_date",
    "completion_date",
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )

print("Date columns converted.")

# %%
# -----------------------------------
# Validate expected category values
# -----------------------------------

expected_statuses = [
    "Completed",
    "Open",
    "Suspended",
]

expected_provider_risks = [
    "HIGH",
    "MEDIUM",
    "LOW",
]

unexpected_statuses = sorted(
    set(df["status"].dropna()) - set(expected_statuses)
)

unexpected_provider_risks = sorted(
    set(df["provider_risk"].dropna()) - set(expected_provider_risks)
)

print("Unexpected statuses:")
print(unexpected_statuses)

print("\nUnexpected provider risk values:")
print(unexpected_provider_risks)

# %%
# -----------------------------------
# Create reporting flags
# -----------------------------------

df["is_open"] = df["status"].isin([
    "Open",
    "Suspended",
])

df["is_completed"] = df["status"] == "Completed"

df["is_suspended"] = df["status"] == "Suspended"

df["is_over_30_days"] = df["days_open"] > 30

df["is_past_delinquency_date"] = (
    df["completion_date"].isna()
    & (pd.Timestamp.today().normalize() > df["delinquency_date"])
)

df["has_reassignment"] = df["reassigned_flag"] == "Y"

df["has_coding_hold"] = df["coding_hold_flag"] == "Y"

# %%
# -----------------------------------
# Add month fields for trending
# -----------------------------------

df["open_month"] = df["open_date"].dt.to_period("M").astype(str)

df["completion_month"] = df["completion_date"].dt.to_period("M").astype(str)

# %%
# -----------------------------------
# Basic data quality summary
# -----------------------------------

print("Missing values by column:")
print(df.isna().sum())

print("\nStatus distribution:")
print(df["status"].value_counts())

print("\nAging bucket distribution:")
print(df["aging_bucket"].value_counts())

print("\nOpen deficiency count:")
print(df["is_open"].sum())

print("\nOver 30 days count:")
print(df["is_over_30_days"].sum())

# %%
# -----------------------------------
# Provider-level validation sumamry
# -----------------------------------

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
        open_deficiencies=("is_open", "sum"),
        completed_deficiencies=("is_completed", "sum"),
        suspended_deficiencies=("is_suspended", "sum"),
        over_30_days=("is_over_30_days", "sum"),
        avg_days_open=("days_open", "mean"),
    )
    .reset_index()
    .sort_values(
        by="total_deficiencies",
        ascending=False
    )
)

provider_summary

# %%
# -----------------------------
# Check current working directory
# -----------------------------

import os

print("Current working directory:")
print(os.getcwd())

print("\nCleaned output path:")
print(CLEANED_PATH)

# %%
# -----------------------------
#Convert boolean reporting flags to 1/0 for SQL Server BIT columns
# -----------------------------

flag_columns = [
    "is_open",
    "is_completed",
    "is_suspended",
    "is_over_30_days",
    "is_past_delinquency_date",
    "has_reassignment",
    "has_coding_hold",
]

for column in flag_columns:
    df[column] = df[column].astype(int)

# %%
# -----------------------------------
# Exported cleaned dataset
# -----------------------------------

df.to_csv(CLEANED_PATH, index=False)

print("Cleaned dataset exported successfully!")
print(f"Output location: {CLEANED_PATH}")
# %%
