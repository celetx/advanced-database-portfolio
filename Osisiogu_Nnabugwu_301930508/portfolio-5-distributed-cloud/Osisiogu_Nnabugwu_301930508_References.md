# Official references and source notes

Sources checked on 13 November 2026. No cloud pricing, regional resource availability or legal compliance is inferred from the local lab.

| Source | Use in this portfolio |
|---|---|
| [PostgreSQL 16: replication overview](https://www.postgresql.org/docs/16/high-availability.html) | Physical versus logical replication and availability context |
| [PostgreSQL 16: streaming standby](https://www.postgresql.org/docs/16/warm-standby.html) | WAL, asynchronous mode, slots and standby behaviour |
| [PostgreSQL 16: pg_basebackup](https://www.postgresql.org/docs/16/app-pgbasebackup.html) | Initial full-cluster backup and recovery configuration |
| [PostgreSQL 16: failover](https://www.postgresql.org/docs/16/warm-standby-failover.html) | Promotion, fencing and rebuilding a standby |
| [PostgreSQL 16: monitoring statistics](https://www.postgresql.org/docs/16/monitoring-stats.html) | Replication status and lag interpretation |
| [PostgreSQL 16: pg_dump](https://www.postgresql.org/docs/16/app-pgdump.html) | Logical backup versus physical replication |
| [AWS RDS Multi-AZ overview](https://aws.amazon.com/rds/features/multi-az/) | Proposed managed writer HA; distinguish instance and cluster products |
| [AWS RDS read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html) | Asynchronous reporting replicas and promotion |
| [AWS RDS automated backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html) | Backup retention and proposed PITR |
| [AWS PostgreSQL TLS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html) | Certificate and hostname verification |
| [AWS RDS encryption](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html) | At-rest protection and key management |
| [RDS PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/) | Cost categories; no price quote is asserted |
| [NDPC final GAID 2025](https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf) | Nigerian privacy governance and implementation context |
| [Nigeria Data Protection Commission](https://ndpc.gov.ng/) | Regulator and current instruments |

Official indexed GAID excerpts were available, but direct retrieval of the regulator's PDF returned HTTP 403. The cloud design identifies matters requiring assessment rather than claiming a completed legal audit or substituting the earlier draft for the final directive. Review current NDPA/GAID requirements with qualified privacy oversight before real healthcare deployment. No downloaded reference PDF is submitted as original student work.
