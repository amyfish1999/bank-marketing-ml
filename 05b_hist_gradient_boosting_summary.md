# Phase 4B — HistGradientBoosting development and fair comparison

## Scope and preservation

Added only HistGradientBoostingClassifier (HGB), with the approved 15 Provisional predictors and the same 32,940-row development assignment. Held-out 8,236-row features/labels were not parsed, fitted, evaluated, plotted or used for selection. No new train-test split, old-model grids or nested CV were run. Raw/cleaned CSVs, split JSON, preprocessing.py and earlier Phase 3/4 artifacts remain unchanged.

Reviewed README, project DOCX, Phase 2C summary, Phase 3 summary, Phase 4 notebook/summary, cleaned schema/data and saved split. Exact cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` verified before indices; this binds both content and ordering. Only development CSV rows were parsed, then reordered to saved development positions. Five identical StratifiedKFold(5,shuffle=True,random_state=42) pairs were regenerated from that same ordered development set, and Phase 4 notebook code was checked for the identical recipe/factory. Each fold trains on 26,352 rows and validates on 6,588; coverage/disjointness/reproducibility passed. Validation-position checksum `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4`.

Versions: sklearn 1.8.0, pandas 2.2.3, NumPy 2.3.5. Standard Colab packages with sklearn >=1.2 are sufficient. Notebook executed locally; hosted Colab is not claimed. threadpoolctl limits OpenMP/BLAS to one thread during fit/prediction to avoid uncontrolled CPU cost; GridSearchCV n_jobs=1.

## Compatibility before training and minimal implementation

No additional model configuration in preprocessing.py is necessary. `make_preprocessor('decision_tree')` is exactly the existing approved unscaled numeric/one-hot setup also used for RF. HGB consumes its dense finite numeric output. Explicit `categorical_features=None` prevents native category inference: each one-hot level is a separate numeric 0/1 feature, not a categorical column index or integer level. No new encoding, native-category mode or LR-preprocessing change.

A stateless experiment-only FiniteNumericCheck step checks array/dtype/finiteness, numeric one-hot and availability bits, recency bounds and zero unavailable placeholders after approved preprocessing and **before classifier fitting on every fold**. It returns values unchanged, with no learned scaling/encoding. Raw development numeric domains were validated first. sklearn cloneability of the complete pipeline was checked before fitting; GridSearchCV subsequently cloned it successfully 81 times. Fitted HGB categorical masks and disabled early-stopping state were asserted on every fit.

## Untuned baseline configuration and results

learning_rate=0.1, max_iter=100, max_leaf_nodes=31, l2_regularization=0.0, early_stopping=False, random_state=42, class_weight=None, categorical_features=None. Other sklearn defaults retained (including min_samples_leaf=20 and log_loss). Classification rule is probability >=0.5, identical to Phase 4, including tie convention. Precision/recall/F1 use zero_division=0. Positive probabilities supply ROC-AUC/AP. AP means Average Precision, not trapezoidal PR area.

| model | fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | 0.899514 | 0.631579 | 0.258760 | 0.367113 | 0.801227 | 0.440846 |
| HistGradientBoosting | 2 | 0.898452 | 0.632727 | 0.234501 | 0.342183 | 0.786152 | 0.435501 |
| HistGradientBoosting | 3 | 0.899211 | 0.635417 | 0.246631 | 0.355340 | 0.787113 | 0.424695 |
| HistGradientBoosting | 4 | 0.898300 | 0.633333 | 0.230458 | 0.337945 | 0.795083 | 0.454304 |
| HistGradientBoosting | 5 | 0.898907 | 0.650980 | 0.223419 | 0.332665 | 0.780021 | 0.441713 |

Untuned mean: accuracy 0.898877, precision 0.636807, recall 0.238754, F1 0.347049, ROC-AUC 0.789919, AP 0.439412. All means/sample SDs are in the four-model table below. Pooled OOF confusion matrix (actual rows no/yes, predicted columns no/yes): [[28723,506],[2825,886]].

## Prespecified 16-configuration grid and cost

learning_rate=[0.05,0.1], max_iter=[100,200], max_leaf_nodes=[15,31], l2_regularization=[0.0,1.0]. learning_rate controls shrinkage per stage; max_iter fixes boosting stages; max_leaf_nodes controls interaction/partition complexity; l2_regularization penalizes leaf values, potentially stabilizing small/noisy regions. No expansion/reduction based on validation or held-out results. All candidates keep early_stopping=False, seed=42, class_weight=None and categorical_features=None.

GridSearchCV uses the same five folds, joint six-metric probability scorer, refit='AP', n_jobs=1, error_score='raise', return_train_score=False. 16 candidates × 5 folds = 80 candidate-fold fits, plus one winning development refit; five untuned folds bring the total to **86 HGB fits**. The refit occurs only after selection, not before CV; its training predictions are never used for targeting or reported performance, and no fitted artifact is saved. With early stopping disabled every fit ran its specified 100/200 iterations; no internal validation partition was created.

All candidates, including AP/ROC-AUC sample SD and mean fit/scoring time:

| parameters | rank_AP | AP_mean | AP_SD | ROC_AUC_mean | ROC_AUC_SD | mean_fit_seconds | mean_score_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 5 | 0.446923 | 0.014697 | 0.794122 | 0.012523 | 0.789596 | 0.052239 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 8 | 0.446531 | 0.012252 | 0.795288 | 0.012299 | 1.011899 | 0.059440 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 7 | 0.446655 | 0.016581 | 0.793915 | 0.010589 | 1.426995 | 0.074689 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 13 | 0.442447 | 0.011931 | 0.792777 | 0.009787 | 1.567118 | 0.073790 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 6 | 0.446716 | 0.016051 | 0.794003 | 0.011032 | 0.720186 | 0.052472 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 14 | 0.439412 | 0.010735 | 0.789919 | 0.008285 | 0.839507 | 0.052769 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 12 | 0.442594 | 0.015280 | 0.792566 | 0.009397 | 1.340722 | 0.071460 |
| {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 16 | 0.433244 | 0.009231 | 0.785127 | 0.006288 | 1.487636 | 0.072479 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 4 | 0.447537 | 0.013504 | 0.795131 | 0.011893 | 0.790027 | 0.051589 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 3 | 0.447787 | 0.013058 | 0.795661 | 0.011904 | 0.992006 | 0.056457 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 1 | 0.448069 | 0.015163 | 0.794969 | 0.012023 | 1.330763 | 0.070388 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 9 | 0.446156 | 0.015023 | 0.795018 | 0.010438 | 1.650478 | 0.078667 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 2 | 0.447969 | 0.017061 | 0.795216 | 0.011353 | 0.757885 | 0.053491 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 11 | 0.442953 | 0.012135 | 0.792861 | 0.010244 | 0.897822 | 0.055210 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 10 | 0.444781 | 0.015512 | 0.794004 | 0.010998 | 1.391359 | 0.081440 |
| {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 15 | 0.435400 | 0.012171 | 0.788606 | 0.009184 | 1.591462 | 0.084546 |

Best selected parameters: `{"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15}`.

Selected configuration's five fold scores:

| model | fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | 0.899211 | 0.632653 | 0.250674 | 0.359073 | 0.810399 | 0.449426 |
| HistGradientBoosting | 2 | 0.897845 | 0.640816 | 0.211590 | 0.318136 | 0.791854 | 0.442427 |
| HistGradientBoosting | 3 | 0.899059 | 0.638989 | 0.238544 | 0.347399 | 0.788073 | 0.427352 |
| HistGradientBoosting | 4 | 0.900729 | 0.677419 | 0.226415 | 0.339394 | 0.803839 | 0.469064 |
| HistGradientBoosting | 5 | 0.899514 | 0.670886 | 0.213997 | 0.324490 | 0.780681 | 0.452076 |

These are tuning-reused model-selection estimates, potentially optimistic, **not independent generalization estimates**. Sample SD uses ddof=1 and is recomputed from five split values (GridSearchCV's stored std uses ddof=0). Folds share training data; neither those SDs nor small mean differences establish statistical significance.

## Four-model comparison — previous results imported, not rerun

| stage | model | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | AP mean ± SD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tuned selection CV | DecisionTree | 0.897086 ± 0.000759 | 0.609805 ± 0.013621 | 0.241989 ± 0.023383 | 0.345758 ± 0.022213 | 0.771798 ± 0.007445 | 0.420499 ± 0.016574 |
| tuned selection CV | HistGradientBoosting | 0.899271 ± 0.001033 | 0.652153 ± 0.020441 | 0.228244 ± 0.016529 | 0.337698 ± 0.016666 | 0.794969 ± 0.012023 | 0.448069 ± 0.015163 |
| tuned selection CV | LogisticRegression | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193748 ± 0.009698 | 0.302069 ± 0.011779 | 0.761875 ± 0.012192 | 0.422430 ± 0.011606 |
| tuned selection CV | RandomForest | 0.899514 ± 0.000872 | 0.677882 ± 0.019648 | 0.206686 ± 0.012368 | 0.316506 ± 0.013598 | 0.791376 ± 0.011315 | 0.445417 ± 0.016226 |
| untuned | DecisionTree | 0.832726 ± 0.004730 | 0.292132 ± 0.014206 | 0.340619 ± 0.023808 | 0.314344 ± 0.016824 | 0.619816 ± 0.011450 | 0.180763 ± 0.008793 |
| untuned | HistGradientBoosting | 0.898877 ± 0.000508 | 0.636807 ± 0.008045 | 0.238754 ± 0.014003 | 0.347049 ± 0.014007 | 0.789919 ± 0.008285 | 0.439412 ± 0.010735 |
| untuned | LogisticRegression | 0.899120 ± 0.001282 | 0.680966 ± 0.027358 | 0.197520 ± 0.010100 | 0.306015 ± 0.012010 | 0.762279 ± 0.012382 | 0.422182 ± 0.011316 |
| untuned | RandomForest | 0.883394 ± 0.002188 | 0.470874 ± 0.015925 | 0.283486 ± 0.012541 | 0.353863 ± 0.013727 | 0.760706 ± 0.007271 | 0.361307 ± 0.010714 |

Old LR/DT/RF values are reconstructed from Phase 4's six-decimal published fold rows. Thus comparisons carry rounding error of approximately 1e-6; old experiments and grids were not rerun or overwritten. HGB values come from this execution. Untuned AP ordering: HistGradientBoosting, LogisticRegression, RandomForest, DecisionTree. Tuned selection AP ordering: HistGradientBoosting, RandomForest, LogisticRegression, DecisionTree.

HGB selected AP=0.448069 versus RF=0.445417, difference +0.002652; ROC-AUC=0.794969 versus RF=0.791376, difference +0.003593. Evaluate these descriptive differences alongside sample SD, compute and selection bias; no paired significance test or nested estimate was run. Small gains alone do not prove practically meaningful improvement, and greater model complexity is not automatically preferable. The AP advantage is small relative to the observed fold-to-fold spread (HGB sample SD 0.015163; RF 0.016226). That supports further comparison rather than a conclusion that HGB should replace RF; it is not a paired significance test.

Measured cost, including unchanged imported Phase 4 timing for context:

| model | stage | configurations | CV_fits | refits | wall_seconds |
| --- | --- | --- | --- | --- | --- |
| LogisticRegression | untuned CV | 1 | 5 | 0 | 0.575625 |
| DecisionTree | untuned CV | 1 | 5 | 0 | 0.968842 |
| RandomForest | untuned CV | 1 | 5 | 0 | 11.395223 |
| LogisticRegression | GridSearchCV | 3 | 15 | 1 | 1.691800 |
| DecisionTree | GridSearchCV | 6 | 30 | 1 | 4.157416 |
| RandomForest | GridSearchCV | 8 | 40 | 1 | 96.440842 |
| HistGradientBoosting | untuned CV | 1 | 5 | 0 | 4.646194 |
| HistGradientBoosting | GridSearchCV | 16 | 80 | 1 | 99.896127 |

HGB experiment elapsed 105.40 seconds including scoring/audits/plots; untuned CV 4.65s, grid+refit 99.90s. Candidate fit times exclude scoring/refit overhead. Imported timings are historical runtime measurements, not a controlled hardware benchmark or guaranteed Colab runtime; HGB thread counts were explicitly limited. The grid was kept intact. No old-model compute is included as a new run.

## Development-only pooled OOF targeting — untuned models only

K=ceil(fraction*N); rank descending probability, break ties by saved cleaned-row position, never outcome labels. Exactly K records selected. Precision@K=captured/K; Recall@K=captured/3711; Lift@K=Precision@K/0.112659. Development prevalence=11.2659%. No known costs, subscription values or campaign capacity are assumed.

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
| HistGradientBoosting | 0.050000 | 1647 | 985 | 0.598057 | 0.265427 | 5.308542 |
| HistGradientBoosting | 0.100000 | 3294 | 1608 | 0.488160 | 0.433306 | 4.333064 |
| HistGradientBoosting | 0.200000 | 6588 | 2361 | 0.358379 | 0.636217 | 3.181083 |

At the same top-10% contact volume (3,294), untuned HGB captures 1,608 subscribers versus LR 1,562 and RF 1,397. HGB precision is 48.82%, recall 43.33% and lift 4.33×: 46 additional historical subscribers captured versus LR, with a 1.40 percentage-point precision increase. This is a modest descriptive targeting gain, not causal or independent-test evidence. At top 5% HGB captures 985 versus LR 960; at top 20% 2,361 versus LR 2,269. Whether these differences justify operational complexity needs capacity/cost evidence.

Contact volume and captured subscriber counts are historical validation observations, not actual assigned outreach or evidence outreach caused subscription. Smaller fractions may offer greater concentration, broader fractions more capture; inspect the observed trade-off. Tie rules can materially affect coarse tree scores. Pooled OOF combines five model probability scales and overlapping training sets, so also inspect fold-local rankings rather than treating pooled ranking as a single deployable model.

HGB fold-local targeting details (contact/capture counts included):

| model | fraction | fold | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 0.050000 | 1 | 330 | 203 | 0.615152 | 0.273585 | 5.461750 |
| HistGradientBoosting | 0.050000 | 2 | 330 | 195 | 0.590909 | 0.262803 | 5.246508 |
| HistGradientBoosting | 0.050000 | 3 | 330 | 197 | 0.596970 | 0.265499 | 5.300319 |
| HistGradientBoosting | 0.050000 | 4 | 330 | 200 | 0.606061 | 0.269542 | 5.381034 |
| HistGradientBoosting | 0.050000 | 5 | 330 | 196 | 0.593939 | 0.263795 | 5.266316 |
| HistGradientBoosting | 0.100000 | 1 | 659 | 315 | 0.477997 | 0.424528 | 4.243995 |
| HistGradientBoosting | 0.100000 | 2 | 659 | 327 | 0.496206 | 0.440701 | 4.405671 |
| HistGradientBoosting | 0.100000 | 3 | 659 | 311 | 0.471927 | 0.419137 | 4.190103 |
| HistGradientBoosting | 0.100000 | 4 | 659 | 332 | 0.503794 | 0.447439 | 4.473036 |
| HistGradientBoosting | 0.100000 | 5 | 659 | 318 | 0.482549 | 0.427995 | 4.278647 |
| HistGradientBoosting | 0.200000 | 1 | 1318 | 485 | 0.367982 | 0.653639 | 3.267202 |
| HistGradientBoosting | 0.200000 | 2 | 1318 | 459 | 0.348255 | 0.618598 | 3.092053 |
| HistGradientBoosting | 0.200000 | 3 | 1318 | 460 | 0.349014 | 0.619946 | 3.098790 |
| HistGradientBoosting | 0.200000 | 4 | 1318 | 479 | 0.363429 | 0.645553 | 3.226783 |
| HistGradientBoosting | 0.200000 | 5 | 1318 | 473 | 0.358877 | 0.636608 | 3.182076 |

Four-model fold-local mean ± sample SD comparison (old models imported):

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
| HistGradientBoosting | 0.050000 | 0.600606 | 0.009912 | 0.267045 | 0.004471 | 5.331185 | 0.089251 |
| HistGradientBoosting | 0.100000 | 0.486495 | 0.013168 | 0.431960 | 0.011741 | 4.318290 | 0.117372 |
| HistGradientBoosting | 0.200000 | 0.357511 | 0.008724 | 0.634869 | 0.015467 | 3.173381 | 0.077311 |

No tuned HGB Top-K predictions were produced. Comparing selected-tuned HGB targeting against untuned LR/RF would mix experiments and selection bias. Future less-biased tuned targeting requires outer-fold predictions with tuning confined to each outer training partition. A five-outer/five-inner HGB-only experiment with this grid would add 5*(80 inner fits+1 refit)=405 fits. No nested CV was started; it would still not remove timing/client overlap limitations.

## Technical validation and warning log

| phase | rows | fit_count |
| --- | --- | --- |
| grid search | 26352 | 80 |
| grid search | 32940 | 1 |
| untuned | 26352 | 5 |

All 86 fits started with fresh approved preprocessors. Training partitions match the fixed training folds except one explicit post-search full-development refit. OHE vocabularies equal training-only observed categories; no global encoded matrix or caching/reuse of fitted preprocessing. Numeric indicators verified before HGB fit; fitted categorical mask confirms no native categorical interpretation. Every fit uses early_stopping=False, correct iteration count, no class weights and seed=42. All 85 probability calls used exact development validation folds; complete feature names/category snapshots stayed unchanged and all transformed/probability/metric values were finite. Unscaled numeric/recency/availability outputs exactly matched validation input; unavailable recency remains 0 and no 999 sentinel is reintroduced.

The LR factory and custom ConditionalRecencyScaler are not called or modified for these experiments; their approved behavior is preserved byte-for-byte. All four existing preprocessing unit tests passed when rerun as a regression check; no LR experiment was run. Input hashes and in-memory development equality passed after execution; saved split and earlier artifacts are unchanged. No held-out matrix was constructed or predicted.

Warnings/errors:

None recorded across all 86 HGB fits.

## Business implications and Phase 5A recommendation

Current leading AP-selected family is **HistGradientBoosting**. Consider **HistGradientBoosting and Random Forest** for a selection-bias-aware Phase 5A comparison, with Logistic Regression retained as a simpler reference and strong untuned targeting comparator. Use actual tables above rather than automatically declaring boosting superior. The selected HGB/RF scores are not independent test results; business value also needs capacity/cost/error trade-offs. No final model or threshold is selected here. No class-weighting/resampling/threshold experiment is authorized by this report.

All 15 predictors remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Fold-specific preprocessing controls preprocessing leakage; historical-contact cutoff and recency reference dates, economic publication/revision vintage, campaign-start customer/status snapshots and target outcome/follow-up window remain unverified. No customer IDs or campaign dates means random stratified folds can overlap customers/economic periods; prior whole-dataset EDA also requires disclosure. No claim of full leakage freedom, causal outreach lift, unseen-customer or future-period generalization.

Team approval still needed: whether observed AP/ROC/Top-K differences and compute justify advancing HGB; candidate shortlist and nested-CV budget/estimand; campaign-start metadata/assumptions; correlated variables/rare-level policy for future work; and business capacity/error values before any threshold decisions. Keep the holdout untouched for a later approved final evaluation.

Deliverables: executed 05b_hist_gradient_boosting.ipynb and this 05b_hist_gradient_boosting_summary.md in the repository. No commit/push, nested CV or Phase 5A work; stop after Phase 4B.
