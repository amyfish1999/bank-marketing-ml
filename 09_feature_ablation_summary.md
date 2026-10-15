# Phase 6A — Feature availability and ablation study

## Completion review

| feature_group | predictors | HGB AP mean ± sample SD | LR AP mean ± sample SD |
| --- | --- | --- | --- |
| Full | 15 | 0.448145 ± 0.014219 | 0.422429 ± 0.011606 |
| No Economic Indicators | 10 | 0.351146 ± 0.015153 | 0.334394 ± 0.021340 |
| No Previous Campaign History | 12 | 0.389129 ± 0.009401 | 0.355256 ± 0.013265 |
| Customer Attributes Only | 7 | 0.232569 ± 0.009506 | 0.202251 ± 0.015223 |

HGB full-minus-subset mean AP losses: no economics 0.096999; no history 0.059017; customer-only 0.215576. HGB has higher mean AP than LR in all four feature groups. This is a descriptive development comparison, not a significance test or final selection.

At identical pooled contact capacities of 1,647 / 3,294 / 6,588 (5% / 10% / 20%), HGB captures:

- Full: 1005 / 1628 / 2377 historical subscribers.
- No Economic Indicators: 947 / 1300 / 1707 historical subscribers.
- No Previous Campaign History: 869 / 1540 / 2356 historical subscribers.
- Customer Attributes Only: 640 / 926 / 1387 historical subscribers.

Removing economic context or history therefore has a measurable predictive cost in this experiment. The two group losses cannot be added to infer the combined loss. ROC-AUC, AP, fixed-.50 results and fold-local targeting below should be read together; lower .50 recall alone is not proof of poor ranking or a basis for new threshold tuning.

**Conditional shortlist for Phase 6B discussion:** keep original full HGB as a research reference and the reduced HGB variants corresponding to whichever feature contract the team can verify. Retain original LR as a simpler benchmark. If economic availability cannot be verified but history can, discuss No Economic Indicators; if history cannot be verified but economic as-of values can, discuss No Previous Campaign History; if neither can, use Customer Attributes Only as the information-restricted comparison, with its observed performance loss. None is certified deployable, including customer-only. Do not select a final subset solely from the largest outer score. These conclusions concern the tested unweighted grids and do not extrapolate imbalance-treatment findings to untested reduced-feature variants.

Source SHA-256 evidence (whole-file integrity checks, not held-out feature/label analysis):

| artifact | sha256 |
| --- | --- |
| dataset.csv | 81fd5eb4b659dddbc704edd90376c32714c3f6a43b887cb686762903bc793f0d |
| 02_cleaned_dataset.csv | c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49 |
| 03_split_indices.json | 397e6e9c66ba3b6b5f6bef6232e00dc392c9ae9d77fdfda28a2d7dc02693596b |
| preprocessing.py | 3959b4db9a561be5bf7373dfcf82ab85c24a288250e26180599a403b7e551ed8 |

Reported runtime includes audit, search and refit overhead; it is not a hardware-independent algorithm speed benchmark. All predictors in every group remain Provisional. Approve campaign-start source snapshots/as-of rules and a development-only final model/policy-selection plan before Phase 6B; no held-out evaluation or final decision is made here.

At top 5%, HGB without economics captures 947 subscribers versus 869 without history, despite lower overall AP. At top 20%, HGB without history captures 2,356 versus full's 2,377, while no-economics captures 1,707. Thus the relative value of the groups depends on contact capacity; the overall AP order does not settle every Top-K comparison. These remain historical out-of-sample associations, not causal outreach effects.

Customer-only LR predicts no subscribers at .50 in any fold: precision/recall/F1=0 and accuracy 0.887341. Its AP is nevertheless 0.202251, above development prevalence 0.112659. Customer-only HGB also has low .50 recall (0.021287). This illustrates why fixed-threshold outcomes and ranking metrics must be distinguished; no new threshold was selected.

Separate final local checks passed: notebook nbformat schema, six executed code cells and syntax, three figures; independently recomputed all 40 outer-fold metric records plus 120 fold-local and 24 pooled Top-K records; all pre-existing tracked artifacts match approved HEAD byte-for-byte. Model warnings: zero. Four approved preprocessing tests pass. Hosted Colab execution was not directly tested.

## Scope, source and prespecified experiments

Started from latest fetched/merged main **11b6638** (Phase 5B-2 merge included); current feature branch fast-forwarded to it without a new commit. Reviewed README, project planning DOCX and Phase 2C–5B-2 notebooks/summaries/preprocessing/split. Original HGB and LR only, class_weight=None. No resampling, new features, new grids, threshold optimization, final model/policy selection, held-out evaluation or Phase 6B.

This is **development-only sensitivity analysis**, not independent validation of model families, grids or feature concerns identified after prior development exploration. Groups were specified by the user before this experiment, not selected from outer outcomes. All remaining fields stay Provisional. Ablation measures predictive dependence under this validation design, not causality, feature availability or safety.

## Exact feature groups and ordering

| feature_group | n_predictors | ordered_input_columns | categorical_columns | quantitative_columns | recency_transformer_columns |
| --- | --- | --- | --- | --- | --- |
| Full | 15 | age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days | job, marital, education, default, housing, loan | age, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed | recency_days, recency_available |
| No Economic Indicators | 10 | age, job, marital, education, default, housing, loan, previous, recency_available, recency_days | job, marital, education, default, housing, loan | age, previous | recency_days, recency_available |
| No Previous Campaign History | 12 | age, job, marital, education, default, housing, loan, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed | job, marital, education, default, housing, loan | age, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed | REMOVED |
| Customer Attributes Only | 7 | age, job, marital, education, default, housing, loan | job, marital, education, default, housing, loan | age | REMOVED |

Input order filters the approved FEATURES sequence; it is not alphabetically reordered. Transformer output order remains approved categorical blocks, selected NUMERICAL order, then [recency_days, recency_available] only when included. Every group keeps all six categorical fields; quantitative counts are 7 / 2 / 6 / 1. Recency is either a complete two-column component or completely removed, with no zero-filled stand-ins for excluded predictors.

## Data integrity, row order and validation design

Cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` equals the saved split manifest hash before positions are applied. Unique/disjoint/exhaustive saved indices: 32,940 development / 8,236 held-out; unchanged assignment and row order. CSV parser skips held-out rows; only development features/labels are materialized, restored to saved development-index order. The original raw CSV, if present, is only byte-hashed. No held-out feature/label fitting, profiling or evaluation here.

Outer StratifiedKFold(n_splits=5, shuffle=True, random_state=42), validation-position SHA-256 `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4`, matches Phases 5A/5B. Each validation cohort has 6,588 rows, each outer training set 26,352. Same ordered outer/inner folds across all eight procedures. Each outer-training set gets a fresh five-fold GridSearchCV, AP-only model selection, refit='AP', n_jobs=1, error_score='raise'. Selected complete pipelines refit only outer-training rows and predict outer-validation rows once. No complete-development fitting or preprocessing. No reduced-feature set borrows full-feature optimal parameters.

Grids exactly match approved Phase 5A:
- LR C=[0.1,1,10], lbfgs/default L2, max_iter=1000, seed=42, class_weight=None: 3 candidates.
- HGB learning_rate=[0.05,0.1], max_iter=[100,200], max_leaf_nodes=[15,31], l2_regularization=[0,1], early_stopping=False, categorical_features=None, seed=42, class_weight=None: 16 candidates.

C controls LR inverse regularization; HGB learning rate and iteration count control boosting updates/budget, leaf count controls tree complexity, L2 regularizes leaf predictions. Every feature set has equal search budget within each family. All grids rerun freshly, including Full: **1,900 candidate-fold fits +40 selected outer-training refits =1,940 fits**. No outer-score-driven grid changes. Full metrics and selected parameters reproduce Phase 5A at reported precision.

Classification threshold is fixed at positive probability >=0.50, used only as a reference. Precision/recall/F1 use zero_division=0. AP is Average Precision, not trapezoidal PR area. SDs use sample ddof=1 across five outer folds; these folds share training observations and are not independent confidence intervals. Inner scores/candidate rankings below are selection data, not independent performance estimates.

## Experiment-specific adapter and equivalence

preprocessing.py has no subset argument, so a small notebook-only adapter obtains a fresh approved factory Pipeline, filters each unfitted ColumnTransformer column list to the prespecified group, and removes empty transformer entries. Approved transformer objects/behavior are reused rather than reimplemented. Original factory/module remain unchanged and subsequent calls still have full original columns. Excluded features are not passed to estimator fitting or prediction and are not filled with constants.

Full-feature adapter versus original factory: identical transformed arrays, feature names, categories and fitted ordinary/conditional statistics on a 300-fit/100-transform fixture drawn solely from outer fold 1 training rows. Synthetic unseen job in the validation fixture confirms all-zero unknown-level block without changing source rows. Every group/model is cloneable and finite; absent recency means no recency transformer or output names. Fixture tests do not fit any predictive model or full-development transformer.

| model | feature_group | fixture_fit_rows | fixture_transform_rows | output_columns | full_equivalence | status |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 300 | 100 | 40 | True | PASS |
| HistGradientBoosting | No Economic Indicators | 300 | 100 | 35 | False | PASS |
| HistGradientBoosting | No Previous Campaign History | 300 | 100 | 37 | False | PASS |
| HistGradientBoosting | Customer Attributes Only | 300 | 100 | 32 | False | PASS |
| LogisticRegression | Full | 300 | 100 | 40 | True | PASS |
| LogisticRegression | No Economic Indicators | 300 | 100 | 35 | False | PASS |
| LogisticRegression | No Previous Campaign History | 300 | 100 | 37 | False | PASS |
| LogisticRegression | Customer Attributes Only | 300 | 100 | 32 | False | PASS |

OHE retains drop=None, handle_unknown='ignore', dense float64 indicators, six training-only vocabularies. LR StandardScaler uses only selected quantitative fitting columns; ConditionalRecencyScaler, when present, uses only available-recency fitting observations with approved fallback behavior, unavailable transformed days=0 and indicator unscaled. HGB numeric/recency values pass through unchanged; dummy indicators are numeric, native categorical handling off. A stateless guard checks values and returns them unchanged. No global encoded/scaled matrix.

## Individual outer-validation predictive results

| model | feature_group | outer_fold | AP | ROC_AUC | Accuracy | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 1 | 0.450109 | 0.810998 | 0.899666 | 0.650558 | 0.235849 | 0.346192 |
| HistGradientBoosting | No Economic Indicators | 1 | 0.348171 | 0.709687 | 0.898452 | 0.645418 | 0.218329 | 0.326284 |
| HistGradientBoosting | No Previous Campaign History | 1 | 0.389072 | 0.804676 | 0.887067 | 0.495652 | 0.153639 | 0.234568 |
| HistGradientBoosting | Customer Attributes Only | 1 | 0.230079 | 0.667594 | 0.886612 | 0.368421 | 0.009434 | 0.018397 |
| LogisticRegression | Full | 1 | 0.432797 | 0.773340 | 0.899211 | 0.671053 | 0.206199 | 0.315464 |
| LogisticRegression | No Economic Indicators | 1 | 0.345362 | 0.699877 | 0.898452 | 0.656652 | 0.206199 | 0.313846 |
| LogisticRegression | No Previous Campaign History | 1 | 0.367771 | 0.765169 | 0.888889 | 0.530120 | 0.118598 | 0.193833 |
| LogisticRegression | Customer Attributes Only | 1 | 0.207683 | 0.651452 | 0.887371 | 0.000000 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 2 | 0.442077 | 0.791971 | 0.899211 | 0.668103 | 0.208895 | 0.318275 |
| HistGradientBoosting | No Economic Indicators | 2 | 0.335618 | 0.689822 | 0.895416 | 0.612766 | 0.194070 | 0.294780 |
| HistGradientBoosting | No Previous Campaign History | 2 | 0.395964 | 0.786320 | 0.891773 | 0.567442 | 0.164420 | 0.254963 |
| HistGradientBoosting | Customer Attributes Only | 2 | 0.225444 | 0.654580 | 0.886460 | 0.411765 | 0.018868 | 0.036082 |
| LogisticRegression | Full | 2 | 0.420805 | 0.758226 | 0.899970 | 0.698565 | 0.196765 | 0.307045 |
| LogisticRegression | No Economic Indicators | 2 | 0.310010 | 0.680650 | 0.896023 | 0.627803 | 0.188679 | 0.290155 |
| LogisticRegression | No Previous Campaign History | 2 | 0.353047 | 0.751471 | 0.886764 | 0.484848 | 0.086253 | 0.146453 |
| LogisticRegression | Customer Attributes Only | 2 | 0.187630 | 0.634901 | 0.887371 | 0.000000 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 3 | 0.428814 | 0.788546 | 0.899666 | 0.652830 | 0.233154 | 0.343595 |
| HistGradientBoosting | No Economic Indicators | 3 | 0.338092 | 0.701590 | 0.897693 | 0.655963 | 0.192722 | 0.297917 |
| HistGradientBoosting | No Previous Campaign History | 3 | 0.374931 | 0.784633 | 0.889800 | 0.531008 | 0.184636 | 0.274000 |
| HistGradientBoosting | Customer Attributes Only | 3 | 0.227339 | 0.665531 | 0.885853 | 0.407407 | 0.029650 | 0.055276 |
| LogisticRegression | Full | 3 | 0.403262 | 0.742708 | 0.897996 | 0.660550 | 0.194070 | 0.300000 |
| LogisticRegression | No Economic Indicators | 3 | 0.316501 | 0.687731 | 0.898604 | 0.668182 | 0.198113 | 0.305613 |
| LogisticRegression | No Previous Campaign History | 3 | 0.333502 | 0.736900 | 0.886916 | 0.491329 | 0.114555 | 0.185792 |
| LogisticRegression | Customer Attributes Only | 3 | 0.190917 | 0.641975 | 0.887371 | 0.000000 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 4 | 0.467601 | 0.802185 | 0.900273 | 0.683983 | 0.212938 | 0.324769 |
| HistGradientBoosting | No Economic Indicators | 4 | 0.367246 | 0.717205 | 0.897845 | 0.663507 | 0.188679 | 0.293809 |
| HistGradientBoosting | No Previous Campaign History | 4 | 0.399072 | 0.798145 | 0.888585 | 0.516949 | 0.164420 | 0.249489 |
| HistGradientBoosting | Customer Attributes Only | 4 | 0.230856 | 0.663597 | 0.886308 | 0.410256 | 0.021563 | 0.040973 |
| LogisticRegression | Full | 4 | 0.425777 | 0.770552 | 0.897996 | 0.678571 | 0.179245 | 0.283582 |
| LogisticRegression | No Economic Indicators | 4 | 0.337873 | 0.709611 | 0.898148 | 0.668246 | 0.190027 | 0.295908 |
| LogisticRegression | No Previous Campaign History | 4 | 0.359657 | 0.762743 | 0.886308 | 0.475177 | 0.090296 | 0.151755 |
| LogisticRegression | Customer Attributes Only | 4 | 0.199383 | 0.654519 | 0.887371 | 0.000000 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 5 | 0.452125 | 0.780853 | 0.899514 | 0.683258 | 0.203230 | 0.313278 |
| HistGradientBoosting | No Economic Indicators | 5 | 0.366602 | 0.705303 | 0.899970 | 0.703883 | 0.195155 | 0.305585 |
| HistGradientBoosting | No Previous Campaign History | 5 | 0.386604 | 0.773673 | 0.887978 | 0.512195 | 0.141319 | 0.221519 |
| HistGradientBoosting | Customer Attributes Only | 5 | 0.249127 | 0.667376 | 0.887067 | 0.487805 | 0.026918 | 0.051020 |
| LogisticRegression | Full | 5 | 0.429507 | 0.764549 | 0.900729 | 0.725888 | 0.192463 | 0.304255 |
| LogisticRegression | No Economic Indicators | 5 | 0.362222 | 0.702096 | 0.899666 | 0.713542 | 0.184388 | 0.293048 |
| LogisticRegression | No Previous Campaign History | 5 | 0.362304 | 0.756524 | 0.887371 | 0.503268 | 0.103634 | 0.171875 |
| LogisticRegression | Customer Attributes Only | 5 | 0.225640 | 0.651188 | 0.887219 | 0.000000 | 0.000000 | 0.000000 |

## Mean and sample SD of outer metrics

| model | feature_group | AP mean ± SD | ROC_AUC mean ± SD | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Customer Attributes Only | 0.232569 ± 0.009506 | 0.663736 ± 0.005367 | 0.886460 ± 0.000443 | 0.417131 ± 0.043411 | 0.021287 ± 0.007875 | 0.040350 ± 0.014467 |
| HistGradientBoosting | Full | 0.448145 ± 0.014219 | 0.794911 ± 0.011816 | 0.899666 ± 0.000387 | 0.667746 ± 0.015987 | 0.218813 ± 0.014761 | 0.329222 ± 0.014903 |
| HistGradientBoosting | No Economic Indicators | 0.351146 ± 0.015153 | 0.704721 ± 0.010157 | 0.897875 ± 0.001643 | 0.656308 ± 0.032901 | 0.197791 ± 0.011740 | 0.303675 ± 0.013458 |
| HistGradientBoosting | No Previous Campaign History | 0.389129 ± 0.009401 | 0.789489 ± 0.012138 | 0.889041 ± 0.001821 | 0.524649 ± 0.027050 | 0.161687 ± 0.015978 | 0.246908 ± 0.020015 |
| LogisticRegression | Customer Attributes Only | 0.202251 ± 0.015223 | 0.646807 ± 0.008145 | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 |
| LogisticRegression | Full | 0.422429 ± 0.011606 | 0.761875 ± 0.012192 | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 |
| LogisticRegression | No Economic Indicators | 0.334394 ± 0.021340 | 0.695993 ± 0.011635 | 0.898179 ± 0.001334 | 0.666885 ± 0.030873 | 0.193481 ± 0.008673 | 0.299714 ± 0.009808 |
| LogisticRegression | No Previous Campaign History | 0.355256 ± 0.013265 | 0.754562 ± 0.011234 | 0.887250 ± 0.000992 | 0.496949 ± 0.021168 | 0.102667 ± 0.014305 | 0.169942 ± 0.020665 |

## Paired full-minus-subset losses and model rankings

Positive loss means reduced AP/ROC-AUC after removal; negative means an observed gain. These are matched validation-fold differences, not significance tests.

| model | feature_group | outer_fold | AP_loss_vs_full | ROC_AUC_loss_vs_full |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 1 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 2 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 3 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 4 | 0.000000 | 0.000000 |
| HistGradientBoosting | Full | 5 | 0.000000 | 0.000000 |
| HistGradientBoosting | No Economic Indicators | 1 | 0.101938 | 0.101311 |
| HistGradientBoosting | No Economic Indicators | 2 | 0.106459 | 0.102150 |
| HistGradientBoosting | No Economic Indicators | 3 | 0.090721 | 0.086956 |
| HistGradientBoosting | No Economic Indicators | 4 | 0.100355 | 0.084981 |
| HistGradientBoosting | No Economic Indicators | 5 | 0.085523 | 0.075550 |
| HistGradientBoosting | No Previous Campaign History | 1 | 0.061037 | 0.006322 |
| HistGradientBoosting | No Previous Campaign History | 2 | 0.046113 | 0.005652 |
| HistGradientBoosting | No Previous Campaign History | 3 | 0.053882 | 0.003913 |
| HistGradientBoosting | No Previous Campaign History | 4 | 0.068529 | 0.004041 |
| HistGradientBoosting | No Previous Campaign History | 5 | 0.065521 | 0.007180 |
| HistGradientBoosting | Customer Attributes Only | 1 | 0.220030 | 0.143404 |
| HistGradientBoosting | Customer Attributes Only | 2 | 0.216633 | 0.137391 |
| HistGradientBoosting | Customer Attributes Only | 3 | 0.201475 | 0.123015 |
| HistGradientBoosting | Customer Attributes Only | 4 | 0.236745 | 0.138588 |
| HistGradientBoosting | Customer Attributes Only | 5 | 0.202998 | 0.113477 |
| LogisticRegression | Full | 1 | 0.000000 | 0.000000 |
| LogisticRegression | Full | 2 | 0.000000 | 0.000000 |
| LogisticRegression | Full | 3 | 0.000000 | 0.000000 |
| LogisticRegression | Full | 4 | 0.000000 | 0.000000 |
| LogisticRegression | Full | 5 | 0.000000 | 0.000000 |
| LogisticRegression | No Economic Indicators | 1 | 0.087435 | 0.073463 |
| LogisticRegression | No Economic Indicators | 2 | 0.110795 | 0.077577 |
| LogisticRegression | No Economic Indicators | 3 | 0.086760 | 0.054977 |
| LogisticRegression | No Economic Indicators | 4 | 0.087904 | 0.060941 |
| LogisticRegression | No Economic Indicators | 5 | 0.067284 | 0.062452 |
| LogisticRegression | No Previous Campaign History | 1 | 0.065026 | 0.008171 |
| LogisticRegression | No Previous Campaign History | 2 | 0.067758 | 0.006755 |
| LogisticRegression | No Previous Campaign History | 3 | 0.069760 | 0.005808 |
| LogisticRegression | No Previous Campaign History | 4 | 0.066120 | 0.007809 |
| LogisticRegression | No Previous Campaign History | 5 | 0.067202 | 0.008024 |
| LogisticRegression | Customer Attributes Only | 1 | 0.225114 | 0.121888 |
| LogisticRegression | Customer Attributes Only | 2 | 0.233175 | 0.123326 |
| LogisticRegression | Customer Attributes Only | 3 | 0.212344 | 0.100733 |
| LogisticRegression | Customer Attributes Only | 4 | 0.226394 | 0.116033 |
| LogisticRegression | Customer Attributes Only | 5 | 0.203866 | 0.113360 |

| model | feature_group | AP_loss_mean | AP_loss_sample_SD | ROC_AUC_loss_mean | ROC_AUC_loss_sample_SD |
| --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Customer Attributes Only | 0.215576 | 0.014371 | 0.131175 | 0.012480 |
| HistGradientBoosting | Full | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| HistGradientBoosting | No Economic Indicators | 0.096999 | 0.008606 | 0.090189 | 0.011387 |
| HistGradientBoosting | No Previous Campaign History | 0.059017 | 0.009079 | 0.005422 | 0.001426 |
| LogisticRegression | Customer Attributes Only | 0.220179 | 0.011825 | 0.115068 | 0.009001 |
| LogisticRegression | Full | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| LogisticRegression | No Economic Indicators | 0.088036 | 0.015416 | 0.065882 | 0.009345 |
| LogisticRegression | No Previous Campaign History | 0.067173 | 0.001786 | 0.007313 | 0.001008 |

| feature_group | AP_ranking | HGB_minus_LR_AP |
| --- | --- | --- |
| Full | HistGradientBoosting > LogisticRegression | 0.025716 |
| No Economic Indicators | HistGradientBoosting > LogisticRegression | 0.016752 |
| No Previous Campaign History | HistGradientBoosting > LogisticRegression | 0.033873 |
| Customer Attributes Only | HistGradientBoosting > LogisticRegression | 0.030318 |

## Observed findings

**HistGradientBoosting** full AP 0.448145, ROC-AUC 0.794911. No Economic Indicators: AP 0.351146 (full-minus-subset +0.096999); ROC-AUC 0.704721; pooled captured subscribers at 5/10/20% = 947 / 1300 / 1707. No Previous Campaign History: AP 0.389129 (full-minus-subset +0.059017); ROC-AUC 0.789489; pooled captured subscribers at 5/10/20% = 869 / 1540 / 2356. Customer Attributes Only: AP 0.232569 (full-minus-subset +0.215576); ROC-AUC 0.663736; pooled captured subscribers at 5/10/20% = 640 / 926 / 1387.

**LogisticRegression** full AP 0.422429, ROC-AUC 0.761875. No Economic Indicators: AP 0.334394 (full-minus-subset +0.088036); ROC-AUC 0.695993; pooled captured subscribers at 5/10/20% = 885 / 1246 / 1665. No Previous Campaign History: AP 0.355256 (full-minus-subset +0.067173); ROC-AUC 0.754562; pooled captured subscribers at 5/10/20% = 805 / 1510 / 2205. Customer Attributes Only: AP 0.202251 (full-minus-subset +0.220179); ROC-AUC 0.646807; pooled captured subscribers at 5/10/20% = 537 / 813 / 1312.

Interpret these group-level differences alongside fold spread, not just the best mean. Exclusion/refitting changes available information and the optimal permitted configuration; differences do not isolate an individual feature's importance, prove economic/history causal effects, or establish that any variable is unavailable. The groups may share information and interact; their losses need not add. AP/ROC-AUC and equal-capacity capture measure ranking changes. Precision/recall/F1 at .50 can additionally change with probability scale/calibration; they do not establish the best deployment decision rule.

## Business targeting — fold-local results

Ranking uses untouched outer-validation probabilities. K=ceil(fraction*N), descending score then cleaned-file row position for outcome-independent deterministic ties. Precision@K=captured/K; Recall@K=captured/cohort positives; Lift@K=precision/cohort prevalence. Every model/group gets identical K within the same cohort. Capture refers to historical subscribers, not the causal effect of contacting them.

| model | feature_group | fraction | outer_fold | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 0.050000 | 1 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| HistGradientBoosting | Full | 0.050000 | 2 | 330 | 199 | 0.603030 | 0.268194 | 5.354129 |
| HistGradientBoosting | Full | 0.050000 | 3 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| HistGradientBoosting | Full | 0.050000 | 4 | 330 | 204 | 0.618182 | 0.274933 | 5.488655 |
| HistGradientBoosting | Full | 0.050000 | 5 | 330 | 201 | 0.609091 | 0.270525 | 5.400661 |
| HistGradientBoosting | Full | 0.100000 | 1 | 659 | 322 | 0.488619 | 0.433962 | 4.338306 |
| HistGradientBoosting | Full | 0.100000 | 2 | 659 | 325 | 0.493171 | 0.438005 | 4.378725 |
| HistGradientBoosting | Full | 0.100000 | 3 | 659 | 317 | 0.481032 | 0.427224 | 4.270941 |
| HistGradientBoosting | Full | 0.100000 | 4 | 659 | 334 | 0.506829 | 0.450135 | 4.499982 |
| HistGradientBoosting | Full | 0.100000 | 5 | 659 | 329 | 0.499241 | 0.442799 | 4.426651 |
| HistGradientBoosting | Full | 0.200000 | 1 | 1318 | 492 | 0.373293 | 0.663073 | 3.314358 |
| HistGradientBoosting | Full | 0.200000 | 2 | 1318 | 467 | 0.354325 | 0.629380 | 3.145945 |
| HistGradientBoosting | Full | 0.200000 | 3 | 1318 | 455 | 0.345220 | 0.613208 | 3.065107 |
| HistGradientBoosting | Full | 0.200000 | 4 | 1318 | 483 | 0.366464 | 0.650943 | 3.253729 |
| HistGradientBoosting | Full | 0.200000 | 5 | 1318 | 474 | 0.359636 | 0.637954 | 3.188803 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 1 | 330 | 200 | 0.606061 | 0.269542 | 5.381034 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 2 | 330 | 183 | 0.554545 | 0.246631 | 4.923646 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 3 | 330 | 178 | 0.539394 | 0.239892 | 4.789120 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 4 | 330 | 192 | 0.581818 | 0.258760 | 5.165793 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 5 | 330 | 200 | 0.606061 | 0.269179 | 5.373792 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 1 | 659 | 267 | 0.405159 | 0.359838 | 3.597291 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 2 | 659 | 247 | 0.374810 | 0.332884 | 3.327831 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 3 | 659 | 257 | 0.389985 | 0.346361 | 3.462561 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 4 | 659 | 263 | 0.399090 | 0.354447 | 3.543399 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 5 | 659 | 265 | 0.402124 | 0.356662 | 3.565539 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 1 | 1318 | 334 | 0.253414 | 0.450135 | 2.249991 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 2 | 1318 | 326 | 0.247344 | 0.439353 | 2.196099 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 3 | 1318 | 334 | 0.253414 | 0.450135 | 2.249991 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 4 | 1318 | 357 | 0.270865 | 0.481132 | 2.404930 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 5 | 1318 | 347 | 0.263278 | 0.467026 | 2.334419 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 1 | 330 | 174 | 0.527273 | 0.234501 | 4.681500 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 2 | 330 | 178 | 0.539394 | 0.239892 | 4.789120 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 3 | 330 | 176 | 0.533333 | 0.237197 | 4.735310 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 4 | 330 | 173 | 0.524242 | 0.233154 | 4.654594 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 5 | 330 | 179 | 0.542424 | 0.240915 | 4.809544 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 1 | 659 | 302 | 0.458270 | 0.407008 | 4.068846 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 2 | 659 | 313 | 0.474962 | 0.421833 | 4.217049 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 3 | 659 | 298 | 0.452200 | 0.401617 | 4.014954 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 4 | 659 | 316 | 0.479514 | 0.425876 | 4.257468 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 5 | 659 | 315 | 0.477997 | 0.423957 | 4.238283 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 1 | 1318 | 487 | 0.369499 | 0.656334 | 3.280675 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 2 | 1318 | 465 | 0.352807 | 0.626685 | 3.132472 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 3 | 1318 | 458 | 0.347496 | 0.617251 | 3.085317 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 4 | 1318 | 484 | 0.367223 | 0.652291 | 3.260466 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 5 | 1318 | 469 | 0.355842 | 0.631225 | 3.155166 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 1 | 330 | 123 | 0.372727 | 0.165768 | 3.309336 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 2 | 330 | 119 | 0.360606 | 0.160377 | 3.201715 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 3 | 330 | 123 | 0.372727 | 0.165768 | 3.309336 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 4 | 330 | 126 | 0.381818 | 0.169811 | 3.390051 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 5 | 330 | 137 | 0.415152 | 0.184388 | 3.681047 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 1 | 659 | 179 | 0.271624 | 0.241240 | 2.411667 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 2 | 659 | 185 | 0.280728 | 0.249326 | 2.492505 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 3 | 659 | 181 | 0.274659 | 0.243935 | 2.438613 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 4 | 659 | 187 | 0.283763 | 0.252022 | 2.519451 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 5 | 659 | 193 | 0.292868 | 0.259758 | 2.596789 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 1 | 1318 | 277 | 0.210167 | 0.373315 | 1.866010 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 2 | 1318 | 269 | 0.204097 | 0.362534 | 1.812118 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 3 | 1318 | 282 | 0.213961 | 0.380054 | 1.899693 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 4 | 1318 | 288 | 0.218513 | 0.388140 | 1.940112 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 5 | 1318 | 284 | 0.215478 | 0.382234 | 1.910591 |
| LogisticRegression | Full | 0.050000 | 1 | 330 | 199 | 0.603030 | 0.268194 | 5.354129 |
| LogisticRegression | Full | 0.050000 | 2 | 330 | 184 | 0.557576 | 0.247978 | 4.950551 |
| LogisticRegression | Full | 0.050000 | 3 | 330 | 183 | 0.554545 | 0.246631 | 4.923646 |
| LogisticRegression | Full | 0.050000 | 4 | 330 | 197 | 0.596970 | 0.265499 | 5.300319 |
| LogisticRegression | Full | 0.050000 | 5 | 330 | 200 | 0.606061 | 0.269179 | 5.373792 |
| LogisticRegression | Full | 0.100000 | 1 | 659 | 315 | 0.477997 | 0.424528 | 4.243995 |
| LogisticRegression | Full | 0.100000 | 2 | 659 | 313 | 0.474962 | 0.421833 | 4.217049 |
| LogisticRegression | Full | 0.100000 | 3 | 659 | 306 | 0.464340 | 0.412399 | 4.122738 |
| LogisticRegression | Full | 0.100000 | 4 | 659 | 319 | 0.484067 | 0.429919 | 4.297887 |
| LogisticRegression | Full | 0.100000 | 5 | 659 | 317 | 0.481032 | 0.426649 | 4.265192 |
| LogisticRegression | Full | 0.200000 | 1 | 1318 | 460 | 0.349014 | 0.619946 | 3.098790 |
| LogisticRegression | Full | 0.200000 | 2 | 1318 | 448 | 0.339909 | 0.603774 | 3.017952 |
| LogisticRegression | Full | 0.200000 | 3 | 1318 | 427 | 0.323976 | 0.575472 | 2.876485 |
| LogisticRegression | Full | 0.200000 | 4 | 1318 | 464 | 0.352049 | 0.625337 | 3.125736 |
| LogisticRegression | Full | 0.200000 | 5 | 1318 | 457 | 0.346737 | 0.615074 | 3.074437 |
| LogisticRegression | No Economic Indicators | 0.050000 | 1 | 330 | 186 | 0.563636 | 0.250674 | 5.004362 |
| LogisticRegression | No Economic Indicators | 0.050000 | 2 | 330 | 170 | 0.515152 | 0.229111 | 4.573879 |
| LogisticRegression | No Economic Indicators | 0.050000 | 3 | 330 | 176 | 0.533333 | 0.237197 | 4.735310 |
| LogisticRegression | No Economic Indicators | 0.050000 | 4 | 330 | 176 | 0.533333 | 0.237197 | 4.735310 |
| LogisticRegression | No Economic Indicators | 0.050000 | 5 | 330 | 192 | 0.581818 | 0.258412 | 5.158840 |
| LogisticRegression | No Economic Indicators | 0.100000 | 1 | 659 | 256 | 0.388467 | 0.345013 | 3.449088 |
| LogisticRegression | No Economic Indicators | 0.100000 | 2 | 659 | 233 | 0.353566 | 0.314016 | 3.139209 |
| LogisticRegression | No Economic Indicators | 0.100000 | 3 | 659 | 243 | 0.368741 | 0.327493 | 3.273939 |
| LogisticRegression | No Economic Indicators | 0.100000 | 4 | 659 | 250 | 0.379363 | 0.336927 | 3.368250 |
| LogisticRegression | No Economic Indicators | 0.100000 | 5 | 659 | 273 | 0.414264 | 0.367429 | 3.673178 |
| LogisticRegression | No Economic Indicators | 0.200000 | 1 | 1318 | 340 | 0.257967 | 0.458221 | 2.290410 |
| LogisticRegression | No Economic Indicators | 0.200000 | 2 | 1318 | 311 | 0.235964 | 0.419137 | 2.095051 |
| LogisticRegression | No Economic Indicators | 0.200000 | 3 | 1318 | 321 | 0.243551 | 0.432615 | 2.162416 |
| LogisticRegression | No Economic Indicators | 0.200000 | 4 | 1318 | 345 | 0.261760 | 0.464960 | 2.324092 |
| LogisticRegression | No Economic Indicators | 0.200000 | 5 | 1318 | 352 | 0.267071 | 0.473755 | 2.368056 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 1 | 330 | 170 | 0.515152 | 0.229111 | 4.573879 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 2 | 330 | 162 | 0.490909 | 0.218329 | 4.358638 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 3 | 330 | 151 | 0.457576 | 0.203504 | 4.062681 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 4 | 330 | 160 | 0.484848 | 0.215633 | 4.304827 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 5 | 330 | 167 | 0.506061 | 0.224764 | 4.487116 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 1 | 659 | 302 | 0.458270 | 0.407008 | 4.068846 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 2 | 659 | 310 | 0.470410 | 0.417790 | 4.176630 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 3 | 659 | 295 | 0.447648 | 0.397574 | 3.974535 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 4 | 659 | 309 | 0.468892 | 0.416442 | 4.163157 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 5 | 659 | 297 | 0.450683 | 0.399731 | 3.996095 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 1 | 1318 | 454 | 0.344461 | 0.611860 | 3.058371 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 2 | 1318 | 435 | 0.330046 | 0.586253 | 2.930377 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 3 | 1318 | 418 | 0.317147 | 0.563342 | 2.815857 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 4 | 1318 | 456 | 0.345979 | 0.614555 | 3.071844 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 5 | 1318 | 441 | 0.334598 | 0.593540 | 2.966798 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 1 | 330 | 109 | 0.330303 | 0.146900 | 2.932664 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 2 | 330 | 103 | 0.312121 | 0.138814 | 2.771233 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 3 | 330 | 99 | 0.300000 | 0.133423 | 2.663612 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 4 | 330 | 104 | 0.315152 | 0.140162 | 2.798138 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 5 | 330 | 128 | 0.387879 | 0.172275 | 3.439227 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 1 | 659 | 158 | 0.239757 | 0.212938 | 2.128734 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 2 | 659 | 141 | 0.213961 | 0.190027 | 1.899693 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 3 | 659 | 158 | 0.239757 | 0.212938 | 2.128734 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 4 | 659 | 156 | 0.236722 | 0.210243 | 2.101788 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 5 | 659 | 191 | 0.289833 | 0.257066 | 2.569879 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 1 | 1318 | 264 | 0.200303 | 0.355795 | 1.778436 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 2 | 1318 | 251 | 0.190440 | 0.338275 | 1.690861 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 3 | 1318 | 261 | 0.198027 | 0.351752 | 1.758226 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 4 | 1318 | 253 | 0.191958 | 0.340970 | 1.704334 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 5 | 1318 | 279 | 0.211684 | 0.375505 | 1.876954 |

Mean/sample SD across five validation cohorts:

| model | feature_group | fraction | contacts_mean | contacts_SD | captured_mean | captured_SD | Precision_mean | Precision_SD | Recall_mean | Recall_SD | Lift_mean | Lift_SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 330.000000 | 0.000000 | 125.600000 | 6.841053 | 0.380606 | 0.020730 | 0.169223 | 0.009116 | 3.378297 | 0.181995 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 659.000000 | 0.000000 | 185.000000 | 5.477226 | 0.280728 | 0.008311 | 0.249256 | 0.007254 | 2.491805 | 0.072522 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 1318.000000 | 0.000000 | 280.000000 | 7.314369 | 0.212443 | 0.005550 | 0.377255 | 0.009790 | 1.885705 | 0.048933 |
| HistGradientBoosting | Full | 0.050000 | 330.000000 | 0.000000 | 202.000000 | 2.000000 | 0.612121 | 0.006061 | 0.272164 | 0.002745 | 5.433389 | 0.054809 |
| HistGradientBoosting | Full | 0.100000 | 659.000000 | 0.000000 | 325.400000 | 6.503845 | 0.493778 | 0.009869 | 0.438425 | 0.008686 | 4.382921 | 0.086838 |
| HistGradientBoosting | Full | 0.200000 | 1318.000000 | 0.000000 | 474.200000 | 14.272351 | 0.359788 | 0.010829 | 0.638912 | 0.019242 | 3.193588 | 0.096180 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 330.000000 | 0.000000 | 190.600000 | 9.939819 | 0.577576 | 0.030121 | 0.256801 | 0.013311 | 5.126677 | 0.265734 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 659.000000 | 0.000000 | 259.800000 | 8.074652 | 0.394234 | 0.012253 | 0.350039 | 0.010807 | 3.499324 | 0.108035 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 1318.000000 | 0.000000 | 339.600000 | 12.300406 | 0.257663 | 0.009333 | 0.457556 | 0.016485 | 2.287086 | 0.082399 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 330.000000 | 0.000000 | 176.000000 | 2.549510 | 0.533333 | 0.007726 | 0.237132 | 0.003342 | 4.734014 | 0.066724 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 659.000000 | 0.000000 | 308.800000 | 8.228001 | 0.468589 | 0.012486 | 0.416058 | 0.010984 | 4.159320 | 0.109804 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 1318.000000 | 0.000000 | 472.600000 | 12.461942 | 0.358574 | 0.009455 | 0.636757 | 0.016861 | 3.182819 | 0.084278 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 330.000000 | 0.000000 | 108.600000 | 11.414903 | 0.329091 | 0.034591 | 0.146315 | 0.015285 | 2.920974 | 0.305151 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 659.000000 | 0.000000 | 160.800000 | 18.322118 | 0.244006 | 0.027803 | 0.216642 | 0.024550 | 2.165766 | 0.245427 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 1318.000000 | 0.000000 | 261.600000 | 11.126545 | 0.198483 | 0.008442 | 0.352459 | 0.014798 | 1.761762 | 0.073967 |
| LogisticRegression | Full | 0.050000 | 330.000000 | 0.000000 | 192.600000 | 8.384510 | 0.583636 | 0.025408 | 0.259496 | 0.011221 | 5.180487 | 0.224006 |
| LogisticRegression | Full | 0.100000 | 659.000000 | 0.000000 | 314.000000 | 5.000000 | 0.476480 | 0.007587 | 0.423066 | 0.006657 | 4.229372 | 0.066547 |
| LogisticRegression | Full | 0.200000 | 1318.000000 | 0.000000 | 451.200000 | 14.754660 | 0.342337 | 0.011195 | 0.607920 | 0.019807 | 3.038680 | 0.099004 |
| LogisticRegression | No Economic Indicators | 0.050000 | 330.000000 | 0.000000 | 180.000000 | 8.831761 | 0.545455 | 0.026763 | 0.242518 | 0.011785 | 4.841540 | 0.235267 |
| LogisticRegression | No Economic Indicators | 0.100000 | 659.000000 | 0.000000 | 251.000000 | 14.983324 | 0.380880 | 0.022736 | 0.338176 | 0.020012 | 3.380733 | 0.200057 |
| LogisticRegression | No Economic Indicators | 0.200000 | 1318.000000 | 0.000000 | 333.800000 | 17.166828 | 0.253263 | 0.013025 | 0.449738 | 0.022968 | 2.248005 | 0.114804 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 330.000000 | 0.000000 | 162.000000 | 7.314369 | 0.490909 | 0.022165 | 0.218268 | 0.009807 | 4.357428 | 0.195777 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 659.000000 | 0.000000 | 302.600000 | 6.804410 | 0.459181 | 0.010325 | 0.407709 | 0.009284 | 4.075852 | 0.092809 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 1318.000000 | 0.000000 | 440.800000 | 15.482248 | 0.334446 | 0.011747 | 0.593910 | 0.020866 | 2.968649 | 0.104299 |

## Pooled OOF targeting diagnostics

| model | feature_group | fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K | capture_change_vs_same_model_full |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 0.050000 | 1647 | 1005 | 0.610200 | 0.270816 | 5.416330 | 0 |
| HistGradientBoosting | Full | 0.100000 | 3294 | 1628 | 0.494232 | 0.438696 | 4.386958 | 0 |
| HistGradientBoosting | Full | 0.200000 | 6588 | 2377 | 0.360808 | 0.640528 | 3.202641 | 0 |
| HistGradientBoosting | No Economic Indicators | 0.050000 | 1647 | 947 | 0.574985 | 0.255187 | 5.103746 | -58 |
| HistGradientBoosting | No Economic Indicators | 0.100000 | 3294 | 1300 | 0.394657 | 0.350310 | 3.503099 | -328 |
| HistGradientBoosting | No Economic Indicators | 0.200000 | 6588 | 1707 | 0.259107 | 0.459984 | 2.299919 | -670 |
| HistGradientBoosting | No Previous Campaign History | 0.050000 | 1647 | 869 | 0.527626 | 0.234169 | 4.683374 | -136 |
| HistGradientBoosting | No Previous Campaign History | 0.100000 | 3294 | 1540 | 0.467517 | 0.414982 | 4.149825 | -88 |
| HistGradientBoosting | No Previous Campaign History | 0.200000 | 6588 | 2356 | 0.357620 | 0.634869 | 3.174347 | -21 |
| HistGradientBoosting | Customer Attributes Only | 0.050000 | 1647 | 640 | 0.388585 | 0.172460 | 3.449205 | -365 |
| HistGradientBoosting | Customer Attributes Only | 0.100000 | 3294 | 926 | 0.281117 | 0.249528 | 2.495284 | -702 |
| HistGradientBoosting | Customer Attributes Only | 0.200000 | 6588 | 1387 | 0.210534 | 0.373754 | 1.868769 | -990 |
| LogisticRegression | Full | 0.050000 | 1647 | 962 | 0.584092 | 0.259229 | 5.184586 | 0 |
| LogisticRegression | Full | 0.100000 | 3294 | 1564 | 0.474803 | 0.421450 | 4.214497 | 0 |
| LogisticRegression | Full | 0.200000 | 6588 | 2257 | 0.342593 | 0.608192 | 3.040959 | 0 |
| LogisticRegression | No Economic Indicators | 0.050000 | 1647 | 885 | 0.537341 | 0.238480 | 4.769604 | -77 |
| LogisticRegression | No Economic Indicators | 0.100000 | 3294 | 1246 | 0.378264 | 0.335759 | 3.357586 | -318 |
| LogisticRegression | No Economic Indicators | 0.200000 | 6588 | 1665 | 0.252732 | 0.448666 | 2.243331 | -592 |
| LogisticRegression | No Previous Campaign History | 0.050000 | 1647 | 805 | 0.488767 | 0.216923 | 4.338453 | -157 |
| LogisticRegression | No Previous Campaign History | 0.100000 | 3294 | 1510 | 0.458409 | 0.406898 | 4.068984 | -54 |
| LogisticRegression | No Previous Campaign History | 0.200000 | 6588 | 2205 | 0.334699 | 0.594179 | 2.970897 | -52 |
| LogisticRegression | Customer Attributes Only | 0.050000 | 1647 | 537 | 0.326047 | 0.144705 | 2.894099 | -425 |
| LogisticRegression | Customer Attributes Only | 0.100000 | 3294 | 813 | 0.246812 | 0.219078 | 2.190784 | -751 |
| LogisticRegression | Customer Attributes Only | 0.200000 | 6588 | 1312 | 0.199150 | 0.353544 | 1.767718 | -945 |

Pooled capacities are 1,647 / 3,294 / 6,588; per-fold capacities are 330 / 659 / 1,318, so summed fold-local capacities are 1,650 / 3,295 / 6,590. Pooled scores come from five separately fitted/calibrated models and are descriptive diagnostics, not a single deployable model's independent test performance. Fold-local rankings reduce sensitivity to cross-fold score calibration. No capacity, call cost, incremental response or financial value was supplied. Lift is predictive concentration, not causal campaign uplift.

## Inner-selected hyperparameters and search evidence

| model | feature_group | outer_fold | best_parameters | inner_AP_selection_only |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447887 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.354747 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.388790 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.239026 |
| LogisticRegression | Full | 1 | {"classifier__C": 0.1} | 0.420089 |
| LogisticRegression | No Economic Indicators | 1 | {"classifier__C": 0.1} | 0.332856 |
| LogisticRegression | No Previous Campaign History | 1 | {"classifier__C": 1.0} | 0.353287 |
| LogisticRegression | Customer Attributes Only | 1 | {"classifier__C": 0.1} | 0.202501 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.448053 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.354214 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.385514 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.237556 |
| LogisticRegression | Full | 2 | {"classifier__C": 0.1} | 0.424254 |
| LogisticRegression | No Economic Indicators | 2 | {"classifier__C": 0.1} | 0.342613 |
| LogisticRegression | No Previous Campaign History | 2 | {"classifier__C": 1.0} | 0.356946 |
| LogisticRegression | Customer Attributes Only | 2 | {"classifier__C": 0.1} | 0.206778 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.449117 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.348147 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.390891 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.228336 |
| LogisticRegression | Full | 3 | {"classifier__C": 0.1} | 0.429173 |
| LogisticRegression | No Economic Indicators | 3 | {"classifier__C": 0.1} | 0.339208 |
| LogisticRegression | No Previous Campaign History | 3 | {"classifier__C": 1.0} | 0.365666 |
| LogisticRegression | Customer Attributes Only | 3 | {"classifier__C": 0.1} | 0.207323 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.439208 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.337017 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.392714 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.232150 |
| LogisticRegression | Full | 4 | {"classifier__C": 0.1} | 0.420936 |
| LogisticRegression | No Economic Indicators | 4 | {"classifier__C": 1.0} | 0.334378 |
| LogisticRegression | No Previous Campaign History | 4 | {"classifier__C": 0.1} | 0.356622 |
| LogisticRegression | Customer Attributes Only | 4 | {"classifier__C": 0.1} | 0.202445 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441518 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.344936 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.387400 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.230394 |
| LogisticRegression | Full | 5 | {"classifier__C": 0.1} | 0.420355 |
| LogisticRegression | No Economic Indicators | 5 | {"classifier__C": 0.1} | 0.330268 |
| LogisticRegression | No Previous Campaign History | 5 | {"classifier__C": 1.0} | 0.355674 |
| LogisticRegression | Customer Attributes Only | 5 | {"classifier__C": 0.1} | 0.200701 |

Every candidate's inner AP (model-selection estimates only):

| model | feature_group | outer_fold | parameters | inner_AP_mean_selection_only | inner_AP_sample_SD | rank |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447887 | 0.031014 | 1 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.440386 | 0.029071 | 8 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.442757 | 0.030448 | 4 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.433699 | 0.027028 | 12 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.442555 | 0.027097 | 5 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.436154 | 0.028676 | 11 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.431907 | 0.028558 | 14 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.423397 | 0.027666 | 15 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447326 | 0.029205 | 2 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.443312 | 0.028093 | 3 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.442305 | 0.028678 | 6 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.437256 | 0.026840 | 10 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441527 | 0.029359 | 7 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.437813 | 0.027225 | 9 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.432298 | 0.030351 | 13 |
| HistGradientBoosting | Full | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.422612 | 0.025874 | 16 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.354747 | 0.025342 | 1 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.351687 | 0.025453 | 3 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.350483 | 0.026658 | 4 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.344217 | 0.025506 | 10 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.349778 | 0.024996 | 5 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.341172 | 0.025236 | 12 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.340795 | 0.025060 | 13 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.330240 | 0.023087 | 16 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.353413 | 0.026971 | 2 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.349634 | 0.026807 | 6 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.349250 | 0.026572 | 7 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.344219 | 0.023484 | 9 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.348945 | 0.027382 | 8 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.343428 | 0.023882 | 11 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.339639 | 0.025166 | 14 |
| HistGradientBoosting | No Economic Indicators | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.332908 | 0.023190 | 15 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.385482 | 0.021661 | 3 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.384098 | 0.024960 | 6 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.381888 | 0.022354 | 7 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.376779 | 0.023612 | 12 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.381071 | 0.020664 | 9 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.376252 | 0.022081 | 14 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.376531 | 0.020099 | 13 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.366931 | 0.025974 | 16 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.387214 | 0.024292 | 2 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.388790 | 0.024699 | 1 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.384162 | 0.024903 | 4 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.381286 | 0.023339 | 8 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.384161 | 0.023936 | 5 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.379990 | 0.022581 | 10 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.377853 | 0.023940 | 11 |
| HistGradientBoosting | No Previous Campaign History | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.371688 | 0.021792 | 15 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.239026 | 0.020231 | 1 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.236277 | 0.017668 | 3 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.234507 | 0.018826 | 7 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.230941 | 0.018092 | 10 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.231712 | 0.015640 | 8 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.228309 | 0.015533 | 13 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.225621 | 0.016336 | 14 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.218798 | 0.017034 | 16 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.238500 | 0.019892 | 2 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.235834 | 0.018826 | 4 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.234962 | 0.018999 | 5 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.231405 | 0.019450 | 9 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.234650 | 0.018979 | 6 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.229463 | 0.015619 | 11 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.228881 | 0.017307 | 12 |
| HistGradientBoosting | Customer Attributes Only | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.221906 | 0.016269 | 15 |
| LogisticRegression | Full | 1 | {"classifier__C": 0.1} | 0.420089 | 0.024124 | 1 |
| LogisticRegression | Full | 1 | {"classifier__C": 1.0} | 0.419482 | 0.024330 | 2 |
| LogisticRegression | Full | 1 | {"classifier__C": 10.0} | 0.419301 | 0.024441 | 3 |
| LogisticRegression | No Economic Indicators | 1 | {"classifier__C": 0.1} | 0.332856 | 0.022908 | 1 |
| LogisticRegression | No Economic Indicators | 1 | {"classifier__C": 1.0} | 0.332052 | 0.023271 | 2 |
| LogisticRegression | No Economic Indicators | 1 | {"classifier__C": 10.0} | 0.331773 | 0.023250 | 3 |
| LogisticRegression | No Previous Campaign History | 1 | {"classifier__C": 0.1} | 0.353113 | 0.011805 | 2 |
| LogisticRegression | No Previous Campaign History | 1 | {"classifier__C": 1.0} | 0.353287 | 0.012004 | 1 |
| LogisticRegression | No Previous Campaign History | 1 | {"classifier__C": 10.0} | 0.353073 | 0.011726 | 3 |
| LogisticRegression | Customer Attributes Only | 1 | {"classifier__C": 0.1} | 0.202501 | 0.010617 | 1 |
| LogisticRegression | Customer Attributes Only | 1 | {"classifier__C": 1.0} | 0.201641 | 0.010447 | 2 |
| LogisticRegression | Customer Attributes Only | 1 | {"classifier__C": 10.0} | 0.201507 | 0.010377 | 3 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447211 | 0.026291 | 2 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.443425 | 0.028580 | 8 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.444159 | 0.029082 | 7 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.437493 | 0.028210 | 13 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.444227 | 0.030402 | 6 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.438155 | 0.027961 | 11 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.436524 | 0.031091 | 14 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.429241 | 0.026466 | 15 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.448053 | 0.029665 | 1 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.446022 | 0.028696 | 4 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.446296 | 0.031430 | 3 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.440136 | 0.030691 | 9 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.444417 | 0.029795 | 5 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.437534 | 0.027361 | 12 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.439630 | 0.030830 | 10 |
| HistGradientBoosting | Full | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.428691 | 0.029186 | 16 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.354214 | 0.026411 | 1 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.348206 | 0.026836 | 8 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.351258 | 0.024704 | 5 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.345187 | 0.027028 | 14 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.351312 | 0.022566 | 4 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.345708 | 0.026013 | 11 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.346045 | 0.027165 | 10 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.333099 | 0.024432 | 16 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.353568 | 0.025119 | 2 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.349147 | 0.023449 | 7 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.350971 | 0.025794 | 6 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.345446 | 0.024140 | 13 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.351637 | 0.023382 | 3 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.345687 | 0.023524 | 12 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.347295 | 0.024282 | 9 |
| HistGradientBoosting | No Economic Indicators | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.337125 | 0.025355 | 15 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.383589 | 0.026168 | 4 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.384428 | 0.025815 | 2 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.379959 | 0.024176 | 8 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.374912 | 0.027912 | 12 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.380394 | 0.028551 | 7 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.374075 | 0.027131 | 14 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.376623 | 0.029464 | 11 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.371887 | 0.030075 | 15 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.385514 | 0.024027 | 1 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.382038 | 0.022885 | 6 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.383582 | 0.026064 | 5 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.374644 | 0.025354 | 13 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.383727 | 0.028150 | 3 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.376931 | 0.025937 | 10 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.379932 | 0.028469 | 9 |
| HistGradientBoosting | No Previous Campaign History | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.371180 | 0.028612 | 16 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.235433 | 0.013823 | 4 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.233655 | 0.012941 | 7 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.234508 | 0.014417 | 5 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.228817 | 0.013370 | 14 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.233952 | 0.014273 | 6 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.229895 | 0.014371 | 13 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.230509 | 0.012800 | 12 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.220390 | 0.013126 | 16 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.237556 | 0.014518 | 1 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.233030 | 0.013222 | 8 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.236442 | 0.013776 | 3 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.230707 | 0.013753 | 11 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.237167 | 0.014049 | 2 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.231190 | 0.013945 | 10 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.231352 | 0.013367 | 9 |
| HistGradientBoosting | Customer Attributes Only | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.224170 | 0.012232 | 15 |
| LogisticRegression | Full | 2 | {"classifier__C": 0.1} | 0.424254 | 0.028525 | 1 |
| LogisticRegression | Full | 2 | {"classifier__C": 1.0} | 0.423837 | 0.029173 | 2 |
| LogisticRegression | Full | 2 | {"classifier__C": 10.0} | 0.423763 | 0.029272 | 3 |
| LogisticRegression | No Economic Indicators | 2 | {"classifier__C": 0.1} | 0.342613 | 0.027748 | 1 |
| LogisticRegression | No Economic Indicators | 2 | {"classifier__C": 1.0} | 0.341592 | 0.027525 | 2 |
| LogisticRegression | No Economic Indicators | 2 | {"classifier__C": 10.0} | 0.341404 | 0.027464 | 3 |
| LogisticRegression | No Previous Campaign History | 2 | {"classifier__C": 0.1} | 0.356902 | 0.026857 | 2 |
| LogisticRegression | No Previous Campaign History | 2 | {"classifier__C": 1.0} | 0.356946 | 0.027127 | 1 |
| LogisticRegression | No Previous Campaign History | 2 | {"classifier__C": 10.0} | 0.356763 | 0.027129 | 3 |
| LogisticRegression | Customer Attributes Only | 2 | {"classifier__C": 0.1} | 0.206778 | 0.020582 | 1 |
| LogisticRegression | Customer Attributes Only | 2 | {"classifier__C": 1.0} | 0.206411 | 0.021680 | 2 |
| LogisticRegression | Customer Attributes Only | 2 | {"classifier__C": 10.0} | 0.206214 | 0.021830 | 3 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.448758 | 0.022024 | 2 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.443508 | 0.023505 | 6 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.442987 | 0.022323 | 7 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.433621 | 0.025046 | 13 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.442431 | 0.019630 | 8 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.435187 | 0.024899 | 12 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.433026 | 0.020852 | 14 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.423249 | 0.019764 | 16 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.449117 | 0.021630 | 1 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.443981 | 0.024783 | 4 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.443939 | 0.019865 | 5 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.437736 | 0.024397 | 10 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.444211 | 0.019595 | 3 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.438953 | 0.023631 | 9 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.435964 | 0.019116 | 11 |
| HistGradientBoosting | Full | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.429198 | 0.022365 | 15 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.346684 | 0.027900 | 3 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.344175 | 0.024130 | 6 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.344924 | 0.026062 | 5 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.337587 | 0.022381 | 12 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.343938 | 0.026627 | 7 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.337188 | 0.023246 | 14 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.338738 | 0.024653 | 11 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.329368 | 0.021387 | 16 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.348147 | 0.028336 | 1 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.343638 | 0.026126 | 8 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.346786 | 0.025921 | 2 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.337458 | 0.023629 | 13 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.346667 | 0.025839 | 4 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.341712 | 0.022319 | 9 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.341116 | 0.024325 | 10 |
| HistGradientBoosting | No Economic Indicators | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.333435 | 0.024657 | 15 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.390891 | 0.015528 | 1 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.382863 | 0.014145 | 5 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.382089 | 0.013931 | 7 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.374526 | 0.014383 | 12 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.380672 | 0.013746 | 8 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.374305 | 0.013403 | 13 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.373624 | 0.013172 | 14 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.365971 | 0.015673 | 16 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.389839 | 0.015908 | 2 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.385702 | 0.013720 | 3 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.383740 | 0.015378 | 4 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.376881 | 0.012920 | 11 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.382779 | 0.015088 | 6 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.378299 | 0.014794 | 9 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.378108 | 0.014015 | 10 |
| HistGradientBoosting | No Previous Campaign History | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.369162 | 0.012693 | 15 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.228336 | 0.011042 | 1 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.224633 | 0.012787 | 8 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.226519 | 0.011520 | 5 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.222551 | 0.014019 | 10 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.225893 | 0.011678 | 6 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.220756 | 0.014270 | 14 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.221775 | 0.014888 | 13 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.212724 | 0.015180 | 16 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.227989 | 0.010874 | 2 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.225265 | 0.012741 | 7 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.226879 | 0.012229 | 3 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.222374 | 0.014392 | 11 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.226686 | 0.012412 | 4 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.221967 | 0.015511 | 12 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.223682 | 0.013607 | 9 |
| HistGradientBoosting | Customer Attributes Only | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.215442 | 0.016458 | 15 |
| LogisticRegression | Full | 3 | {"classifier__C": 0.1} | 0.429173 | 0.025237 | 1 |
| LogisticRegression | Full | 3 | {"classifier__C": 1.0} | 0.428439 | 0.024909 | 2 |
| LogisticRegression | Full | 3 | {"classifier__C": 10.0} | 0.428369 | 0.024881 | 3 |
| LogisticRegression | No Economic Indicators | 3 | {"classifier__C": 0.1} | 0.339208 | 0.029387 | 1 |
| LogisticRegression | No Economic Indicators | 3 | {"classifier__C": 1.0} | 0.339168 | 0.028283 | 2 |
| LogisticRegression | No Economic Indicators | 3 | {"classifier__C": 10.0} | 0.339123 | 0.028206 | 3 |
| LogisticRegression | No Previous Campaign History | 3 | {"classifier__C": 0.1} | 0.364594 | 0.019997 | 3 |
| LogisticRegression | No Previous Campaign History | 3 | {"classifier__C": 1.0} | 0.365666 | 0.019942 | 1 |
| LogisticRegression | No Previous Campaign History | 3 | {"classifier__C": 10.0} | 0.365652 | 0.019879 | 2 |
| LogisticRegression | Customer Attributes Only | 3 | {"classifier__C": 0.1} | 0.207323 | 0.011967 | 1 |
| LogisticRegression | Customer Attributes Only | 3 | {"classifier__C": 1.0} | 0.206133 | 0.011788 | 2 |
| LogisticRegression | Customer Attributes Only | 3 | {"classifier__C": 10.0} | 0.205635 | 0.011161 | 3 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.439208 | 0.011794 | 1 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.433708 | 0.010781 | 5 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.433523 | 0.008475 | 6 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.428145 | 0.009472 | 12 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.431617 | 0.008350 | 8 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.428140 | 0.006065 | 13 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.426273 | 0.007693 | 14 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.419281 | 0.004707 | 16 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.438721 | 0.011393 | 2 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.436915 | 0.008905 | 3 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.435087 | 0.011225 | 4 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.430998 | 0.009263 | 9 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.432601 | 0.010686 | 7 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.429814 | 0.009490 | 11 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.430500 | 0.010940 | 10 |
| HistGradientBoosting | Full | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.420596 | 0.008911 | 15 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.336354 | 0.014209 | 5 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.334201 | 0.010856 | 8 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.337017 | 0.012392 | 1 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.330200 | 0.010133 | 12 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.336133 | 0.012253 | 6 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.329044 | 0.010373 | 13 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.332382 | 0.012786 | 10 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.320016 | 0.010642 | 16 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.336587 | 0.013135 | 3 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.334822 | 0.009479 | 7 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.336473 | 0.013395 | 4 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.331189 | 0.010048 | 11 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.336652 | 0.011159 | 2 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.328789 | 0.009503 | 14 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.333120 | 0.008955 | 9 |
| HistGradientBoosting | No Economic Indicators | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.321937 | 0.007941 | 15 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.388207 | 0.013918 | 6 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.390883 | 0.014317 | 2 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.388942 | 0.015708 | 5 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.386086 | 0.020608 | 8 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.384230 | 0.012953 | 11 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.382623 | 0.017003 | 13 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.382141 | 0.016094 | 14 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.375094 | 0.017809 | 16 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.389118 | 0.016034 | 3 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.392714 | 0.012746 | 1 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.389059 | 0.016549 | 4 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.385356 | 0.017940 | 9 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.387869 | 0.014506 | 7 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.383845 | 0.014892 | 12 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.384667 | 0.014571 | 10 |
| HistGradientBoosting | No Previous Campaign History | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.377628 | 0.015657 | 15 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.230843 | 0.013980 | 4 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.229921 | 0.012861 | 7 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.230664 | 0.012908 | 6 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.227874 | 0.010324 | 12 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.230708 | 0.013384 | 5 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.226719 | 0.010864 | 14 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.228720 | 0.012904 | 10 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.218466 | 0.007961 | 16 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.232110 | 0.014859 | 2 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.229744 | 0.013027 | 8 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.232150 | 0.013420 | 1 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.228145 | 0.009904 | 11 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.231652 | 0.013724 | 3 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.227129 | 0.010765 | 13 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.229386 | 0.011060 | 9 |
| HistGradientBoosting | Customer Attributes Only | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.220462 | 0.009915 | 15 |
| LogisticRegression | Full | 4 | {"classifier__C": 0.1} | 0.420936 | 0.015567 | 1 |
| LogisticRegression | Full | 4 | {"classifier__C": 1.0} | 0.420098 | 0.015264 | 3 |
| LogisticRegression | Full | 4 | {"classifier__C": 10.0} | 0.420158 | 0.015606 | 2 |
| LogisticRegression | No Economic Indicators | 4 | {"classifier__C": 0.1} | 0.333720 | 0.021413 | 3 |
| LogisticRegression | No Economic Indicators | 4 | {"classifier__C": 1.0} | 0.334378 | 0.022382 | 1 |
| LogisticRegression | No Economic Indicators | 4 | {"classifier__C": 10.0} | 0.334165 | 0.022353 | 2 |
| LogisticRegression | No Previous Campaign History | 4 | {"classifier__C": 0.1} | 0.356622 | 0.012062 | 1 |
| LogisticRegression | No Previous Campaign History | 4 | {"classifier__C": 1.0} | 0.356489 | 0.012276 | 2 |
| LogisticRegression | No Previous Campaign History | 4 | {"classifier__C": 10.0} | 0.356314 | 0.012168 | 3 |
| LogisticRegression | Customer Attributes Only | 4 | {"classifier__C": 0.1} | 0.202445 | 0.013893 | 1 |
| LogisticRegression | Customer Attributes Only | 4 | {"classifier__C": 1.0} | 0.202226 | 0.014050 | 2 |
| LogisticRegression | Customer Attributes Only | 4 | {"classifier__C": 10.0} | 0.202096 | 0.013905 | 3 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441299 | 0.015309 | 2 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.436628 | 0.017586 | 7 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.437847 | 0.015683 | 3 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.430425 | 0.017801 | 12 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.434567 | 0.012886 | 8 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.431364 | 0.016225 | 10 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.428601 | 0.012969 | 14 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.420687 | 0.016479 | 16 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441518 | 0.015292 | 1 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.437500 | 0.016490 | 4 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.437407 | 0.013156 | 5 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.432322 | 0.014983 | 9 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.437324 | 0.015410 | 6 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.430342 | 0.015912 | 13 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.431290 | 0.014613 | 11 |
| HistGradientBoosting | Full | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.423067 | 0.018126 | 15 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.344164 | 0.008783 | 2 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.343281 | 0.009273 | 4 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.342671 | 0.009163 | 6 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.338403 | 0.008205 | 10 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.342050 | 0.009254 | 8 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.337156 | 0.007954 | 12 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.336539 | 0.012876 | 14 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.328204 | 0.011576 | 16 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.344936 | 0.009460 | 1 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.343107 | 0.006951 | 5 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.343686 | 0.009213 | 3 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.338852 | 0.008497 | 9 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.342205 | 0.009317 | 7 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.337172 | 0.009139 | 11 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.336694 | 0.008857 | 13 |
| HistGradientBoosting | No Economic Indicators | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.328966 | 0.010573 | 15 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.387400 | 0.018126 | 1 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.379984 | 0.017641 | 8 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.383048 | 0.013535 | 5 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.376430 | 0.014300 | 14 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.382044 | 0.012093 | 7 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.377001 | 0.011320 | 13 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.377616 | 0.011106 | 11 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.369252 | 0.014028 | 16 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.386511 | 0.021600 | 2 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.383323 | 0.014183 | 4 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.382220 | 0.016884 | 6 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.378606 | 0.009977 | 9 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.384320 | 0.013459 | 3 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.377274 | 0.014650 | 12 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.377706 | 0.013008 | 10 |
| HistGradientBoosting | No Previous Campaign History | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.370329 | 0.014546 | 15 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.229527 | 0.011796 | 4 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.228238 | 0.011834 | 7 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.228382 | 0.011596 | 5 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.225673 | 0.012796 | 11 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.227835 | 0.012396 | 8 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.225103 | 0.013146 | 13 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.224242 | 0.011822 | 14 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.218405 | 0.012233 | 16 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.230282 | 0.011065 | 2 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.230014 | 0.011327 | 3 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.230394 | 0.012076 | 1 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.226276 | 0.012621 | 10 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.228293 | 0.012640 | 6 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.227519 | 0.011319 | 9 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.225120 | 0.012546 | 12 |
| HistGradientBoosting | Customer Attributes Only | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.222129 | 0.011178 | 15 |
| LogisticRegression | Full | 5 | {"classifier__C": 0.1} | 0.420355 | 0.008603 | 1 |
| LogisticRegression | Full | 5 | {"classifier__C": 1.0} | 0.419858 | 0.009049 | 2 |
| LogisticRegression | Full | 5 | {"classifier__C": 10.0} | 0.419556 | 0.008948 | 3 |
| LogisticRegression | No Economic Indicators | 5 | {"classifier__C": 0.1} | 0.330268 | 0.013094 | 1 |
| LogisticRegression | No Economic Indicators | 5 | {"classifier__C": 1.0} | 0.330066 | 0.013540 | 2 |
| LogisticRegression | No Economic Indicators | 5 | {"classifier__C": 10.0} | 0.329986 | 0.013799 | 3 |
| LogisticRegression | No Previous Campaign History | 5 | {"classifier__C": 0.1} | 0.355572 | 0.009641 | 2 |
| LogisticRegression | No Previous Campaign History | 5 | {"classifier__C": 1.0} | 0.355674 | 0.009240 | 1 |
| LogisticRegression | No Previous Campaign History | 5 | {"classifier__C": 10.0} | 0.355474 | 0.009173 | 3 |
| LogisticRegression | Customer Attributes Only | 5 | {"classifier__C": 0.1} | 0.200701 | 0.015577 | 1 |
| LogisticRegression | Customer Attributes Only | 5 | {"classifier__C": 1.0} | 0.199722 | 0.014574 | 2 |
| LogisticRegression | Customer Attributes Only | 5 | {"classifier__C": 10.0} | 0.199635 | 0.014552 | 3 |

## Computational cost

| model | feature_group | outer_fold | candidates | candidate_fold_fits | outer_refits | search_refit_seconds | outer_prediction_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Full | 1 | 16 | 80 | 1 | 77.466870 | 0.042047 |
| HistGradientBoosting | No Economic Indicators | 1 | 16 | 80 | 1 | 71.377293 | 0.042457 |
| HistGradientBoosting | No Previous Campaign History | 1 | 16 | 80 | 1 | 73.383965 | 0.044641 |
| HistGradientBoosting | Customer Attributes Only | 1 | 16 | 80 | 1 | 68.891240 | 0.044296 |
| LogisticRegression | Full | 1 | 3 | 15 | 1 | 1.435740 | 0.019971 |
| LogisticRegression | No Economic Indicators | 1 | 3 | 15 | 1 | 1.298198 | 0.018954 |
| LogisticRegression | No Previous Campaign History | 1 | 3 | 15 | 1 | 1.542963 | 0.017709 |
| LogisticRegression | Customer Attributes Only | 1 | 3 | 15 | 1 | 1.355114 | 0.019986 |
| HistGradientBoosting | Full | 2 | 16 | 80 | 1 | 78.188098 | 0.048252 |
| HistGradientBoosting | No Economic Indicators | 2 | 16 | 80 | 1 | 72.506163 | 0.041519 |
| HistGradientBoosting | No Previous Campaign History | 2 | 16 | 80 | 1 | 76.436702 | 0.046057 |
| HistGradientBoosting | Customer Attributes Only | 2 | 16 | 80 | 1 | 70.910983 | 0.043970 |
| LogisticRegression | Full | 2 | 3 | 15 | 1 | 1.742674 | 0.019466 |
| LogisticRegression | No Economic Indicators | 2 | 3 | 15 | 1 | 1.361270 | 0.023405 |
| LogisticRegression | No Previous Campaign History | 2 | 3 | 15 | 1 | 1.417412 | 0.017107 |
| LogisticRegression | Customer Attributes Only | 2 | 3 | 15 | 1 | 1.169695 | 0.016429 |
| HistGradientBoosting | Full | 3 | 16 | 80 | 1 | 78.982849 | 0.042501 |
| HistGradientBoosting | No Economic Indicators | 3 | 16 | 80 | 1 | 69.711487 | 0.039435 |
| HistGradientBoosting | No Previous Campaign History | 3 | 16 | 80 | 1 | 72.227685 | 0.040394 |
| HistGradientBoosting | Customer Attributes Only | 3 | 16 | 80 | 1 | 69.382150 | 0.042692 |
| LogisticRegression | Full | 3 | 3 | 15 | 1 | 1.590229 | 0.021220 |
| LogisticRegression | No Economic Indicators | 3 | 3 | 15 | 1 | 1.350786 | 0.022238 |
| LogisticRegression | No Previous Campaign History | 3 | 3 | 15 | 1 | 1.565196 | 0.018169 |
| LogisticRegression | Customer Attributes Only | 3 | 3 | 15 | 1 | 1.285474 | 0.018203 |
| HistGradientBoosting | Full | 4 | 16 | 80 | 1 | 77.853591 | 0.045559 |
| HistGradientBoosting | No Economic Indicators | 4 | 16 | 80 | 1 | 74.799663 | 0.074238 |
| HistGradientBoosting | No Previous Campaign History | 4 | 16 | 80 | 1 | 76.664623 | 0.046260 |
| HistGradientBoosting | Customer Attributes Only | 4 | 16 | 80 | 1 | 69.815856 | 0.065147 |
| LogisticRegression | Full | 4 | 3 | 15 | 1 | 1.681462 | 0.023629 |
| LogisticRegression | No Economic Indicators | 4 | 3 | 15 | 1 | 1.286804 | 0.020368 |
| LogisticRegression | No Previous Campaign History | 4 | 3 | 15 | 1 | 1.419579 | 0.017854 |
| LogisticRegression | Customer Attributes Only | 4 | 3 | 15 | 1 | 1.221323 | 0.017535 |
| HistGradientBoosting | Full | 5 | 16 | 80 | 1 | 83.851595 | 0.043913 |
| HistGradientBoosting | No Economic Indicators | 5 | 16 | 80 | 1 | 70.889140 | 0.043658 |
| HistGradientBoosting | No Previous Campaign History | 5 | 16 | 80 | 1 | 75.830805 | 0.049315 |
| HistGradientBoosting | Customer Attributes Only | 5 | 16 | 80 | 1 | 68.372794 | 0.058216 |
| LogisticRegression | Full | 5 | 3 | 15 | 1 | 1.884776 | 0.023741 |
| LogisticRegression | No Economic Indicators | 5 | 3 | 15 | 1 | 1.504959 | 0.020149 |
| LogisticRegression | No Previous Campaign History | 5 | 3 | 15 | 1 | 1.441849 | 0.017903 |
| LogisticRegression | Customer Attributes Only | 5 | 3 | 15 | 1 | 1.289429 | 0.018476 |

| model | feature_group | candidate_fold_fits | outer_refits | search_refit_seconds | prediction_seconds |
| --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Customer Attributes Only | 400 | 5 | 347.373022 | 0.254321 |
| HistGradientBoosting | Full | 400 | 5 | 396.343005 | 0.222272 |
| HistGradientBoosting | No Economic Indicators | 400 | 5 | 359.283747 | 0.241308 |
| HistGradientBoosting | No Previous Campaign History | 400 | 5 | 374.543779 | 0.226667 |
| LogisticRegression | Customer Attributes Only | 75 | 5 | 6.321035 | 0.090628 |
| LogisticRegression | Full | 75 | 5 | 8.334880 | 0.108028 |
| LogisticRegression | No Economic Indicators | 75 | 5 | 6.802017 | 0.105115 |
| LogisticRegression | No Previous Campaign History | 75 | 5 | 7.386999 | 0.088742 |

Elapsed through experiments, figures and tests: 1512.60s. Versions: sklearn 1.8.0, pandas 2.2.3, NumPy 2.3.5. GridSearchCV/native threads limited to one. No reduction/expansion of approved grids. Colab instructions are in the executed notebook; local Python execution is verified, hosted Colab was not directly exercised. Previous grids/results were preserved.

## Technical leakage and reproducibility audit

All 1,940 fresh complete pipeline fits and 1,940 probability calls passed partition assertions. Every fit uses exactly an authorized inner-training partition or outer-training refit, never all development; all fitting/prediction rows exclude held-out indices. Validation prediction rows are disjoint from their estimator's fitting rows, with exact authorized cohort identity. Threshold stays .50. No outer-label feature/hyperparameter/threshold selection.

Every OHE category vocabulary matches its fitting rows. LR ordinary mean/variance/scale/sample count equals fitting-only selected numerical data. Available-only conditional statistics match fitting observations; unavailable days remain zero and availability remains unscaled on validation. History-free configurations have no recency component or names. HGB selected numerical/recency outputs equal the raw subset values exactly. Validation transformation signatures stay fixed. Finite representations/probabilities/metrics, [0,1] class order, seeds, no weighting/resampling, full-feature original equivalence and original CV replication all passed. Source hashes and development snapshot unchanged after execution; separate final Git checks compare all pre-existing tracked artifacts against approved main byte-for-byte.

| model | feature_group | role | rows | input_columns | output_columns | recency_component | fits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Customer Attributes Only | inner-training fit | 21081 | 7 | 33 | removed | 16 |
| HistGradientBoosting | Customer Attributes Only | inner-training fit | 21081 | 7 | 34 | removed | 144 |
| HistGradientBoosting | Customer Attributes Only | inner-training fit | 21082 | 7 | 33 | removed | 16 |
| HistGradientBoosting | Customer Attributes Only | inner-training fit | 21082 | 7 | 34 | removed | 224 |
| HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | 5 |
| HistGradientBoosting | Full | inner-training fit | 21081 | 15 | 41 | included | 16 |
| HistGradientBoosting | Full | inner-training fit | 21081 | 15 | 42 | included | 144 |
| HistGradientBoosting | Full | inner-training fit | 21082 | 15 | 41 | included | 16 |
| HistGradientBoosting | Full | inner-training fit | 21082 | 15 | 42 | included | 224 |
| HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | 5 |
| HistGradientBoosting | No Economic Indicators | inner-training fit | 21081 | 10 | 36 | included | 16 |
| HistGradientBoosting | No Economic Indicators | inner-training fit | 21081 | 10 | 37 | included | 144 |
| HistGradientBoosting | No Economic Indicators | inner-training fit | 21082 | 10 | 36 | included | 16 |
| HistGradientBoosting | No Economic Indicators | inner-training fit | 21082 | 10 | 37 | included | 224 |
| HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 5 |
| HistGradientBoosting | No Previous Campaign History | inner-training fit | 21081 | 12 | 38 | removed | 16 |
| HistGradientBoosting | No Previous Campaign History | inner-training fit | 21081 | 12 | 39 | removed | 144 |
| HistGradientBoosting | No Previous Campaign History | inner-training fit | 21082 | 12 | 38 | removed | 16 |
| HistGradientBoosting | No Previous Campaign History | inner-training fit | 21082 | 12 | 39 | removed | 224 |
| HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | 5 |
| LogisticRegression | Customer Attributes Only | inner-training fit | 21081 | 7 | 33 | removed | 3 |
| LogisticRegression | Customer Attributes Only | inner-training fit | 21081 | 7 | 34 | removed | 27 |
| LogisticRegression | Customer Attributes Only | inner-training fit | 21082 | 7 | 33 | removed | 3 |
| LogisticRegression | Customer Attributes Only | inner-training fit | 21082 | 7 | 34 | removed | 42 |
| LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | 5 |
| LogisticRegression | Full | inner-training fit | 21081 | 15 | 41 | included | 3 |
| LogisticRegression | Full | inner-training fit | 21081 | 15 | 42 | included | 27 |
| LogisticRegression | Full | inner-training fit | 21082 | 15 | 41 | included | 3 |
| LogisticRegression | Full | inner-training fit | 21082 | 15 | 42 | included | 42 |
| LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 5 |
| LogisticRegression | No Economic Indicators | inner-training fit | 21081 | 10 | 36 | included | 3 |
| LogisticRegression | No Economic Indicators | inner-training fit | 21081 | 10 | 37 | included | 27 |
| LogisticRegression | No Economic Indicators | inner-training fit | 21082 | 10 | 36 | included | 3 |
| LogisticRegression | No Economic Indicators | inner-training fit | 21082 | 10 | 37 | included | 42 |
| LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 5 |
| LogisticRegression | No Previous Campaign History | inner-training fit | 21081 | 12 | 38 | removed | 3 |
| LogisticRegression | No Previous Campaign History | inner-training fit | 21081 | 12 | 39 | removed | 27 |
| LogisticRegression | No Previous Campaign History | inner-training fit | 21082 | 12 | 38 | removed | 3 |
| LogisticRegression | No Previous Campaign History | inner-training fit | 21082 | 12 | 39 | removed | 42 |
| LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | 5 |

Selected refit statistics (inner candidate fits are also audited above):

| outer_fold | model | feature_group | role | rows | input_columns | output_columns | recency_component | recency_mean | recency_scale | warnings | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 1 | HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 1 | HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 1 | HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 1 | LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 6.070750 | 3.843597 | 0 | PASS |
| 1 | LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 6.070750 | 3.843597 | 0 | PASS |
| 1 | LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 1 | LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 6.022989 | 3.855744 | 0 | PASS |
| 2 | LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 6.022989 | 3.855744 | 0 | PASS |
| 2 | LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 2 | LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 6.024819 | 3.885566 | 0 | PASS |
| 3 | LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 6.024819 | 3.885566 | 0 | PASS |
| 3 | LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 3 | LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 6.208589 | 3.993022 | 0 | PASS |
| 4 | LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 6.208589 | 3.993022 | 0 | PASS |
| 4 | LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 4 | LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | HistGradientBoosting | Full | outer-training refit | 26352 | 15 | 42 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | HistGradientBoosting | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | HistGradientBoosting | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | HistGradientBoosting | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | LogisticRegression | Full | outer-training refit | 26352 | 15 | 42 | included | 6.097038 | 3.992815 | 0 | PASS |
| 5 | LogisticRegression | No Economic Indicators | outer-training refit | 26352 | 10 | 37 | included | 6.097038 | 3.992815 | 0 | PASS |
| 5 | LogisticRegression | No Previous Campaign History | outer-training refit | 26352 | 12 | 39 | removed | not scaled / absent | not scaled / absent | 0 | PASS |
| 5 | LogisticRegression | Customer Attributes Only | outer-training refit | 26352 | 7 | 34 | removed | not scaled / absent | not scaled / absent | 0 | PASS |

Inner-fold manifest, identical across models/groups:

| outer_fold | inner_fold | fit_rows | validation_rows | validation_row_sha256 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 21081 | 5271 | 7e8b5302e5eafb75153470b1d4fa55eca90704f9a95e0e13ed5c85deba5bcbe9 |
| 1 | 2 | 21081 | 5271 | b39de3d11984f80230b43c4bc0885bb9aba45b665d06744b816efa1352edc6ec |
| 1 | 3 | 21082 | 5270 | 45ee03ffde5df5088e85da744281f7418402bcead26afe123be40c9c82e92acc |
| 1 | 4 | 21082 | 5270 | ecb5d2e223590b50e552be102ed30131259499ce4a82b238f4820d419bb9faac |
| 1 | 5 | 21082 | 5270 | d8f918784b127dba07b74994b041fe0684acf86104711e7d95f07377bcce2e0e |
| 2 | 1 | 21081 | 5271 | 55013b6f2af26b49bcc512c318533f754ffb48dbe8209b74225b8ec740529bbd |
| 2 | 2 | 21081 | 5271 | 036cad2ce15624dce29a2bc59f90d26084c2b49eff6178dd2deab21cc42d531b |
| 2 | 3 | 21082 | 5270 | cd2ec5a0b84903e201d6139ad7a4d60fc5b1891e6e5927e23efe9ef0bc3ca9bc |
| 2 | 4 | 21082 | 5270 | 6ca901c486ef83a9abd9253beffeaa1569fba23448f1dd30985d1310faf8912a |
| 2 | 5 | 21082 | 5270 | 03450a42c131b55fbe42cbd626034197f4a73c5f91252e56dd86e1d9909b62e6 |
| 3 | 1 | 21081 | 5271 | d5165c5aa1716154af5579d1712391a4c588acca45568e58a4ad44869ad098d1 |
| 3 | 2 | 21081 | 5271 | 8012b67988f3f27c7349e719dce304563ad345f8665e121a32e22aed096b6ea3 |
| 3 | 3 | 21082 | 5270 | 917743c173f94e120ea352c63cb226d7d14ea67263f9c79da10371b15b0e82b7 |
| 3 | 4 | 21082 | 5270 | 5971e03c1f264355e82cada6d72df7fd5760aa9c4705fe4fce525ddf041555d5 |
| 3 | 5 | 21082 | 5270 | 62b83659cb5c49e6dce34b5ebae1c5348aa1f14f196f4eae53cbb35046d0db98 |
| 4 | 1 | 21081 | 5271 | 7b9fdbe954730f25887d32c809464cd0b024ca8f00010ce2003cef94d7bc22d0 |
| 4 | 2 | 21081 | 5271 | 78e4b0f7288971a0ead2bdf40624a5c44bcc8c82ae5f947cfee90a02d1bd69c6 |
| 4 | 3 | 21082 | 5270 | 77291f5ed2b841f9c12a57051b4eac50955e165cb39723fb5927e117c0d6aab1 |
| 4 | 4 | 21082 | 5270 | 6225bd68f2074fb0def8258254592e70221946e37e939159b43744dc71c117ff |
| 4 | 5 | 21082 | 5270 | deeb556569bb904e7396cef6612f9349c62e60c8540c3dddba2ad3bfeea3f218 |
| 5 | 1 | 21081 | 5271 | 3e0ef6b2ebbdf6b0888eb9798ccffdd90dbce068136f32fcae2da3744af3e336 |
| 5 | 2 | 21081 | 5271 | 6c11632078fceb0968b3d71f189e3403d5b192e7a7cb3e096935b3970f2234d0 |
| 5 | 3 | 21082 | 5270 | 22bbe238f551f3749572d901547e54a4a288cc74f0b03185a10b9da298f4c891 |
| 5 | 4 | 21082 | 5270 | 5dc93495ea90c24daaa3d80468e0d018c5a25868154db7bc137f563a938d4300 |
| 5 | 5 | 21082 | 5270 | 74503bcd217eda8e5b0527e20b6f820758d6f36d11ceb90bc03c6512115c86ad |

Existing preprocessing tests: **PASS — all 4 existing preprocessing tests**.

```text
test_factory_is_unfitted_and_cloneable (test_preprocessing.ConditionalRecencyTests.test_factory_is_unfitted_and_cloneable) ... ok
test_invalid_input_and_unfitted (test_preprocessing.ConditionalRecencyTests.test_invalid_input_and_unfitted) ... ok
test_observed_only_and_no_refit (test_preprocessing.ConditionalRecencyTests.test_observed_only_and_no_refit) ... ok
test_safe_fallbacks (test_preprocessing.ConditionalRecencyTests.test_safe_fallbacks) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.021s

