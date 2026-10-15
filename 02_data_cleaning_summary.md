# Phase 2B — Data cleaning summary

## Scope and implemented decisions

Scenario: predict subscription before the current marketing campaign begins. Implemented only the user's approved deterministic cleaning; Phase 2B supersedes Phase 2A's tentative pre-call scenario and duplicate-retention proposal. Reviewed README, project DOCX, Phase 1 notebook/summary, Phase 2A review/table and raw CSV. Source CSV SHA-256: `81fd5eb4b659dddbc704edd90376c32714c3f6a43b887cb686762903bc793f0d`.

Original dimensions: **41,188 × 20** (19 predictors plus target). Cleaned dimensions: **41,176 × 16** (15 predictors plus target). The README headline says 21 columns, but its detailed list and supplied data both have 20; no missing feature has been invented.

## Approved exclusions

- duration: last-call duration is unavailable before the call/campaign.
- campaign: current-campaign contacts are not known before campaign initiation.
- contact, month, day_of_week: recorded contact-event channel/date are not established campaign-start inputs.
- Original pdays: replaced by the two approved derived recency fields, not otherwise feature-selected away.

All original columns and records remain unchanged in dataset.csv.

## Duplicate removal and target distribution

Exactly **12** duplicate rows beyond first occurrences were removed using **all 20 original columns before exclusions**. Kept first occurrences in original order; no other rows deleted. Retained row count: 41,176. Customer identity still cannot be verified without IDs. Projected duplicate rows (5841) and repeated predictor profiles (6488 beyond first) were retained and are not an additional deletion criterion.

| y | original_count | removed_count | cleaned_count | original_percent | cleaned_percent |
| --- | --- | --- | --- | --- | --- |
| 0 | 36548 | 11 | 36537 | 88.734583 | 88.733728 |
| 1 | 4640 | 1 | 4639 | 11.265417 | 11.266272 |

Target counts change only by approved duplicate removal: 11 no and 1 yes removed. Class proportions change slightly, not identically. Only 0/1 target labels exist; no target imputation or extra exclusion occurred.

## Unknown-value handling

job, marital and education retain their exact text including unknown. default/housing/loan use the deterministic human-readable mapping -1 → unknown, 0 → no, 1 → yes. This is category relabelling for clarity, not model-oriented categorical encoding or a learned transformation. CSV status columns read as strings; do not reinterpret them as continuous values.

| feature | original_unknown | removed_with_duplicates | cleaned_unknown | original_percent | cleaned_percent |
| --- | --- | --- | --- | --- | --- |
| job | 330 | 0 | 330 | 0.801204 | 0.801438 |
| marital | 80 | 0 | 80 | 0.194231 | 0.194288 |
| education | 1731 | 1 | 1730 | 4.202680 | 4.201477 |
| default | 8597 | 1 | 8596 | 20.872584 | 20.876239 |
| housing | 990 | 0 | 990 | 2.403613 | 2.404313 |
| loan | 990 | 0 | 990 | 2.403613 | 2.404313 |

Education and default unknown counts each fall by one only because a removed exact duplicate carried that unknown. All other unknown counts are unchanged; retained-row unknown masks match raw retained rows exactly. No unknown observations were dropped or statistically imputed.

## Pdays transformation and verification

- recency_available = 1 iff original pdays != 999; otherwise 0.
- recency_days = original pdays when available, otherwise fixed placeholder 0.
- previous is unchanged; no inference that mixed history records are erroneous.
- Availability=0 with days=0 is an unavailable-recency placeholder, not an actual zero-day interval. All 15 actual zero-day cases have availability=1.

| case | original | cleaned |
| --- | --- | --- |
| pdays_999 | 39673 | 39661 |
| actual_recency | 1515 | 1515 |
| previous_positive_pdays_999 | 4110 | 4110 |
| actual_zero_day_recency | 15 | 15 |
| previous_zero_actual_recency | 0 | 0 |

