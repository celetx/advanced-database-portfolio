
-- MIT 8103 Advanced Database Systems
-- Portfolio 3: ROLLBACK Demonstration
-- Case Study: MediCare Health Clinic

-- Display original balances
SELECT AccountID, AccountName, Balance
FROM ClinicAccounts
ORDER BY AccountID;

-- Begin transaction
BEGIN;

-- Attempt to deduct NGN 20,000
UPDATE ClinicAccounts
SET Balance = Balance - 20000
WHERE AccountID = 1;

-- Attempt to credit Laboratory Account
UPDATE ClinicAccounts
SET Balance = Balance + 20000
WHERE AccountID = 2;

-- Display temporary balances before rollback
SELECT AccountID, AccountName, Balance
FROM ClinicAccounts
ORDER BY AccountID;

-- Cancel all changes
ROLLBACK;

-- Verify balances after rollback
SELECT AccountID, AccountName, Balance
FROM ClinicAccounts
ORDER BY AccountID;

-- Verify total balance
SELECT SUM(Balance) AS TotalBalance
FROM ClinicAccounts;
