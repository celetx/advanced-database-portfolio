# MongoDB and PostgreSQL comparison

The reference is Portfolio 1's seven-table MediCare schema and Portfolio 3's transaction experiments. No PostgreSQL migration or new cross-engine benchmark was executed for Portfolio 4.

| Concern | Existing PostgreSQL design | Portfolio 4 MongoDB model |
|---|---|---|
| Structure | Normalised tables; VisitServices joins visits to services | Five collections; service lines/payments embedded per visit |
| Schema | Typed columns, NOT NULL, CHECK, migrations | BSON documents with strict validators and flexible optional notes |
| Relationships | Foreign keys enforce existence | Application consistency and reference audits required |
| Reports | JOIN, WHERE, GROUP BY | `$lookup`, `$match`, `$unwind`, `$group`, `$sort` |
| Local atomicity | Transaction around related statements | Atomic write to one document including embedded arrays |
| Multi-record atomicity | BEGIN/COMMIT/ROLLBACK; isolation tested in Portfolio 3 | Transactions on replica sets/sharded clusters; not tested on this standalone |
| Historical charges | Catalogue joins use current fee unless snapshots are added | Name and unit fee copied into delivered-service lines |
| Money | NUMERIC(12,2) | Whole-kobo fixture values; larger systems need safe bounds/Long/Decimal128 |
| Indexes | B-tree scalar indexes | Compound and multikey indexes; no universal speed advantage |
| Scale | Replication, partitioning and appropriate sharding architecture | Replica sets/native sharding; shard key and cross-shard work matter |
| Fit for clinic | Strict relationships, ledgers, complex joins | Flexible encounter content, encounter-local reads and updates |

## Equivalent report

The reporting intent of completed revenue is:

```sql
SELECT PaymentMethod, SUM(Amount) AS TotalNGN, COUNT(*) AS PaymentCount
FROM Payments
WHERE PaymentStatus = 'Completed'
GROUP BY PaymentMethod
ORDER BY PaymentMethod;
```

MongoDB unwinds payments, filters Completed entries, groups by method and sums amountKobo. Divide by 100 to display NGN. Filtering after unwind avoids counting a Pending payment that shares a visit with a Completed one. Service utilisation sums quantity rather than counting lines. Provider workload starts with providers and looks up appointments, so a provider with zero bookings can remain in the report.

## Consistency and evaluation limits

MongoDB supports ACID transactions; NoSQL does not imply that every write is eventually consistent. Read concern, write concern, read preference and deployment topology determine guarantees. This standalone validates CRUD/aggregations but does not establish replica-set failover, majority durability or multi-document transaction behaviour. PostgreSQL replication and durability also depend on configuration. CAP concerns the tradeoff during network partitions, not a simple ranking of products.

The verified explain output demonstrates an index access path, not a latency comparison. A fair benchmark needs equivalent business invariants, realistic volumes, controlled hardware, concurrency, repeated measurements and a stated cache policy.

## References for further reading

- [MongoDB data modelling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [MongoDB atomicity](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/)
- [MongoDB aggregation](https://www.mongodb.com/docs/manual/aggregation/)
- [MongoDB compound indexes](https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html)

These links are references; execution of their examples is not claimed.
