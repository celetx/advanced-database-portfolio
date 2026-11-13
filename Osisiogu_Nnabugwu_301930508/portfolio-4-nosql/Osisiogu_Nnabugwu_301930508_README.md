# Portfolio 4: NoSQL and Advanced Data Models

**Course:** MIT 8103 – Advanced Database Systems

**Student:** Osisiogu Nnabugwu · **ID:** 301930508

**Case study:** MediCare Health Clinic (simulated)

**Implementation:** MongoDB 8.0.16, mongosh and Docker

**Verification environment:** managed Codex cloud; not GitHub Codespaces

## 1. Objectives and continuity

This portfolio implements a MongoDB document model using fictional MediCare records, demonstrates CRUD operations, produces four aggregation reports, validates data rules and inspects a compound index plan. It compares document modelling with the PostgreSQL work in Portfolios 1–3 and evaluates advanced-model alternatives. All Portfolio 1–3 files remain unchanged.

No separate assessment rubric was supplied in the repository. Coverage follows the requested practical tasks; check any institution-specific submission requirements before submitting.

## 2. Files and navigation

Every newly submitted file follows `Osisiogu_Nnabugwu_301930508_DocumentType.extension`. This prefixed README is the entry point; the existing root README links here.

| Files (all names use the required prefix) | Purpose |
|---|---|
| [Patients.json](Osisiogu_Nnabugwu_301930508_Patients.json), [Providers.json](Osisiogu_Nnabugwu_301930508_Providers.json), [Services.json](Osisiogu_Nnabugwu_301930508_Services.json) | Fictional master data |
| [Appointments.json](Osisiogu_Nnabugwu_301930508_Appointments.json), [Visits.json](Osisiogu_Nnabugwu_301930508_Visits.json) | Scheduling and embedded encounter datasets |
| [Common.js](Osisiogu_Nnabugwu_301930508_Common.js), [Setup.js](Osisiogu_Nnabugwu_301930508_Setup.js) | Helpers, strict validators, seed loading, indexes |
| [CRUD.js](Osisiogu_Nnabugwu_301930508_CRUD.js) | Temporary appointment lifecycle with state assertions |
| [Aggregations.js](Osisiogu_Nnabugwu_301930508_Aggregations.js) | Four report pipelines |
| [Tests.js](Osisiogu_Nnabugwu_301930508_Tests.js) | Expected results, negative cases, reference audits and explain |
| [Run.js](Osisiogu_Nnabugwu_301930508_Run.js), [Run.sh](Osisiogu_Nnabugwu_301930508_Run.sh) | Complete mongosh workflow and disposable Docker runner |
| [Modelling.md](Osisiogu_Nnabugwu_301930508_Modelling.md) | Entity mapping, diagram, embedding/references, schema/index decisions and advanced alternatives |
| [PostgreSQLComparison.md](Osisiogu_Nnabugwu_301930508_PostgreSQLComparison.md) | Relational comparison, equivalent SQL report and references |
| [ExecutionOutput.txt](Osisiogu_Nnabugwu_301930508_ExecutionOutput.txt), [EvidenceManifest.json](Osisiogu_Nnabugwu_301930508_EvidenceManifest.json) | Actual stdout and provenance/hash/image digest |
| [CaptureEvidence.py](Osisiogu_Nnabugwu_301930508_CaptureEvidence.py) | Reproducible screenshots of the saved actual output |
| [Verification.md](Osisiogu_Nnabugwu_301930508_Verification.md) | Verified scope, reconstruction note and remaining manual checks |
| [AIUseDeclaration.md](Osisiogu_Nnabugwu_301930508_AIUseDeclaration.md) | Disclosure of assistance |
| `screenshots/` | Two genuine PNG captures of actual saved output excerpts |

## 3. Document model and fixture

Five collections contain 5 patients, 3 providers, 5 catalogue services, 5 appointments and 5 visits. Visits embed 6 service lines and 5 payments. They reference patient/provider master records. Service names and fees within visits are historical snapshots; optional clinical notes illustrate flexible document content. Arrays are capped at 100 items per visit.

For example, visit 1 references patient 1 and provider 1 and contains General Consultation (500,000 kobo), Blood Pressure Check (150,000 kobo) and a Completed Cash payment of 650,000 kobo. Whole-kobo amounts avoid fractional binary currency arithmetic. Extended JSON `$date` values are parsed into BSON Date. Modelling.md explains UTC assumptions, fixed timestamps and other differences from the SQL defaults.

## 4. Reproduce using Docker (verified route)

Requirements: Bash, Docker CLI, a running local Docker daemon accessible to the current user, and permission to pull `mongo:8.0.16`. MongoDB, mongosh, Node and Python need not be installed on the host for this route.

From the repository root:

```bash
cd Osisiogu_Nnabugwu_301930508/portfolio-4-nosql
bash Osisiogu_Nnabugwu_301930508_Run.sh
```

