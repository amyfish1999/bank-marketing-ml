# Phase 6B — Final model-selection and pre-holdout evaluation plan

Version 1.0 **proposed lock, pending team approval**, 16 October 2026 (Asia/Singapore). Source: latest fetched merged main `7d8678d`, including Phase 6A. No model has been trained, tuned, threshold-fitted or evaluated in this phase. No held-out records were parsed or inspected. Companion: [feature availability contract](10_feature_availability_matrix.md).

## Executive recommendation and decision status

Recommend **original HistGradientBoosting (HGB), Full 15-feature set**, as the primary academic evaluation scenario, with fixed-capacity **top 10%** as the illustrative primary business reporting scenario. AP remains the primary predictive metric; ROC-AUC is secondary. Report top 5% and 20% as predefined secondary capacities and threshold .50 classification metrics as reference diagnostics. Ten percent is a research convention requested for this plan, not a bank-confirmed capacity or profit optimum.

Recommend **original HGB, Customer Attributes Only**, as one conservative information-requirement sensitivity. Keep original LR as a simple secondary benchmark on both these feature sets. No feature is currently Verified. Full-feature evaluation must therefore be labelled **conditional historical/academic research**, not verified pre-campaign deployment. Customer-only is also Provisional; fewer dependencies do not prove time safety.

The scenario roster, grids, metrics and policies below form a proposed locked protocol. It becomes approved only after recorded team sign-off; this document does not authorize execution. No fitted final hyperparameters exist yet. A future development-only search selects them by the rule below, not by voting among outer-fold winners or inspecting held-out results. No held-out performance acceptance threshold or financial target is invented.

## 1. Consolidated experimental evidence

All figures in this section are imported from approved summaries, not new experiments. SD is descriptive sample SD across five folds (ddof=1), not an independent confidence interval. Different designs are explicitly separated. Untuned/nested AP rows are means of fold metrics, not AP recomputed after pooling OOF scores; pooled business counts are separately labelled.

### Model comparison, untuned versus nested versus tuning-selected scores

| Design / source | Model | AP mean ± sample SD | ROC-AUC mean ± sample SD |
| --- | --- | --- | --- |
| Untuned five-fold OOF — Phase 4 | DecisionTree | 0.180763 ± 0.008793 | 0.619816 ± 0.011450 |
| Untuned five-fold OOF — Phase 4 | LogisticRegression | 0.422181 ± 0.011316 | 0.762279 ± 0.012382 |
| Untuned five-fold OOF — Phase 4 | RandomForest | 0.361307 ± 0.010715 | 0.760706 ± 0.007271 |
| Untuned five-fold OOF — Phase 4B | HistGradientBoosting | 0.439412 ± 0.010735 | 0.789919 ± 0.008285 |
| Nested outer CV, inner AP tuning — Phase 5A | HistGradientBoosting | 0.448145 ± 0.014219 | 0.794911 ± 0.011816 |
| Nested outer CV, inner AP tuning — Phase 5A | LogisticRegression | 0.422429 ± 0.011606 | 0.761875 ± 0.012192 |
| Nested outer CV, inner AP tuning — Phase 5A | RandomForest | 0.443930 ± 0.018936 | 0.790424 ± 0.010734 |
| Selected tuning-CV, potentially optimistic — Phase 4 | DecisionTree | 0.420499 ± 0.016574 | 0.771797 ± 0.007445 |
| Selected tuning-CV, potentially optimistic — Phase 4 | LogisticRegression | 0.422429 ± 0.011606 | 0.761875 ± 0.012192 |
| Selected tuning-CV, potentially optimistic — Phase 4 | RandomForest | 0.445417 ± 0.016226 | 0.791376 ± 0.011315 |
| Selected tuning-CV, potentially optimistic — Phase 4B | HistGradientBoosting | 0.448069 ± 0.015163 | 0.794969 ± 0.012023 |

