# Phase 7 — Mandatory pre-holdout technical release gate

**PASS — All requirements satisfied.**

Saved UTC: 2026-10-16T01:52:21.438245+00:00

Authority: User Phase 7 instruction explicitly approves historical academic evaluation of P1/S1/B1/B2, locked capacities/metrics/bootstrap, and automatic Stage 2 continuation after PASS. All 15 predictors remain Provisional; this is conditional historical academic evaluation, not deployment validation.

| requirement | status |
| --- | --- |
| 194 development-only fits / 190 CV +4 final refits | PASS |
| Exact four scenarios/roles and fixed parameter choices recorded | PASS |
| Exact ordered full/customer input schemas | PASS |
| Fitting-only OHE/ordinary/conditional statistics audited | PASS |
| Approved conditional recency, placeholder and unscaled indicator behavior | PASS |
| Customer-only recency components fully removed | PASS |
| Finite probabilities and correct [0,1] mapping | PASS |
| Four trusted serialized pipelines reload identically | PASS |
| All sources, split, code and model digests unchanged | PASS |
| Roster P1 sole primary / S1 B1 B2 secondary unchanged | PASS |
| Metrics/capacities/ties/2,000 paired-stratified bootstrap frozen | PASS |
| No unexpected warnings/errors and all four preprocessing tests pass | PASS |
| Explicit user authorization and academic-only interpretation recorded | PASS |
| No test parse/profile/transform/prediction/evaluation before this gate | PASS |

Frozen selected configurations:

| scenario | role | group | selected_parameters | CV_AP_selection_only | seconds |
| --- | --- | --- | --- | --- | --- |
| P1 | Sole Primary | Full | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.448069 | 100.591032 |
| S1 | Secondary Sensitivity | Customer Attributes Only | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.233785 | 85.355146 |
| B1 | Secondary Benchmark | Full | {"classifier__C": 0.1} | 0.422429 | 2.079500 |
| B2 | Secondary Benchmark | Customer Attributes Only | {"classifier__C": 0.1} | 0.202251 | 1.738402 |

Source main: `9578ebc`. Full data/split/source hashes, pipeline statistics, ordered schemas, versions, full classifier configurations and artifact hashes are in models/model_manifest.json and models/phase7_protocol.json.

Manifest SHA-256: `84aad6db0ad97b619fdf27c4e6fccdef3263ac65c178ca4f9898a0b0b773d96a`. Protocol SHA-256: `77dc25ff60e8408ffd53aff04378cc0df4293dae847f3c263acfce93cf982dfd`. Execution code SHA-256: `eb82e4b5d6cfde38df114adde5ba3702e2fda70786cf9f1ea72abdec7293764e`.

No test records or performance have been accessed at the time this document is saved. Training-only category/scaler/recency audits and original/full-adapter equivalence passed. Four models reloaded with bit-identical development-fixture probabilities; no unexpected warnings. Metric/targeting synthetic checks and four approved preprocessing unit tests passed.

Locked positive class 1; threshold >=0.50; AP primary, ROC-AUC secondary; top 10% (824) primary illustrative business capacity and top 5% (412)/20% (1648) secondary. Ties: descending score then cleaned-row position, bootstrap duplicate occurrence last. Bootstrap: 2,000 paired stratified within-class replacement draws, NumPy default_rng(42), original class counts retained, no fitting/calibration; descriptive 2.5/97.5 percentile intervals.

This PASS authorizes continuation to exactly one batch under the existing user approval. It is a technical isolation gate, not verification of feature timing, customer independence, causality or prospective deployment. Any mandatory failure prohibits test access. This document is preserved unchanged after test opening.