The runner targets the local Unix Docker socket, starts a uniquely named disposable container with no external network or published ports, waits for MongoDB ping readiness, copies this directory, executes mongosh and removes the container on exit. Failures propagate as a nonzero exit code. Its temporary database is intentionally removed after the run. It does not modify PostgreSQL.

To save a rerun without replacing submitted evidence:

```bash
set -o pipefail
bash Osisiogu_Nnabugwu_301930508_Run.sh 2>&1 | tee /tmp/medicare-p4-rerun.txt
```

The exact image digest used for the recorded execution is in EvidenceManifest.json. The runner uses a version tag for convenience; use the recorded digest when byte-identical image selection is needed.

## 5. Direct MongoDB / Codespaces alternative (not verified here)

With a running disposable local MongoDB and mongosh installed using official instructions appropriate to your Codespace image, execute from this portfolio directory:

```bash
mongosh 'mongodb://127.0.0.1:27017/medicare_portfolio4' \
  --quiet --file Osisiogu_Nnabugwu_301930508_Run.js
```

Run.js explicitly selects `medicare_portfolio4` regardless of the URI database. Setup.js drops/recreates only its five named collections on each run. Do not use a database containing work you want to retain. The workflow does not access the existing PostgreSQL `medicare_clinic_db`.

This direct-host/Codespaces route was not executed in the student's Codespace. If Docker is enabled there, the verified Docker command is also reproducible there, subject to that environment's permissions.

Use a fresh mongosh session for the entry point. Individual JS files share helpers and pipeline results; they are workflow components, not independent CLI programs. For exploration, load Common.js, Setup.js, CRUD.js, Aggregations.js and Tests.js in that order.

## 6. CRUD and aggregation results

CRUD.js inserts temporary appointment 9001, reads patient 1's appointments, conditionally updates Scheduled to Completed, reads the changed status, deletes the temporary document and verifies deletion. Tests check affected-document counts and resulting state.

| Report | Pipeline features | Verified fixture result |
|---|---|---|
| Completed revenue by method | `$unwind`, `$match`, `$group`, `$sort` | Card NGN 2,500; Cash NGN 9,500; Transfer NGN 10,000 |
| Service utilisation and billing | `$unwind`, `$group`, `$multiply` | Service IDs 1–5: quantities 1, 2, 1, 1, 1; billed NGN 22,000 |
| Patient 1 visit history | `$match`, two `$lookup`s, `$unwind`, `$project`, `$sort` | Ada Okeke, Dr. James Okoro, one completed visit |
| Provider workload | `$lookup` from providers, `$size` | Providers 1–3: 2, 2, 1 appointments |

Billed charges derive from service snapshots; collected revenue derives from Completed payments. They happen to match in this fully paid fixture and must not be assumed equal for arbitrary records.

## 7. Verification and evidence

The fresh recorded execution returned exit code 0, with **25 PASS assertions** and `ALL TESTS PASSED` on MongoDB 8.0.16. The raw log contains server version, UTC timestamp, all report outputs and full executionStats. Validators/unique indexes rejected duplicates, invalid/missing fields, negative price, invalid dates/statuses, zero service quantity and zero payment. Seed references passed audits. A controlled orphan was accepted, showing the absence of foreign-key enforcement, and then removed. The hinted patient/date index produced IXSCAN, one returned document, one examined key and one examined document. This tiny fixture is not a performance benchmark.

- [CRUD and aggregation screenshot](screenshots/Osisiogu_Nnabugwu_301930508_CRUDAndAggregations.png)
- [Validation and final verdict screenshot](screenshots/Osisiogu_Nnabugwu_301930508_ValidationResults.png)

These are actual Chromium screenshots of unmodified saved mongosh output excerpts, visibly labelled as a browser log viewer. They are not live-terminal or Codespaces screenshots. Their displayed source SHA-256 matches EvidenceManifest.json. The validation image joins the validation section to the final index-test verdict; the full explain remains in ExecutionOutput.txt.

CaptureEvidence.py can recreate these screenshots from a successfully saved ExecutionOutput.txt. It requires Python, the Playwright package, an installed Chromium browser (default `/usr/bin/chromium`, configurable through CHROMIUM_PATH) and the local Docker image for digest inspection. These optional capture dependencies are separate from the database runner.

## 8. Interpretation and limits

Embedding simplifies encounter-local reads and atomic updates, but duplicates historical values and limits document growth. References avoid repeated identities but require application-managed integrity. Schema validation controls shape and local values without enforcing every business rule. Indexes should follow workloads and be measured with realistic data before claiming a speed improvement.

No Codespaces execution, distributed transactions, failover, sharding, production security hardening, scale benchmark or new PostgreSQL execution is claimed. Verification.md records the remaining manual checks. AI assistance and the reconstruction after workspace replacement are disclosed in AIUseDeclaration.md.
