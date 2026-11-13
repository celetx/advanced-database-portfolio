# Verification record

## Actual execution

The reconstructed Portfolio 4 was run again using Run.sh in a fresh real standalone MongoDB 8.0.16 Docker container in a managed Codex cloud environment. It exited 0 and printed 25 PASS assertions followed by ALL TESTS PASSED. ExecutionOutput.txt is actual stdout; its first line records the UTC execution time. EvidenceManifest.json records the source hash and image digest.

Executed checks cover Extended JSON loading, validators/index creation, fixture counts, CRUD state transitions and cleanup, all four aggregation outputs against independent expected values, invalid document rejection, reference audits, controlled orphan acceptance/cleanup and a hinted compound IXSCAN with expected result count. Node syntax checks for each JS file and Bash syntax checking for Run.sh also passed. No cross-engine performance comparison was conducted.

## Evidence provenance

CaptureEvidence.py launched installed Chromium through Playwright and captured two PNG screenshots of escaped actual saved stdout excerpts. Headers identify the browser log viewer and source SHA-256. This is genuine output evidence, not a live terminal or Codespaces screenshot. Explain details omitted from the validation image remain in the authoritative raw log. The script does not invent query results.

## Workspace reconstruction and progressive history

The initial push attempts failed with GitHub HTTP 403. After the user reconnected GitHub, the installation became visible. The cloud workspace had been replaced and no earlier bundle, ZIP or checkout remained. Therefore the lost unpushed local commits were not available to push verbatim.

The implementation was reconstructed from the retained session instructions and code, freshly executed and given new incremental commits based on original main `798f316`. The earlier local hashes (including ab7d8d3) are not claimed as recovered. This preserves the existing repository history and Portfolios 1–3 without inventing commit objects or reusing stale evidence. The user explicitly authorised publication to main after reconnection.

## Remaining manual verification

1. Review the exact assignment rubric and permitted AI-use policy; no rubric file was supplied.
2. Reproduce in the student's Codespace if the assessment specifically requires Codespaces terminal screenshots. Current evidence establishes managed cloud Docker execution only.
3. Review model assumptions, UTC interpretation, integer-kobo currency and the AI-use declaration before submission.
4. Replica-set transactions, concurrent referential-integrity enforcement, production security, failover/sharding and realistic performance comparisons remain future work, not verified features.
