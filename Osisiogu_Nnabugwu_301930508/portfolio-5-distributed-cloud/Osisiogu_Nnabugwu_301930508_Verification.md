# Verification and quality-assurance record

## Repository review and preservation

Work began from main commit `20ed34d`, including the student's latest Portfolio 4 Codespaces evidence. Root navigation and all four prior portfolio directories were inspected; Portfolio 1 schema/sample SQL and Portfolio 3 account setup informed this implementation. The Portfolio 4 saved execution outputs were checked for the success verdict and 25 PASS assertions. No lecturer rubric, assignment PDF, marks schedule or AGENTS.md was found in the repository. The later detailed user task is the assessment-coverage basis.

Changes are confined to portfolio-5-distributed-cloud and the root README navigation link. No PostgreSQL service belonging to prior portfolios was contacted, and all Portfolio 1–4 files are preserved. A dedicated portfolio-5-distributed-cloud branch holds progressive implementation, evidence and documentation commits for pull-request review. Existing ancestor history is retained; no force push, squash or automatic main merge is required.

## Executed database verification

Run.sh was executed in a managed Codex cloud environment. PostgreSQL 16.11 physical streaming replication ran between two independent server processes with separate cluster data directories and ports inside one isolated container. The final result was exit 0, 37 PASS assertions and ALL PORTFOLIO 5 TESTS PASSED. ExecutionOutput.txt records actual output. The run timestamp and immutable image digest are in EvidenceManifest.json, along with hashes of the exact implementation files that were executed.

All setup SQL/configuration and local experiment stages were exercised: clone/streaming, separate replica reads, full-fixture hash comparisons, insert/update propagation, commit/rollback, expected read-only rejection, stopped-replica write availability/catch-up, primary immediate-stop, surviving reads, fenced manual promotion, fresh-base-backup rejoin and ten-table logical restore. The sole SQL ERROR in the successful log is the intentionally rejected standby write (SQLSTATE 25006).

Client-observed times are genuine samples from that run, not invented benchmarks. One physical-standby failure exercise and one manual promotion were performed; no distributed election or provider failover was tested. The initial MongoDB exploration and its disk-space failure are outside the submitted PostgreSQL implementation. The PostgreSQL run itself had no failed assertion.

## Evidence capture and static QA

Four Chromium/Playwright screenshots show actual saved stdout in a clearly identified plain browser log viewer. They do not imitate terminal output or claim Codespaces execution. Source SHA-256 appears on the images; the manifest also contains screenshot hashes. CaptureEvidence.py and Validate.py support reproduction and audit.

Validate.py checks Python AST syntax, Bash syntax, JSON, filename prefix, relative Markdown links, expected log verdict/count, measurement extraction, manifest hashes and absence of changes to the four prior portfolio directories. It also screens common credential patterns; this is a focused repository check, not a comprehensive secret-scanning guarantee. All static checks passed before publication. Source scripts contain no private cloud credential or password-bearing connection URI. PgHba.conf uses trust only for the intentionally isolated loopback lab and is explicitly unsuitable for production.

## Untested or manual items

- The student's own Codespaces run of Portfolio 5; commands are provided in README.
- Managed RDS provisioning and CloudVerification.sql against a real cloud endpoint; no account/credentials/resources were supplied or created.
- Multi-host/AZ/geographic failures, WAN partitions, automatic failover/routing, multi-writer conflict resolution, long-outage slot exhaustion, cloud PITR, performance under realistic concurrency and production security/legal compliance.
- Actual lecturer rubric/allocated marks and institutional AI-use rules; the supplied-task checklist is not a promise of assessment marks.
- Direct retrieval of the NDPC final GAID PDF returned HTTP 403; official indexed excerpts informed the proposed privacy considerations. Review the full current regulator text before a real deployment.

After a local Codespaces reproduction, commit its prefixed output and genuine terminal screenshots separately and update verification wording based on the actual new result. Review the pull request before merging to main.
