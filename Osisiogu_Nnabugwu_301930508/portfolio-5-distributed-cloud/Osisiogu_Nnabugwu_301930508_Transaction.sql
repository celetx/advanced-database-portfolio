-- Related financial updates execute together on the writer, then replay on the standby.
BEGIN;
DO $$
BEGIN
    UPDATE ClinicAccounts SET Balance = Balance - 10000 WHERE AccountID = 1 AND Balance >= 10000;
    IF NOT FOUND THEN RAISE EXCEPTION 'Source account missing or insufficient balance'; END IF;
    UPDATE ClinicAccounts SET Balance = Balance + 10000 WHERE AccountID = 2;
    IF NOT FOUND THEN RAISE EXCEPTION 'Destination account missing'; END IF;
END $$;
COMMIT;
SELECT AccountID, AccountName, Balance FROM ClinicAccounts ORDER BY AccountID;
