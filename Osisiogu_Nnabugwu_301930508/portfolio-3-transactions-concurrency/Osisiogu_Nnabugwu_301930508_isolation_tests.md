
# Transaction Isolation Tests

**Course:** MIT 8103 Advanced Database Systems

**Case Study:** MediCare Health Clinic

**Database:** PostgreSQL

## 1. Objective

The experiment was about concurrent reads and updates in postgresql under those two isolation levels. Two sessions were set up for it.

## 2. READ COMMITTED

Two database sessions were used.

Two sessions were running at the same time. One started a read committed transaction and pulled the main clinic balance which came back as 91000. The other one added 1000 to it and saved the change right away. 

When the first session checked again inside the same transaction the number was now 92000. It seems read committed lets you see stuff that got committed after you began. This part gets a bit messy sometimes.

## 3. REPEATABLE READ

Session A started a REPEATABLE READ transaction and
retrieved a balance of NGN 92,000.

Session B increased the balance by NGN 1,000 and
committed the transaction.

Session A repeated the query but continued to see
NGN 92,000.

After Session A committed, a new query returned
NGN 93,000.

This demonstrated that REPEATABLE READ maintains a
consistent snapshot throughout the transaction.

## 4. Results

| Isolation Level | First Read | Second Read |
|---|---:|---:|
| READ COMMITTED | NGN 91,000 | NGN 92,000 |
| REPEATABLE READ | NGN 92,000 | NGN 92,000 |

## 5. Conclusion

The experiments showed that PostgreSQL provides

different levels of transaction isolation.

READ COMMITTED allows a transaction to observe changes

committed by another session between statements.

REPEATABLE READ maintains a consistent snapshot,

preventing non-repeatable reads within the transaction.

Both experiments were conducted using separate.

PostgreSQL sessions in GitHub Codespaces.
