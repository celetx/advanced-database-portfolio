
-- MIT 8103 Advanced Database Systems
-- Portfolio 3: COMMIT Transaction Demonstration
-- Case Study: MediCare Health Clinic
-- Transaction: Transfer NGN 10,000
-- from Main Clinic to Laboratory.

-- Display balances before the transaction
SELECT AccountID, AccountName, Balance
FROM ClinicAccounts
ORDER BY AccountID;

-- Begin transaction
BEGIN;

-- Deduct NGN 10,000 from Main Clinic
UPDATE ClinicAccounts
SET Balance = Balance - 10000
WHERE AccountID = 1
  AND Balance >= 10000;

-- Add NGN 10,000 to Laboratory
UPDATE ClinicAccounts
SET Balance = Balance + 10000
WHERE AccountID = 2;

-- Permanently save changes
COMMIT;

-- Display balances after the transaction
SELECT AccountID, AccountName, Balance
FROM ClinicAccounts
ORDER BY AccountID;

-- Verify total balance is unchanged
SELECT SUM(Balance) AS TotalBalance
FROM ClinicAccounts;