Sources: [Phase 4](05_model_comparison_summary.md), [Phase 4B](05b_hist_gradient_boosting_summary.md), [Phase 5A](06_nested_cv_targeting_summary.md). Small reconstructed historical rounding differences of approximately 1e-6 are documented in Phase 4B. Selected tuning-CV estimates reuse model-selection folds and may be optimistic; do not rank them as independent test performance or silently substitute them for nested outer CV. DT was not included in Phase 5A nested CV, so it has no nested result here.

HGB exceeds RF nested mean AP by 0.004215, but RF leads in one of five outer folds and no significance test establishes a winner. At pooled development top 10%, HGB captures 1,628 subscribers versus RF 1,588 and LR 1,564 among 3,294 contacts. HGB's small advantage over RF and greater advantage over LR support an academic shortlist, not a deployment guarantee. These pooled outer probabilities come from five different fitted models; fold-local evidence is also retained in Phase 5A.

### Threshold-policy evidence — Phase 5B-1 outer validation

| Model | Policy | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Reference_0.50 | 0.667746 ± 0.015987 | 0.218813 ± 0.014761 | 0.329222 ± 0.014903 |
| HistGradientBoosting | Training_F1 | 0.428506 ± 0.014222 | 0.586634 ± 0.025850 | 0.495146 ± 0.016996 |
| HistGradientBoosting | Training_Precision50 | 0.527200 ± 0.013837 | 0.379681 ± 0.008766 | 0.441264 ± 0.004494 |
| LogisticRegression | Reference_0.50 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 |
| LogisticRegression | Training_F1 | 0.438715 ± 0.012656 | 0.500136 ± 0.014471 | 0.467336 ± 0.011666 |
| LogisticRegression | Training_Precision50 | 0.531257 ± 0.020313 | 0.330098 ± 0.012439 | 0.407013 ± 0.012233 |

These are outer-fold evaluations of thresholds selected exclusively on the corresponding outer-training data after inner-only hyperparameter selection; they are not globally optimized OOF thresholds. AP/ROC-AUC do not change when only the decision threshold changes. F1 selection chose .20 for LR in all folds and .20/.15 for HGB; the illustrative precision>=50% rule selected .35 in every fold. Those are historical fold decisions, **not final-model thresholds**.

Compared with HGB .50, the training-F1 policy substantially raises recall and contact volume while lowering precision. Pooled HGB contact counts were 1,218 (.50), 5,081 (F1) and 2,675 (precision-constrained), versus 3,294 for top 10%. These policies pursue different objectives and capacities; none demonstrates causal response or known financial optimality. Every observed original-arm validation fold met the illustrative 50% target for its constrained rule, but that is not a future precision guarantee. See [Phase 5B-1](07_threshold_decision_summary.md).

### Imbalance treatments — Phase 5B-2 nested treatment comparison

| Model | Original AP mean ± sample SD | Balanced AP mean ± sample SD | RandomUnderSampler AP mean ± sample SD |
| --- | --- | --- | --- |
| HGB | 0.448145 ± 0.014219 | 0.450883 ± 0.015341 | 0.436259 ± 0.019079 |
| LR | 0.422429 ± 0.011606 | 0.420526 ± 0.011461 | 0.419671 ± 0.012471 |

Balanced HGB's +0.002738 AP advantage was small and capacity-dependent: it captured +13 / -18 / -6 subscribers versus original HGB at pooled top 5% / 10% / 20%. It is a secondary research alternative, not promoted into the final roster. HGB undersampling lost 17 / 50 / 29 subscribers at equal capacities and lowered AP; both LR treatments lowered mean AP. Deprioritize RandomUnderSampler for this final original-model protocol. These conclusions concern the tested grids/full features and do not prove treatments cannot help other settings.

