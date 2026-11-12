
-- MIT 8103 Advanced Database Systems
-- Portfolio 2: Query Performance Analysis
-- Case Study: MediCare Health Clinic

-- Update PostgreSQL statistics
ANALYZE Appointments;

-- Test 1: Appointment date filtering
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE AppointmentDate >= '2026-01-01'
  AND AppointmentDate < '2027-01-01';

-- Test 2: Patient appointment lookup
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Appointments
WHERE PatientID = 1;

-- Test 3: Payments lookup
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM Payments
WHERE PaymentStatus = 'Completed';
