# Phase 2C — Split and preprocessing validation summary

## Scope

Implemented only the complete supplied instructions: fixed stratified 80/20 split; unfitted model-specific sklearn preprocessing factories; conditional recency scaling; limited technical assertions. No predictive estimator, GridSearchCV, class resampling or performance evaluation. The pasted request ends mid-sentence during section 9 item 4; additional requirements, filenames or publication instructions were not received.

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

No change to raw or cleaned CSV, existing notebooks or previous summaries. No model training, tuning, resampling or final evaluation. Learned parameters exist only in disposable small-subset test instances, not a production artifact. The factory objects remain unfitted. Missing continuation of the user's pasted request should be checked before additional workflow/publishing requirements are assumed.
