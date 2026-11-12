
-- MIT 8103 Advanced Database Systems
-- Portfolio 3: Transactions and Concurrency
-- Case Study: MediCare Health Clinic
-- All financial records are fictional.

CREATE TABLE IF NOT EXISTS ClinicAccounts (
    AccountID INTEGER PRIMARY KEY,
    AccountName VARCHAR(100) NOT NULL UNIQUE,
    Balance NUMERIC(12,2) NOT NULL
        CHECK (Balance >= 0)
);

INSERT INTO ClinicAccounts
    (AccountID, AccountName, Balance)
VALUES
    (1, 'Main Clinic Account', 100000.00),
    (2, 'Laboratory Account', 50000.00)
ON CONFLICT (AccountID) DO NOTHING;

SELECT
    AccountID,
    AccountName,
    Balance
FROM ClinicAccounts
ORDER BY AccountID;
