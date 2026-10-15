# Phase 5A — Nested CV and business targeting comparison

## Scope, provenance and data isolation

Started from fetched latest GitHub main **9cc20a6**, which includes Phase 4B. The local branch was fast-forwarded to that main commit before development; no new merge commit was created. Reviewed preprocessing.py, Phase 2C summaries/split/data, Phase 3 summary, Phase 4 and Phase 4B notebooks/summaries. Existing Decision Tree results remain historical references; DT is not retuned here. No previous result files or approved preprocessing were changed.

Exact cleaned CSV SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` matched saved 03_split_indices.json before applying zero-based row positions. This validates values and row order, not just dimensions. Saved partitions contain 32,940 development and 8,236 held-out positions; unique/disjoint/exhaustive checks passed. Only development CSV rows were parsed and put back into saved development order; held-out feature/label rows were not parsed or used. Original CSV, if present, was only byte-hashed. No new train-test split. Development subscribers: 3,711, prevalence 0.112659 (11.2659%).

Outer validation-position hash `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4` matches Phase 4B's recorded folds. Both outer and inner CV use StratifiedKFold(n_splits=5,shuffle=True,random_state=42), with common outer/inner pairs across the three models. Seeds for every classifier are 42. No class weighting, resampling, feature selection/ablation, threshold optimization, held-out evaluation or Phase 5B work.

Versions: sklearn 1.8.0, pandas 2.2.3, NumPy 2.3.5. Google Colab-compatible notebook requires standard packages and sklearn >=1.2, uploaded preprocessing.py/cleaned CSV/split JSON/Phase 4B summary, or PROJECT_DIR set to mounted Drive. Executed locally, not a live hosted Colab session. threadpoolctl limits native threads to one; GridSearchCV and RF use n_jobs=1.

## Fixed search procedures and nested design

- LR: C=[0.1,1,10], lbfgs/default L2, max_iter=1000, class_weight=None (3 candidates).
- RF: n_estimators=[100,200], max_depth=[10,None], min_samples_leaf=[5,20], max_features='sqrt', class_weight=None (8 candidates).
- HGB: learning_rate=[0.05,0.1], max_iter=[100,200], max_leaf_nodes=[15,31], l2_regularization=[0,1], early_stopping=False, categorical_features=None, class_weight=None (16 candidates).

These exact grids are fixed throughout all outer folds; no outer-result-driven changes. GridSearchCV(scoring=inner_score,refit='AP',cv=inner_folds,n_jobs=1,error_score='raise') selects only by inner Average Precision. The scorer returns the named AP result from positive-class predict_proba. Every search uses only 26,352 outer-training rows, with five inner validation splits (training 21,081/21,082; validation 5,270/5,271). The winner is refitted on all outer-training rows and predicts its 6,588-row untouched outer-validation fold once. There are 675 inner candidate-fold fits plus 15 outer-training refits = **690 fits**; 675 inner-validation probability calls and 15 outer-validation calls. No fitted object ever receives all 32,940 development rows for fitting. No production model was fitted or exported.

Complete pipelines reuse the approved factories. LR retains ordinary numerical scaling and available-only ConditionalRecencyScaler. RF uses its existing unscaled factory; HGB uses the equivalent existing decision_tree factory as approved in Phase 4B, with numeric one-hot indicators (native categorical handling off). An experiment-only stateless finite/representation guard returns arrays unchanged and checks them before classifier fit. Audit wrappers verify every partition and fit/transform state without replacing approved preprocessing. No global encoder/scaler or encoded matrix is cached/shared.

Threshold is fixed at probability >=0.5. Accuracy/precision/recall/F1 use positive class 1, zero_division=0; ROC-AUC/AP use positive probabilities. AP is Average Precision, not trapezoidal PR area. All reported SDs use ddof=1 (sample SD) across five outer-fold values; overlapping training partitions mean these are descriptive spread, not independent confidence intervals or significance tests.

## Individual outer-fold predictive results

| model | outer_fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 1 | 0.899211 | 0.671053 | 0.206199 | 0.315464 | 0.773340 | 0.432797 |
| RandomForest | 1 | 0.899818 | 0.683036 | 0.206199 | 0.316770 | 0.804058 | 0.442925 |
| HistGradientBoosting | 1 | 0.899666 | 0.650558 | 0.235849 | 0.346192 | 0.810998 | 0.450109 |
| LogisticRegression | 2 | 0.899970 | 0.698565 | 0.196765 | 0.307045 | 0.758226 | 0.420805 |
| RandomForest | 2 | 0.899362 | 0.670996 | 0.208895 | 0.318602 | 0.788798 | 0.444596 |
| HistGradientBoosting | 2 | 0.899211 | 0.668103 | 0.208895 | 0.318275 | 0.791971 | 0.442077 |
| LogisticRegression | 3 | 0.897996 | 0.660550 | 0.194070 | 0.300000 | 0.742708 | 0.403262 |
| RandomForest | 3 | 0.898907 | 0.679245 | 0.194070 | 0.301887 | 0.781868 | 0.414406 |
| HistGradientBoosting | 3 | 0.899666 | 0.652830 | 0.233154 | 0.343595 | 0.788546 | 0.428814 |
| LogisticRegression | 4 | 0.897996 | 0.678571 | 0.179245 | 0.283582 | 0.770552 | 0.425777 |
| RandomForest | 4 | 0.899514 | 0.698020 | 0.190027 | 0.298729 | 0.798528 | 0.466453 |
| HistGradientBoosting | 4 | 0.900273 | 0.683983 | 0.212938 | 0.324769 | 0.802185 | 0.467601 |
| LogisticRegression | 5 | 0.900729 | 0.725888 | 0.192463 | 0.304255 | 0.764549 | 0.429507 |
| RandomForest | 5 | 0.899970 | 0.705882 | 0.193809 | 0.304118 | 0.778870 | 0.451270 |
| HistGradientBoosting | 5 | 0.899514 | 0.683258 | 0.203230 | 0.313278 | 0.780853 | 0.452125 |

## Nested outer-CV mean ± sample SD

| model | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | AP mean ± SD |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 0.899666 ± 0.000387 | 0.667746 ± 0.015987 | 0.218813 ± 0.014761 | 0.329222 ± 0.014903 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 |
| LogisticRegression | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 |
| RandomForest | 0.899514 ± 0.000416 | 0.687436 ± 0.014222 | 0.198600 ± 0.008377 | 0.308021 ± 0.009051 | 0.790424 ± 0.010734 | 0.443930 ± 0.018936 |

Nested AP ranking: HistGradientBoosting, RandomForest, LogisticRegression. Leading mean AP is **HistGradientBoosting: 0.448145**. HGB minus RF nested mean AP = +0.004215. This measured difference describes these fixed-grid procedures under random stratified folds; it is not a significance conclusion or proof of future-campaign performance.

Outer-fold AP leaders:

| outer_fold | model | AP |
| --- | --- | --- |
| 1 | HistGradientBoosting | 0.450109 |
| 2 | RandomForest | 0.444596 |
| 3 | HistGradientBoosting | 0.428814 |
| 4 | HistGradientBoosting | 0.467601 |
| 5 | HistGradientBoosting | 0.452125 |

## Fold-specific selected hyperparameters and stability

| model | outer_fold | best_parameters | inner_best_AP_selection_only |
| --- | --- | --- | --- |
| LogisticRegression | 1 | {"classifier__C": 0.1} | 0.420089 |
| RandomForest | 1 | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 200} | 0.441305 |
| HistGradientBoosting | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447887 |
| LogisticRegression | 2 | {"classifier__C": 0.1} | 0.424254 |
| RandomForest | 2 | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 0.445270 |
| HistGradientBoosting | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.448053 |
| LogisticRegression | 3 | {"classifier__C": 0.1} | 0.429173 |
| RandomForest | 3 | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 0.448989 |
| HistGradientBoosting | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.449117 |
| LogisticRegression | 4 | {"classifier__C": 0.1} | 0.420936 |
| RandomForest | 4 | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 0.435859 |
| HistGradientBoosting | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.439208 |
| LogisticRegression | 5 | {"classifier__C": 0.1} | 0.420355 |
| RandomForest | 5 | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 0.439988 |
| HistGradientBoosting | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441518 |

inner_best_AP_selection_only is an inner tuning statistic, never substituted for the outer validation score. Distinct winning configurations across five outer folds: {"HistGradientBoosting": 2, "LogisticRegression": 1, "RandomForest": 4}.

| model | best_parameters | outer_fold_selections |
| --- | --- | --- |
| HistGradientBoosting | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 2 |
| HistGradientBoosting | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 3 |
| LogisticRegression | {"classifier__C": 0.1} | 5 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 1 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 200} | 1 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 2 |
| RandomForest | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 1 |

Different choices show sensitivity to outer-training composition; repeated choices do not establish a universal optimum. No single final hyperparameter configuration is selected or refitted on complete development data here.

## Comparison with previous potentially optimistic selected-CV scores

| model | previous_selected_CV_AP | previous_selected_CV_ROC_AUC | nested_outer_AP | nested_outer_ROC_AUC | AP_nested_minus_previous |
| --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.422430 | 0.761875 | 0.422429 | 0.761875 | -0.000001 |
| RandomForest | 0.445417 | 0.791376 | 0.443930 | 0.790424 | -0.001487 |
| HistGradientBoosting | 0.448069 | 0.794969 | 0.448145 | 0.794911 | 0.000076 |

Previous values are imported from Phase 4B's six-decimal published comparison, not rerun or overwritten. They selected winners and reported scores on the same tuning folds. Current outer scores assess the fixed hyperparameter-selection procedures without using outer validation to choose that fold's hyperparameters. Changes can reflect both prior selection optimism and variation in winners; they do not by themselves quantify all optimism or statistical significance. Prior phases already explored this development set and helped define model families/grids. Nested CV reduces immediate tuning-fold reuse but is not a pristine new external evaluation; selecting a winning family using these outer means also introduces model-selection uncertainty.

## Business targeting — fold-local outer-validation ranks

Use only probabilities from outer-validation predictions. Rank each validation cohort separately. K=ceil(fraction*N), sorting by descending probability then saved cleaned-row position as reproducible, outcome-independent tie-break. Precision@K=captured/K; Recall@K=captured/actual subscribers in that cohort; Lift@K=Precision@K/cohort prevalence. Target fractions 5%,10%,20% were fixed before results. Every model has exactly the same contact capacity within each view/fold. Subscriber counts reflect historical validation outcomes, not causal outreach response or a known financial return.

| model | fraction | outer_fold | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.050000 | 1 | 330 | 199 | 0.603030 | 0.268194 | 5.354129 |
| LogisticRegression | 0.050000 | 2 | 330 | 184 | 0.557576 | 0.247978 | 4.950551 |
| LogisticRegression | 0.050000 | 3 | 330 | 183 | 0.554545 | 0.246631 | 4.923646 |
| LogisticRegression | 0.050000 | 4 | 330 | 197 | 0.596970 | 0.265499 | 5.300319 |
| LogisticRegression | 0.050000 | 5 | 330 | 200 | 0.606061 | 0.269179 | 5.373792 |
| LogisticRegression | 0.100000 | 1 | 659 | 315 | 0.477997 | 0.424528 | 4.243995 |
| LogisticRegression | 0.100000 | 2 | 659 | 313 | 0.474962 | 0.421833 | 4.217049 |
| LogisticRegression | 0.100000 | 3 | 659 | 306 | 0.464340 | 0.412399 | 4.122738 |
| LogisticRegression | 0.100000 | 4 | 659 | 319 | 0.484067 | 0.429919 | 4.297887 |
| LogisticRegression | 0.100000 | 5 | 659 | 317 | 0.481032 | 0.426649 | 4.265192 |
| LogisticRegression | 0.200000 | 1 | 1318 | 460 | 0.349014 | 0.619946 | 3.098790 |
| LogisticRegression | 0.200000 | 2 | 1318 | 448 | 0.339909 | 0.603774 | 3.017952 |
| LogisticRegression | 0.200000 | 3 | 1318 | 427 | 0.323976 | 0.575472 | 2.876485 |
| LogisticRegression | 0.200000 | 4 | 1318 | 464 | 0.352049 | 0.625337 | 3.125736 |
| LogisticRegression | 0.200000 | 5 | 1318 | 457 | 0.346737 | 0.615074 | 3.074437 |
| RandomForest | 0.050000 | 1 | 330 | 196 | 0.593939 | 0.264151 | 5.273413 |
| RandomForest | 0.050000 | 2 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| RandomForest | 0.050000 | 3 | 330 | 194 | 0.587879 | 0.261456 | 5.219603 |
| RandomForest | 0.050000 | 4 | 330 | 205 | 0.621212 | 0.276280 | 5.515560 |
| RandomForest | 0.050000 | 5 | 330 | 200 | 0.606061 | 0.269179 | 5.373792 |
| RandomForest | 0.100000 | 1 | 659 | 311 | 0.471927 | 0.419137 | 4.190103 |
| RandomForest | 0.100000 | 2 | 659 | 323 | 0.490137 | 0.435310 | 4.351779 |
| RandomForest | 0.100000 | 3 | 659 | 304 | 0.461305 | 0.409704 | 4.095792 |
| RandomForest | 0.100000 | 4 | 659 | 323 | 0.490137 | 0.435310 | 4.351779 |
| RandomForest | 0.100000 | 5 | 659 | 331 | 0.502276 | 0.445491 | 4.453560 |
| RandomForest | 0.200000 | 1 | 1318 | 467 | 0.354325 | 0.629380 | 3.145945 |
| RandomForest | 0.200000 | 2 | 1318 | 463 | 0.351290 | 0.623989 | 3.118999 |
| RandomForest | 0.200000 | 3 | 1318 | 458 | 0.347496 | 0.617251 | 3.085317 |
| RandomForest | 0.200000 | 4 | 1318 | 485 | 0.367982 | 0.653639 | 3.267202 |
| RandomForest | 0.200000 | 5 | 1318 | 470 | 0.356601 | 0.632571 | 3.161893 |
| HistGradientBoosting | 0.050000 | 1 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| HistGradientBoosting | 0.050000 | 2 | 330 | 199 | 0.603030 | 0.268194 | 5.354129 |
| HistGradientBoosting | 0.050000 | 3 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| HistGradientBoosting | 0.050000 | 4 | 330 | 204 | 0.618182 | 0.274933 | 5.488655 |
| HistGradientBoosting | 0.050000 | 5 | 330 | 201 | 0.609091 | 0.270525 | 5.400661 |
| HistGradientBoosting | 0.100000 | 1 | 659 | 322 | 0.488619 | 0.433962 | 4.338306 |
| HistGradientBoosting | 0.100000 | 2 | 659 | 325 | 0.493171 | 0.438005 | 4.378725 |
| HistGradientBoosting | 0.100000 | 3 | 659 | 317 | 0.481032 | 0.427224 | 4.270941 |
| HistGradientBoosting | 0.100000 | 4 | 659 | 334 | 0.506829 | 0.450135 | 4.499982 |
| HistGradientBoosting | 0.100000 | 5 | 659 | 329 | 0.499241 | 0.442799 | 4.426651 |
| HistGradientBoosting | 0.200000 | 1 | 1318 | 492 | 0.373293 | 0.663073 | 3.314358 |
| HistGradientBoosting | 0.200000 | 2 | 1318 | 467 | 0.354325 | 0.629380 | 3.145945 |
| HistGradientBoosting | 0.200000 | 3 | 1318 | 455 | 0.345220 | 0.613208 | 3.065107 |
| HistGradientBoosting | 0.200000 | 4 | 1318 | 483 | 0.366464 | 0.650943 | 3.253729 |
| HistGradientBoosting | 0.200000 | 5 | 1318 | 474 | 0.359636 | 0.637954 | 3.188803 |

Mean and sample SD across the five cohorts (including contact volumes/captured counts):

| model | fraction | contacts_mean | contacts_SD | captured_mean | captured_SD | Precision_mean | Precision_SD | Recall_mean | Recall_SD | Lift_mean | Lift_SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 0.050000 | 330.000000 | 0.000000 | 202.000000 | 2.000000 | 0.612121 | 0.006061 | 0.272164 | 0.002745 | 5.433389 | 0.054809 |
| HistGradientBoosting | 0.100000 | 659.000000 | 0.000000 | 325.400000 | 6.503845 | 0.493778 | 0.009869 | 0.438425 | 0.008686 | 4.382921 | 0.086838 |
| HistGradientBoosting | 0.200000 | 1318.000000 | 0.000000 | 474.200000 | 14.272351 | 0.359788 | 0.010829 | 0.638912 | 0.019242 | 3.193588 | 0.096180 |
| LogisticRegression | 0.050000 | 330.000000 | 0.000000 | 192.600000 | 8.384510 | 0.583636 | 0.025408 | 0.259496 | 0.011221 | 5.180487 | 0.224006 |
| LogisticRegression | 0.100000 | 659.000000 | 0.000000 | 314.000000 | 5.000000 | 0.476480 | 0.007587 | 0.423066 | 0.006657 | 4.229372 | 0.066547 |
| LogisticRegression | 0.200000 | 1318.000000 | 0.000000 | 451.200000 | 14.754660 | 0.342337 | 0.011195 | 0.607920 | 0.019807 | 3.038680 | 0.099004 |
| RandomForest | 0.050000 | 330.000000 | 0.000000 | 199.600000 | 4.615192 | 0.604848 | 0.013985 | 0.268930 | 0.006214 | 5.368824 | 0.124058 |
| RandomForest | 0.100000 | 659.000000 | 0.000000 | 318.400000 | 10.761041 | 0.483156 | 0.016329 | 0.428990 | 0.014328 | 4.288602 | 0.143241 |
| RandomForest | 0.200000 | 1318.000000 | 0.000000 | 468.600000 | 10.212737 | 0.355539 | 0.007749 | 0.631366 | 0.013740 | 3.155871 | 0.068678 |

Fold-local highest mean Precision@K at each capacity: {"0.05": "HistGradientBoosting", "0.1": "HistGradientBoosting", "0.2": "HistGradientBoosting"}. At equal capacity this is also the highest mean captured count (all outer cohorts have equal size). Compare Recall/Lift separately because prevalence varies slightly across cohorts. Mean subscriber capture can be fractional across folds; it is not an actual fractional person.

## Business targeting — pooled nested outer OOF ranks

| model | fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.050000 | 1647 | 962 | 0.584092 | 0.259229 | 5.184586 |
| LogisticRegression | 0.100000 | 3294 | 1564 | 0.474803 | 0.421450 | 4.214497 |
| LogisticRegression | 0.200000 | 6588 | 2257 | 0.342593 | 0.608192 | 3.040959 |
| RandomForest | 0.050000 | 1647 | 999 | 0.606557 | 0.269200 | 5.383994 |
| RandomForest | 0.100000 | 3294 | 1588 | 0.482089 | 0.427917 | 4.279170 |
| RandomForest | 0.200000 | 6588 | 2341 | 0.355343 | 0.630827 | 3.154136 |
| HistGradientBoosting | 0.050000 | 1647 | 1005 | 0.610200 | 0.270816 | 5.416330 |
| HistGradientBoosting | 0.100000 | 3294 | 1628 | 0.494232 | 0.438696 | 4.386958 |
| HistGradientBoosting | 0.200000 | 6588 | 2377 | 0.360808 | 0.640528 | 3.202641 |

Pooled highest Precision@K at each capacity: {"0.05": "HistGradientBoosting", "0.1": "HistGradientBoosting", "0.2": "HistGradientBoosting"}. Pooled contact counts are 1,647/3,294/6,588; fold-local counts are 330/659/1,318 per fold. Ceil rounding makes sums across fold-local cohorts differ slightly from pooled capacities. Do not equate the two ranking views.

Each development observation has exactly one out-of-sample outer prediction, but pooled scores come from five separately tuned/fitted models with potentially different calibration/scales and overlapping training sets. Fold-local rankings are the cleaner comparison at a consistent per-cohort capacity; pooled targeting is an additional development diagnostic, not a single deployable prioritization model. Ties may materially change coarse ranks; no labels determine their ordering. Broader groups may capture more subscribers at lower precision/lift; use the actual tables rather than assume monotonic precision. Costs, product value, operational capacity and treatment effects are unknown, so no financial optimum is claimed.

Pooled predictive diagnostics (not a substitute for mean outer metrics):

| model | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.899180 | 0.686069 | 0.193748 | 0.302164 | 0.761768 | 0.421094 |
| RandomForest | 0.899514 | 0.686859 | 0.198599 | 0.308110 | 0.789795 | 0.442110 |
| HistGradientBoosting | 0.899666 | 0.666667 | 0.218809 | 0.329479 | 0.794260 | 0.445335 |

## Computational costs and practical trade-offs

| model | outer_fold | candidates | inner_CV_fits | outer_training_refits | search_refit_seconds | outer_prediction_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 1 | 3 | 15 | 1 | 1.548229 | 0.023019 |
| RandomForest | 1 | 8 | 40 | 1 | 78.988955 | 0.089764 |
| HistGradientBoosting | 1 | 16 | 80 | 1 | 77.513013 | 0.046056 |
| LogisticRegression | 2 | 3 | 15 | 1 | 1.512575 | 0.018960 |
| RandomForest | 2 | 8 | 40 | 1 | 76.941852 | 0.094189 |
| HistGradientBoosting | 2 | 16 | 80 | 1 | 78.906073 | 0.042657 |
| LogisticRegression | 3 | 3 | 15 | 1 | 1.564975 | 0.019266 |
| RandomForest | 3 | 8 | 40 | 1 | 80.054255 | 0.064710 |
| HistGradientBoosting | 3 | 16 | 80 | 1 | 80.486319 | 0.045566 |
| LogisticRegression | 4 | 3 | 15 | 1 | 1.619060 | 0.018728 |
| RandomForest | 4 | 8 | 40 | 1 | 75.808792 | 0.069085 |
| HistGradientBoosting | 4 | 16 | 80 | 1 | 84.895952 | 0.041066 |
| LogisticRegression | 5 | 3 | 15 | 1 | 1.634699 | 0.030595 |
| RandomForest | 5 | 8 | 40 | 1 | 84.047828 | 0.098416 |
| HistGradientBoosting | 5 | 16 | 80 | 1 | 82.079195 | 0.043360 |

| model | candidates_per_outer | total_inner_CV_fits | total_outer_refits | search_refit_seconds | outer_prediction_seconds |
| --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 16 | 400 | 5 | 403.880552 | 0.218705 |
| LogisticRegression | 3 | 75 | 5 | 7.879538 | 0.110568 |
| RandomForest | 8 | 200 | 5 | 395.841682 | 0.416164 |

Total elapsed through experiments/plots: 810.18 seconds on this runtime, not a promised Colab time. Wall times include fold auditing and selected outer-training refits. RF/HGB explore more candidates than LR; cost should be considered alongside observed AP, targeting and stability, not just a nominal complexity ranking. No candidate grid was reduced or expanded. LR remains useful as a simpler log-odds/linear reference; one-hot coding and correlated indicators still complicate coefficients. Nonlinear ensembles may add targeting value but that must be judged from these measurements, not assumed from complexity.

## Technical audit evidence

| model | role | rows | fits |
| --- | --- | --- | --- |
| HistGradientBoosting | inner-training fit | 21081 | 160 |
| HistGradientBoosting | inner-training fit | 21082 | 240 |
| HistGradientBoosting | outer-training refit | 26352 | 5 |
| LogisticRegression | inner-training fit | 21081 | 30 |
| LogisticRegression | inner-training fit | 21082 | 45 |
| LogisticRegression | outer-training refit | 26352 | 5 |
| RandomForest | inner-training fit | 21081 | 80 |
| RandomForest | inner-training fit | 21082 | 120 |
| RandomForest | outer-training refit | 26352 | 5 |

| model | role | probability_calls |
| --- | --- | --- |
| HistGradientBoosting | inner validation | 400 |
| HistGradientBoosting | outer validation | 5 |
| LogisticRegression | inner validation | 75 |
| LogisticRegression | outer validation | 5 |
| RandomForest | inner validation | 200 |
| RandomForest | outer validation | 5 |

Outer-training selected-model refit audits (not in-sample performance):

| outer_fold | model | role | inner_fold | rows | observed_recency | recency_mean | recency_scale | iterations | warnings | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LogisticRegression | outer-training refit | all outer training | 26352 | 947 | 6.070750 | 3.843597 | 58 | 0 | PASS |
| 1 | RandomForest | outer-training refit | all outer training | 26352 | 947 | unscaled | unscaled | not applicable | 0 | PASS |
| 1 | HistGradientBoosting | outer-training refit | all outer training | 26352 | 947 | unscaled | unscaled | 100 | 0 | PASS |
| 2 | LogisticRegression | outer-training refit | all outer training | 26352 | 957 | 6.022989 | 3.855744 | 56 | 0 | PASS |
| 2 | RandomForest | outer-training refit | all outer training | 26352 | 957 | unscaled | unscaled | not applicable | 0 | PASS |
| 2 | HistGradientBoosting | outer-training refit | all outer training | 26352 | 957 | unscaled | unscaled | 100 | 0 | PASS |
| 3 | LogisticRegression | outer-training refit | all outer training | 26352 | 967 | 6.024819 | 3.885566 | 55 | 0 | PASS |
| 3 | RandomForest | outer-training refit | all outer training | 26352 | 967 | unscaled | unscaled | not applicable | 0 | PASS |
| 3 | HistGradientBoosting | outer-training refit | all outer training | 26352 | 967 | unscaled | unscaled | 100 | 0 | PASS |
| 4 | LogisticRegression | outer-training refit | all outer training | 26352 | 978 | 6.208589 | 3.993022 | 56 | 0 | PASS |
| 4 | RandomForest | outer-training refit | all outer training | 26352 | 978 | unscaled | unscaled | not applicable | 0 | PASS |
| 4 | HistGradientBoosting | outer-training refit | all outer training | 26352 | 978 | unscaled | unscaled | 100 | 0 | PASS |
| 5 | LogisticRegression | outer-training refit | all outer training | 26352 | 979 | 6.097038 | 3.992815 | 53 | 0 | PASS |
| 5 | RandomForest | outer-training refit | all outer training | 26352 | 979 | unscaled | unscaled | not applicable | 0 | PASS |
| 5 | HistGradientBoosting | outer-training refit | all outer training | 26352 | 979 | unscaled | unscaled | 100 | 0 | PASS |

All 690 fresh preprocessing fits passed. Each inner training partition is disjoint from its paired inner validation and the current outer validation; inner splits are regenerated reproducibly within each outer-training partition and reused for all models. All outer folds have disjoint training/validation rows and complete exactly-once OOF coverage. Stored indices never overlap held-out positions. Audit wrappers reject whole-development fitting and reject any outer-validation prediction during inner scoring. Correct row-aligned targets, classifier classes/probabilities, class_weight=None and fixed seeds are checked.

Every OHE vocabulary equals its fitting rows' levels only. LR StandardScaler mean/variance/scale/sample count matches the corresponding fitting subset. Conditional recency mean/variance/scale/count uses only available-recency fitting rows, with unavailable standardized values zero and the indicator unscaled. Existing zero-variance/insufficient-sample fallback code remains unchanged; all four original standalone preprocessing tests passed when rerun separately. Tree/HGB transformed numbers exactly equal validation input, preserving zeros/availability and excluding 999. Finite representation is checked before training and at every prediction; coefficients/probability-derived outputs and all final metric/ranking tables contain no NaN/infinity. Fitted state is unchanged by each validation transform. HGB retains numeric indicators, disabled early stopping and its fixed iteration budget. All datasets, saved split, preprocessing and earlier results remain unchanged by hash and in-memory equality checks.

LR fitted iteration range over its inner/outer fits: 26–66, max_iter=1000. Warnings/errors:

None recorded across all 690 fits.

No corrective grid/preprocessing changes were silently made. Inner fold validation-position hashes, complete fit audit records, the most recent search object and all OOF arrays are retained in notebook memory during execution; no fitted estimators or new datasets are exported. The displayed tables/plots preserve the results when the notebook is saved.

## Observed model-selection and targeting takeaways

HGB retains a higher mean nested AP than RF by 0.004215 and leads AP in four of five outer folds. This is small relative to descriptive fold SDs (0.014219 for HGB, 0.018936 for RF), so it supports a provisional shortlist rather than a significant-winner claim. HGB also leads mean fold-local precision/capture and pooled precision/capture at all three prespecified capacities. At pooled top 5%, 10% and 20%, it captures only 6, 40 and 36 more historical subscribers than RF, respectively; the value of these marginal gains depends on unknown operational costs and constraints.

LR remains a useful cheap/simple reference, but trails HGB in nested AP by 0.025716 and in each targeting view here. Its total search/refit time was about 7.88 seconds versus RF 395.84 and HGB 403.88 seconds on this runtime. No universal runtime or deployment-efficiency claim follows from those measurements.

LR chose C=0.1 in all five outer folds. HGB consistently chose learning_rate=0.05, max_iter=100 and max_leaf_nodes=15, with L2=0 in two folds and L2=1 in three. RF chose four distinct configurations. This indicates greater hyperparameter sensitivity for RF within these grids, not proven instability in future data. These nested choices also illustrate why the earlier full-development HGB winner (200 iterations) should not be treated as a universally fixed best configuration.

## Provisional recommendations and Phase 5B approval

Use the nested AP ordering **HistGradientBoosting, RandomForest, LogisticRegression**, fold-local and pooled capacity-specific winners, and the measured cost tables to shortlist procedures. Advance the leading nested-AP family **HistGradientBoosting** for review alongside the closest nonlinear competitor, retaining **Logistic Regression** as a transparent/simple reference. Do not automatically declare the highest mean a significant winner. Assess whether its marginal subscriber capture at a feasible contact budget justifies computational/operational complexity. The capacity-specific winners may differ from the global AP leader.

All 15 predictors remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Confirm campaign-start customer/financial snapshots, historical-contact cutoff and recency reference dates, economic publication/revision vintage, and label outcome/follow-up window. Random stratified CV cannot eliminate repeated-customer or temporal overlap without missing customer IDs/dates. Prior whole-dataset EDA exposure persists. Nested tuning prevents direct inner/outer selection contamination; it does not certify feature-timing safety, unseen-client/future-campaign generalization, deployment readiness or causal effect of outreach.

Team approval still needed: model shortlist/business targeting capacity and error/call value assumptions; whether observed differences merit paired uncertainty analysis rather than significance claims; timing metadata/acceptable academic assumptions; client/time validation requirements; and the scope of Phase 5B. No class weights, resampling, threshold optimization, feature selection/ablation, held-out evaluation, Phase 5B, commit or push occurred.

Deliverables: executed 06_nested_cv_targeting.ipynb and this 06_nested_cv_targeting_summary.md in the repository. Stop after Phase 5A pending approval.
