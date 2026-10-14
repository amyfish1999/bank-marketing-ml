# Phase 2A — Preprocessing decision review

Status: recommendations for team review, not implemented decisions. No dataset transformation, split, fitted preprocessing, model training or Phase 2B work has occurred. Existing Phase 1 files are unchanged.

## Sources and evidence boundaries

Reviewed README.md, MSI5001 Project Bank Telemarketing .docx (paragraphs and tables extracted using python-docx), all Markdown and analysis code in 01_eda.ipynb, eda_summary.md, and dataset.csv. Targeted pandas checks verified unknowns, campaign history, duplicate patterns and economic correlations; the entire EDA was not rerun. Counts use all 41,188 records. Source CSV SHA-256: `81fd5eb4b659dddbc704edd90376c32714c3f6a43b887cb686762903bc793f0d`.

**Observed facts** below come from this dataset or explicit source definitions. **Recommendations** are justified proposals, not empirically validated improvements. **Assumptions requiring confirmation** concern collection semantics and information available at prediction time. Descriptive outcome associations cannot prove causes or future model performance. The project plan requires the team to defend decisions with logical reasoning rather than relying on AI authority; this review provides evidence and alternatives for that discussion.

## 1. Unknown values

No pandas-null values are present. Unknown means the corresponding customer attribute/status is not known in the supplied record; the README does not establish why it is unknown (not collected, refused, unavailable or another mechanism). It must not be interpreted as a negative response. These six features are categorical even when stored as integer codes.

| Feature | Unknown code | Count | Percent of all records | Meaning | Recommendation |
|---|---|---:|---:|---|---|
| job | unknown | 330 | 0.8012% | Occupation unspecified | Retain explicit unknown category; one-hot encode later if approved |
| marital | unknown | 80 | 0.1942% | Marital status unspecified; divorced also includes widowed | Retain explicit unknown category; one-hot encode later if approved |
| education | unknown | 1,731 | 4.2027% | Education level unspecified | Retain explicit unknown category; one-hot encode later if approved |
| default | -1 | 8,597 | 20.8726% | Credit default status unavailable, not evidence of no default | Retain explicit unknown category; one-hot encode later if approved |
| housing | -1 | 990 | 2.4036% | Housing-loan status unavailable | Retain explicit unknown category; one-hot encode later if approved |
| loan | -1 | 990 | 2.4036% | Personal-loan status unavailable | Retain explicit unknown category; one-hot encode later if approved |

### Feature-specific comparison and rationale

- **Job:** explicit unknown preserves 330 observations without inventing an occupation. Mode imputation would assign the most common job without evidence; conditional imputation using education/age still rests on unverified assumptions. Dropping loses 0.80% and may select on who reported occupation. Recommend retention; no evidence justifies dropping even though the fraction is small.
- **Marital:** retaining unknown avoids assigning a marital status to 80 clients. Mode imputation falsely labels them married; dropping loses only 0.19% but may bias a distinct reporting group. Small unknown sample makes its effect unstable, so regularization and cautious interpretation are preferable to automatic deletion.
- **Education:** retaining unknown preserves 1,731 records. Mode imputation assumes university education for unknowns and distorts qualifications; conditional imputation might be evaluated later within training folds, with a missingness indicator. Dropping loses 4.20%. Unknown-group subscription is 14.50% versus 11.12% for known education, evidence that deletion changes the observed mix, not proof of informative missingness in deployment.
- **Default:** retain three states (no, yes, unknown); never scale or ordinal-code -1/0/1 as a numeric severity. Unknowns account for 20.8726% (8,597); dropping would remove 443 subscribers. Known records have a 12.88% subscription rate versus 5.15% for unknown records. Mode imputation would label unknowns “no” and erase that distinction. Only 3 records have default=yes, so imputing yes or interpreting its coefficient is especially unsupported. Unknown retention preserves information but can learn a collection-process proxy that may change in deployment. A missingness indicator plus an imputed no value is an alternative representation only if explicitly documented as a placeholder, not inferred truth. Dropping the entire feature is a later sensitivity option if data collection is unreliable, not a recommendation based solely on its missing fraction.
- **Housing and loan:** both have 990 unknowns (2.4036%), and their unknown flags match on every row. This suggests a shared collection pattern but does not establish its cause. Retain explicit categories. Mode imputation invents loan statuses; dropping selects out the same clients. Unknown-group subscription is 10.81% versus 11.28% for known values. Later consider redundancy of the two unknown indicators with regularization, not removal of the underlying loan features.

For every feature, imputation alternatives must be fitted using training-fold data only, retain an unknown indicator when justified, and be evaluated against simple retention. Categorical statuses cannot be sensibly mean-imputed. No missing-at-random mechanism is established, so deletion and conditional imputation cannot be assumed unbiased.

