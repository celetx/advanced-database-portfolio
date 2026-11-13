-- The runner observes these changes through a separate physical standby connection.
BEGIN;
INSERT INTO DistributionEvents VALUES ('replicated-insert', 2, 'Fictional branch registration event');
UPDATE Patients SET Phone = '08000000999' WHERE PatientID = 1;
COMMIT;
