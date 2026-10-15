# Phase 4 — Model comparison and manageable hyperparameter tuning

## Scope, data and reproducibility

Compared Logistic Regression (LR), Decision Tree (DT) and Random Forest (RF), with random_state=42, class_weight=None, no resampling and a fixed probability >=0.5 decision threshold. Reused the existing development assignment (32,940 rows) from 03_split_indices.json; all 8,236 held-out rows remain unparsed/unused for training, tuning, metrics, plots or importance. No new train-test split. Cleaned input hash/order `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` matched before row selection. Only development rows were materialized. Raw CSV was hash-checked if present, not parsed. All saved inputs, approved preprocessing and Phase 3 baseline files remain unchanged.

Reviewed README, project DOCX, cleaned dataset/split schema, preprocessing.py, Phase 2C summary and Phase 3 notebook/summary. No preprocessing reimplementation or transformer change. Versions: sklearn 1.8.0, pandas 2.2.3, NumPy 2.3.5. Notebook requires sklearn >=1.2 and standard Colab packages; executed locally, not in hosted Colab.

## Models and optional extension assessment

Untuned LR exactly matches Phase 3: max_iter=1000, C=1, default L2, lbfgs, random_state=42, no class weighting. DT uses sklearn defaults plus random_state=42/class_weight=None. RF uses 100 trees, default depth=None/min_samples_leaf=1/max_features='sqrt', random_state=42, n_jobs=1, class_weight=None. The approved tree/RF preprocessing passes numbers without scaling; LR uses ordinary plus conditional scaling. All have full train-fitted one-hot encoding and separate recency days/availability.

Optional HistGradientBoostingClassifier was assessed but **not trained**. Approved one-hot output is dense finite numeric data (42 columns in the untuned folds), compatible with its numeric interface. Histogram boosting is appropriate for nonlinear tabular binary classification, but adds iterative histogram construction, model memory and another search (learning_rate, max_iter, max_leaf_nodes, l2_regularization). An actual implementation would reuse the unscaled factory, confirm supported sklearn/version behavior, and keep any early-stopping subset within the fold training data. Deferred to keep this experiment focused on the three primary course models and a bounded budget; no optional algorithm substituted.

## CV and grids declared before execution