Original HGB's training-F1 F1-score was 0.495146 versus balanced 0.491954 and undersampled 0.489511. Thus recall gains at .50 are not sufficient evidence of improvement beyond threshold-only strategies. Weighted/resampled F1 thresholds hit the .60 grid boundary, and their precision-constrained rules found no feasible candidate in .10–.60 and explicitly abstained. This is grid-limited infeasibility, not proof higher thresholds cannot qualify. No threshold-range expansion or calibration is included now. See [Phase 5B-2](08_imbalance_treatment_summary.md).

### Feature sensitivity — Phase 6A nested development analysis

| feature_group | predictors | HGB AP mean ± sample SD | LR AP mean ± sample SD |
| --- | --- | --- | --- |
| Full | 15 | 0.448145 ± 0.014219 | 0.422429 ± 0.011606 |
| No Economic Indicators | 10 | 0.351146 ± 0.015153 | 0.334394 ± 0.021340 |
| No Previous Campaign History | 12 | 0.389129 ± 0.009401 | 0.355256 ± 0.013265 |
| Customer Attributes Only | 7 | 0.232569 ± 0.009506 | 0.202251 ± 0.015223 |

Each subset was separately retuned within its own outer-training partitions using the same approved family grids. This is development-only sensitivity after prior model-family exploration, not independent confirmation of a newly chosen subset. HGB has higher mean AP than LR for all four groups. HGB mean AP falls by 0.096999 without economics, 0.059017 without history, and 0.215576 with customer-only inputs; effects need not add because groups share information/interact.

HGB pooled outer-OOF targeting diagnostics (all groups have identical capacity within each fraction):

| model | feature_group | fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 0.050000 | 1647 | 1005 | 0.610200 | 0.270816 | 5.416330 |
| HistGradientBoosting | Full | 0.100000 | 3294 | 1628 | 0.494232 | 0.438696 | 4.386958 |
| HistGradientBoosting | Full | 0.200000 | 6588 | 2377 | 0.360808 | 0.640528 | 3.202641 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 1647 | 947 | 0.574985 | 0.255187 | 5.103746 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 3294 | 1300 | 0.394657 | 0.350310 | 3.503099 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 6588 | 1707 | 0.259107 | 0.459984 | 2.299919 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 1647 | 869 | 0.527626 | 0.234169 | 4.683374 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 3294 | 1540 | 0.467517 | 0.414982 | 4.149825 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 6588 | 2356 | 0.357620 | 0.634869 | 3.174347 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 1647 | 640 | 0.388585 | 0.172460 | 3.449205 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 3294 | 926 | 0.281117 | 0.249528 | 2.495284 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 6588 | 1387 | 0.210534 | 0.373754 | 1.868769 |

At top 5%, no-economics HGB captures more than no-history HGB despite lower overall AP; at top 20%, no-history captures 2,356 versus full 2,377. Contact capacity affects the relevance of a performance difference. Fold-local tables in [Phase 6A](09_feature_ablation_summary.md) complement pooling, which mixes score scales across fitted models. Customer-only LR predicts no positives at .50 but has AP 0.202251; high accuracy or low .50 recall must not be confused with ranking ability. No ablation result verifies timing or proves causal feature influence.

### Complexity, interpretability and unresolved validity

LR is the cheaper/simpler benchmark: regularized linear log-odds coefficients can be described, but scaling, full dummy coding and correlated economic variables complicate attribution. HGB models nonlinear effects/interactions through boosted trees and is less directly interpretable; its flexibility and compute are costs, not automatic advantages. Historical DT exposes rules but may be unstable/large; RF averages trees and has less simple interpretation. Impurity importance can favor rich split opportunities and redistribute importance among correlated variables; neither importance nor coefficients are causal evidence.

Keep RF and DT in historical comparisons only. Phase 5A measured about 403.88 seconds for HGB nested searches/refits versus LR 7.88 seconds and RF 395.84 seconds; Phase 6A's eight procedures took about 1,512.60 seconds including audits/figures/tests. These are historical, audit-inclusive runtimes, not controlled speed guarantees. Final proposed searches are smaller than the nested study but still require execution and validation later.

