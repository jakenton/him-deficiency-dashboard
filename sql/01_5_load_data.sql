USE [him-deficiency-project];
GO

BULK INSERT dbo.him_deficiencies_cleaned
FROM 'C:\Data-Analytics-Projects\him-deficiency-dashboard\data\cleaned\him_deficiencies_cleaned.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n',
	TABLOCK
);
GO