OK
```

Warnings during model fitting:

None recorded during all 1,940 experiment fits.

## Feature availability: facts, hypotheses and unresolved assumptions

**Observed documentation facts:** README describes economic indicators with quarterly/monthly/daily frequencies and history as prior-campaign information, but provides no observation/publication/revision timestamps or campaign-start as-of snapshots. The project planning DOCX asks about economic value, preprocessing and appropriate held-out/CV use; its approximate pre-cleaning split counts differ from the approved post-cleaning saved assignment. Prior approved exclusions (duration, campaign, contact, month, day_of_week and original pdays) remain excluded. The original 999 recency sentinel is not reintroduced.

**Evidence-based interpretation:** dropping economic indicators reduces reliance on shared economic-period information and publication-vintage joins. Dropping history removes dependence on prior-contact cutoff/reference-date definitions. Customer attributes only removes both sources and is a useful conservative information-requirement comparison, at the observed predictive cost. Removing those dependencies can make a proposed information requirement easier to defend; it does not certify pre-campaign availability of the remaining fields.

**Hypotheses, not established facts:** economic values might proxy campaign period or later information; contact history might be updated after campaign start; remaining customer/financial status might be retrospectively recorded. Ablation alone cannot decide whether these explanations cause a performance difference. Confirm customer-record effective dates, history cutoff and recency reference date, economic publication vintages/as-of joins and outcome window with the data owner. Customer-only fields (age/job/marital/education/default/housing/loan) all remain Provisional. All other retained fields are Provisional in groups where present.

Missing customer IDs and dates prevent grouped-client/forward-time validation and allow repeated-client or temporal context overlap across random folds. Prior whole-dataset EDA and development-driven model/grid exploration remain limitations. Random stratified nesting prevents this experiment's direct preprocessing/selection leakage, not every kind of leakage or future-campaign risk. No unseen-client/future-period generalization or independent final performance is established.

## Recommendations for Phase 6B discussion — not executed

Use the observed AP/ROC-AUC and equal-capacity capture losses to discuss the cost of information requirements. Retain full original HGB and original LR as references and consider the prespecified reduced-feature counterparts where their required inputs can be verified; do not automatically retain a full feature just because it raises AP. Do not choose final model, subset or policy from a single best outer mean. The four subsets are sensitivity scenarios, not proof of feature timing or new approved deployment schemas.

Team approval is needed for an acceptable campaign-start feature contract, feasible model/subset shortlist, contact capacity and decision objective, treatment of unresolved timestamps/IDs, and a prespecified final development-only model/policy-selection procedure before any one-time held-out evaluation. No threshold search, final policy, Phase 6B, commit or push has been performed. Deliverables: 09_feature_ablation.ipynb and 09_feature_ablation_summary.md in the repository, pending review.