Identical five fold index pairs from StratifiedKFold(5,shuffle=True,random_state=42) for every untuned model and every search candidate. Each training fold has 26,352 original unencoded/unscaled rows and validation has 6,588. Fresh complete estimator pipelines fit within every fold. Positive-class probabilities supply ROC-AUC/AP; precision/recall/F1 use zero_division=0. AP is Average Precision, not trapezoidal PR area. All reported fold SDs use ddof=1 (sample SD), recomputed from individual split scores (GridSearchCV's native std uses ddof=0). No significance or independent-test inference from these dependent folds.

- LR: C=[0.1,1,10] — 3 candidates, fixed compatible lbfgs/default L2. Smaller C strengthens regularization, larger C weakens it. Penalty is deliberately fixed to avoid a solver/regularizer expansion, not omitted accidentally.
- DT: max_depth=[5,10,None], min_samples_leaf=[10,50] — 6 candidates. Depth bounds interactions/complexity; leaf size regularizes small/noisy groups. min_samples_split stays 2 and max_features stays None to bound search; leaf size already constrains splits. No exhaustive search claim.
- RF: n_estimators=[100,200], max_depth=[10,None], min_samples_leaf=[5,20], max_features=['sqrt'] — 8 candidates. Trees count controls Monte Carlo stability/cost; depth and leaf size regulate complexity; feature subsampling diversifies trees, fixed at sqrt for computational control.

GridSearchCV uses a multi-metric probability scorer returning Accuracy/Precision/Recall/F1/ROC_AUC/AP, with refit='AP', n_jobs=1, error_score='raise', and the exact same fold list. Candidate counts: 17 total; 85 candidate-fold fits plus 3 winning full-development **post-search refits**. Untuned comparison adds 15 fold fits: **103 total fits**. Refit happens only after search, is not a pre-CV global transformation, and its training predictions are never evaluated or ranked. No grid was reduced after seeing results. Single-threaded estimator/search settings avoid nested CPU oversubscription.

## Untuned individual fold results

| model | fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 1 | 0.899211 | 0.665254 | 0.211590 | 0.321063 | 0.774180 | 0.432213 |
| LogisticRegression | 2 | 0.899059 | 0.680751 | 0.195418 | 0.303665 | 0.759074 | 0.420763 |
| LogisticRegression | 3 | 0.897845 | 0.653333 | 0.198113 | 0.304033 | 0.742628 | 0.403407 |
| LogisticRegression | 4 | 0.898300 | 0.680000 | 0.183288 | 0.288747 | 0.770513 | 0.425606 |
| LogisticRegression | 5 | 0.901184 | 0.725490 | 0.199192 | 0.312566 | 0.764998 | 0.428919 |
| DecisionTree | 1 | 0.828476 | 0.287746 | 0.354447 | 0.317633 | 0.622349 | 0.179376 |
| DecisionTree | 2 | 0.838950 | 0.311688 | 0.355795 | 0.332284 | 0.631238 | 0.193183 |
| DecisionTree | 3 | 0.828931 | 0.289617 | 0.357143 | 0.319855 | 0.627261 | 0.183706 |
| DecisionTree | 4 | 0.836521 | 0.298436 | 0.334232 | 0.315321 | 0.616298 | 0.178609 |
| DecisionTree | 5 | 0.830753 | 0.273171 | 0.301480 | 0.286628 | 0.601934 | 0.168939 |
| RandomForest | 1 | 0.886157 | 0.491111 | 0.297844 | 0.370805 | 0.766870 | 0.372430 |
| RandomForest | 2 | 0.885094 | 0.482993 | 0.287062 | 0.360101 | 0.759431 | 0.361995 |
| RandomForest | 3 | 0.882058 | 0.462366 | 0.289757 | 0.356255 | 0.749421 | 0.348094 |
| RandomForest | 4 | 0.882817 | 0.466063 | 0.277628 | 0.347973 | 0.767372 | 0.370937 |
| RandomForest | 5 | 0.880844 | 0.451835 | 0.265141 | 0.334182 | 0.760438 | 0.353080 |

## Tuned selected-configuration fold results — model-selection estimates

| model | fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 1 | 0.899211 | 0.671053 | 0.206199 | 0.315464 | 0.773340 | 0.432797 |
| LogisticRegression | 2 | 0.899970 | 0.698565 | 0.196765 | 0.307045 | 0.758226 | 0.420805 |
| LogisticRegression | 3 | 0.897996 | 0.660550 | 0.194070 | 0.300000 | 0.742708 | 0.403262 |
| LogisticRegression | 4 | 0.897996 | 0.678571 | 0.179245 | 0.283582 | 0.770552 | 0.425777 |
| LogisticRegression | 5 | 0.900729 | 0.725888 | 0.192463 | 0.304255 | 0.764549 | 0.429507 |
| DecisionTree | 1 | 0.897237 | 0.598784 | 0.265499 | 0.367880 | 0.776334 | 0.428947 |
| DecisionTree | 2 | 0.896934 | 0.618868 | 0.221024 | 0.325720 | 0.767976 | 0.411627 |
| DecisionTree | 3 | 0.898148 | 0.628159 | 0.234501 | 0.341511 | 0.766785 | 0.399164 |
| DecisionTree | 4 | 0.897086 | 0.595808 | 0.268194 | 0.369888 | 0.782669 | 0.442709 |
| DecisionTree | 5 | 0.896023 | 0.607407 | 0.220727 | 0.323791 | 0.765224 | 0.420048 |
| RandomForest | 1 | 0.900729 | 0.680328 | 0.223720 | 0.336714 | 0.803990 | 0.446430 |
| RandomForest | 2 | 0.899362 | 0.670996 | 0.208895 | 0.318602 | 0.788798 | 0.444596 |
| RandomForest | 3 | 0.898452 | 0.651452 | 0.211590 | 0.319430 | 0.782943 | 0.420046 |
| RandomForest | 4 | 0.899059 | 0.680751 | 0.195418 | 0.303665 | 0.802279 | 0.464743 |
| RandomForest | 5 | 0.899970 | 0.705882 | 0.193809 | 0.304118 | 0.778870 | 0.451270 |

These are the five selection-fold scores for each family winner, chosen using those folds. They may be optimistic. They are not independent test performance and are not nested-CV estimates.

## Mean ± sample SD, both stages

| stage | model | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | AP mean ± SD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tuned selection CV | DecisionTree | 0.897086 ± 0.000759 | 0.609805 ± 0.013621 | 0.241989 ± 0.023383 | 0.345758 ± 0.022214 | 0.771797 ± 0.007445 | 0.420499 ± 0.016574 |
| tuned selection CV | LogisticRegression | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 |
| tuned selection CV | RandomForest | 0.899514 ± 0.000872 | 0.677882 ± 0.019648 | 0.206686 ± 0.012368 | 0.316506 ± 0.013598 | 0.791376 ± 0.011315 | 0.445417 ± 0.016226 |
| untuned | DecisionTree | 0.832726 ± 0.004730 | 0.292132 ± 0.014206 | 0.340620 ± 0.023808 | 0.314344 ± 0.016824 | 0.619816 ± 0.011450 | 0.180763 ± 0.008793 |
| untuned | LogisticRegression | 0.899120 ± 0.001282 | 0.680966 ± 0.027358 | 0.197520 ± 0.010100 | 0.306015 ± 0.012010 | 0.762279 ± 0.012382 | 0.422181 ± 0.011316 |
| untuned | RandomForest | 0.883394 ± 0.002188 | 0.470874 ± 0.015925 | 0.283486 ± 0.012541 | 0.353863 ± 0.013727 | 0.760706 ± 0.007271 | 0.361307 ± 0.010715 |

Best hyperparameters:

| model | best_parameters | selection_AP |
| --- | --- | --- |
| LogisticRegression | {"classifier__C": 0.1} | 0.422429 |
| DecisionTree | {"classifier__max_depth": null, "classifier__min_samples_leaf": 50} | 0.420499 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 0.445417 |

All candidates (AP and ROC-AUC overview; complete multi-metric candidate results are retained by cv_results_ in notebook memory):

| model | parameters | rank_AP | AP_mean | AP_SD | ROC_AUC_mean | ROC_AUC_SD | mean_fit_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | {"classifier__C": 0.1} | 1 | 0.422429 | 0.011606 | 0.761875 | 0.012192 | 0.089728 |
| LogisticRegression | {"classifier__C": 1.0} | 2 | 0.422181 | 0.011316 | 0.762279 | 0.012382 | 0.074936 |
| LogisticRegression | {"classifier__C": 10.0} | 3 | 0.422112 | 0.011427 | 0.762429 | 0.012432 | 0.074046 |
| DecisionTree | {"classifier__max_depth": 5, "classifier__min_samples_leaf": 10} | 4 | 0.398487 | 0.018946 | 0.779219 | 0.012058 | 0.079445 |
| DecisionTree | {"classifier__max_depth": 5, "classifier__min_samples_leaf": 50} | 3 | 0.404168 | 0.016611 | 0.781041 | 0.011003 | 0.079546 |
| DecisionTree | {"classifier__max_depth": 10, "classifier__min_samples_leaf": 10} | 5 | 0.387560 | 0.014266 | 0.759113 | 0.007582 | 0.108595 |
| DecisionTree | {"classifier__max_depth": 10, "classifier__min_samples_leaf": 50} | 2 | 0.420319 | 0.017907 | 0.775270 | 0.010934 | 0.107202 |
| DecisionTree | {"classifier__max_depth": null, "classifier__min_samples_leaf": 10} | 6 | 0.352227 | 0.018575 | 0.730012 | 0.010432 | 0.146301 |
| DecisionTree | {"classifier__max_depth": null, "classifier__min_samples_leaf": 50} | 1 | 0.420499 | 0.016574 | 0.771797 | 0.007445 | 0.125383 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 100} | 2 | 0.445087 | 0.016845 | 0.791393 | 0.010983 | 1.343890 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 1 | 0.445417 | 0.016226 | 0.791376 | 0.011315 | 2.742396 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 6 | 0.443942 | 0.018704 | 0.790223 | 0.011881 | 1.308232 |
| RandomForest | {"classifier__max_depth": 10, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 200} | 3 | 0.444877 | 0.018531 | 0.790480 | 0.011831 | 2.625959 |
| RandomForest | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 100} | 8 | 0.442755 | 0.016385 | 0.784870 | 0.008710 | 1.775434 |
| RandomForest | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 5, "classifier__n_estimators": 200} | 7 | 0.442763 | 0.016475 | 0.785443 | 0.008657 | 3.479159 |
| RandomForest | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 100} | 4 | 0.444290 | 0.019360 | 0.788788 | 0.010302 | 1.560728 |
| RandomForest | {"classifier__max_depth": null, "classifier__max_features": "sqrt", "classifier__min_samples_leaf": 20, "classifier__n_estimators": 200} | 5 | 0.444228 | 0.019061 | 0.788783 | 0.010127 | 2.994997 |

