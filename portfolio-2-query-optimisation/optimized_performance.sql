
-- MIT 8103 Advanced Database Systems
-- Portfolio 2: Optimised Query Performance

-- TEST 1: Appointment date filtering
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE AppointmentDate >= '2026-03-15'
  AND AppointmentDate < '2026-03-16';

-- TEST 2: Patient appointment lookup
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE PatientID = 1;
