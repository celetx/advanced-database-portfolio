# Portfolio 3: Transactions and Concurrency

**Course:** MIT 8103 – Advanced Database Systems  
**Assessment:** Individual Practical Database Portfolio  
**Case Study:** MediCare Health Clinic  
**Database Management System:** PostgreSQL  
**Development Environment:** GitHub Codespaces

## 1. Introduction

This portfolio looks at how PostgreSQL deals with transactions and concurrent operations. It's built on the MediCare Health Clinic database from Portfolios 1 and 2.

Database transactions are important because at times you do need several operations to be carried out together in order to maintain data accuracy and consistency. In healthcare they're used to manage financial records, appointments, payments and all sorts of other shared 

The practical exercises focused on COMMIT, ROLLBACK, transaction isolation, and concurrency control.

## 2. Objectives

The objectives of this portfolio were to:

- Demonstrate successful database transactions using COMMIT.
- Examine how ROLLBACK reverses uncommitted changes.
- Compare READ COMMITTED and REPEATABLE READ isolation levels.
- Demonstrate concurrent access using two PostgreSQL sessions.
- Examine row-level locking and lock timeout behaviour.
- Document practical results and observations.

## 3. Experimental Setup

The experiments were conducted using PostgreSQL within GitHub Codespaces.

The existing `medicare_clinic_db` database was used, and an additional table named `ClinicAccounts` was created to simulate internal financial transactions.

The table contains the following fields:

| Field | Description |
|---|---|
| AccountID | Unique account identifier |
| AccountName | Name of the clinic account |
| Balance | Account balance |

Two fictional accounts were created:

| Account | Initial Balance |
|---|---:|
| Main Clinic Account | NGN 100,000 |
| Laboratory Account | NGN 50,000 |
| **Total** | **NGN 150,000** |

The setup script is available in `Osisiogu_Nnabugwu_301930508_setup.sql`.

The experiments used fictional financial data rather than real patient or organisational records.

## 4. COMMIT Transaction Demonstration

### 4.1 Objective

The purpose of this experiment was to demonstrate how PostgreSQL permanently saves changes made within a successful transaction.

### 4.2 Implementation

A transaction was created to transfer NGN 10,000 from the Main Clinic Account to the Laboratory Account.

The transaction used the following SQL operations:

```sql
BEGIN;

UPDATE ClinicAccounts
SET Balance = Balance - 10000
WHERE AccountID = 1
  AND Balance >= 10000;

UPDATE ClinicAccounts
SET Balance = Balance + 10000
WHERE AccountID = 2;

COMMIT;
```

### 4.3 Results

| Account | Before COMMIT | After COMMIT |
|---|---:|---:|
| Main Clinic Account | NGN 100,000 | NGN 90,000 |
| Laboratory Account | NGN 50,000 | NGN 60,000 |
| **Total** | **NGN 150,000** | **NGN 150,000** |

The transaction completed successfully, and the combined balance remained unchanged.

### 4.4 Discussion

The experiment showed that PostgreSQL can apply multiple related updates as part of a single transaction.

Once COMMIT was executed the changes were permanent and would be visible in subsequent DB operations.

This kind of transaction processing is useful for maintaining consistency in an application that's doing financial transfers and associated database updates.

The demo was under the assumption that both of the account updates had actually updated the correct records. You'd obviously need some form of validation in a production financial system.

## 5. ROLLBACK Transaction Demonstration

### 5.1 Objective

The purpose of this experiment was to demonstrate how PostgreSQL reverses changes made within an uncommitted transaction.

### 5.2 Implementation

A transaction was started to transfer NGN 20,000 from the Main Clinic Account to the Laboratory Account.

The operations were:

```sql
BEGIN;

UPDATE ClinicAccounts
SET Balance = Balance - 20000
WHERE AccountID = 1;

UPDATE ClinicAccounts
SET Balance = Balance + 20000
WHERE AccountID = 2;

ROLLBACK;
```

### 5.3 Results

| Stage | Main Clinic | Laboratory |
|---|---:|---:|
| Before transaction | NGN 90,000 | NGN 60,000 |
| During transaction | NGN 70,000 | NGN 80,000 |
| After ROLLBACK | NGN 90,000 | NGN 60,000 |