## Comparison with preserved Phase 3 LR

Untuned LR rerun matches all five published Phase 3 fold scores to their six-decimal rounding precision (AP mean 0.422181). Untuned AP ranking: LogisticRegression, RandomForest, DecisionTree. Tuned selection AP ranking: RandomForest, LogisticRegression, DecisionTree. Highest selected AP is **RandomForest: 0.445417**, ROC-AUC 0.791376. The table below compares selected-CV mean scores with the untuned Phase 3 reference; selecting winners on these same folds can bias apparent improvements.

| model | AP | ROC_AUC | AP_minus_Phase3_LR |
| --- | --- | --- | --- |
| RandomForest | 0.445417 | 0.791376 | 0.023236 |
| LogisticRegression | 0.422429 | 0.761875 | 0.000248 |
| DecisionTree | 0.420499 | 0.771797 | -0.001682 |

## Untuned development OOF business targeting

Every OOF probability comes from an untuned pipeline that excluded that customer's row during training. K=ceil(fraction*N); select exactly K with descending probability and saved cleaned-row position as deterministic, outcome-independent tie-break. Precision@K=captured/K, Recall@K=captured/total actual subscribers, Lift@K=Precision@K/development prevalence. Prevalence=0.112659 (11.2659%), actual development subscribers=3,711. Historical predicted conversion is not a causal response-to-calling effect. Ties can materially affect targeting, especially for unpruned trees with coarse probabilities; the fixed row-position rule is reproducible but does not identify an optimal tie-break.

