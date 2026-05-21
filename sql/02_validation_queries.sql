/*
02_validation_queries.sql

Purpose: Validate that the cleaned HIM deficiency dataset loaded correctly.
*/

-- Confirm table exists
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'him_deficiencies_cleaned';

-- Review table schema
SELECT
    column_name,
    data_type,
    character_maximum_length
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'him_deficiencies_cleaned'
ORDER BY ordinal_position;

-- Total row count
SELECT
    COUNT(*) AS total_rows
FROM dbo.him_deficiencies_cleaned;

-- Preview first 100 rows
SELECT TOP 100
    *
FROM dbo.him_deficiencies_cleaned;

-- Status distribution
SELECT
    status,
    COUNT(*) AS deficiency_count
FROM dbo.him_deficiencies_cleaned
GROUP BY status
ORDER BY deficiency_count DESC;

-- Provider risk distribution
SELECT
    provider_risk,
    count(*) AS deficiency_count
FROM dbo.him_deficiencies_cleaned
GROUP BY provider_risk
ORDER BY deficiency_count DESC;

-- Check date ranges
SELECT
    MIN(open_date) AS earliest_open_date,
    MAX(open_date) AS latest_open_date,
    MIN(completion_date) AS earliest_completion_date,
    MAX(completion_date) AS latest_completion_date
FROM dbo.him_deficiencies_cleaned;

-- Check missing completion dates by status
SELECT
    status,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN completion_date IS NULL THEN 1 ELSE 0 END) AS missing_completion_dates
FROM dbo.him_deficiencies_cleaned
GROUP BY status
ORDER BY status;