# Phase 3 — Logistic Regression baseline summary

## Scope and data isolation

Academic pre-campaign subscription baseline using approved Provisional predictors. Reused 03_split_indices.json unchanged: 32,940 development rows; 8,236 held-out positions reserved. No new train-test split. Cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` verified before saved indices were applied; this binds row ordering as well as values. Saved positions were checked for bounds, uniqueness, coverage and separation. CSV parsing skipped held-out rows, materializing only development features/labels; no held-out feature/label rows were used for fitting, model selection, performance analysis or threshold tuning. Raw dataset was only byte-hashed if present, not parsed for training.

Reviewed README, project DOCX, Phase 2B cleaning summary/data, Phase 2C summary/split/notebook, preprocessing.py and tests/test_preprocessing.py. No approved preprocessing code was replaced or modified. Current request approves this limited experiment while feature-timing concerns remain.

## Model configurations

- DummyClassifier(strategy='most_frequent'), learning only each training-fold majority class. Constant placeholder covariates are used because DummyClassifier ignores customer features. Metrics use predict_proba for class 1 where appropriate.
- LogisticRegression(max_iter=1000, random_state=42, C=1.0, class_weight=None, solver='lbfgs'), default L2 regularization, no resampling. Threshold fixed at 0.5, not optimized. Each new complete sklearn Pipeline is [('preprocessing', make_preprocessor('logistic_regression')), ('classifier', LogisticRegression(...))]. The existing factory is used without modification or prefit.
- Reused full OneHotEncoder, seven-feature StandardScaler and ConditionalRecencyScaler. No full-development preprocessing, no tree/forest models, no GridSearchCV, no hyperparameter/class-weight/threshold trials.

Versions: scikit-learn 1.8.0, pandas 2.2.3, NumPy 2.3.5. Notebook is Colab-compatible with uploaded module/cleaned CSV/split JSON; scikit-learn >=1.2 is required. Execution was local standard Python, not a live hosted Colab session.

## Cross-validation design and metric definitions

StratifiedKFold(n_splits=5, shuffle=True, random_state=42), identical fold pairs for both baselines. Every fold fits 26,352 and validates 6,588 development rows. Each development observation has exactly one OOF prediction. All original covariates enter each complete fold pipeline without prior global encoding/scaling. Precision/recall/F1 use positive label 1 and zero_division=0. ROC-AUC and Average Precision (AP) use positive probabilities. PR-AUC is represented by AP, not trapezoidal PR area. Five-fold standard deviations below use ddof=1 (sample SD); folds are dependent, so these are descriptive spread, not confidence intervals.

## Individual fold results

| model | fold | Accuracy | Precision | Recall | F1 | ROC_AUC | Average_Precision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dummy | 1 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112629 |
| LogisticRegression | 1 | 0.899211 | 0.665254 | 0.211590 | 0.321063 | 0.774180 | 0.432213 |
| Dummy | 2 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112629 |
| LogisticRegression | 2 | 0.899059 | 0.680751 | 0.195418 | 0.303665 | 0.759074 | 0.420763 |
| Dummy | 3 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112629 |
| LogisticRegression | 3 | 0.897845 | 0.653333 | 0.198113 | 0.304033 | 0.742628 | 0.403407 |
| Dummy | 4 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112629 |
| LogisticRegression | 4 | 0.898300 | 0.680000 | 0.183288 | 0.288747 | 0.770513 | 0.425606 |
| Dummy | 5 | 0.887219 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112781 |
| LogisticRegression | 5 | 0.901184 | 0.725490 | 0.199192 | 0.312566 | 0.764998 | 0.428919 |

## Dummy versus Logistic Regression: mean ± sample SD

| model | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | Average_Precision mean ± SD |
| --- | --- | --- | --- | --- | --- | --- |
| Dummy | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.500000 ± 0.000000 | 0.112659 ± 0.000068 |
| LogisticRegression | 0.899120 ± 0.001282 | 0.680966 ± 0.027358 | 0.197520 ± 0.010100 | 0.306015 ± 0.012010 | 0.762279 ± 0.012382 | 0.422181 ± 0.011316 |

Mean-score differences LR minus Dummy:

| metric | LR_minus_Dummy_mean |
| --- | --- |
| Accuracy | 0.011779 |
| Precision | 0.680966 |
| Recall | 0.197520 |
| F1 | 0.306015 |
| ROC_AUC | 0.262279 |
| Average_Precision | 0.309522 |

## Development-only OOF diagnostics

Plots embedded in 04_logistic_regression_baseline.ipynb show confusion matrices, ROC and Precision–Recall curves; all use pooled OOF development predictions, never held-out observations. Pooled values are separate from fold averages:

| model | Accuracy | Precision | Recall | F1 | ROC_AUC | Average_Precision |
| --- | --- | --- | --- | --- | --- | --- |
| Dummy | 0.887341 | 0.000000 | 0.000000 | 0.000000 | 0.500000 | 0.112659 |
| LogisticRegression | 0.899120 | 0.679963 | 0.197521 | 0.306118 | 0.762216 | 0.420750 |

Logistic Regression OOF confusion matrix at 0.5 (actual rows no/yes; predicted columns no/yes): [[28884, 345], [2978, 733]]. It predicts 1,078 positives (3.27% of development records); 733 are true subscriptions and 345 false positives. It misses 2,978 actual subscriptions. No threshold was selected using these diagnostics.

## Interpretation: observations versus hypotheses

Observed: development subscription prevalence is 11.2659%. Dummy accuracy is 0.8873, despite precision/recall/F1 all zero; predicting no for everyone exploits the majority class while identifying no subscribers. Its ROC-AUC is 0.5 and AP is prevalence, with no discrimination.

Logistic Regression mean accuracy is 0.8991, precision 0.6810, recall 0.1975, F1 0.3060, ROC-AUC 0.7623 and AP 0.4222. The measured mean accuracy difference is +0.0118; F1 difference +0.3060; ROC-AUC difference +0.2623; AP difference +0.3095. Assessing meaningful business benefit requires call costs/capacity and missed-sale value. These descriptive comparisons are not formal statistical significance or evidence of future deployment performance.

At the fixed threshold, precision and recall must be interpreted together: 68.10% mean precision versus 19.75% mean recall. The positive volume above may support prioritization, but usefulness is not established without business constraints. Score ranges across folds: accuracy 0.8978–0.9012; recall 0.1833–0.2116; ROC-AUC 0.7426–0.7742; AP 0.4034–0.4322. These ranges and SDs indicate reasonably consistent baseline results within this random-fold design, with recall varying by about 2.8 percentage points from lowest to highest fold. Logistic Regression improves ranking and positive detection over Dummy in every fold, but its low recall remains a practical limitation. This does not establish stability across unseen customers or future economic periods.

Hypotheses for later approved experiments: class weighting or altered thresholds may change recall/precision; resampling might help or hurt. None has been tested, so no improvement is asserted. This single fixed baseline cannot determine which alternative would help. Do not alter the held-out set based on these development results.

## Convergence and training-fold leakage audit

| fold | train_rows | validation_rows | observed_recency_training_rows | recency_mean | recency_sd | encoded_features | solver_iterations | convergence_warnings | all_fit_warnings | positive_predictions | training_only_checks | validation_state_unchanged |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 26352 | 6588 | 947 | 6.070750 | 3.843597 | 42 | 36 | 0 | 0 | 236 | PASS | PASS |
| 2 | 26352 | 6588 | 957 | 6.022989 | 3.855744 | 42 | 36 | 0 | 0 | 213 | PASS | PASS |
| 3 | 26352 | 6588 | 967 | 6.024819 | 3.885566 | 42 | 33 | 0 | 0 | 225 | PASS | PASS |
| 4 | 26352 | 6588 | 978 | 6.208589 | 3.993022 | 42 | 27 | 0 | 0 | 200 | PASS | PASS |
| 5 | 26352 | 6588 | 979 | 6.097038 | 3.992815 | 42 | 53 | 0 | 0 | 204 | PASS | PASS |

ConvergenceWarning count: 0. Solver iterations range 27–53, max_iter=1000. Finite coefficients/probabilities/transformed validation matrices were verified. If warnings are present they are disclosed below; no hidden solver/tuning changes were made.

Fit-warning log:

No fit warnings recorded.

All five complete estimator pipelines are distinct, with separate fitted preprocessing and conditional-transformer objects. For each fold, OHE vocabularies match only that fold's training levels; ordinary scaler mean, population variance, scale and sample count match its training rows; recency mean/variance/scale/count match only availability=1 training rows. Validation transforms preserve every audited fitted parameter; unavailable transformed recency remains zero and the availability bit is unscaled. Training/validation indices are disjoint, confined to the saved development partition, and OOF coverage is exactly once per row. No preprocessors were fitted on all development data before CV. No NaN/infinity or input mutation was detected.

Source hash checks for all supplied inputs passed after execution. Saved split and raw/cleaned datasets remain unchanged; the preprocessing module remains unchanged. No final whole-development fit, held-out transform/prediction, or model serialization occurred.

## Remaining limitations and team discussion

All 15 features remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Preprocessing leakage is addressed by fold-specific complete pipelines; feature-timing leakage is unresolved. Verify pre-campaign customer/status snapshots, previous-history cutoff, pdays reference date, economic publication/revision vintages and target outcome/follow-up window. A last-contact-period economic value may be unavailable at campaign start. Neither these metrics nor proper preprocessing certify timing safety.

No customer IDs/full dates means stratified random folds may share clients or economic periods; results cannot guarantee unseen-customer or future-campaign performance. Repeated predictor profiles remain by approval. Prior full-data EDA exposure must be disclosed. Rare categories can be absent in a fold and are handled as unseen without global vocabulary learning. Economic collinearity may complicate coefficient interpretation; no feature selection or causal inference is performed.

## Recommended next steps (not executed)

1. Review baseline results, call-capacity/error costs and unresolved feature availability before approving further experiments.
2. If approved, investigate class weighting and threshold selection strictly on development data with properly nested fold preprocessing; assess any added complexity against this saved baseline. No resampling benefit is claimed.
3. Obtain customer/date metadata for an approved group/time validation design if future/generalization claims are needed; do not replace the saved split without approval.
4. Keep the held-out test reserved for a later explicitly approved final evaluation. Do not start another model family or tune now.

Deliverables: executed 04_logistic_regression_baseline.ipynb and this 04_baseline_summary.md, saved directly in the repository. No commit or push is made pending approval. Phase 3 stops here.