All studies share missing customer IDs/timestamps, unresolved campaign-start/economic/history snapshots, prior whole-dataset EDA and development-driven model/grid exploration. Random stratified folds allow repeated-customer and shared-period overlap. Nested fitting controls direct preprocessing/selection leakage within each experiment; it does not establish unseen-client/future-campaign transportability or erase prior exposure. The held-out set has not been used for predictive development, but prior whole-data EDA means it is not pristine data never previously viewed.

## 2. Availability contract and conditional shortlist

The companion matrix documents all 15 variables, original names, meanings, timing requirements, existing/missing evidence and statuses. **All 15 remain Provisional; none is Verified.** Deployment eligibility requires row-aligned evidence of customer/status snapshots, prior-history cutoff and recency reference dates, publication/revision vintages, t0 definition and outcome/follow-up window. A semantic README definition or high AP is insufficient.

| Existing group | Original HGB / original LR development mean AP | Conditional information requirement | Role before held-out access |
| --- | --- | --- | --- |
| Full (15) | 0.448145 / 0.422429 | Customer + history + economic inputs and outcome contract verified for prospective claims | Primary HGB conditional academic reference; LR benchmark |
| No Economic Indicators (10) | 0.351146 / 0.334394 | Customer/history evidence verified; economic availability unresolved | Retain as development-evidence alternative; not in default held-out roster |
| No Previous Campaign History (12) | 0.389129 / 0.355256 | Customer/economic evidence verified; history timing unresolved | Retain as development-evidence alternative; not in default held-out roster |
| Customer Attributes Only (7) | 0.232569 / 0.202251 | All seven customer snapshots and outcome contract verified for prospective claims | Conservative HGB sensitivity; LR sensitivity benchmark |

Exact ordered membership is in the matrix. Customer Attributes Only = age, job, marital, education, default, housing, loan. Full preserves the approved FEATURES sequence. No new variables, interactions, lagged features, label definitions or data cleaning are proposed for this frozen-data evaluation.

If external evidence arrives before approval, the team may amend the primary information requirement/roster using that evidence and development results, explicitly documenting the reason and re-locking before test access. There is **no automatic switch** of primary scenario based on later test scores, and no automatic addition of the middle two subsets. If timing remains unverifiable, the default academic roster below can proceed only after explicit acknowledgment of historical/conditional interpretation; no model may be described as verified deployable. If retained values contradict the source contract, stop rather than silently repair the frozen test data.

## 3. Proposed fixed scenario roster

| ID | Role | Model and feature set | Class weighting / sampling | Reporting policies |
| --- | --- | --- | --- | --- |
| P1 | Sole primary academic scenario | Original HGB, Full 15 | None / none | AP primary; ROC-AUC secondary; top 10% primary business capacity, top 5%/20% secondary; .50 classification reference |
| S1 | Conservative information-requirement sensitivity | Original HGB, Customer Attributes Only 7 | None / none | Same predefined metrics/capacities and .50 reference |
| B1 | Simple full-feature benchmark, secondary | Original LR, Full 15 | None / none | Same predefined metrics/capacities and .50 reference |
| B2 | Simple customer-only benchmark, secondary | Original LR, Customer Attributes Only 7 | None / none | Same predefined metrics/capacities and .50 reference |

The team must approve all four entries or revise this roster **before** test access. Secondary analyses are descriptive sensitivity/benchmark reports, not an opportunity to re-designate a test winner as primary. Balanced HGB, RandomUnderSampler, SMOTE/SMOTENC, RF and DT are not fitted or tested under this proposed final roster. No new family searches.

## 4. Policy A versus Policy B