**Observed row-level unknown burden:** 30,488 records have none; 9,034 have one; 1,338 have two; 306 have three; 20 have four; 2 have five. Any-unknown deletion would remove 10,700 records (25.98%); deleting rows with two or more would remove 1,666 (4.04%). Recommend no blanket threshold. An unknown-count feature is an optional later candidate, with collection-proxy/redundancy risks, not an approved transformation.

**Target:** y contains 36,548 no and 4,640 yes; no -1 unknown labels. The plan says remove unknown y. Recommend excluding unknown-target records from supervised training/evaluation if future data contains them, documenting excluded counts and preserving raw records for possible unlabeled use. Do not impute labels. This policy has no effect on the present dataset.

## 2. Pdays sentinel and previous-contact history

README defines pdays=999 as not previously contacted; previous is the number of contacts before the current campaign. The literal descriptions do not fully explain the mixed group. Do not overwrite either field or call these records erroneous.

| Previous | Pdays | Records | Subscribers | Subscription rate |
|---|---|---:|---:|---:|
| 0 | 999 | 35,563 | 3,141 | 8.8322% |
| >0 | 999 | 4,110 | 532 | 12.9440% |
| >0 | Actual recency | 1,515 | 967 | 63.8284% |
| 0 | Actual recency | 0 | 0 | Not applicable |

The 4,110 group is 9.9786% of the dataset and 73.07% of the 5,625 records with previous>0. Its prior-count distribution is 1:3,696; 2:349; 3:50; 4:12; 5:2; 6:1. Actual pdays ranges 0–27, median 6; 999 appears in 39,673 records (96.3217%). High observed response among known-recency records may reflect selection or campaign context; it is not proof of a causal recency effect.

**Recommended representation, subject to approval:** retain previous as a count; define a neutrally named `recency_available = (pdays != 999)`; use numerical actual recency only when available. For an eventual conventional pipeline, represent unavailable recency with a fixed placeholder 0 plus that indicator, so actual zero days remains distinguishable from unavailable recency. Never treat 999 as a measured 999-day interval or derive “never contacted” solely from pdays. For LR, preferably scale using actual recency observations in each training fold and set the standardized unavailable value to 0; this requires an explicitly designed conditional transformer, not a globally fitted mean. Trees need no scaling and can use the placeholder with the indicator.

Alternative: a three-level history category (previous=0/sentinel; previous>0/sentinel; actual recency) plus conditional recency; its levels are descriptive rather than asserted contact outcomes. This retains the 4,110 group but overlaps with previous/availability, so do not automatically include all redundant representations. Another option is recency bands including a sentinel category, at the cost of lost resolution. Native missing-value handling depends on the estimator/version and still benefits from an availability indicator. Deleting the sentinel group removes most observations and is unsuitable; arbitrary recency imputation without an indicator invents timing. Ask the data owner whether previous and pdays cover different campaign windows, contact success definitions, or recency retention rules.

## 3. Duplicate records

**Observed:** 12 exact groups, each a pair (24 involved records); 12 rows beyond first occurrences, or 0.0291% of the dataset. Eleven pairs have y=0 and one pair has y=1; all have previous=0 and pdays=999. No identical full-predictor groups have conflicting y. These rows match across all columns, including call duration, but this is not proof of the same customer. Excluding duration and y yields 2,021 repeated predictor rows beyond first, demonstrating that shared demographic/context profiles alone cannot establish identity.

**Recommendation:** retain pending provenance confirmation; document the small extra weight. Deleting could erase distinct clients/events and alter frequency; retaining ingestion copies could slightly overweight records and allow identical events across future partitions. If confirmed ingestion duplicates, deduplicate only in a documented derived dataset after approval. If unresolved, consider keeping exact predictor-signature groups together in held-out/CV assignment; group on predictors without y, not on labels, and recognize this is a leakage-reduction heuristic, not customer grouping. Grouping broad profiles may combine distinct people and change the estimand. Deduplication and grouping choices need approval before splitting. Later a keep-versus-deduplicate sensitivity check may assess impact inside development data; no such experiment is performed now.

## 4. Encoding recommendations

Recommend one-hot encoding for all nine categorical predictors: job, marital, education, default, housing, loan, contact, month and day_of_week, contingent on the availability audit. Retain unknown levels explicitly. Low cardinality makes this practical and avoids artificial distances/order. For regularized LR, full one-hot with an intercept is workable but individual coefficients are not uniquely interpretable without a convention; use a documented reference-category scheme if coefficient interpretation is required. Trees/RF can use full one-hot; ensure identical category vocabularies and column alignment across training and inference.

