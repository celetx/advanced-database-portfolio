
-- MIT 8103 Advanced Database Systems
-- Portfolio 2: Generate Performance Test Data
-- Case Study: MediCare Health Clinic
-- All generated records are fictional.

BEGIN;

-- STEP 1: Generate 2,000 additional patients
INSERT INTO Patients (FullName, Gender, Phone)
SELECT
    'Load Test Patient ' || n,
    CASE WHEN n % 2 = 0 THEN 'Female' ELSE 'Male' END,
    'TEST-' || LPAD(n::TEXT, 6, '0')
FROM generate_series(1, 2000) AS n;

-- STEP 2: Generate 100,000 appointments
-- Reference actual existing patient and provider IDs.
WITH patient_ids AS (
    SELECT ARRAY_AGG(PatientID ORDER BY PatientID) AS ids
    FROM Patients
),
provider_ids AS (
    SELECT ARRAY_AGG(ProviderID ORDER BY ProviderID) AS ids
    FROM Providers
)
INSERT INTO Appointments
    (PatientID, ProviderID, AppointmentDate, Status)
SELECT
    p.ids[1 + (n % CARDINALITY(p.ids))],
    pr.ids[1 + (n % CARDINALITY(pr.ids))],
    TIMESTAMP '2025-01-01'
        + (n % 730) * INTERVAL '1 day'
        + (n % 24) * INTERVAL '1 hour',
    CASE
        WHEN n % 4 = 0 THEN 'Completed'
        WHEN n % 4 = 1 THEN 'Scheduled'
        WHEN n % 4 = 2 THEN 'Cancelled'
        ELSE 'Pending'
    END
FROM generate_series(1, 100000) AS n
CROSS JOIN patient_ids p
CROSS JOIN provider_ids pr;

COMMIT;

-- Refresh PostgreSQL statistics
ANALYZE Patients;
ANALYZE Appointments;

-- Verify the number of records
SELECT COUNT(*) AS TotalPatients FROM Patients;
SELECT COUNT(*) AS TotalAppointments FROM Appointments;
