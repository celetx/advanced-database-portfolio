
-- MIT 8103 Advanced Database Systems
-- Portfolio 1: Sample Data
-- Case Study: MediCare Health Clinic
-- All records are fictional.

BEGIN;

-- Insert Patients
INSERT INTO Patients
(FullName, Gender, Phone)
VALUES
('Ada Okeke', 'Female', '08000000001'),
('John Musa', 'Male', '08000000002'),
('Grace Bello', 'Female', '08000000003'),
('Samuel Ade', 'Male', '08000000004'),
('Fatima Ibrahim', 'Female', '08000000005');

-- Insert Healthcare Providers
INSERT INTO Providers
(FullName, Speciality)
VALUES
('Dr. James Okoro', 'General Medicine'),
('Dr. Amina Yusuf', 'Family Planning'),
('Dr. Peter Eze', 'Laboratory Medicine');

-- Insert Medical Services
INSERT INTO MedicalServices
(ServiceName, ServiceFee)
VALUES
('General Consultation', 5000),
('Family Planning Consultation', 3000),
('Blood Pressure Check', 1500),
('Laboratory Investigation', 7000),
('Follow-up Consultation', 2500);

-- Insert Appointments
INSERT INTO Appointments
(PatientID, ProviderID, AppointmentDate, Status)
VALUES
(1, 1, '2026-11-15 09:00:00', 'Scheduled'),
(2, 2, '2026-11-15 10:00:00', 'Scheduled'),
(3, 1, '2026-11-16 11:00:00', 'Scheduled'),
(4, 3, '2026-11-17 09:30:00', 'Scheduled'),
(5, 2, '2026-11-18 14:00:00', 'Scheduled');

-- Insert Clinic Visits
INSERT INTO ClinicVisits
(PatientID, ProviderID, VisitDate, VisitStatus)
VALUES
(1, 1, '2026-10-15 09:00:00', 'Completed'),
(2, 2, '2026-10-16 10:00:00', 'Completed'),
(3, 1, '2026-10-17 11:00:00', 'Completed'),
(4, 3, '2026-10-18 09:30:00', 'Completed'),
(5, 2, '2026-10-19 14:00:00', 'Completed');

-- Insert Services Provided
INSERT INTO VisitServices
(VisitID, ServiceID, Quantity)
VALUES
(1, 1, 1),
(1, 3, 1),
(2, 2, 1),
(3, 5, 1),
(4, 4, 1),
(5, 2, 1);

-- Insert Payments
INSERT INTO Payments
(VisitID, Amount, PaymentMethod, PaymentStatus)
VALUES
(1, 6500, 'Cash', 'Completed'),
(2, 3000, 'Transfer', 'Completed'),
(3, 2500, 'Card', 'Completed'),
(4, 7000, 'Transfer', 'Completed'),
(5, 3000, 'Cash', 'Completed');

COMMIT;