The total balance remained NGN 150,000.

### 5.4 Discussion

The experiment confirmed that ROLLBACK cancels uncommitted changes.

Although the account balances changed temporarily during the transaction, PostgreSQL restored the previous values after ROLLBACK.

This demonstrates the atomicity property of database transactions, which ensures that a transaction's operations are treated as a single unit.

## 6. Transaction Isolation

Transaction isolation is what determines how changes made by one transaction become visible to other transactions that are running concurrently.

Two isolation levels were looked at using separate PostgreSQL sessions.

### 6.1 READ COMMITTED

Session A started a READ COMMITTED transaction and retrieved the Main Clinic Account balance of NGN 91,000.

Session B increased the balance by NGN 1,000 and committed the transaction.

When Session A repeated the SELECT query within its original transaction, the balance had changed to NGN 92,000.

| Operation | Balance |
|---|---:|
| Session A: First SELECT | NGN 91,000 |
| Session B: Committed update | NGN 92,000 |
| Session A: Second SELECT | NGN 92,000 |

The experiment demonstrated that READ COMMITTED allows successive SELECT statements within the same transaction to observe newly committed changes.

### 6.2 REPEATABLE READ

Session A started a REPEATABLE READ transaction and retrieved a balance of NGN 92,000.

Session B increased the balance by NGN 1,000 and committed the change.

Session A repeated the query but continued to see NGN 92,000.

After Session A committed, a new SELECT query returned NGN 93,000.

| Operation | Balance |
|---|---:|
| Session A: First SELECT | NGN 92,000 |
| Session B: Committed update | NGN 93,000 |
| Session A: Second SELECT | NGN 92,000 |
| Session A: SELECT after COMMIT | NGN 93,000 |

### 6.3 Isolation Comparison

| Behaviour | READ COMMITTED | REPEATABLE READ |
|---|---|---|
| Snapshot behaviour | New snapshot per statement | Consistent transaction snapshot |
| Sees another session's newly committed update during repeated SELECTs | Yes | No |
| Prevents non-repeatable reads | No | Yes |

The experiments demonstrated the difference between statement-level and transaction-level snapshot behaviour in PostgreSQL.

Further details are documented in `Osisiogu_Nnabugwu_301930508_isolation_tests.md`.

## 7. Concurrency Control and Row-Level Locking

### 7.1 Objective

The objective was to demonstrate how PostgreSQL controls conflicting updates to the same record.

### 7.2 Implementation

Two PostgreSQL sessions were connected to the same database.

Session A started a transaction and acquired a row-level lock on the Main Clinic Account using:

```sql
BEGIN;

SELECT AccountID, Balance
FROM ClinicAccounts
WHERE AccountID = 1
FOR UPDATE;
```

Session A was left open.

While the lock was held, Session B attempted to increase the account balance by NGN 2,000.

A five-second lock timeout was configured:

```sql
BEGIN;

SET LOCAL lock_timeout = '5s';

UPDATE ClinicAccounts
SET Balance = Balance + 2000
WHERE AccountID = 1;
```

### 7.3 Lock Timeout Result

PostgreSQL returned:

```text
ERROR: canceling statement due to lock timeout
CONTEXT: while updating tuple (0,9) in relation "clinicaccounts"
```

This confirms that Session B couldn't get the required lock whilst Session A was still holding it.

Session B did a ROLLBACK to get out of the failed transaction.

After Session A had released the lock Session B had a go at the update.

### 7.4 Successful Update

The repeated transaction completed successfully.

PostgreSQL returned `UPDATE 1` and `COMMIT`, and the balance increased from NGN 93,000 to NGN 95,000.

| Test | Result |
|---|---|
| Initial balance | NGN 93,000 |
| Concurrent update while locked | Blocked |
| Lock timeout | Occurred |
| Failed transaction rollback | Successful |
| Retry after lock release | Successful |
| Final balance | NGN 95,000 |

### 7.5 Discussion

The experiment showed that PostgreSQL can coordinate concurrent transactions via row-level locking.

The first transaction prevented a conflicting update until its lock was released.

