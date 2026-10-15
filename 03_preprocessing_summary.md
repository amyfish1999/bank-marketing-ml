# Phase 2C — Split and preprocessing validation summary

## Scope

Implemented only the complete supplied instructions: fixed stratified 80/20 split; unfitted model-specific sklearn preprocessing factories; conditional recency scaling; limited technical assertions. No predictive estimator, GridSearchCV, class resampling or performance evaluation. The originally pasted request was truncated; the subsequently supplied Sections 9 and 10 have now been reviewed and completed. This completion review makes documentation-only corrections; no preprocessing implementation change was needed.

Reviewed README.md, MSI5001 Project Bank Telemarketing .docx, Phase 2A decision review/table, Phase 2B cleaning notebook/summary and cleaned dataset. Earlier project artifacts are unchanged. The approved cleaned CSV has 41,176 rows, 15 predictors and binary y; validation against original-row duplicate mask confirms the approved 12 keep-first deletions and all original-to-cleaned values. Unknown counts and both recency formulas match Phase 2B; all 4,110 mixed-history records remain. No Phase 2B cleaning was rerun or saved over the input.

## Reproducible partitions

| partition | n | no | yes | no_percent | yes_percent |
| --- | --- | --- | --- | --- | --- |
| development | 32940 | 29229 | 3711 | 88.73406193078324 | 11.265938069216757 |
| held_out | 8236 | 7308 | 928 | 88.73239436619718 | 11.267605633802818 |

Split uses test_size=0.2, random_state=42, stratify=y. 32,940 development and 8,236 held-out rows are disjoint and cover every cleaned position once; repeating the split produced identical ordered arrays. 03_split_indices.json stores zero-based cleaned-file positions, source SHA-256, dimensions and parameters. Verify the file hash before using .iloc; positions are not customer IDs or original CSV line numbers. Required class proportions above are the only held-out outcome report; no held-out features were transformed/profiled to choose preprocessing, and no held-out predictive performance was measured.

## Pipeline decisions implemented

- Six categorical features: full OneHotEncoder(drop=None, handle_unknown='ignore', sparse_output=False). Vocabularies are fit-input-only. Observed unknowns retain distinct one-hot columns; categories absent from fit data, including unknown if absent, yield an all-zero block. Unseen differs from observed unknown. No rare grouping, ordinal/label/target encoding or reference-level dropping.
- Logistic Regression configuration: StandardScaler for age, previous and five economic indicators; custom conditional scaler for recency_days controlled by recency_available; availability remains a separate unscaled bit.
- Decision Tree / Random Forest configurations: same one-hot strategy, all numerical values and the separate recency indicator pass through unchanged.
- Pipeline/ColumnTransformer factories are unfitted on creation and import, cloneable, and export no fitted objects. Output order is categorical blocks, seven quantitative columns, recency_days, recency_available. Feature names are stable for a fitted instance; independent fold widths can vary legitimately with rare-category coverage.

For actual recency samples in a training fold, mean and population standard deviation (ddof=0) exclude every availability=0 placeholder. Transform available values as (days-mean)/scale, set unavailable output days to 0, retain the indicator unchanged. With no available samples use mean=0/scale=1 and warn; with one sample or zero variance use observed mean/unit scale and warn. Validation cannot modify fitted parameters. The indicator distinguishes unavailable placeholders from genuine zero days even when transformed numerical values coincide.

## Technical checks actually run

A 400-record reproducible subset was selected only from development data, then split into 300 fit and 100 technical-validation rows. No complete-development fit/transform was run. The held-out feature matrix was not accessed by technical tests.

| configuration | fit_rows | validation_rows | output_features | status |
| --- | --- | --- | --- | --- |
| logistic_regression | 300 | 100 | 39 | PASS |
| decision_tree | 300 | 100 | 39 | PASS |
| random_forest | 300 | 100 | 39 | PASS |

Five-fold compatibility checks on those same 400 development records used StratifiedKFold(n_splits=5, shuffle=True, random_state=42): each fold fit fresh preprocessing clones on 320 rows and transformed 80 validation rows, for all three configurations. Each fold's vocabulary, ordinary-scaler means, conditional mean/variance and observed-sample count were checked against only its training rows. This was software validation, not model CV scoring. Future model CV must receive untransformed development data and a fresh complete estimator Pipeline, never a preprocessed whole-development matrix.

All technical output shapes/names, finite values, unscaled indicators/tree values, training-only categories, explicit unknowns, synthetic unseen categories and frozen validation-time parameters passed. Synthetic unit tests cover placeholder exclusion, actual zero days, zero/one/constant available samples, invalid inputs, no-refit behavior and cloneability. Run `python -m unittest discover -s tests -v` from repository root. All four standalone tests passed. Notebook code cells also executed successfully. No NaN/infinity or input mutation was introduced.

