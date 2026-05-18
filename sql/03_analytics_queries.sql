/*
03_analytics_queries.sql

Purpose:
Create starter analytics queries for the HIM Deficiency Dashboard project.
*/

-- Overall KPI summary
SELECT
    COUNT(*) AS total_deficiencies,
    SUM(CASE WHEN is_open = 1 THEN 1 ELSE 0 END) AS open_deficiencies,
    SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS completed_deficiencies,
    SUM(CASE WHEN is_suspended = 1 THEN 1 ELSE 0 END) AS suspended_deficiencies,
    SUM(CASE WHEN is_over_30_days = 1 THEN 1 ELSE 0 END) AS deficiencies_over_30_days,
    AVG(CAST(days_open AS FLOAT)) AS avg_days_open
FROM dbo.him_deficiencies_cleanedñ

-- Deficiencies by department
SELECT
    department_name,
    COUNT(*) AS total_deficiencies,
    SUM(CASE WHEN is_open = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN is_over_30_days = 1 THEN 1 ELSE 0 END) AS is_over_30_days
FROM dbo.him_deficiencies_cleaned
GROUP BY department name
ORDER BY total_deficiencies DESC;

-- Deficiencies by provider
SELECT
    provider_id,
    provider_name,
    provider_specialty,
    department_name,
    provider_risk,
    COUNT(*) AS total_deficiencies,
    SUM(CASE WHEN is_open = 1 THEN 1 ELSE 0 END) AS open_deficiencies,
    SUM(CASE WHEN is_suspended = 1 THEN 1 ELSE 0 END) AS suspended_deficiencies,
    AVG(CAST(days_open AS FLOAT)) AS avg_days_open
FROM dbo.him_deficiencies_cleaned
GROUP BY
    provider_id,
    provider_name,
    provider_specialty,
    department_name,
    provider_risk
ORDER BY total_deficiencies DESC;

-- Deficiency type summary
SELECT
    deficiency_type,
    COUNT(*) AS total_deficiencies,
    SUM(CASE WHEN is_open = 1 THEN 1 ELSE 0 END) AS open_deficiencies,
    AVG(CAST(days_open AS FLOAT)) AS avg_days_open
FROM dbo.him_deficiencies_cleaned
GROUP BY deficiency_type
ORDER BY total_deficiencies DESC;

-- Monthly opening trend
SELECT
    open_month,
    COUNT(*) AS deficiencies_opened
FROM dbo.him_deficiencies_cleaned
GROUP BY open_month
ORDER BY open_monthñ

-- Monthly completion trend
SELECT
    completion_month,
    COUNT(*) AS deficiencies_completed
FROM dbo.him_deficiencies_cleaned
WHERE completion_month IS NOT NULL
GROUP BY completion_month
ORDER BY completion_monthñ