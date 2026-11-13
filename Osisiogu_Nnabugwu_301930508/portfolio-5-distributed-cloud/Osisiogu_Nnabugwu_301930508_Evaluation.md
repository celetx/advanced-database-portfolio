# Performance, consistency and reliability evaluation

## Method and actual scope

The submitted run used PostgreSQL 16.11 in two independent database processes inside one Docker container on a managed cloud execution host. It completed with exit code 0 and 37 PASS assertions. The complete raw log records the timestamp, image digest, PostgreSQL version, SQL output, expected read-only error and final verdict. Measurements.json preserves the measured values in machine-readable form. This was one successful PostgreSQL run, not a statistical benchmark.

The controller records the primary WAL LSN after each write phase and polls pg_last_wal_replay_lsn on the standby until it reaches that target. A 30-second deadline makes a failure explicit. These waits include Docker/psql process startup and polling overhead and begin after the write command returns. They do not measure exact commit-to-replay latency, network RTT or transaction throughput. A rollback may leave the visible target LSN unchanged; its wait is not a measurement of replicated rolled-back data.

| Observation | Client-observed milliseconds | Target WAL LSN |
|---|---:|---|
| before_primary_failure | 80.739 | 0/3002618 |
| committed_transfer | 104.023 | 0/3002440 |
| initial_sync | 81.395 | 0/3000000 |
| insert_update | 103.477 | 0/30022C0 |
| manual_promotion | 516.259 | not applicable |
| rejoin_sync | 77.62 | 0/5000000 |
| restart_catchup | 88.66 | 0/3002618 |
| rolled_back_transfer | 77.38 | 0/3002440 |

The manual-promotion measurement includes stopping the old primary, checking its status, reading from the standby and manually promoting it. It excludes failure detection by an HA controller, real WAN delay and application/DNS reconnection. It is not a production RTO or provider SLA. Values will vary across reruns.

## Functional evidence

| Experiment | Observed result | Evidence scope |
|---|---|---|
| Initial clone and streaming | One async streaming sender and active physical slot | Genuine physical replication, not periodic row-copy code |
| Initial consistency | Ten table digests match between endpoints | Quiescent small-fixture comparison |
| Insert and phone update | Both changes visible on standby | Replay barrier reached before assertions |
| Committed transfer | NGN 90,000 and NGN 60,000 on standby | Combined NGN 150,000 preserved |
| Rolled-back transfer | Visible balances unchanged | Transaction rollback confirmed via standby reads |
| Direct standby write | PostgreSQL SQLSTATE 25006 | Expected rejection, not a failed overall run |
| Standby interruption | Primary accepts a new event with replica stopped | Asynchronous write availability demonstrated |
| Standby restart | New event appears and ten table hashes match | Short outage recoverable with retained WAL |
| Primary interruption | Standby still returns five patients | Existing read availability on surviving process |
| Manual promotion | New primary accepts post-promotion event | Old writer stopped first |
| Rejoin | Fresh standby at old endpoint sees new timeline event | Full new base backup, not automatic failback |
| Backup/restore | Ten restored table hashes match; NGN 150,000 total | Logical dump into separate restore database |

For the five seeded visits, branch completed revenue is Ikeja NGN 9,000, Lekki NGN 6,000 and Abuja NGN 7,000, totalling NGN 22,000. Branch visit counts are 2, 2 and 1. These reports were actually queried on the standby. Hash comparisons sort row JSON representations before MD5 aggregation and include every row in all ten tables. They are convenient fixture consistency checks, not cryptographic tamper evidence; the raw-log evidence uses SHA-256 separately.

## Availability and consistency tradeoffs

The asynchronous writer does not wait for remote acknowledgement. When the standby is offline, central writes continue but remote reads cannot reach that stopped server. If the primary fails, the surviving standby can serve its existing data; new writes require controlled promotion and application routing. The lab deliberately waits for replay before crashing the primary, so this run preserved the checked data. It does not establish zero data loss for arbitrary asynchronous failures.

Replication-lag samples in pg_stat_replication show a point in time only. A zero byte difference after catch-up does not mean the replica is always current. PostgreSQL's time-based replay_lag can become NULL when idle; time since the last replayed transaction also includes idle time and is not a universal replication-lag measure. Production needs workload-aware monitoring and an appropriate freshness policy.

This is not a quorum-based or multi-writer system, and no automatic election/partition reconciliation was tested. A production failover controller must prevent two live writers. This lab stops and fences the old process, then rebuilds the endpoint as a standby. Replication copies user mistakes too, making separate backups and restore drills necessary.

## Limits and further evaluation

No separate host, availability-zone failure, WAN network partition, packet loss, sustained workload, concurrent writer conflict, automatic routing, managed-cloud deployment, cloud PITR or production security hardening was tested. Shared CPU, storage and loopback networking make this an instructional functional exercise. Longer outages can exceed the configured retained WAL and require recloning. A future evaluation should repeat controlled workloads on separate hosts, define consistency requirements first, test application reconnection and record distributions rather than extrapolating from one run.
