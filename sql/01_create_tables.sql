/*
01_create_tables.sql

Purpose: Create the main SQL table for the cleaned synthetics HIM deficiency dataset.

This table is designed for SQL Server / T-SQL.
*/

DROP TABLE IF EXISTS dbo.him_deficiencies_cleaned;
GO

CREATE TABLE dbo.him_deficiencies_cleaned (
    deficiency_id VARCHAR(20),
    patient_encounter_id VARCHAR(20),
    mrn VARCHAR(20),
    patient_name VARCHAR(100),
    facility_name VARCHAR(100),
    department_name VARCHAR (100),

    provider_id VARCHAR(20),
    provider_name VARCHAR(100),
    provider_type VARCHAR(20),
    provider_specialty VARCHAR(100),
    provider_risk VARCHAR(20),

    deficiency_type VARCHAR(100),
    priority_flag VARCHAR(20),

    open_date DATE,
    delinquency_date DATE,
    completion_date DATE,

    status VARCHAR(30),
    reassigned_flag CHAR(1),
    coding_hold_flag(1),

    days_open INT,
    aging_bucket VARCHAR(30),
    comments VARCHAR(255),

    is_open BIT,
    is_completed BIT,
    is_suspended BIT,
    is_over_30_days BIT,
    is_past_delinquency_date BIT,
    has_reassignment BIT,
    has_coding_hold BIT,

    open_month VARCHAR(7),
    completion_month VARCHAR(7)
);
GO