## Feature availability table

All retained predictors are approved to remain **Provisional**, not verified campaign-start measurements. Technically isolated preprocessing does not certify feature-timing leakage safety.

| feature | assumed_availability | potential_leakage_risk | required_confirmation | status |
| --- | --- | --- | --- | --- |
| age | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| job | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| marital | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| education | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| default | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| housing | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| loan | Customer-record value recorded before campaign start | Retrospective demographic/financial update after campaign or subscription | Customer attribute/status effective date and campaign-start snapshot | Provisional |
| previous | Historical campaigns only, known at campaign start | Current/future-history updates; recency may be calculated at later contact date | Timestamped historical snapshot, campaign-start date, pdays reference date and history scope | Provisional |
| emp.var.rate | Published economic value available by campaign start | Later call-period value or revised publication; shared temporal context | Campaign-start timestamp, publication/revision vintage and as-of join or approved lag | Provisional |
| cons.price.idx | Published economic value available by campaign start | Later call-period value or revised publication; shared temporal context | Campaign-start timestamp, publication/revision vintage and as-of join or approved lag | Provisional |
| cons.conf.idx | Published economic value available by campaign start | Later call-period value or revised publication; shared temporal context | Campaign-start timestamp, publication/revision vintage and as-of join or approved lag | Provisional |
| euribor3m | Published economic value available by campaign start | Later call-period value or revised publication; shared temporal context | Campaign-start timestamp, publication/revision vintage and as-of join or approved lag | Provisional |
| nr.employed | Published economic value available by campaign start | Later call-period value or revised publication; shared temporal context | Campaign-start timestamp, publication/revision vintage and as-of join or approved lag | Provisional |
| recency_available | Historical campaigns only, known at campaign start | Current/future-history updates; recency may be calculated at later contact date | Timestamped historical snapshot, campaign-start date, pdays reference date and history scope | Provisional |
| recency_days | Historical campaigns only, known at campaign start | Current/future-history updates; recency may be calculated at later contact date | Timestamped historical snapshot, campaign-start date, pdays reference date and history scope | Provisional |

## Team discussion and limitations

1. Obtain campaign-start snapshots, historical cutoff/reference dates, publication vintages and outcome-window confirmation. Retaining provisional variables is explicitly approved; it does not establish their availability.
2. Keep rare categories unchanged now; grouping or alternate reference-level coding requires approval. No predictive evidence is claimed for any alternative.
3. Retain correlated economic indicators as approved; any later ablation/regularization decisions must use development-only model validation.
4. No client IDs or historical timestamps means random stratification cannot rule out repeat clients or shared economic periods across partitions. Obtain metadata for future group/time validation; predictor equality is not identity and row order is not verified chronology.
5. Previous full-data EDA was already performed; do not describe the future holdout as never viewed. It remains unused here for fitting, tuning, thresholding or predictive evaluation.

## Artifacts and use

- preprocessing.py: reusable unfitted factories and custom transformer; scikit-learn >=1.2 required (validated here with 1.8.0).
- 03_train_test_preprocessing.ipynb: Colab instructions, dataset checks, split, mathematical explanation, development-only technical tests and availability discussion.
- 03_split_indices.json: reproducible hash-bound row assignments; no scaled/encoded datasets.
- tests/test_preprocessing.py: synthetic automated tests.
- 03_preprocessing_summary.md: this review record.

No change to raw or cleaned CSV, existing notebooks or previous summaries. No model training, tuning, resampling or final evaluation. Learned parameters exist only in disposable small-subset test instances, not a production artifact. The factory objects remain unfitted. The supplied completion requirements are covered by the review below. No commit or push is authorized for these review amendments until team approval.

## Section 9 — Execution and repository requirements: completion review

Review date: 15 October 2026. All five Phase 2C deliverables are inside the repository: the notebook, reusable module, split-index JSON, synthetic tests and this summary. Only this summary and notebook Markdown were amended; completed implementation, execution outputs and code cells are preserved.

The nine original notebook code cells were re-executed in a fresh temporary directory containing only the module and both input CSVs, matching the documented Colab upload-style file layout. The generated manifest matched the existing repository manifest byte-for-byte. No repository split file was rewritten. This verifies portable path handling and standard Python execution with scikit-learn 1.8.0; a live hosted Google Colab session was not available and is not claimed. The documented minimum is scikit-learn 1.2. The notebook's runtime artifact is **only 03_split_indices.json**; this Markdown summary is a bundled repository deliverable, not generated by the notebook.

Both input CSVs were verified unchanged by SHA-256 before/after execution and against their committed Git content. Pipeline code, standalone tests and the saved split manifest were unchanged as well. No predictive estimator was trained, no hyperparameters tuned, no resampling performed, and no held-out predictive evaluation or transformation occurred. Test-label counts remain the previously approved stratification report only. Whole-file provenance checks are not predictive evaluation. No next-phase work was performed.

