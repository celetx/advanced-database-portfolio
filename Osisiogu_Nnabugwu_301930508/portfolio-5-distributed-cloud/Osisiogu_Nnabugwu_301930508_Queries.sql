-- Valid on the primary and read-only standby; no data modification.
SELECT current_database() AS database_name, inet_server_port() AS server_port,
       pg_is_in_recovery() AS is_standby, current_setting('transaction_read_only') AS read_only;
SELECT b.BranchID, b.BranchName, COUNT(v.VisitID) AS visits
FROM ClinicBranches b LEFT JOIN ClinicVisits v USING (BranchID)
GROUP BY b.BranchID, b.BranchName ORDER BY b.BranchID;
SELECT b.BranchID, b.BranchName, SUM(p.Amount) AS completed_revenue_ngn
FROM ClinicBranches b JOIN ClinicVisits v USING (BranchID) JOIN Payments p USING (VisitID)
WHERE p.PaymentStatus = 'Completed'
GROUP BY b.BranchID, b.BranchName ORDER BY b.BranchID;
SELECT AccountID, AccountName, Balance FROM ClinicAccounts ORDER BY AccountID;
