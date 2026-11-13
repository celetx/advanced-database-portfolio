-- Run only in the fresh medicare_portfolio5 teaching database.
CREATE TABLE ClinicBranches (
    BranchID INTEGER PRIMARY KEY,
    BranchName TEXT NOT NULL UNIQUE,
    City TEXT NOT NULL
);
INSERT INTO ClinicBranches VALUES
(1, 'MediCare Ikeja', 'Lagos'),
(2, 'MediCare Lekki', 'Lagos'),
(3, 'MediCare Abuja', 'Abuja');
ALTER TABLE ClinicVisits ADD COLUMN BranchID INTEGER REFERENCES ClinicBranches(BranchID);
UPDATE ClinicVisits SET BranchID = CASE VisitID WHEN 1 THEN 1 WHEN 2 THEN 2
    WHEN 3 THEN 1 WHEN 4 THEN 3 WHEN 5 THEN 2 END;
ALTER TABLE ClinicVisits ALTER COLUMN BranchID SET NOT NULL;
CREATE INDEX idx_visits_branch_date ON ClinicVisits (BranchID, VisitDate);
CREATE TABLE ClinicAccounts (
    AccountID INTEGER PRIMARY KEY,
    AccountName TEXT NOT NULL UNIQUE,
    Balance NUMERIC(12,2) NOT NULL CHECK (Balance >= 0)
);
INSERT INTO ClinicAccounts VALUES
(1, 'Main Clinic Account', 100000.00),
(2, 'Laboratory Account', 50000.00);
CREATE TABLE DistributionEvents (
    EventKey TEXT PRIMARY KEY,
    BranchID INTEGER NOT NULL REFERENCES ClinicBranches(BranchID),
    Note TEXT NOT NULL
);