Once the lock was released the second transaction could go through.

This behaviour ensures consistency when multiple users are attempting to update shared database records.

A lock timeout is not a successful update. The application must deal with the resulting error and determine whether a retry is warranted.
The detailed concurrency experiment is documented in `Osisiogu_Nnabugwu_301930508_concurrency_tests.md`.

## 8. ACID Properties

The experiments also illustrated important database transaction properties.

| Property | Meaning | Practical Application |
|---|---|---|
| Atomicity | A transaction succeeds as a unit or its changes are rolled back | COMMIT and ROLLBACK experiments |
| Consistency | Transactions should preserve defined database rules | Account constraints and balance checks |
| Isolation | Concurrent transactions are controlled according to an isolation level | READ COMMITTED and REPEATABLE READ |
| Durability | Committed changes persist in the database | COMMIT experiment |

The experiments particularly demonstrated atomicity and isolation. Durability under a system crash was not separately tested.

## 9. Challenges and Lessons Learned

Several practical observations were made during the experiments.

First, SQL transaction commands initially produced errors because they were entered in the Bash terminal instead of the PostgreSQL interactive terminal. The issue was resolved by connecting to PostgreSQL using the `psql` command.

Another issue was getting the PostgreSQL service restarted when GitHub Codespaces came back online after a period of inactivity.

The READ COMMITTED experiment also required some coordination between two database sessions. One attempt generated a warning as COMMIT was issued without an active transaction. The experiment was then successfully re-run and gave the expected result.

The main lessons learned were:

- Database transactions require careful control of BEGIN, COMMIT, and ROLLBACK.
- The order of operations matters when testing transaction isolation.
- Different isolation levels produce different data visibility behaviour.
- Row-level locking prevents conflicting updates from proceeding simultaneously.
- Lock timeouts require appropriate error handling.
- Practical database experiments should be supported by verifiable outputs.

## 10. Practical Evidence

Supporting screenshots are stored in the `screenshots/` directory.

The evidence includes:

- Initial clinic account balances.
- Successful COMMIT transaction.
- ROLLBACK demonstration.
- READ COMMITTED isolation test.
- REPEATABLE READ isolation test.
- Row-level lock timeout.
- Successful update after lock release.

The SQL scripts and Markdown documentation provide further evidence of the work completed.

## 11. Reproducing the Experiments

The experiments can be reproduced using PostgreSQL in GitHub Codespaces.

### Step 1: Start PostgreSQL

```bash
sudo service postgresql start
```

### Step 2: Execute the setup script

Run the setup SQL file from the repository root:

```bash
sudo -n runuser -u postgres -- psql \
-d medicare_clinic_db \
-v ON_ERROR_STOP=1 \
-f Osisiogu_Nnabugwu_301930508/portfolio-3-transactions-concurrency/Osisiogu_Nnabugwu_301930508_setup.sql
```

### Step 3: Execute COMMIT and ROLLBACK Tests

The COMMIT and ROLLBACK SQL scripts can be executed through PostgreSQL using `psql`.

The COMMIT script should only be run against the correct initial balances as each successful run will result in an extra transfer.

The ROLLBACK script can be used to demonstrate that uncommitted changes to balances are canceled.

### Step 4: Test Isolation and Concurrency

Open two PostgreSQL terminal sessions.

Connect each session to `medicare_clinic_db` and follow the commands documented in the isolation and concurrency test files.

The commands must be run in the correct session order if you're to reproduce the behaviour we saw.

For repeatable experiments you should either use a fresh test database or restore the account balances to a known starting point prior to running the experiment.

## 12. Conclusion

Portfolio three was transaction processing with concurrency control using PostgreSQL. The commit tests were very clear in terms of how related updates could be persisted, and the rollback tests demonstrated how changes that hadn't been committed could be undone. There were also isolation tests carried out and it appears there was a difference between read committed and repeatable read. 

The concurrency part demonstrated row-level locking to prevent conflicting updates, and transactions could recover from lock timeout errors in some cases. That provided practical evidence of database transaction management and isolation in the Medicare health clinic system, but some details about how everything connects still feel a bit messy to me.