**One-hot:** transparent and target-independent; more columns, with unstable sparse levels and potentially less efficient multi-category splits in trees. Recommend train-fitted category vocabularies and a documented fallback for unseen categories; unseen is distinct from the documented unknown state. `handle_unknown='ignore'` is a possible operational fallback but yields an all-zero vector and needs monitoring. Do not infer categories from held-out records. Explicit README vocabularies are schema metadata, not learned frequencies.

**Ordinal:** suitable only for defensible order. Education has partial ordering but professional-course placement and unknown are ambiguous; numeric ranks in LR also impose equal-step effects. Recommend one-hot initially; consider justified education ordering later as a sensitivity option. No/yes statuses can be a binary indicator plus a separate unknown indicator; do not pass -1/0/1 directly. Job/marital/channel have no meaningful order. Month/day integer labels imply a linear trend and do not respect calendar cycles. Sine/cosine month encoding is an alternative assuming smooth annual cycles; absent Jan/Feb and missing year limit the evidence. Weekday cycle features omit weekend observations and impose unjustified smoothness. One-hot is the less assumptive initial proposal.

**Target encoding:** can reduce dimension for high-cardinality variables, but these categories are small enough for one-hot. Rare levels (default=yes 3; education=illiterate 18) would produce noisy target estimates. Recommend against it initially. Any later target encoding needs smoothing and cross-fitting within each CV training fold; validation/test labels must never determine encoded values. Encoding the full dataset before splitting would leak outcomes. No supervised encoder is fitted here.

## 5. Scaling and model-specific pipeline designs (not implemented)

Scaling is an optimization/regularization concern for LR, not a claim that every feature mathematically requires it. For a regularized LR, recommend training-fold StandardScaler for age, approved pre-call campaign count, previous, conditional recency, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m and nr.employed. Their units/ranges differ; common scales make coefficient penalties comparable and improve solver conditioning. Leave binary indicators and one-hot categories unscaled. Duration is excluded. Standard scaling does not make distributions normal or remove outliers. Counts are skewed (campaign max 56, previous max 7); log1p/robust scaling are alternatives only after development validation. Never log negative economic values indiscriminately. No automatic clipping is justified.

| Model | Proposed numerical path | Proposed categorical path | Rationale and limits |
|---|---|---|---|
| Logistic Regression | Sentinel-aware recency representation; StandardScaler on quantitative features; regularized LR later | Explicit unknowns + one-hot; binary availability unscaled | Different units and correlated indicators affect penalties/conditioning; nonlinear count effects may require later justified transformations |
| Decision Tree | Same recency representation; retain other numeric values without scaling | Explicit unknowns + one-hot | Threshold splits do not require scale normalization; rare categories and large count tails still need validation |
| Random Forest | Same numeric path as tree; no scaling | Explicit unknowns + one-hot | Tree splits are insensitive to feature units; correlated indicators can dilute importance and rare levels remain uncertain |

Conceptual order: approved availability/schema exclusion → approved deterministic sentinel/status representation → train-fitted categorical handling and model-specific scaling → optional approved imbalance strategy → estimator. Put learned operations in a pipeline inside grid-search/CV. Fit each transformer only on the CV training portion, refit on the full development set only after selection, then transform/evaluate the held-out set once. Class weighting is simpler to consider than synthetic resampling with categorical indicators; ordinary SMOTE after one-hot can produce fractional category combinations. Any later SMOTENC/undersampling comparison requires a suitable mixed-type representation and training-fold-only application. No imbalance method is chosen or run in Phase 2A.

## 6. Feature availability, leakage and selection

**Working assumption requiring confirmation:** prediction is made immediately before a particular planned call, rather than before the whole campaign. A column recorded after the call is not admissible merely because it is correlated with y. If the objective is customer selection before any calls, use the stricter campaign-start rules below. This document proposes exclusion of duration from the predictor schema; the original dataset retains it unchanged.

| Feature(s) | Pre-call availability audit / recommendation | Confirmation required |
|---|---|---|
| age, job, marital, education, default, housing, loan | Potentially available from customer records, including unknown status | Verify as-of-call snapshots, not retrospective updates after subscription; audit age derivation and status update time |
| duration | Unavailable before call; exclude from realistic predictors | None for exclusion: explicitly required by user/README; no post-call benchmark here |
| campaign | Historical count includes last call; raw final count is not approved for direct use | Before a particular call, completed prior attempts or planned attempt number can be known. `campaign-1` is only valid if each row is a contemporaneous attempt and definitions/counting match; no derivation now. Before campaign start, exclude current-campaign totals |
| month, day_of_week | Planned date can be known before a scheduled call; observed last-contact date may be post-outcome information | Confirm the date refers to this prediction event and schedule was fixed before outcome. Before campaign start, final last-contact date is unavailable; exclude absent known schedule |
| contact | Planned communication channel may be known | Confirm planned versus realized channel and any post-call changes; exclude if it represents outcome-dependent last contact |
| previous, pdays | Prior campaign history could be known before current call | Confirm historical cutoff, campaign scope and 999 semantics; avoid histories updated using current/future contacts |
| economic indicators | Use only information published and available by prediction time | Frequencies (quarterly/monthly/daily) do not prove publication timing. Confirm releases, revisions and lag; exclude unsafe fields pending confirmation |
| y | Outcome label only; never predictor | Confirm label/event window and follow-up completeness |