All 4,110 previous>0/sentinel records remain with previous unchanged, availability=0 and days=0. Actual recency range: 0–27 days. No invalid/nonfinite/negative day values were found. The sentinel count falls by 12 solely through duplicate removal. Availability does not assert whether a person was ever contacted. No scaling or statistical recency imputation occurred.

## Remaining feature list and types

Predictors (in export order): age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days.
Target: y (binary 0/1, not a predictor).

Categorical: job, marital, education, default, housing, loan. Quantitative: age, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_days. Deterministic binary indicator: recency_available.

## Observed data quality and validation evidence

No raw/cleaned nulls, blank categorical strings, undocumented category values, nonfinite numerical values, negative contact/recency counts or invalid target labels were found. Numeric/code domains were checked before transformations. Legitimate extremes remain: age 17–98, previous 0–7; negative economic rates/index values were preserved. Rare groups remain (default=yes 3; education=illiterate 18). No outlier correction or feature selection beyond the approved exclusions was applied.

Notebook assertions check raw duplicate count, exact keep-first row indices, expected output dimensions/columns, unknown masks/count conservation, unchanged columns exactly equal in value/dtype, exact status relabelling, both recency formulas row by row, valid labels, no introduced nulls, unchanged raw-file hash and exact exported CSV read-back. All 15 recorded validation checks passed, together with the detailed equality assertions and CSV read-back check. No estimator/encoder/scaler was fitted or applied. Original in-memory values and CSV bytes are unchanged.

## Unresolved questions: campaign-start availability

The output is a cleaned candidate modeling dataset, **not certified leakage-free**. All remaining fields were retained as approved; collection timing cannot be established from this CSV alone.

- Customer attributes and financial statuses: require campaign-start snapshots, not retrospective changes after subscription.
- previous: verify prior-campaign cutoff excludes current/future events and matches the intended campaign window.
- pdays-derived recency: confirm its reference date. A value calculated at a later contact date is not automatically valid at campaign start; obtain start dates/as-of history before using it predictively. Confirm the meaning/scope of the 4,110 mixed history records without marking them erroneous.
- emp.var.rate/nr.employed (quarterly), cons.price.idx/cons.conf.idx (monthly), euribor3m (daily): confirm publication dates, revision vintage and campaign-start alignment. Last-contact-period economic values may be unavailable at campaign start. No lag or replacement has been invented.
- y: confirm outcome window and follow-up completeness for campaign-start customer prioritization.
- No customer ID, campaign-start timestamp or full dated history exists here. Repeated-client and temporal leakage cannot be excluded; row order is not verified chronology.

Recommendations for discussion: obtain timestamped customer/history snapshots, campaign-start dates and economic publication vintages. Seek team approval for any later recomputation, lagging or additional feature exclusion. Strong socioeconomic correlations persist; no automatic selection was made. No psychographic feature is inferred from call timing.

## Readiness and subsequent-phase boundaries

Approved cleaning is complete and reproducible. Do not train until timing/availability concerns are resolved or an explicit limited-use assumption is approved. Later encode the six categorical predictors; for LR consider training-only scaling of age, previous, economic indicators and an approved conditional recency treatment, keeping recency_available unscaled. Trees/RF ordinarily need no numeric scaling. Exact encoding/scaling methods require the next phase's approval.

No scaling, One-Hot/Label/Ordinal/Target Encoding, log transform, train-test split, cross-validation, SMOTE/undersampling or model training was performed. Only approved category relabelling and deterministic features were applied. Planned next steps are stratified 80/20 and stratified five-fold CV; update counts for 41,176 records rather than old 41,188-based estimates. All learned preprocessing must be fitted on training folds only. Disclose prior whole-dataset EDA when discussing the eventual held-out set. Duplicate deletion alone does not establish client/time-disjoint evaluation.

Deliverables: 02_data_cleaning.ipynb, 02_cleaned_dataset.csv, 02_data_cleaning_summary.md, all in the repository. Team approval is still needed for unresolved feature availability, historical/label definitions, any additional changes, and later encoding/scaling/validation choices. No subsequent phase was started.
