
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