| model | target_fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- |
| LogisticRegression | 0.050000 | 1647 | 960 | 0.582878 | 0.258690 | 5.173808 |
| LogisticRegression | 0.100000 | 3294 | 1562 | 0.474196 | 0.420911 | 4.209108 |
| LogisticRegression | 0.200000 | 6588 | 2269 | 0.344414 | 0.611425 | 3.057127 |
| DecisionTree | 0.050000 | 1647 | 255 | 0.154827 | 0.068715 | 1.374293 |
| DecisionTree | 0.100000 | 3294 | 875 | 0.265634 | 0.235786 | 2.357855 |
| DecisionTree | 0.200000 | 6588 | 1332 | 0.202186 | 0.358933 | 1.794665 |
| RandomForest | 0.050000 | 1647 | 826 | 0.501518 | 0.222582 | 4.451630 |
| RandomForest | 0.100000 | 3294 | 1397 | 0.424104 | 0.376448 | 3.764484 |
| RandomForest | 0.200000 | 6588 | 2126 | 0.322708 | 0.572891 | 2.864457 |

These pooled OOF ranks combine five fitted probability scales and their training sets overlap; they are a useful development diagnostic, not deployment evidence. For transparency, fold-local rank summaries (each validation cohort ranked separately) are also reported:

| model | fraction | Precision_mean | Precision_SD | Recall_mean | Recall_SD | Lift_mean | Lift_SD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DecisionTree | 0.050000 | 0.151515 | 0.031199 | 0.067367 | 0.013876 | 1.344896 | 0.277007 |
| DecisionTree | 0.100000 | 0.265250 | 0.026748 | 0.235514 | 0.023727 | 2.354424 | 0.237200 |
| DecisionTree | 0.200000 | 0.202883 | 0.012358 | 0.360288 | 0.022105 | 1.800896 | 0.110490 |
| LogisticRegression | 0.050000 | 0.578788 | 0.029768 | 0.257339 | 0.013147 | 5.137432 | 0.262463 |
| LogisticRegression | 0.100000 | 0.475266 | 0.009501 | 0.421987 | 0.008354 | 4.218594 | 0.083517 |
| LogisticRegression | 0.200000 | 0.344006 | 0.011626 | 0.610884 | 0.020551 | 3.053493 | 0.102722 |
| RandomForest | 0.050000 | 0.504242 | 0.020619 | 0.224201 | 0.009239 | 4.475862 | 0.184449 |
| RandomForest | 0.100000 | 0.423369 | 0.008380 | 0.375911 | 0.007558 | 3.757973 | 0.075556 |
| RandomForest | 0.200000 | 0.322458 | 0.007158 | 0.572622 | 0.012698 | 2.862240 | 0.063473 |

