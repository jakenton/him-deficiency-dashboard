USE [him-deficiency-project];
GO

TRUNCATE TABLE dbo.him_deficiencies_cleaned;
GO

BULK INSERT dbo.him_deficiencies_cleaned
FROM 'C:\Data-Analytics-Projects\him-deficiency-dashboard\data\cleaned\him_deficiencies_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);
GO