**Policy A — fixed capacity (recommended primary business reporting).** Use the fitted model's positive-class score; order descending, ties ascending immutable cleaned-row position. K=ceil(fraction*N); take exactly K rows without outcome-informed tie breaking. Top 10% is illustrative primary reporting; top 5% and 20% are predefined secondary scenarios. On the planned N=8,236 held-out cohort, these imply **824 primary contacts**, with **412** and **1,648** secondary contacts. These are calculations from the saved partition size, not inspection of test records or a known bank budget. No numeric probability threshold is learned for ranking. The top-K cutoff is determined solely by the unlabeled cohort scores under the frozen capacity rule.

**Policy B — fixed probability threshold (secondary reference).** Use probability>=0.50, positive class 1. It does not enforce a fixed contact capacity. Report actual volume and classification metrics; do not call .50 optimal, calibrated or guaranteed profitable. The same .50 convention may be applied as a reference to every subset; learned full-feature thresholds (.15/.20/.35) must not be transplanted to reduced-feature models or to a new final fit.

**Optional training-selected policies are discussed, not included in the default roster.** If the team elects one before test access, amend the protocol first. After that subset's own development-only AP search, obtain five-fold development OOF probabilities from fresh complete pipelines at its selected hyperparameters. Hyperparameter selection used all development labels, so these conditional OOF scores are training-side threshold-fitting data, not unbiased performance estimates. Select and freeze that model/subset's threshold using only these probabilities, then fit/refit the selected pipeline on all development rows; never use test probabilities/labels to fit or calibrate it.

To preserve the prior threshold design if approved: grid [.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60]; maximize F1, ties higher threshold; or maximize recall subject to positive contact count and empirical precision>=.50, ties higher precision then higher threshold. The precision target is illustrative. If no candidate qualifies within that grid, freeze explicit abstention/zero contacts; precision/recall/F1 use zero_division=0 and are not reported as a met constraint. Any wider grid/calibration requires a pre-test amendment and new training-only fitting, never test-driven extension. Such fitting is not executed or budgeted in this phase.

All policy results identify historical subscribers among previously observed marketing records. Predictive lift is not incremental campaign uplift. No known call cost, product value, bank capacity, treatment effect or revenue is supplied; no financial optimum or causal claim follows.

## 5. Exact development-only fitting rule — planned, not executed

1. Verify source digests and saved positional indices below before selecting rows. Load only development records; preserve saved order and target 0/1. Do not regenerate a split, rerun cleaning, inspect held-out features/labels, or construct a global encoded/scaled matrix.
2. For each of P1/S1/B1/B2 independently, construct a **fresh unfitted complete sklearn Pipeline**: approved subset preprocessing, optional stateless representation/audit guard returning values unchanged, classifier. Use `make_preprocessor('decision_tree')` for HGB and `make_preprocessor('logistic_regression')` for LR. For customer-only, reuse the notebook-only Phase 6A adapter: filter fresh ColumnTransformer column lists and remove empty recency component, without modifying preprocessing.py or zero-filling excluded features. Verify full equivalence to the factory with training-only fixtures before final access.
3. CV is StratifiedKFold(n_splits=5, shuffle=True, random_state=42) on the ordered 32,940 development rows, identical to approved outer fold positions. Use fresh encoder/scaler fitting in each candidate's training fold. Labels may be used for development AP scoring only. HGB uses numeric one-hot features, unscaled numeric values and categorical_features=None; no native categorical handling.
4. Run each scenario's own GridSearchCV with the exact grids below, a callable scorer returning {'AP': average_precision_score(y_validation, estimator.predict_proba(X_validation)[:, positive_class_index])}, refit='AP', n_jobs=1, error_score='raise', no sample/class weighting and no resampling. Use the previously approved named positive-probability AP scorer; do not silently switch LR scoring to decision_function through the built-in scorer. Positive_class_index must identify classifier class 1. Select **largest arithmetic mean five-fold AP**. Do not select by ROC-AUC, top-K, .50 F1 or a rounded display score. If exact stored means tie, take the first candidate in sklearn ParameterGrid order (sorted parameter keys; value lists in the order below). Record full candidate order and unrounded scores. Do not use outer-fold winners as automatically optimal final settings.
5. GridSearchCV's selected-pipeline refit is the permitted final fit on **all 32,940 development rows**, after CV selection; preprocessing is then fitted on all development for that final estimator only. It never includes held-out rows. This is distinct from prohibited global preprocessing before CV. The new full-development CV best score is a selection estimate, not independent final performance. No final full-development search/refit is executed now.
6. Assert fresh vocabularies/scalers within CV, observed-only recency statistics, frozen prediction transforms, finite arrays/probabilities, class order [0,1], no unexpected convergence/model warnings, source/index integrity and no held-out overlap. A failure halts release before test access. Investigate on development/synthetic data; document any substantive amendment and re-approve rather than quietly changing grids, dropping rows or choosing a different model.
7. Record environment versions, candidate results, selected parameters, feature order/output names, fitted preprocessing statistics, random seeds, model artifact digests and chosen reporting policies. Freeze all four estimators/roles before opening any test records. No probability calibration or optional threshold fitting under the default protocol.