## Section 10 — Final completion review for approval

### Implemented work retained

Reproducible stratified 80/20 partitions (32,940 development / 8,236 held-out); six-feature full one-hot encoding; LR ordinary and conditional recency scaling; unscaled tree/RF configurations; unfitted Pipeline/ColumnTransformer factories; five-fold configuration; hash-bound split indices; development-only software validation; provisional-availability table and discussion. No scaled/encoded CSV or fitted production artifact is saved.

### Technical test results

| Test/check | Scope and result |
|---|---|
| Existing cleaned-artifact validation | PASS — 41,176 × 16 schema, binary labels, excluded columns, exact original-to-cleaned values, 12 approved duplicate deletions, retained unknowns and both recency formulas |
| Split reproducibility and integrity | PASS — repeated ordered indices identical; development/held-out disjoint and exhaustive; source hash verified; isolated rerun manifest byte-for-byte identical |
| Standalone test_observed_only_and_no_refit | PASS — observed-only mean/variance, placeholder independence, genuine zero days, feature names and frozen statistics after validation transform |
| Standalone test_safe_fallbacks | PASS — zero available, one available, constant and all-zero actual recency; unit-scale safeguards, warnings, finite outputs and unchanged availability indicator |
| Standalone test_invalid_input_and_unfitted | PASS — rejects transform-before-fit, NaN/infinity, negative recency, invalid indicator, nonzero placeholder and incorrect input names |
| Standalone test_factory_is_unfitted_and_cloneable | PASS — all three fresh configurations clone correctly, remain unfitted and reject unsupported configuration names |
| Three configuration fit/transform checks | PASS — each fits 300 development-subset rows and transforms 100 technical-validation rows, yielding 39 named finite features in this subset |
| Categories and output schema | PASS — vocabularies equal fit-row levels; full one-hot; observed unknowns preserved; synthetic unseen job produces an all-zero job block without failure; fitted output dimensions/names consistent |
| Model-specific numerical behavior | PASS — ordinary scaler means equal fit rows; tree/RF numerical values unchanged; conditional recency excludes unavailable values and leaves availability unscaled |
| Five-fold software compatibility | PASS — five folds × three configurations; cloned preprocessors fit on 320 and transform 80 rows per fold within the same 400-record development subset; fold-specific parameters verified |
| Validation isolation | PASS — vocabulary and scaler parameter snapshots unchanged by validation transform; conditional statistics match only available training recencies |
| Full notebook portability check | PASS — all nine code cells run from an isolated upload-style directory; standard imports/relative paths and JSON export work; live hosted Colab not exercised |
| Dataset/artifact integrity | PASS — both CSVs, module, tests and saved split manifest unchanged; no NaN/infinity introduced or predictive artifact generated |

Reproduce standalone tests with `python -m unittest discover -s tests -v`. Detailed executable pipeline assertions remain in the notebook. Results are technical correctness checks, not estimates of predictive performance.

### All Provisional features

All 15 predictors remain provisional for campaign-start timing: **age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days**. Their meanings can be documented while their as-of availability remains unverified. The feature-availability table above gives the required evidence for each.

### Unresolved team decisions

1. Confirm customer demographic/financial snapshots existed before campaign start, historical-contact cutoff and pdays reference date, economic publication/revision vintages, and the target outcome/follow-up window.
2. Decide whether rare categories need grouping or a different coding convention; current approved full one-hot stays unchanged. A category absent from fit data, including unknown, is handled as unseen rather than learning its presence from held-out data.
3. Decide whether correlated socioeconomic indicators should remain together in future models; no feature selection or model comparison has been performed.
4. Determine whether the lack of customer identifiers and dated campaign history is acceptable for the intended claim, or obtain metadata for approved group/time validation. Random stratification and duplicate deletion cannot certify unseen-customer/future-campaign generalization.
5. Disclose prior full-data EDA; the holdout is unused for fitting/tuning/performance evaluation here, not historically never viewed. Approve any later preprocessing/validation revisions before implementation.

### Training-only fitting confirmation

All fits on real data occurred only on the approved small development subset: 300 training rows for direct technical checks, or each small fold's 320 training rows. Synthetic fits are unit-test fixtures only. No preprocessing was fitted on the complete dataset, complete development partition, validation rows or held-out rows. Each future model CV iteration must clone an unfitted complete estimator pipeline and fit vocabularies, ordinary scaling and conditional recency statistics within that iteration's training fold. Existing APIs support this discipline but cannot prevent a caller from supplying the wrong rows; the future workflow must enforce it. No complete-development preprocessed matrix is available for accidental CV reuse, and no fitted production object was exported.

**Review status:** Sections 9 and 10 are complete; awaiting team approval. No new commit or push was made for this completion review, and the next development phase has not started.
