# 1.Database Normalisation (1NF, 2NF and 3NF)

Course: MIT 8103 – Advanced Database Systems
Portfolio: 1 – Database Design and Modelling
Case Study: MediCare Health Clinic
Database Management System: PostgreSQL

## 1. Introduction

Database normalization is basically about setting up tables so there is less repeated information and fewer issues when adding or changing records. The MediCare Health Clinic database manages patients and providers, as well as appointments, visits, and payments. It uses seven tables that connect to each other. 

## 2. First Normal Form(1NF)

Each table already has its own primary key, so records can be uniquely identified. Patient information sits in separate columns rather than mixed together, and appointments are kept as single records. Services provided during a visit are broken out into their own rows in the VisitServices table rather than being listed in a single location. That seems to cover the main parts of 1NF, though I am not totally sure if every possible repeating group was checked.

## 3. Second Normal Form (2NF)

All the tables rely on single-column keys like PatientID or VisitID, so there are no partial dependencies to worry about. In the Appointments table, the date and status clearly go with the appointment itself. The whole thing aligns with 2NF given how the keys are set up. 

## 4. Third Normal Form (3NF)

Moving to 3NF, the design keeps different kinds of information apart. Foreign keys reference patients and providers without duplicating names or specialties in every appointment row. The same idea applies to service details in VisitServices. It reduces duplication and makes updates easier to manage. The database design appears to satisfy Third Normal Form (3NF), based on the functional dependencies identified in the current schema. Further validation may be necessary as the database evolves

## 5. Benefits of Normalization

Reduced redundancy comes from storing patient and provider details once in their own tables. Integrity stays better because keys link everything correctly. Maintenance gets simpler because changes only need to be made in one place. Update problems are less likely when entities are separated. Extensibility improves, too, because new visits or payments can be added without copying old data. Some of these points overlap a bit, but they all add up in practice.

## 6. Conclusion

The database follows the first three normal forms by keeping values atomic and avoiding extra dependencies. Primary keys and foreign keys, along with other constraints, provide a solid foundation for the clinic records. It is not clear yet how this will hold up once real optimization work starts.