| Model | Fixed configuration | Allowed grid (parameter names prefixed classifier__) | Candidates / CV fits / final refits per scenario |
| --- | --- | --- | --- |
| HGB | HistGradientBoostingClassifier(random_state=42, class_weight=None, early_stopping=False, categorical_features=None); remaining sklearn 1.8.0 defaults, including loss='log_loss', min_samples_leaf=20 | learning_rate=[0.05,0.1]; max_iter=[100,200]; max_leaf_nodes=[15,31]; l2_regularization=[0.0,1.0] | 16 / 80 / 1 |
| LR | LogisticRegression(solver='lbfgs', default L2, max_iter=1000, random_state=42, class_weight=None) | C=[0.1,1.0,10.0] | 3 / 15 / 1 |

Proposed four-scenario budget: 190 candidate-fold fits +4 final refits = **194 fits**, not executed. Seeds and candidate lists are fixed; do not expand a search based on test results. Use the previously tested sklearn 1.8.0, pandas 2.2.3 and NumPy 2.3.5 environment (record other dependency versions). No new feature handling, rare-category grouping, encoding, imputation, scaling or clipping is approved by this plan.

## 6. Locked held-out evaluation protocol — future authorized execution only

### Provenance and frozen assignment

| Artifact | SHA-256 |
| --- | --- |
| dataset.csv | 81fd5eb4b659dddbc704edd90376c32714c3f6a43b887cb686762903bc793f0d |
| 02_cleaned_dataset.csv | c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49 |
| 03_split_indices.json | 397e6e9c66ba3b6b5f6bef6232e00dc392c9ae9d77fdfda28a2d7dc02693596b |
| preprocessing.py | 3959b4db9a561be5bf7373dfcf82ab85c24a288250e26180599a403b7e551ed8 |
| 09_feature_ablation.ipynb | b753760b1f329cb89882e872a2c594e4606e8db61335ff2fa8212c1f56f9e662 |

The cleaned SHA binds content **and row order** to `03_split_indices.json`: 41,176 cleaned rows; development 32,940 / held-out 8,236, ordered zero-based CSV positions, random_state=42, test_size=.2, stratify=y. Verify uniqueness, bounds, disjointness and exhaustive coverage using positions only. No new split or customer identity inferred from these positions. Approved development validation-position checksum: `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4`. Whole-file byte hashing is integrity verification, not inspection of held-out records. Raw CSV is not parsed for this plan.

### Release gate before reading the test partition

Obtain recorded approval of both documents, four scenario IDs/roles, research-only interpretation if timing remains unresolved, exact grids/tie rule, feature order, metrics, capacities, uncertainty method and prohibitions. Record source commit and digests of the approved plans. Complete development-only fitting/audits and freeze estimator artifact digests, selected hyperparameters and policies. There must be no unresolved training/audit error. No held-out previews, distributions, missingness checks, category browsing or partial scores to guide these choices.

### One batch of evaluation and fixed outputs