Until those confirmations, only duration is definitively excluded; other conditional fields are pending availability approval, not certified safe. A conservative future baseline would omit unresolved fields, provided remaining features also have verified snapshots. Absence of full dates/client IDs prevents a definitive as-of audit from the CSV alone. Mental state/busyness raised in the planning document is not measured; do not invent such features or causal interpretations from weekdays.

**Observed socioeconomic redundancy:** emp.var.rate–euribor3m Pearson r=0.9722; euribor3m–nr.employed r=0.9452; emp.var.rate–nr.employed r=0.9070. Price index also correlates with employment variation (0.7753). Confidence has weaker pairwise correlations. Recommend retain verified available indicators as initial candidates with regularized LR; evaluate approved reduced sets within development CV rather than drop on correlation alone. Correlation is not identical information and does not establish predictive value. PCA is an alternative that loses interpretability and must be training-fold fitted; not recommended initially. Trees need no collinearity correction for solvability, but importance/interpretation can be unstable among correlated predictors. No feature selection or importance estimation occurs now.

**Schema investigation:** actual file has 19 predictors plus y (20 columns). README's detailed named list also enumerates 19 predictors: 7 demographics + 3 contact + 4 campaign + 5 socioeconomic = 19. Thus its headline “20 features + 1 target” is internally inconsistent with its own feature list, not evidence of a specific missing column. The planning DOCX confirms 41,188 records but does not name a twentieth predictor or resolve schema completeness. Recommend document the supplied schema and ask the owner whether the headline is a counting error or an omitted field. Do not reconstruct an absent field from external versions of similar datasets.

## 7. Split and validation review — no split performed

The DOCX specifies stratified 80/20: 32,950 development and 8,238 held-out records, then stratified five-fold CV on development (6,590 validation records per fold, 26,360 training records per iteration if records retained). These are rotating train/validation partitions, not five independent trained datasets. Record a reproducible seed and split indices only after approvals. Counts would change if future approved exclusions/grouping alter the sample; stratified grouping may only approximate desired proportions.

Stratification preserves outcome balance but cannot prevent the same customer/events or economic periods crossing partitions. Exact pairs can cross under random assignment; distinct rows can still belong to a repeat client. Signature grouping only mitigates known coincidences. Obtain client IDs for group-aware splitting and exact dates/year for chronological validation if possible. Do not assume row order is chronology; month/day cannot establish temporal order across years. With neither identifier nor chronology, label results as within-sample random-split evaluation, not a validated forecast for future campaigns or unseen clients.

The full dataset has already been used for descriptive EDA. The future holdout can remain untouched for fitting, tuning, thresholds and model comparison, but cannot honestly be called never viewed; document this prior exposure. Prefer a new prospective/external holdout for stronger claims if feasible. Do not use observed full-data group rates for target-derived features or tune choices against the holdout. Select features, imputation, scaling, encoding, resampling, regularization and thresholds exclusively through development data. Grid-search uses the plan's five folds; any repeated tuning can itself overfit CV. Report precision, recall, F1, ROC-AUC, PR-AUC and confusion matrix, with business costs and threshold approved in development. Neither models nor evaluation metrics are calculated here.

## 8. Approval register and Phase 1 alignment

The Phase 1 facts are consistent with targeted rechecks. Its statements that the DOCX is missing are historical and now outdated; Phase 1 files remain unchanged. The new review adopts the planning document's concrete split proportions and candidate models rather than treating them as unspecified. No evidence supports removing the 4,110 history records as errors.

Team sign-off is required before implementation on: unknown retention/rare levels; sentinel representation and history definitions; duplicate retention/grouping; intended prediction time and all conditional availability; one-hot conventions/unseen category behavior; LR scaling/count transformations; socioeconomic candidate/reduced sets; stratified versus group/time validation and limits on generalization; held-out exposure disclosure; imbalance strategy, metrics/business threshold and later model-development scope. Duration exclusion is already explicitly required, but the implementation has not been performed.

See `02_feature_preprocessing_decision_table.md` for every supplied column. Approval status means a proposal awaits team sign-off, not that unexplained decisions are final. Resolve schema/provenance questions before Phase 2B. A dataset's readiness requires checked schema/labels, documented sentinel/unknown policies, an approved as-of feature list, partition safeguards and training-only learned transformations; low missingness alone does not establish readiness.
