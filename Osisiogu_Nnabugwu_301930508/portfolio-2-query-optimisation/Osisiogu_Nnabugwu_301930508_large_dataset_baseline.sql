
-- Portfolio 2: Large Dataset Baseline
-- Run BEFORE adding optimisation indexes.

ANALYZE Appointments;

-- TEST 1: Find appointments for a specific date
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE AppointmentDate >= '2026-03-15'
  AND AppointmentDate < '2026-03-16';

-- TEST 2: Find appointments for one patient
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE PatientID = 1;