After that separate authorization, select only the saved held-out rows in saved order, with no removal/rebalancing/relabeling. For all four frozen pipelines, transform with fitted development-only preprocessing and produce one positive-class probability vector, N=8,236. No fit/fit_transform, vocabulary update, scaler update, calibration or threshold selection on test inputs or labels. Unseen categories use the preapproved all-zero block, not a newly fitted encoder. Check only prespecified technical schema/finite/row-alignment conditions for execution correctness; test issues cannot be used for adaptive preprocessing.

Compute all predeclared reports in a single evaluation batch for the frozen roster; do not inspect one scenario first and decide whether to evaluate another. Preserve predictions, row positions, code/version logs and metrics so rerendering tables does not become a second modeling iteration.

| Output | Frozen definition / reporting role |
| --- | --- |
| Primary predictive metric | Average Precision, sklearn average_precision_score(y, positive_probability); not trapezoidal PR area. P1 is primary; S1/B1/B2 labelled secondary |
| Secondary ranking metric | ROC-AUC from the same probabilities |
| Primary business scenario | Top 10%: K=824. Precision@K=captured/K; Recall@K=captured/actual positives; Lift@K=Precision@K/cohort positive prevalence |
| Secondary business scenarios | Top 5% (K=412), top 20% (K=1648), same formulas and deterministic ties; report contacts and captured historical subscribers for each |
| Classification reference | Probability>=.50 for accuracy, precision, recall, F1, predicted-positive count/rate and confusion matrix, rows actual [0,1], columns predicted [0,1] = [[TN,FP],[FN,TP]]; precision/recall/F1 zero_division=0 |
| Diagnostic plots | ROC and precision-recall curves and .50 confusion matrix for each fixed scenario, labelled held-out once authorized; no optimal cutoff highlighted/selected from curves |
| Context | Report observed test prevalence only as evaluation context after release; do not reweight to development prevalence or interpret accuracy alone |

If the cohort unexpectedly lacks a target class, explicitly mark mathematically undefined metrics/intervals rather than inventing values or changing the cohort. If predictions/row alignment fail technical assertions, stop and log the failure; no silent exclusion of problematic observations. If labels/scores have already been exposed, disclose exposure and obtain review before any correction; do not restore a pristine-holdout claim.

### Performance uncertainty and its limits

Proposed method, requiring pre-test team approval: 2,000 paired stratified **metric-bootstrap** replicates, random_state=42, sampling held-out rows with replacement within each observed target class to keep original class counts. Use identical draw positions for every frozen scenario, no estimator refitting or training resampling. Recompute AP, ROC-AUC, .50 classification metrics and Top-K metrics on each resampled cohort; same capacities/ceil rule. For duplicate draws use descending score, original cleaned-row position, then draw-occurrence position for outcome-independent deterministic ties. Report 2.5th/97.5th percentiles as descriptive 95% intervals conditional on fitted models and observed class balance. Contact volume and captured-subscriber counts remain explicit; mark zero-contact precision with the stated convention.

This evaluation-only bootstrap is not an imbalance treatment, probability calibration or model retraining. It does not account for uncertainty from training/model-family/subset selection, unknown client clustering, temporal overlap, feature timing or prevalence shift. Missing IDs/dates make row-wise intervals potentially optimistic. CV sample SD is a separate descriptive quantity, not substituted for a test interval. Multiple secondary comparisons are descriptive, without a significance-winner or multiplicity-free inference claim. Do not use interval overlap, bootstrap differences or a surprising test result to reselect the primary scenario. No uncertainty computation occurs in Phase 6B.

### Prohibition on test-informed iteration

Once any test feature/label distribution or score is exposed, do not choose or alter model family, feature set, hyperparameters, capacity, thresholds, calibration, cleaning, resampling, reporting roster, metric definitions or uncertainty method. No new grid expansion, feature ablation, class weighting or repeated-test tuning. Report poor results and limitations faithfully, including all secondary scenarios. A later scientifically necessary redesign requires a separately approved study and genuinely new evaluation data; the current test set becomes exposed, not reusable as untouched validation. Re-rendering the same frozen predictions is allowed; it is not permission to refit or select.

