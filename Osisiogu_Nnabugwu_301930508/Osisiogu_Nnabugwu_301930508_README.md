# MIT 8103 — Advanced Database Systems Portfolio

**Student:** Osisiogu Nnabugwu
**Student ID:** 301930508
**Academic session:** 2026/2027, First Semester — September Cohort 2026
**Assessment:** Individual Practical Database Portfolio
**Selected organisation:** MediCare Health Clinic (simulated)

## Public GitHub repository

https://github.com/celetx/advanced-database-portfolio

The repository is public in accordance with the lecturer's later verbal instruction. It preserves progressive commits, source files, documentation and execution evidence. Full URLs are shown so the links remain readable when this Markdown file is opened as plain text.

## Organisation and purpose

MediCare Health Clinic is a fictional healthcare organisation. Receptionists register patients and book appointments; healthcare providers record visits and delivered services; finance officers record payments; administrators maintain records and analyse activity. The main data comprises patients, providers, appointments, clinic visits, medical services, service quantities and payments. All patient and financial records used for the exercises are fictional. Portfolio 5 extends the scenario to fictional Ikeja, Lekki and Abuja clinic branches.

## Submission contents

The ZIP contains one top-level folder, `Osisiogu_Nnabugwu_301930508/`, with all five portfolio folders, the final documentation and a copy of this README. Source scripts and evidence retain the required `Osisiogu_Nnabugwu_301930508_DocumentType.extension` naming convention. This same README is also provided separately for the form's ReadME upload.

| Folder | Contents |
|---|---|
| `portfolio-1-database-design/` | PostgreSQL schema, fictional sample data, ER diagram, normalisation, constraint tests and screenshots |
| `portfolio-2-query-optimisation/` | SQL reports, execution plans, generated test data, indexing and recorded performance comparison |
| `portfolio-3-transactions-concurrency/` | COMMIT/ROLLBACK, isolation, locking and concurrency demonstrations with evidence |
| `portfolio-4-nosql/` | MongoDB document model, JSON data, executable CRUD/aggregation/validation scripts, explanation and evidence |
| `portfolio-5-distributed-cloud/` | PostgreSQL physical streaming replication, reliability/restore tests, cloud proposal, scripts and evidence |
| `final-documentation/` | Combined three-page PDF covering all five activities and editable Word copy |

## Final documentation for assessment

The combined summary includes the selected organisation, GitHub link, five activity summaries, selected genuine evidence, individual reflection, references and an AI-use declaration. The PDF is the page-checked three-page version; the Word document is an editable companion whose pagination can vary by editor.

**Three-page summary PDF:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/final-documentation/Osisiogu_Nnabugwu_301930508_FinalSummary.pdf

**Editable Word copy:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/final-documentation/Osisiogu_Nnabugwu_301930508_FinalSummary.docx

## Activity documentation

1. Portfolio 1 — Database Design and Modelling:
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-1-database-design/Osisiogu_Nnabugwu_301930508_README.md

2. Portfolio 2 — Query Processing and Optimisation:
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-2-query-optimisation/Osisiogu_Nnabugwu_301930508_README.md

3. Portfolio 3 — Transactions and Concurrency:
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-3-transactions-concurrency/Osisiogu_Nnabugwu_301930508_README.md

4. Portfolio 4 — NoSQL and Advanced Data Models:
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-4-nosql/Osisiogu_Nnabugwu_301930508_README.md

5. Portfolio 5 — Distributed and Cloud Databases:
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud/Osisiogu_Nnabugwu_301930508_README.md

## Verification and evidence

Portfolios 1–3 contain their existing SQL, session instructions, screenshots and recorded results. The Portfolio 2 recorded index comparisons reduced the appointment-date query from 4.747 to 0.645 ms and patient lookup from 6.792 to 0.086 ms; these are environment-specific observations, not universal performance guarantees.

The Portfolio 4 student's Codespaces log records 25 PASS assertions and ALL TESTS PASSED. The Portfolio 5 student's Codespaces log records 37 PASS assertions and ALL PORTFOLIO 5 TESTS PASSED. Portfolio 5 also includes the genuine student-uploaded terminal screenshot. Original managed-cloud logs and clearly labelled log-viewer screenshots remain separate from the student's Codespaces evidence.

**Portfolio 4 Codespaces execution log:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-4-nosql/Osisiogu_Nnabugwu_301930508_CodespacesExecution.txt

**Portfolio 5 Codespaces execution log:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud/Osisiogu_Nnabugwu_301930508_CodespacesExecution.txt

**Portfolio 5 Codespaces terminal screenshot:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud/screenshots/Osisiogu_Nnabugwu_301930508_CodespacesTests.png

The PostgreSQL replication lab runs separate database processes on one host/container. Its failover is controlled and manual. The Amazon RDS deployment is a proposed design; no managed cloud instance, multi-AZ failure, cloud PITR or WAN performance is claimed as verified.

## Reproduction

The detailed READMEs identify requirements, script order and test limitations. After extracting the ZIP, commands described as running from the repository root should be run from the directory containing `Osisiogu_Nnabugwu_301930508/`. Per-portfolio commands should be run from the specified activity folder. Existing data should be protected before running any setup/reset script.

Portfolios 1–3 require PostgreSQL and the supplied psql instructions. Portfolio 4 requires Bash and a local Docker daemon; Portfolio 5 additionally requires Python 3.9+ (standard library only). The Docker runners use isolated temporary containers and remove their own lab databases when complete. They do not require a paid cloud subscription.

From the directory containing the student folder, Portfolio 4 can be run with:

```bash
cd Osisiogu_Nnabugwu_301930508/portfolio-4-nosql
bash Osisiogu_Nnabugwu_301930508_Run.sh
```

From the directory containing the student folder, Portfolio 5 can be run with:

```bash
cd Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud
bash Osisiogu_Nnabugwu_301930508_Run.sh
```

## Reflection, references and AI use

The final summary includes the student's observation about related PostgreSQL tables, keys, reduced duplication and referential integrity, together with the recorded Codespaces verification and guided Git recovery. Detailed technical references are included in the activity documentation and the final summary.

OpenAI Codex assisted with Portfolio 4–5 design, implementation, testing, explanations and evidence preparation, and preparation of the combined summary and submission package. The student reviewed and edited documentation, reproduced Portfolios 4 and 5 in Codespaces, checked the success outputs, committed execution evidence and reviewed the final summary. AI assistance does not replace the student's responsibility for accuracy, source acknowledgement and understanding. No private credentials or real patient records are included.

**Portfolio 4 AI-use declaration:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-4-nosql/Osisiogu_Nnabugwu_301930508_AIUseDeclaration.md

**Portfolio 5 AI-use declaration:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud/Osisiogu_Nnabugwu_301930508_AIUseDeclaration.md

**Portfolio 5 official references:**
https://github.com/celetx/advanced-database-portfolio/blob/main/Osisiogu_Nnabugwu_301930508/portfolio-5-distributed-cloud/Osisiogu_Nnabugwu_301930508_References.md
