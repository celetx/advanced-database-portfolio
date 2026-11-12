
-- MIT 8103 Advanced Database Systems
-- Portfolio 1: Database Constraint Testing
-- Case Study: MediCare Health Clinic

-- TEST 1: Primary Key Constraint
-- Attempt to insert a duplicate PatientID.

DO $$
BEGIN
    INSERT INTO Patients (PatientID, FullName, Gender)
    OVERRIDING SYSTEM VALUE
    VALUES (1, 'Duplicate Patient', 'Male');

    RAISE EXCEPTION 'TEST FAILED: Duplicate primary key accepted';

EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'TEST 1 PASSED: Duplicate primary key rejected';
END $$;


-- TEST 2: Foreign Key Constraint
-- Attempt to create appointment for nonexistent patient.

DO $$
BEGIN
    INSERT INTO Appointments
    (PatientID, ProviderID, AppointmentDate)
    VALUES (99999, 1, CURRENT_TIMESTAMP);

    RAISE EXCEPTION 'TEST FAILED: Invalid foreign key accepted';

EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE NOTICE 'TEST 2 PASSED: Invalid foreign key rejected';
END $$;


-- TEST 3: NOT NULL Constraint
-- Attempt to insert patient without a name.

DO $$
BEGIN
    INSERT INTO Patients (FullName, Gender)
    VALUES (NULL, 'Female');

    RAISE EXCEPTION 'TEST FAILED: NULL patient name accepted';

EXCEPTION
    WHEN not_null_violation THEN
        RAISE NOTICE 'TEST 3 PASSED: NULL patient name rejected';
END $$;


-- TEST 4: CHECK Constraint
-- Attempt to insert service with negative fee.

DO $$
BEGIN
    INSERT INTO MedicalServices
    (ServiceName, ServiceFee)
    VALUES ('Invalid Service', -500);

    RAISE EXCEPTION 'TEST FAILED: Negative service fee accepted';

EXCEPTION
    WHEN check_violation THEN
        RAISE NOTICE 'TEST 4 PASSED: Negative service fee rejected';
END $$;


-- TEST 5: UNIQUE Constraint
-- Attempt to insert duplicate medical service.

DO $$
BEGIN
    INSERT INTO MedicalServices
    (ServiceName, ServiceFee)
    VALUES ('General Consultation', 5000);

    RAISE EXCEPTION 'TEST FAILED: Duplicate service accepted';

EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'TEST 5 PASSED: Duplicate service rejected';
END $$;