## 7. Technical integrity review for this planning phase

Inspected approved module, saved manifest, summaries and relevant notebook specifications; no modeling cells were executed. Confirmed approved source digests above and saved position counts/uniqueness/disjoint coverage without loading CSV rows. All pre-existing tracked files are compared byte-for-byte with main HEAD during final document verification. Existing Phase 6A records 1,940 audited fits/probability calls, four preprocessing tests, original-factory full-equivalence, full-feature Phase 5A replication and zero model warnings; those are **previous execution evidence**, not new training/test results from this phase.

| Safeguard | Preserved plan / evidence |
| --- | --- |
| Approved cleaning | Use frozen cleaned CSV: prior approved keep-first removal of 12 exact duplicates, unknown category mapping/retention, approved exclusions and two deterministic recency fields; do not repeat cleaning or modify rows |
| One-hot | Six categorical variables, OneHotEncoder(drop=None, handle_unknown='ignore', sparse_output=False); learn levels only from current fitting rows |
| LR numeric scaling | StandardScaler on selected quantitative columns, training-fold mean/variance only; final scaler fitted on development only after selection |
| Conditional recency | When present, estimate mean/population SD only from fitting availability=1 rows; unavailable transformed days stay 0, indicator unscaled; original zero/one/constant-observation fallbacks unchanged |
| Tree recency | HGB numeric/recency passthrough; no 999 sentinel, availability separate; numeric one-hot indicators, native categorical handling off |
| History exclusions | Remove previous and both recency inputs and the entire recency transformer in customer-only; no zero-filled substitutes |
| Fresh pipeline CV | Each candidate/fold clones a fresh complete unfitted pipeline on raw selected development columns; no globally learned encoded/scaled input |
| Original HGB | class_weight=None, no random under/oversampling, SMOTE/SMOTENC or internal early-stopping split |
| Split and code preservation | Same ordered saved indices, unchanged preprocessing.py and all historical notebooks/data; selected winning final refit uses development only |
| Held-out isolation | Phase 6B reads metadata/documents and file bytes for integrity only; no held-out observations loaded, fitted, plotted or scored |

Unit tests and modeling experiments were not rerun because this phase changes only methodological documents. Missing availability/label evidence remains explicitly missing; technical preprocessing correctness is not a substitute for it.

## 8. Required team approvals and handoff

1. Accept P1 as the sole primary **conditional historical/academic** scenario if availability remains unverified, with S1 conservative sensitivity and B1/B2 secondary LR benchmarks; or revise and re-lock the roster before any test access. Confirm that no deployment-readiness claim is permitted.
2. Approve the feature contract, responsibility for obtaining row-aligned timing evidence, campaign-start definition and outcome window/follow-up interpretation. No field becomes Verified merely by approving academic use.
3. Approve AP primary, ROC-AUC secondary, illustrative top 10% primary capacity with 5%/20% secondary, .50-only classification reference and no calibration/learned threshold under the default protocol. If a learned threshold is desired, approve the explicit training-only amendment first.
4. Approve exact grids, deterministic selection/tie rules, environment, four-search budget, audit/release gates and proposed 2,000-replicate conditional uncertainty procedure. Freeze plan/version/model digests before opening test records.
5. Separately authorize the future development-only fitting and one batch of final evaluation after the release gate. Approval to review these documents does not automatically start Phase 7, train a final model, evaluate held-out records, commit or push.

**Ready:** evidence consolidation, exact availability matrix, conditional shortlist, scenario labels, final-fitting algorithm and proposed held-out reporting/uncertainty rules. **Not ready/executed:** availability verification, final parameter selection/refits, final model artifacts, team sign-off, test predictions or performance. Stop after these two planning documents.