The contacted counts represent historical development records, not an approved future campaign budget. Smaller groups can concentrate subscribers, while larger groups may capture more at lower precision/lift; inspect each actual table rather than assume monotonic precision. We do not know call costs, subscription value, treatment effects or capacity, so no financial optimum or capacity recommendation is inferred. The three targeting fractions are prespecified ranking diagnostics, not tuned probability thresholds.

**Tuned-model unbiased targeting is deferred.** No selected hyperparameters were rerun through the same tuning folds and called unbiased OOF. No in-sample winning-refit predictions are used for metrics/ranking. A nested design using five outer folds and the same five-fold inner grids would require 5*(85 inner fits+3 refits)=440 fits across three families (in addition to this comparison), versus 88 search/refit fits here. It would estimate the selection procedure more honestly, but still inherit feature-timing/client overlap limitations. Phase 5 approval is needed for a nested experiment; no equivalence of untuned OOF and tuned selection estimates is fabricated.

## Interpretability

LR offers directional log-odds coefficients but full one-hot coding, scaling and correlated indicators complicate interpretation; coefficients are not causal and need a stated reference/regularization convention. A DT can expose decision rules but the default unpruned tree can be large/unstable. RF averages trees and can represent nonlinear interactions, trading simple rules for ensemble complexity. Optional boosting adds sequential nonlinear flexibility and tuning/compute cost without guaranteed gains.

The notebook shows untuned training-derived mean-decrease-in-impurity importance, grouped from all one-hot columns back to each original feature, then averaged across five fold-trained DT/RF models. This is descriptive training-model interpretation, not validation permutation importance or evidence for feature removal. It can favor richer split opportunities, and correlated economic variables share or displace importance. Grouping avoids displaying each dummy as an unrelated concept but does not remove bias. No feature selection was performed.

| model | feature | mean | std |
| --- | --- | --- | --- |
| DecisionTree | age | 0.197607 | 0.008157 |
| DecisionTree | nr.employed | 0.164057 | 0.003545 |
| DecisionTree | euribor3m | 0.152197 | 0.005599 |
| DecisionTree | job | 0.110597 | 0.005798 |
| DecisionTree | education | 0.089790 | 0.004669 |
| DecisionTree | housing | 0.054599 | 0.003006 |
| DecisionTree | marital | 0.049077 | 0.006632 |
| DecisionTree | loan | 0.038473 | 0.003010 |
| DecisionTree | cons.conf.idx | 0.031154 | 0.001690 |
| DecisionTree | recency_available | 0.031001 | 0.000762 |
| DecisionTree | previous | 0.026731 | 0.004985 |
| DecisionTree | default | 0.022700 | 0.002027 |
| DecisionTree | cons.price.idx | 0.014184 | 0.004808 |
| DecisionTree | recency_days | 0.012347 | 0.001467 |
| DecisionTree | emp.var.rate | 0.005487 | 0.001735 |
| RandomForest | age | 0.231194 | 0.001984 |
| RandomForest | euribor3m | 0.207429 | 0.001490 |
| RandomForest | job | 0.099880 | 0.001261 |
| RandomForest | education | 0.079877 | 0.001320 |
| RandomForest | nr.employed | 0.053380 | 0.001897 |
| RandomForest | housing | 0.043178 | 0.000409 |
| RandomForest | marital | 0.039638 | 0.000899 |
| RandomForest | cons.conf.idx | 0.038424 | 0.001606 |
| RandomForest | recency_days | 0.035038 | 0.001031 |
| RandomForest | cons.price.idx | 0.033455 | 0.001175 |
| RandomForest | emp.var.rate | 0.033417 | 0.001091 |
| RandomForest | loan | 0.031628 | 0.000437 |
| RandomForest | previous | 0.030217 | 0.000503 |
| RandomForest | recency_available | 0.029227 | 0.001675 |
| RandomForest | default | 0.014016 | 0.000647 |

