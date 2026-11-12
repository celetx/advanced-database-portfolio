# Portfolio 2: Query Processing and Optimisation

**Course:** MIT 8103 – Advanced Database Systems  
**Assessment:** Individual Practical Database Portfolio  
**Case Study:** MediCare Health Clinic  
**Database Management System:** PostgreSQL  
**Development Environment:** GitHub Codespaces

## 1. Introduction

This portfolio focuses on SQL query processing and database performance optimisation using PostgreSQL. It builds on the MediCare Health Clinic database developed in Portfolio 1.

The objective is to demonstrate how SQL queries retrieve and analyse healthcare information, how PostgreSQL executes these queries, and how indexing can improve query performance.

The work covers SQL joins, aggregation functions, query execution plans, synthetic data generation, B-tree indexing, and performance comparisons.

The practical exercises were carried out in GitHub Codespaces, with SQL scripts, execution results, and supporting screenshots saved in this repository.

## 2. Case Study Overview

MediCare Health Clinic is a simulated healthcare organisation that manages patient registrations, healthcare providers, appointments, clinical visits, medical services, and payments.

The database supports several activities, including:

- Retrieving patient appointments and assigned healthcare providers.
- Counting appointments handled by each provider.
- Calculating revenue from completed payments.
- Identifying frequently delivered healthcare services.
- Searching appointment records by date or patient.
- Analysing and improving database query performance.

The database consists of seven related tables:

| Table | Purpose |
|---|---|
| Patients | Stores patient registration information |
| Providers | Stores healthcare provider information |
| Appointments | Records scheduled patient appointments |
| ClinicVisits | Records clinical visits |
| MedicalServices | Stores available healthcare services and fees |
| VisitServices | Records services delivered during visits |
| Payments | Records payments associated with visits |

The existing relational database was reused throughout this portfolio to maintain consistency with Portfolio 1.

## 3. SQL Query Implementation

Four SQL queries were developed to demonstrate the retrieval, joining, grouping, and aggregation of relational data.

The SQL statements are available in [queries.sql](queries.sql).

### 3.1 Patient Appointments and Healthcare Providers

The first query retrieves patient names, healthcare provider names, appointment dates, and appointment statuses.

It uses INNER JOIN operations to combine records from the Patients, Providers, and Appointments tables.

This query demonstrates how relationships established through foreign keys can be used to retrieve meaningful information from multiple tables.

**Practical application:** Clinic receptionists and administrators can use this type of query to review appointments and identify the providers assigned to patients.

### 3.2 Appointments per Healthcare Provider

The second query counts appointments associated with each healthcare provider.

It uses a LEFT JOIN to include providers who may not have any appointments, followed by GROUP BY and COUNT operations.

The results are ordered by the total number of appointments.

**Practical application:** Clinic administrators can use this information to assess provider workload and support appointment planning.

### 3.3 Revenue by Payment Method

The third query calculates revenue from completed payments.

It uses WHERE to select completed transactions, GROUP BY to organise results by payment method, and SUM to calculate total revenue.

COUNT is also used to determine the number of payment records for each method.

**Practical application:** Finance officers can use the results to understand how much revenue was recorded through cash, card, and bank transfer payments.

### 3.4 Most Frequently Delivered Medical Services

The fourth query identifies the most frequently delivered healthcare services.

It joins VisitServices with MedicalServices and uses SUM to calculate the quantity of each service delivered.

The results are ordered from the highest to the lowest quantity.

**Practical application:** Clinic management can use this information to identify services with higher demand and support operational planning.

Screenshots of the query results are available in the [screenshots](screenshots/) folder.

## 4. Query Performance Testing

After successfully executing the SQL queries, the next activity involved examining PostgreSQL query execution plans.

The purpose was to understand how PostgreSQL retrieves records and identify opportunities for optimisation.

The following command was used:

`EXPLAIN (ANALYZE, BUFFERS)`

This command provides information about:

- **Execution plan:** The operations PostgreSQL uses to retrieve data.
- **Sequential Scan:** A scan that examines table records without using an index for the search.
- **Index Scan:** An access method that uses an index to locate matching records.
- **Planning Time:** The time PostgreSQL spends preparing an execution plan.
- **Execution Time:** The time required to execute the query.
- **Buffers:** Information about database blocks accessed during query execution.

The initial performance tests were implemented in [performance_tests.sql](performance_tests.sql).

### 4.1 Initial Baseline Testing

The initial database contained five appointment records and five payment records.

Three queries were tested:

1. Appointment filtering by date.
2. Appointment lookup by PatientID.
3. Completed payment lookup.

