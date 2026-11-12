
-- MIT 8103 Advanced Database Systems
-- Portfolio 2: Query Optimisation
-- Case Study: MediCare Health Clinic

-- Index 1: Optimise appointment date searches
CREATE INDEX IF NOT EXISTS idx_appointment_date
ON Appointments(AppointmentDate);

-- Index 2: Optimise patient appointment searches
CREATE INDEX IF NOT EXISTS idx_appointment_patient
ON Appointments(PatientID);

-- Update PostgreSQL statistics
ANALYZE Appointments;

-- Display indexes created
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'appointments'
ORDER BY indexname;
