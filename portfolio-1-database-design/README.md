
# Portfolio 1: Database Design and Modelling

**Course:** MIT 8103 - Advanced Database Systems

**Case Study:** MediCare Health Clinic

**Database Management System:** PostgreSQL

## 1. Overview

This portfolio presents the design and implementation of a
relational database for MediCare Health Clinic, a simulated
healthcare organisation.

The database is designed to manage patient information,
healthcare providers, appointments, clinical visits,
medical services, and payments.

The purpose is to demonstrate practical database design,
relational modelling, data integrity, and normalisation.

## 2. Database Users

The intended users include:

- Receptionists: Patient registration and appointments.
- Healthcare providers: Clinical visits and services.
- Finance officers: Payment records.
- Administrators: Database administration and reporting.

## 3. Database Tables

The PostgreSQL database contains seven related tables:

| Table | Description |
|---|---|
| Patients | Stores patient registration information |
| Providers | Stores healthcare provider information |
| Appointments | Manages appointment bookings |
| ClinicVisits | Records patient visits |
| MedicalServices | Stores available healthcare services |
| VisitServices | Records services delivered during visits |
| Payments | Records payments associated with visits |

## 4. Database Design

The database uses relational modelling principles.

Each table has a primary key to uniquely identify records.

Foreign keys establish relationships between tables
and help maintain referential integrity.

The database also includes constraints such as:

- PRIMARY KEY
- FOREIGN KEY
- NOT NULL
- UNIQUE
- CHECK

These constraints help prevent invalid or inconsistent data.

## 5. Entity Relationship Diagram

The database relationships are documented in:

[View ER Diagram](ER_Diagram.md)

## 6. Database Normalisation

The database was designed using the principles of
First Normal Form (1NF), Second Normal Form (2NF),
and Third Normal Form (3NF).

The normalisation process reduces data duplication,
improves consistency, and supports efficient maintenance.

[Read Normalisation Documentation](normalisation.md)

## 7. Implementation

PostgreSQL was configured using GitHub Codespaces.

The following SQL scripts were developed:

- `schema.sql`: Creates the initial three tables.
- `schema_extension.sql`: Creates four additional tables.
- `sample_data.sql`: Inserts fictional healthcare records.
- `constraint_tests.sql`: Tests database integrity constraints.

### Database Creation

Create the database:

```bash
sudo -n runuser -u postgres -- createdb medicare_clinic_db
```

Execute the SQL scripts in this order:

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-1-database-design/schema.sql

sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-1-database-design/schema_extension.sql

sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-1-database-design/sample_data.sql
```

These commands should be run from the repository root.
The scripts assume a newly created, empty database.

## 8. Database Testing

Database integrity was tested using PostgreSQL.

The following constraints were tested:

| Test | Expected Result |
|---|---|
| Duplicate primary key | Rejected |
| Invalid foreign key | Rejected |
| NULL patient name | Rejected |
| Negative service fee | Rejected |
| Duplicate medical service | Rejected |

All five constraint tests passed.

To reproduce the tests:

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-1-database-design/constraint_tests.sql
```

## 9. Practical Evidence

Screenshots of database operations and successful
constraint tests are stored in the `screenshots/` folder.

The repository also contains SQL scripts and the
ER diagram to support verification.

All patient records and transactions are fictional.

## 10. Conclusion

This portfolio demonstrates the practical design and
implementation of a relational healthcare database.

The database provides a structured foundation for
subsequent activities involving SQL query optimisation,
transactions, concurrency, NoSQL, and distributed databases.