The results were:

| Query | Scan Type | Execution Time |
|---|---|---:|
| Appointment date filtering | Sequential Scan | 0.026 ms |
| Patient appointment lookup | Sequential Scan | 0.011 ms |
| Completed payment lookup | Sequential Scan | 0.015 ms |

All three queries used sequential scans.

This was reasonable because the tables contained very few records, making sequential scanning inexpensive.

The results indicated that a larger dataset would be useful for evaluating the effects of indexing.

## 5. Synthetic Dataset Generation

To conduct more meaningful performance tests, a larger synthetic dataset was generated.

The dataset generation process is documented in [generate_test_data.sql](generate_test_data.sql).

The script was designed to add:

- 2,000 fictional patient records.
- 100,000 synthetic appointment records.

Together with the initial sample records, the expected database totals were 2,005 patients and 100,005 appointments.

The additional records used generated patient names, fictional identifiers, appointment dates, and appointment statuses.

PostgreSQL's `generate_series()` function was used to produce the additional records.

The use of synthetic data ensured that no real patient information was required for the performance experiments.

After populating the database, the PostgreSQL `ANALYZE` command was executed to update query planner statistics.

The larger dataset provided a more suitable environment for comparing sequential scans with index-assisted query execution.

## 6. Large Dataset Baseline Performance

Before creating the optimisation indexes, two SQL queries were tested against the larger Appointments table.

The queries are available in [large_dataset_baseline.sql](large_dataset_baseline.sql).

### 6.1 Appointment Date Filtering

The first query retrieved appointments scheduled on 15 March 2026.

PostgreSQL returned 137 matching records.

The query plan showed:

- Scan Type: Sequential Scan.
- Rows Returned: 137.
- Rows Removed by Filter: 99,868.
- Shared Buffer Hits: 814.
- Execution Time: 4.747 ms.

The results showed that PostgreSQL examined approximately 100,005 appointment records to retrieve 137 matching records.

### 6.2 Patient Appointment Lookup

The second query retrieved appointments belonging to the patient identified by PatientID = 1.

PostgreSQL returned 50 matching records.

The query plan showed:

- Scan Type: Sequential Scan.
- Rows Returned: 50.
- Rows Removed by Filter: 99,955.
- Shared Buffer Hits: 814.
- Execution Time: 6.792 ms.

These results established the baseline against which the performance of indexed queries could be compared.

## 7. Database Indexing

To improve query performance, two B-tree indexes were created on the Appointments table.

The implementation is available in [indexes.sql](indexes.sql).

### 7.1 Appointment Date Index

The first index was created on the AppointmentDate column.

**Index name:** `idx_appointment_date`

```sql
CREATE INDEX IF NOT EXISTS idx_appointment_date
ON Appointments(AppointmentDate);
```

The index was intended to support queries that filter appointment records using a date or date range.

### 7.2 Patient Appointment Index

The second index was created on the PatientID column.

**Index name:** `idx_appointment_patient`

```sql
CREATE INDEX IF NOT EXISTS idx_appointment_patient
ON Appointments(PatientID);
```

This index was intended to improve searches for appointments belonging to a particular patient.

After creating the indexes, PostgreSQL statistics were refreshed using the `ANALYZE` command.

The database successfully confirmed the existence of both indexes, alongside the existing primary-key index on AppointmentID.

## 8. Optimised Query Performance

The original queries were executed again after indexing.

The optimised query tests are available in [optimized_performance.sql](optimized_performance.sql).

### 8.1 Appointment Date Query

The execution plan changed from a Sequential Scan to a Bitmap Heap Scan supported by a Bitmap Index Scan.

The results were:

- Index Used: `idx_appointment_date`.
- Rows Returned: 137.
- Execution Time: 0.645 ms.
- Shared Buffer Hits: 137.
- Shared Buffer Reads: 2.

The index helped PostgreSQL locate the matching appointment records more efficiently.

### 8.2 Patient Appointment Query

The execution plan also changed from a Sequential Scan to a Bitmap Heap Scan supported by a Bitmap Index Scan.

The results were:

- Index Used: `idx_appointment_patient`.
- Rows Returned: 50.
- Execution Time: 0.086 ms.
- Shared Buffer Hits: 50.
- Shared Buffer Reads: 2.

The results demonstrated that indexing was effective for the patient lookup query.

## 9. Performance Comparison

The execution times recorded before and after indexing are compared below.

| Query | Before Indexing | After Indexing | Time Reduction |
|---|---:|---:|---:|
| Appointment Date Filtering | 4.747 ms | 0.645 ms | 86.41% |
| Patient Appointment Lookup | 6.792 ms | 0.086 ms | 98.73% |

