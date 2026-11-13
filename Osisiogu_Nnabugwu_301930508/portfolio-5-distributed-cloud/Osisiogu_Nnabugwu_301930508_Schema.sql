-- Portfolio 5 isolated copy of Portfolio 1 schema. Previous portfolios are untouched.

-- MIT 8103: Advanced Database Systems
-- Portfolio 1: Database Design and Modelling
-- Case Study: MediCare Health Clinic

-- Table 1: Patients
CREATE TABLE Patients (
    PatientID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    FullName VARCHAR(150) NOT NULL,
    Gender VARCHAR(20),
    Phone VARCHAR(20),
    RegistrationDate DATE DEFAULT CURRENT_DATE
);

-- Table 2: Providers
CREATE TABLE Providers (
    ProviderID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    FullName VARCHAR(150) NOT NULL,
    Speciality VARCHAR(100)
);

-- Table 3: Appointments
CREATE TABLE Appointments (
    AppointmentID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    PatientID INTEGER NOT NULL,
    ProviderID INTEGER NOT NULL,
    AppointmentDate TIMESTAMP NOT NULL,
    Status VARCHAR(20) DEFAULT 'Scheduled',

    CONSTRAINT fk_patient
        FOREIGN KEY (PatientID)
        REFERENCES Patients(PatientID),

    CONSTRAINT fk_provider
        FOREIGN KEY (ProviderID)
        REFERENCES Providers(ProviderID)
);


-- MIT 8103 Advanced Database Systems
-- Portfolio 1: Database Schema Extension
-- Case Study: MediCare Health Clinic

-- Table 4: Clinic Visits
CREATE TABLE ClinicVisits (
    VisitID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    PatientID INTEGER NOT NULL,
    ProviderID INTEGER NOT NULL,
    VisitDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    VisitStatus VARCHAR(30) NOT NULL DEFAULT 'Open',

    CONSTRAINT fk_visit_patient
        FOREIGN KEY (PatientID)
        REFERENCES Patients(PatientID),

    CONSTRAINT fk_visit_provider
        FOREIGN KEY (ProviderID)
        REFERENCES Providers(ProviderID),

    CONSTRAINT chk_visit_status
        CHECK (VisitStatus IN ('Open', 'Completed', 'Cancelled'))
);

-- Table 5: Medical Services
CREATE TABLE MedicalServices (
    ServiceID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ServiceName VARCHAR(150) NOT NULL UNIQUE,
    ServiceFee NUMERIC(12,2) NOT NULL,

    CONSTRAINT chk_service_fee
        CHECK (ServiceFee >= 0)
);

-- Table 6: Services Delivered During Visits
CREATE TABLE VisitServices (
    VisitServiceID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    VisitID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT fk_vs_visit
        FOREIGN KEY (VisitID)
        REFERENCES ClinicVisits(VisitID),

    CONSTRAINT fk_vs_service
        FOREIGN KEY (ServiceID)
        REFERENCES MedicalServices(ServiceID),

    CONSTRAINT chk_quantity
        CHECK (Quantity > 0)
);

-- Table 7: Payments
CREATE TABLE Payments (
    PaymentID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    VisitID INTEGER NOT NULL,
    Amount NUMERIC(12,2) NOT NULL,
    PaymentDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod VARCHAR(30) NOT NULL,
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'Pending',

    CONSTRAINT fk_payment_visit
        FOREIGN KEY (VisitID)
        REFERENCES ClinicVisits(VisitID),

    CONSTRAINT chk_payment_amount
        CHECK (Amount > 0),

    CONSTRAINT chk_payment_method
        CHECK (PaymentMethod IN ('Cash', 'Transfer', 'Card')),

    CONSTRAINT chk_payment_status
        CHECK (PaymentStatus IN ('Pending', 'Completed', 'Failed'))
);