## Computational cost and audits

| model | stage | configurations | CV_fits | refits | wall_seconds |
| --- | --- | --- | --- | --- | --- |
| LogisticRegression | untuned CV | 1 | 5 | 0 | 0.575625 |
| DecisionTree | untuned CV | 1 | 5 | 0 | 0.968842 |
| RandomForest | untuned CV | 1 | 5 | 0 | 11.395223 |
| LogisticRegression | GridSearchCV | 3 | 15 | 1 | 1.691800 |
| DecisionTree | GridSearchCV | 6 | 30 | 1 | 4.157416 |
| RandomForest | GridSearchCV | 8 | 40 | 1 | 96.440842 |

Measured elapsed time through experiments/plots: 116.08 seconds on this runtime; not a forecast for Colab. Grid mean fit times above exclude scoring/refit overhead. RF cost increases with number/depth of trees, so a small score difference must be weighed against runtime/complexity, not automatically favor the complex model. No fit failures triggered grid reduction.

| phase | model | rows | fit_count |
| --- | --- | --- | --- |
| grid search | DecisionTree | 26352 | 30 |
| grid search | DecisionTree | 32940 | 1 |
| grid search | LogisticRegression | 26352 | 15 |
| grid search | LogisticRegression | 32940 | 1 |
| grid search | RandomForest | 26352 | 40 |
| grid search | RandomForest | 32940 | 1 |
| untuned | DecisionTree | 26352 | 5 |
| untuned | LogisticRegression | 26352 | 5 |
| untuned | RandomForest | 26352 | 5 |

An experiment-only Pipeline subclass audits every fit, including GridSearchCV clones, without modifying preprocessing.py. Every fit's indices match an approved fold-training partition, except the three explicitly labelled post-search full-development refits. Each encoder vocabulary equals fit-row levels; LR scaler mean/variance/scale/count match training rows; conditional recency mean/variance/scale/count use only availability=1 fitting rows. All 100 validation predictions are on fixed development validation folds; parameters remain unchanged through transform. Numeric matrices/probabilities are finite, unavailable transformed recency remains zero, the availability bit remains unscaled, and tree/RF numbers are passed through unchanged. Object factories create fresh preprocessors; no global encoded/scaled matrix is shared across folds. All audit assertions passed.

Warnings/errors recorded:

None recorded across all 103 fits.

All previous input hashes, saved split, raw/cleaned data, Phase 3 notebook/summary and approved preprocessing remain unchanged. No held-out prediction/evaluation, class weights, SMOTE/undersampling, threshold optimization or automatic next-phase work.

## Phase 5 candidates and unresolved approval

Advance **RandomForest** as the leading AP-selected candidate for review, while preserving **Logistic Regression** as the transparent/simple reference. This is a provisional development-selection recommendation, not a final model or independent-performance claim. Review the full AP/ROC/precision/recall/cost tables before deciding whether any other family merits further work; model complexity alone is not evidence of superiority. Approve a selection-bias-aware validation plan before interpreting tuned targeting or selecting a deployment configuration.

All 15 predictors remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Confirm campaign-start customer/status snapshots, historical previous/recency cutoff and pdays reference dates, economic publication/revision timing, and target outcome window. Missing client IDs/campaign timestamps permit repeated-client/temporal overlap across random stratified folds; prior whole-dataset EDA exposure also needs disclosure. Preprocessing isolation does not eliminate feature-timing leakage or guarantee future-campaign/unseen-customer performance.

Team decisions still needed: candidate shortlist; whether to budget nested CV and/or optional boosting; valid timing metadata/assumptions; treatment of correlated indicators and rare levels in future experiments; business capacity/error costs and whether later threshold/class-weight experiments are authorized. None of these additional experiments was started. Existing saved holdout must remain reserved for a later approved evaluation.

Deliverables: executed 05_model_comparison.ipynb and this summary in the repository. No commit or push; Phase 4 stops pending review.