The percentage reduction was calculated using:

**Performance Reduction (%) = ((Before − After) / Before) × 100**

For the appointment-date query:

((4.747 − 0.645) / 4.747) × 100 = 86.41%

For the patient appointment query:

((6.792 − 0.086) / 6.792) × 100 = 98.73%

Both queries showed considerable reductions in execution time after indexing.

The patient appointment query recorded the larger percentage reduction.

These percentages describe the observed improvements in the individual tests performed, rather than guaranteed performance improvements under all conditions.

## 10. Performance Analysis and Discussion

The results demonstrate the importance of database indexing when searching larger tables.

Before indexing, PostgreSQL used sequential scans to examine approximately 100,005 appointment records.

Although sequential scans are suitable for small tables and queries that retrieve a large proportion of records, they can become less efficient when only a small number of records are required from a much larger dataset.

After creating the indexes, PostgreSQL selected Bitmap Index Scans combined with Bitmap Heap Scans.

The Bitmap Index Scan identified matching record locations, while the Bitmap Heap Scan retrieved the required table rows.

This reduced the amount of table data accessed during the tested searches.

The performance improvements were particularly noticeable because the queries retrieved a relatively small percentage of the available appointment records.

However, indexing also has limitations. Indexes consume additional storage and require maintenance when records are inserted, updated, or deleted.

For this reason, indexes should be created based on actual query requirements rather than adding indexes to every database column.

The recorded execution times may also vary depending on caching, system load, dataset size, and PostgreSQL query planner decisions.

Repeating the tests under controlled conditions would help establish more representative performance measurements.

## 11. Practical Evidence

The `screenshots/` directory contains supporting evidence from the SQL implementation and performance tests.

The screenshots include:

- Patient appointments and provider activity.
- Payment revenue and service utilisation.
- Initial query execution plans.
- Large-dataset baseline query plans.
- Successfully created database indexes.
- Optimised appointment-date and patient-lookup execution plans.

The SQL scripts and screenshots provide evidence of the practical database operations completed in PostgreSQL.

## 12. Reproducing the Experiments

The experiments can be reproduced using PostgreSQL in GitHub Codespaces.

**Prerequisite:** Portfolio 1 must already be implemented, including the seven database tables and initial sample data.

### Step 1: Start PostgreSQL

```bash
sudo service postgresql start
```

### Step 2: Execute the SQL queries

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/queries.sql
```

### Step 3: Run the initial performance tests

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/performance_tests.sql
```

### Step 4: Generate the performance dataset

On a fresh database containing the original Portfolio 1 sample data, execute:

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/generate_test_data.sql
```

**Important:** This script should only be executed once for the intended dataset size because it inserts additional records each time it runs.

### Step 5: Execute the large-dataset baseline tests

Before creating the optimisation indexes, run:

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/large_dataset_baseline.sql
```

### Step 6: Create the indexes

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/indexes.sql
```

### Step 7: Execute the optimised queries

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db -v ON_ERROR_STOP=1 \
-f portfolio-2-query-optimisation/optimized_performance.sql
```

The new execution plans can then be compared with the baseline results to evaluate the effects of indexing.

For a repeat experiment, use a fresh database or restore the database to its pre-indexing state so that the tests are performed under comparable conditions.

## 13. Challenges and Lessons Learned

One challenge was that the original database contained only a few records, making it difficult to demonstrate meaningful performance differences.

This was addressed by generating a larger synthetic dataset using PostgreSQL's `generate_series()` function.

Another operational issue was that the PostgreSQL service did not automatically restart when the GitHub Codespace resumed after a period of inactivity.

The database connection problem was resolved by manually starting the PostgreSQL service.

The practical exercises helped demonstrate that:

- Database performance depends on dataset size and query conditions.
- Sequential scans are not always inefficient.
- Query execution plans provide useful information about database operations.
- Appropriate indexing can significantly reduce query execution time.
- Performance optimisation should be supported by measurements rather than assumptions.

## 14. Conclusion

Portfolio 2 demonstrated the practical use of SQL queries, PostgreSQL execution plans, and database indexing.

The experiments showed that the appointment-date and patient-lookup queries executed more efficiently after appropriate B-tree indexes were created.

The appointment-date query recorded an 86.41% reduction in execution time, while the patient-lookup query recorded a 98.73% reduction.

The results highlight the value of using execution plans and measured performance data when optimising relational databases.

The work provides a foundation for Portfolio 3, which will focus on transactions, concurrency, and database consistency.