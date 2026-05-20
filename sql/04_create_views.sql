/*
04_create_views.sql

Purpose:
Create reporting views for Power BI and analytics consumption.
*/

--------------------------------------------------
-- Provider Performance View
--------------------------------------------------

CREATE OR ALTER VIEW dbo.vw_provider_performance
AS

SELECT

    provider_id,
    provider_name,
    provider_specialty,
    department_name,
    provider_risk,

    COUNT(*) AS total_deficiencies,

    SUM(
        CASE
            WHEN is_open = 1
            THEN 1
            ELSE 0
        END
    ) AS open_deficiencies,

    SUM(
        CASE
            WHEN is_suspended = 1
            THEN 1
            ELSE 0
        END
    ) AS suspended_deficiencies,

    AVG(
        CAST(days_open AS FLOAT)
    ) AS avg_days_open

FROM dbo.him_deficiencies_cleaned

GROUP BY

    provider_id,
    provider_name,
    provider_specialty,
    department_name,
    provider_risk;

GO

--------------------------------------------------
-- Monthly Trend View
--------------------------------------------------

CREATE OR ALTER VIEW dbo.vw_monthly_deficiency_trends
AS

SELECT

    open_month,

    COUNT(*) AS deficiencies_opened,

    SUM(
        CASE
            WHEN is_completed = 1
            THEN 1
            ELSE 0
        END
    ) AS deficiencies_completed

FROM dbo.him_deficiencies_cleaned

GROUP BY open_month;

GO

--------------------------------------------------
-- Department Summary View
--------------------------------------------------

CREATE OR ALTER VIEW dbo.vw_department_summary
AS

SELECT

    department_name,

    COUNT(*) AS total_deficiencies,

    SUM(
        CASE
            WHEN is_open - 1
            THEN 1
            ELSE 0
        END
    ) AS open_deficiencies,

    AVG(
        CAST(days_open AS FLOAT)
    ) AS avg_days_open

FROM dbo.him_deficiencies_cleaned

GROUP BY department_name;

GO