# Phase 5B-2 — Imbalance treatments and fair decision policies

## Completion review and recommendations

Observed outer-CV ranking (mean AP ± sample SD):

| Model | Original | Balanced | RandomUnderSampler |
| --- | --- | --- | --- |
| HGB | 0.448145 ± 0.014219 | 0.450883 ± 0.015341 | 0.436259 ± 0.019079 |
| Logistic Regression | 0.422429 ± 0.011606 | 0.420526 ± 0.011461 | 0.419671 ± 0.012471 |

Balanced HGB increases mean AP by 0.002738 and ROC-AUC by 0.000587 versus original HGB. AP is higher in four outer folds and lower in one; five dependent folds do not establish statistical significance. At pooled top 5%, 10%, 20% capacities (1,647 / 3,294 / 6,588 contacts), original HGB captures 1,005 / 1,628 / 2,377 historical subscribers; balanced HGB captures 1,018 / 1,610 / 2,371: **+13 / −18 / −6**, respectively. Its top-5% precision is 61.81% versus 61.02%. Fold-local mean capture similarly changes from 202 to 205 at 5%, 325.4 to 322 at 10%, and remains 474.2 at 20%; rounded fold-local capacities differ slightly from pooled capacities. This is a small, capacity-dependent trade-off, not a consistent targeting improvement.

HGB undersampling lowers AP by 0.011886 and loses 17 / 50 / 29 subscribers at the same pooled capacities. Both LR treatments lower AP; balanced LR gains 10 subscribers at 20% versus original LR but loses capture at 5% and 10%. No treatment consistently beats original HGB across the three capacities.

Threshold effects must be judged against the existing threshold-only strategies. At .50, balanced HGB recall rises from 0.218813 to 0.623550, while precision falls from 0.667746 to 0.381950 and contact volume rises from 3.70% to 18.40%. Original HGB's training-F1 rule already achieves recall 0.586634 and F1 0.495146 at 15.43% contact volume; balanced HGB's grid-F1 rule gives recall 0.589328, lower F1 0.491954 and 15.73% volume. Undersampled HGB F1 is 0.489511. Original LR's F1-selected policy also exceeds both LR treatment policies (0.467336 versus 0.457502 / 0.451457). Higher recall at .50 alone therefore does not demonstrate useful imbalance-treatment gains.

All four new model/treatment arms select F1 threshold .60 in all five folds, the upper grid boundary. None finds a precision-constrained candidate within .10–.60 in any fold, so their constrained policies explicitly abstain. Their zero precision/recall/F1 denotes zero contacts under the fallback, not a satisfied 50% constraint. The original arms select .35 for that constraint and obtain mean outer precision 0.527200 (HGB) / 0.531257 (LR). **Grid-limited infeasibility does not rule out higher thresholds**; the F1 maxima are also grid-limited. A wider prespecified range or calibration would require a new training-only selection design and team approval, not post-hoc adjustment here.

Evidence-based shortlist for discussion: retain **original HGB** as the main reference and **original LR** as the simpler benchmark; retain **balanced HGB only as a secondary research candidate**, especially if 5% capacity matters. Deprioritize the tested undersampling arms and balanced LR because they show no consistent advantage over threshold-only references. These are research recommendations, not final model or deployment-policy choices. SMOTENC remains deferred. No causal or financial benefit, statistical significance, or unseen-campaign performance is established.

Separate local technical verification: `python -m unittest discover -s tests -v` passed all **4** existing preprocessing tests. All 1,130 current fits, 1,130 prediction calls and 535 training-only sampler calls passed runtime audits with no model warnings. No previous tracked artifact changed; datasets, saved indices and approved preprocessing.py are preserved. Notebook code executed locally; its nbformat schema, all six code-cell syntax checks, six execution records and three saved figures passed validation. Every pre-existing tracked file was also compared byte-for-byte against approved HEAD and matched. Hosted Colab execution was not directly tested. The Colab setup lists every required input, including the archived Phase 5A notebook used to verify parameter provenance. No held-out records were parsed for fitting/evaluation; no final ablation, Phase 6, commit or push occurred.

## Provenance, scope and reuse

Started from latest fetched/merged GitHub main **596d6bc** (Phase 5B-1 included); local branch fast-forwarded without creating a commit. Reviewed relevant Phase 2C–5B-1 code/notebooks/summaries, especially approved preprocessing, saved split and nested/threshold reports. Only HGB and LR are developed. No held-out evaluation, new model family, feature ablation, final policy selection or Phase 6.

Cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` binds exact data/row order to 03_split_indices.json. Saved positions are unique/disjoint/exhaustive: 32,940 development and 8,236 held-out. Parser skips held-out rows; only development rows are materialized. Outer StratifiedKFold(5,shuffle=True,random_state=42) and validation-position hash `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4` match Phase 5A/5B-1. Inner/threshold-OOF five-fold partitions are identical across treatments within each outer training set. Each outer validation cohort retains its original prevalence and 6,588 records.

Original no-treatment training-only hyperparameter selections from Phase 5A are reused, not chosen from outer scores; selected pipelines and threshold OOF values are regenerated. All 30 no-treatment policy-fold scores, thresholds and positive counts reproduce Phase 5B-1. Both new treatments run fresh complete inner searches on the exact approved grids. Effective selection budget is identical per model/treatment: LR 3 and HGB 16 candidates × five inner folds × five outer folds. No sampler-ratio/weight grid is added. Reusing archived original-arm grid decisions saves 475 duplicate candidate-fold fits, not a smaller baseline tuning budget. Current work executes 1,130 fits: 950 new inner candidate-fold fits +150 threshold-OOF fits +30 selected outer-training refits. Fully rerunning the archived original grid would have required 1,605 fits; no grid was reduced or expanded based on results.

## Treatment and model configurations

- Original: class_weight=None, sampler passthrough; exact Phase 5A per-fold parameter choices and Phase 5B-1 threshold procedure.
- Balanced: class_weight='balanced', no sampling. Each classifier derives class weights from its own fitting labels, not global development prevalence. Preprocessing is unweighted and matches the other arms.
- RandomUnderSampler: sampling_strategy='auto' (binary 1:1 balancing), replacement=False, random_state=42, classifier class_weight=None. Never combined with balanced class weights. Majority information is deliberately discarded within fitting folds; validation prevalence is never changed.

All classifiers use seed=42. LR: C=[0.1,1,10], lbfgs/default L2, max_iter=1000. HGB: learning_rate=[0.05,0.1], max_iter=[100,200], max_leaf_nodes=[15,31], l2_regularization=[0,1], early_stopping=False, categorical_features=None. Only inner AP selects each new treatment's configuration; outer scores do not select hyperparameters. Fixed grids/budgets and original raw covariates/folds are consistent across arms.

## Imbalanced-learn compatibility and sampling order

Validated imbalanced-learn 0.14.2 with sklearn 1.8.0. This environment initially lacked imbalanced-learn; installed it and its required sklearn-compat dependency in a scratch dependency directory, leaving project files unchanged. The first dependency smoke test identified missing sklearn_compat after a no-dependencies install; installing sklearn-compat resolved it before experiments. Colab install instructions are in the notebook; no approved module is overwritten.

Imbalanced-learn rejects a nested sklearn Pipeline as an intermediate step. The experiment therefore takes the fresh, unfitted ColumnTransformer from `make_preprocessor(name).named_steps['preprocessor']` and places that exact approved object in an imbalanced-learn Pipeline. This removes only the redundant outer wrapper; it does not reimplement or change encoding/scaling/recency logic. Every arm uses this same adapter.

Order: approved preprocessing fit/transform on **all current fitting-fold rows** → stateless finite guard → training-only sampler (or passthrough) → classifier. Thus one-hot categories, ordinary scaling and available-only recency statistics are learned from original fitting rows before any row deletion, consistently across arms. Random selection then retains entire transformed rows, preserving categorical/recency relationships. It does not synthesize values or interpolate dummies. Every sampler call asserts original/retained row mapping, target alignment, unique selected positions and exactly equal retained binary class counts. At predict time imbalanced-learn skips the sampler; audit logs assert no sampler calls or sample-state changes occur and validation predictions retain full cohort size.

## Proper hyperparameter and threshold selection

For each outer fold, new treatment grids use GridSearchCV, scoring returning named AP from positive predict_proba, refit='AP', n_jobs=1, error_score='raise', only outer-training rows. Winners refit on outer training, never complete development. Selected-model training-side OOF probabilities then fit thresholds, with fresh full pipelines (and training-only sampling) in five subfolds. Hyperparameters use that entire outer-training partition's previous inner scoring, so training-side OOF is conditional on a training-selected configuration and is not claimed as independent performance; it serves threshold fitting only. The untouched outer layer evaluates both choices.

Threshold grid unchanged from Phase 5B-1: [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]. Three policies: .50 reference; training-OOF F1 maximum (ties higher threshold); maximum recall with empirical precision >=50% and positive volume (ties precision, then higher threshold). The 50% target is illustrative research, not bank policy. If none qualifies **within this grid**, record none feasible and abstain with zero contacts, not a guarantee of precision. This does not prove no threshold outside the grid can qualify. No grid expansion after seeing outcomes. Probability shifts from weighting/sampling can move useful thresholds outside this range; calibration/prior correction is not silently introduced.

Thresholds freeze before outer predictions/labels are used for evaluation. AP/ROC-AUC remain identical across decision policies for the same probability predictions; only treatment/model training can change ranking. No outer-label threshold optimization or global preprocessing.

## Selected hyperparameters

| model | treatment | outer_fold | parameters | source |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | reused exact Phase 5A training-only inner AP selection |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| LogisticRegression | Original | 1 | {"classifier__C": 0.1} | reused exact Phase 5A training-only inner AP selection |
| LogisticRegression | Balanced | 1 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| LogisticRegression | RandomUnderSampler | 1 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| HistGradientBoosting | Original | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | reused exact Phase 5A training-only inner AP selection |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| LogisticRegression | Original | 2 | {"classifier__C": 0.1} | reused exact Phase 5A training-only inner AP selection |
| LogisticRegression | Balanced | 2 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| LogisticRegression | RandomUnderSampler | 2 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| HistGradientBoosting | Original | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | reused exact Phase 5A training-only inner AP selection |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| LogisticRegression | Original | 3 | {"classifier__C": 0.1} | reused exact Phase 5A training-only inner AP selection |
| LogisticRegression | Balanced | 3 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| LogisticRegression | RandomUnderSampler | 3 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| HistGradientBoosting | Original | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | reused exact Phase 5A training-only inner AP selection |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| LogisticRegression | Original | 4 | {"classifier__C": 0.1} | reused exact Phase 5A training-only inner AP selection |
| LogisticRegression | Balanced | 4 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| LogisticRegression | RandomUnderSampler | 4 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| HistGradientBoosting | Original | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | reused exact Phase 5A training-only inner AP selection |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | fresh outer-training-only inner AP search |
| LogisticRegression | Original | 5 | {"classifier__C": 0.1} | reused exact Phase 5A training-only inner AP selection |
| LogisticRegression | Balanced | 5 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |
| LogisticRegression | RandomUnderSampler | 5 | {"classifier__C": 0.1} | fresh outer-training-only inner AP search |

All new-treatment inner candidates (selection scores only, not outer performance):

| model | treatment | outer_fold | parameters | inner_AP_mean | inner_AP_SD | rank_AP |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.446347 | 0.028299 | 1 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.445440 | 0.027461 | 3 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.443956 | 0.029875 | 5 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.436895 | 0.030329 | 11 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.442456 | 0.030645 | 8 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.436069 | 0.027776 | 12 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.432549 | 0.029432 | 14 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.419866 | 0.032012 | 16 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.446002 | 0.030484 | 2 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.444043 | 0.029001 | 4 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.443882 | 0.028874 | 6 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.437411 | 0.030983 | 9 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.443210 | 0.029594 | 7 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.435864 | 0.030608 | 13 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.437234 | 0.031425 | 10 |
| HistGradientBoosting | Balanced | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.421377 | 0.030255 | 15 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.426019 | 0.036307 | 1 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.418555 | 0.035032 | 5 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.418517 | 0.037380 | 6 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.407295 | 0.034450 | 13 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.416919 | 0.035094 | 8 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.403233 | 0.034009 | 14 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.407601 | 0.034953 | 12 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.391860 | 0.032977 | 16 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.425082 | 0.037736 | 2 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.420658 | 0.036184 | 3 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.420644 | 0.039615 | 4 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.409468 | 0.037135 | 11 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.417783 | 0.037550 | 7 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.409828 | 0.032083 | 10 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.410895 | 0.039551 | 9 |
| HistGradientBoosting | RandomUnderSampler | 1 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.397746 | 0.034528 | 15 |
| LogisticRegression | Balanced | 1 | {"classifier__C": 0.1} | 0.419139 | 0.025078 | 1 |
| LogisticRegression | Balanced | 1 | {"classifier__C": 1.0} | 0.418572 | 0.025512 | 2 |
| LogisticRegression | Balanced | 1 | {"classifier__C": 10.0} | 0.418466 | 0.025476 | 3 |
| LogisticRegression | RandomUnderSampler | 1 | {"classifier__C": 0.1} | 0.419047 | 0.026829 | 1 |
| LogisticRegression | RandomUnderSampler | 1 | {"classifier__C": 1.0} | 0.417805 | 0.028427 | 2 |
| LogisticRegression | RandomUnderSampler | 1 | {"classifier__C": 10.0} | 0.416850 | 0.029088 | 3 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.451928 | 0.026906 | 1 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.447552 | 0.026076 | 5 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.447800 | 0.027063 | 4 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.441553 | 0.027709 | 12 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447228 | 0.030056 | 8 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.442947 | 0.029679 | 11 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.438386 | 0.027115 | 14 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.426502 | 0.028951 | 16 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.451063 | 0.026419 | 2 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.447468 | 0.027694 | 7 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.449094 | 0.029395 | 3 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.444831 | 0.029218 | 9 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.447531 | 0.028214 | 6 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.443270 | 0.028737 | 10 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.441427 | 0.028391 | 13 |
| HistGradientBoosting | Balanced | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.432841 | 0.028217 | 15 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.435788 | 0.034303 | 2 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.429641 | 0.032112 | 5 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.424891 | 0.036284 | 8 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.419344 | 0.030992 | 12 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.426831 | 0.033393 | 7 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.418868 | 0.033660 | 13 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.416057 | 0.033772 | 14 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.407367 | 0.035259 | 16 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.438546 | 0.034908 | 1 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.432850 | 0.034779 | 3 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.432390 | 0.033963 | 4 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.421785 | 0.036405 | 10 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.427758 | 0.032691 | 6 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.422781 | 0.035096 | 9 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.421761 | 0.034583 | 11 |
| HistGradientBoosting | RandomUnderSampler | 2 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.412870 | 0.031960 | 15 |
| LogisticRegression | Balanced | 2 | {"classifier__C": 0.1} | 0.422282 | 0.030412 | 1 |
| LogisticRegression | Balanced | 2 | {"classifier__C": 1.0} | 0.421989 | 0.030250 | 2 |
| LogisticRegression | Balanced | 2 | {"classifier__C": 10.0} | 0.421957 | 0.030269 | 3 |
| LogisticRegression | RandomUnderSampler | 2 | {"classifier__C": 0.1} | 0.420813 | 0.032863 | 1 |
| LogisticRegression | RandomUnderSampler | 2 | {"classifier__C": 1.0} | 0.420294 | 0.036688 | 2 |
| LogisticRegression | RandomUnderSampler | 2 | {"classifier__C": 10.0} | 0.419602 | 0.037508 | 3 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.450293 | 0.021534 | 2 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.447661 | 0.022407 | 4 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.444620 | 0.021096 | 7 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.435660 | 0.024986 | 12 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.444313 | 0.020632 | 8 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.434431 | 0.021972 | 14 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.435134 | 0.020668 | 13 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.419752 | 0.025734 | 16 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.452271 | 0.021530 | 1 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.449574 | 0.022301 | 3 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.445871 | 0.019765 | 5 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.438493 | 0.022015 | 9 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.445123 | 0.021224 | 6 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.435810 | 0.023000 | 11 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.436938 | 0.020518 | 10 |
| HistGradientBoosting | Balanced | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.425527 | 0.024809 | 15 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441154 | 0.023596 | 2 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.434081 | 0.022120 | 3 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.433387 | 0.019822 | 5 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.425213 | 0.020167 | 11 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.430891 | 0.019252 | 8 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.424340 | 0.022843 | 12 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.423012 | 0.022570 | 14 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.411450 | 0.024514 | 16 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441236 | 0.022931 | 1 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.433727 | 0.025316 | 4 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.432303 | 0.024250 | 7 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.425706 | 0.023793 | 10 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.433307 | 0.023615 | 6 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.423639 | 0.026621 | 13 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.427147 | 0.022529 | 9 |
| HistGradientBoosting | RandomUnderSampler | 3 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.413040 | 0.024459 | 15 |
| LogisticRegression | Balanced | 3 | {"classifier__C": 0.1} | 0.426659 | 0.023621 | 1 |
| LogisticRegression | Balanced | 3 | {"classifier__C": 1.0} | 0.425979 | 0.023263 | 2 |
| LogisticRegression | Balanced | 3 | {"classifier__C": 10.0} | 0.425797 | 0.023214 | 3 |
| LogisticRegression | RandomUnderSampler | 3 | {"classifier__C": 0.1} | 0.427262 | 0.025618 | 1 |
| LogisticRegression | RandomUnderSampler | 3 | {"classifier__C": 1.0} | 0.425480 | 0.025338 | 2 |
| LogisticRegression | RandomUnderSampler | 3 | {"classifier__C": 10.0} | 0.425193 | 0.025227 | 3 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.440837 | 0.017379 | 1 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.435638 | 0.012254 | 6 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.433899 | 0.014946 | 8 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.427669 | 0.009132 | 13 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.435506 | 0.016500 | 7 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.429054 | 0.008261 | 12 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.427434 | 0.012006 | 14 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.414521 | 0.005232 | 16 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.440386 | 0.016790 | 2 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.438712 | 0.012503 | 3 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.436571 | 0.014357 | 5 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.429525 | 0.009766 | 10 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.438399 | 0.018130 | 4 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.430945 | 0.008272 | 9 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.429217 | 0.010827 | 11 |
| HistGradientBoosting | Balanced | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.421231 | 0.005325 | 15 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.422341 | 0.013477 | 2 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.416719 | 0.015286 | 6 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.413904 | 0.013968 | 7 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.401441 | 0.013802 | 13 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.412251 | 0.014546 | 8 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.402211 | 0.011065 | 12 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.400806 | 0.012594 | 14 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.388172 | 0.013039 | 16 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.428376 | 0.015653 | 1 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.419880 | 0.015199 | 3 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.419247 | 0.016861 | 4 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.405205 | 0.013465 | 11 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.418051 | 0.013512 | 5 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.405249 | 0.013912 | 10 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.406661 | 0.014458 | 9 |
| HistGradientBoosting | RandomUnderSampler | 4 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.392714 | 0.013184 | 15 |
| LogisticRegression | Balanced | 4 | {"classifier__C": 0.1} | 0.419404 | 0.013983 | 1 |
| LogisticRegression | Balanced | 4 | {"classifier__C": 1.0} | 0.418544 | 0.014068 | 2 |
| LogisticRegression | Balanced | 4 | {"classifier__C": 10.0} | 0.418423 | 0.014093 | 3 |
| LogisticRegression | RandomUnderSampler | 4 | {"classifier__C": 0.1} | 0.416999 | 0.015488 | 1 |
| LogisticRegression | RandomUnderSampler | 4 | {"classifier__C": 1.0} | 0.415679 | 0.014867 | 2 |
| LogisticRegression | RandomUnderSampler | 4 | {"classifier__C": 10.0} | 0.415174 | 0.014515 | 3 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.445468 | 0.009421 | 1 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.439392 | 0.010518 | 8 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.440859 | 0.008238 | 7 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.434002 | 0.010987 | 12 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.442717 | 0.011098 | 4 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.432232 | 0.013415 | 14 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.434763 | 0.013013 | 10 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.417542 | 0.013942 | 16 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.444356 | 0.009923 | 2 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.441146 | 0.009772 | 6 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.443780 | 0.010871 | 3 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.436965 | 0.010183 | 9 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.441731 | 0.011767 | 5 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.432498 | 0.011659 | 13 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.434293 | 0.012875 | 11 |
| HistGradientBoosting | Balanced | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.420929 | 0.014414 | 15 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.437645 | 0.019124 | 2 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.428098 | 0.023240 | 7 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.428545 | 0.025002 | 6 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.418110 | 0.025817 | 11 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.428097 | 0.022553 | 8 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.416406 | 0.021379 | 13 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.413624 | 0.024391 | 14 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.406385 | 0.023114 | 16 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.439448 | 0.016410 | 1 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.431430 | 0.017485 | 3 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.429301 | 0.022191 | 5 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.420339 | 0.023978 | 9 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.429593 | 0.020282 | 4 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 31} | 0.420085 | 0.023381 | 10 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.416912 | 0.025090 | 12 |
| HistGradientBoosting | RandomUnderSampler | 5 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.1, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 31} | 0.407663 | 0.028490 | 15 |
| LogisticRegression | Balanced | 5 | {"classifier__C": 0.1} | 0.418145 | 0.013027 | 1 |
| LogisticRegression | Balanced | 5 | {"classifier__C": 1.0} | 0.417628 | 0.013299 | 2 |
| LogisticRegression | Balanced | 5 | {"classifier__C": 10.0} | 0.417595 | 0.013426 | 3 |
| LogisticRegression | RandomUnderSampler | 5 | {"classifier__C": 0.1} | 0.416757 | 0.013743 | 1 |
| LogisticRegression | RandomUnderSampler | 5 | {"classifier__C": 1.0} | 0.416284 | 0.015052 | 2 |
| LogisticRegression | RandomUnderSampler | 5 | {"classifier__C": 10.0} | 0.414875 | 0.015101 | 3 |

## Individual outer-fold policy metrics

| model | treatment | outer_fold | policy | Accuracy | Precision | Recall | F1 | ROC_AUC | AP | predicted_positives | positive_rate | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | 1 | Reference_0.50 | 0.899666 | 0.650558 | 0.235849 | 0.346192 | 0.810998 | 0.450109 | 269 | 0.040832 | 5752 | 94 | 567 | 175 |
| HistGradientBoosting | Original | 1 | Training_F1 | 0.867183 | 0.435749 | 0.607817 | 0.507597 | 0.810998 | 0.450109 | 1035 | 0.157104 | 5262 | 584 | 291 | 451 |
| HistGradientBoosting | Original | 1 | Training_Precision50 | 0.891621 | 0.525547 | 0.388140 | 0.446512 | 0.810998 | 0.450109 | 548 | 0.083182 | 5586 | 260 | 454 | 288 |
| HistGradientBoosting | Balanced | 1 | Reference_0.50 | 0.844566 | 0.385366 | 0.638814 | 0.480730 | 0.812087 | 0.450972 | 1230 | 0.186703 | 5090 | 756 | 268 | 474 |
| HistGradientBoosting | Balanced | 1 | Training_F1 | 0.863236 | 0.424787 | 0.605121 | 0.499166 | 0.812087 | 0.450972 | 1057 | 0.160443 | 5238 | 608 | 293 | 449 |
| HistGradientBoosting | Balanced | 1 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.812087 | 0.450972 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | RandomUnderSampler | 1 | Reference_0.50 | 0.836066 | 0.368175 | 0.636119 | 0.466403 | 0.804137 | 0.430358 | 1282 | 0.194596 | 5036 | 810 | 270 | 472 |
| HistGradientBoosting | RandomUnderSampler | 1 | Training_F1 | 0.859441 | 0.415441 | 0.609164 | 0.493989 | 0.804137 | 0.430358 | 1088 | 0.165149 | 5210 | 636 | 290 | 452 |
| HistGradientBoosting | RandomUnderSampler | 1 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.804137 | 0.430358 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | Original | 1 | Reference_0.50 | 0.899211 | 0.671053 | 0.206199 | 0.315464 | 0.773340 | 0.432797 | 228 | 0.034608 | 5771 | 75 | 589 | 153 |
| LogisticRegression | Original | 1 | Training_F1 | 0.871281 | 0.438799 | 0.512129 | 0.472637 | 0.773340 | 0.432797 | 866 | 0.131451 | 5360 | 486 | 362 | 380 |
| LogisticRegression | Original | 1 | Training_Precision50 | 0.892532 | 0.535270 | 0.347709 | 0.421569 | 0.773340 | 0.432797 | 482 | 0.073163 | 5622 | 224 | 484 | 258 |
| LogisticRegression | Balanced | 1 | Reference_0.50 | 0.767911 | 0.285325 | 0.704852 | 0.406214 | 0.775107 | 0.430936 | 1833 | 0.278233 | 4536 | 1310 | 219 | 523 |
| LogisticRegression | Balanced | 1 | Training_F1 | 0.853218 | 0.397634 | 0.588949 | 0.474742 | 0.775107 | 0.430936 | 1099 | 0.166818 | 5184 | 662 | 305 | 437 |
| LogisticRegression | Balanced | 1 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.775107 | 0.430936 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | RandomUnderSampler | 1 | Reference_0.50 | 0.759866 | 0.277070 | 0.703504 | 0.397563 | 0.775097 | 0.424591 | 1884 | 0.285974 | 4484 | 1362 | 220 | 522 |
| LogisticRegression | RandomUnderSampler | 1 | Training_F1 | 0.843352 | 0.377327 | 0.601078 | 0.463617 | 0.775097 | 0.424591 | 1182 | 0.179417 | 5110 | 736 | 296 | 446 |
| LogisticRegression | RandomUnderSampler | 1 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.775097 | 0.424591 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | Original | 2 | Reference_0.50 | 0.899211 | 0.668103 | 0.208895 | 0.318275 | 0.791971 | 0.442077 | 232 | 0.035216 | 5769 | 77 | 587 | 155 |
| HistGradientBoosting | Original | 2 | Training_F1 | 0.866424 | 0.429158 | 0.563342 | 0.487179 | 0.791971 | 0.442077 | 974 | 0.147845 | 5290 | 556 | 324 | 418 |
| HistGradientBoosting | Original | 2 | Training_Precision50 | 0.892532 | 0.532197 | 0.378706 | 0.442520 | 0.791971 | 0.442077 | 528 | 0.080146 | 5599 | 247 | 461 | 281 |
| HistGradientBoosting | Balanced | 2 | Reference_0.50 | 0.841985 | 0.375727 | 0.609164 | 0.464781 | 0.791629 | 0.451069 | 1203 | 0.182605 | 5095 | 751 | 290 | 452 |
| HistGradientBoosting | Balanced | 2 | Training_F1 | 0.863388 | 0.421000 | 0.567385 | 0.483352 | 0.791629 | 0.451069 | 1000 | 0.151791 | 5267 | 579 | 321 | 421 |
| HistGradientBoosting | Balanced | 2 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.791629 | 0.451069 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | RandomUnderSampler | 2 | Reference_0.50 | 0.842744 | 0.376263 | 0.602426 | 0.463212 | 0.790559 | 0.441690 | 1188 | 0.180328 | 5105 | 741 | 295 | 447 |
| HistGradientBoosting | RandomUnderSampler | 2 | Training_F1 | 0.862933 | 0.419900 | 0.568733 | 0.483114 | 0.790559 | 0.441690 | 1005 | 0.152550 | 5263 | 583 | 320 | 422 |
| HistGradientBoosting | RandomUnderSampler | 2 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.790559 | 0.441690 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | Original | 2 | Reference_0.50 | 0.899970 | 0.698565 | 0.196765 | 0.307045 | 0.758226 | 0.420805 | 209 | 0.031724 | 5783 | 63 | 596 | 146 |
| LogisticRegression | Original | 2 | Training_F1 | 0.872344 | 0.439708 | 0.486523 | 0.461932 | 0.758226 | 0.420805 | 821 | 0.124621 | 5386 | 460 | 381 | 361 |
| LogisticRegression | Original | 2 | Training_Precision50 | 0.890407 | 0.521930 | 0.320755 | 0.397329 | 0.758226 | 0.420805 | 456 | 0.069217 | 5628 | 218 | 504 | 238 |
| LogisticRegression | Balanced | 2 | Reference_0.50 | 0.767001 | 0.277871 | 0.668464 | 0.392560 | 0.759423 | 0.417464 | 1785 | 0.270947 | 4557 | 1289 | 246 | 496 |
| LogisticRegression | Balanced | 2 | Training_F1 | 0.846539 | 0.375578 | 0.547170 | 0.445420 | 0.759423 | 0.417464 | 1081 | 0.164086 | 5171 | 675 | 336 | 406 |
| LogisticRegression | Balanced | 2 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.759423 | 0.417464 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | RandomUnderSampler | 2 | Reference_0.50 | 0.754706 | 0.267800 | 0.679245 | 0.384146 | 0.759165 | 0.419838 | 1882 | 0.285671 | 4468 | 1378 | 238 | 504 |
| LogisticRegression | RandomUnderSampler | 2 | Training_F1 | 0.840923 | 0.366259 | 0.564690 | 0.444327 | 0.759165 | 0.419838 | 1144 | 0.173649 | 5121 | 725 | 323 | 419 |
| LogisticRegression | RandomUnderSampler | 2 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.759165 | 0.419838 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | Original | 3 | Reference_0.50 | 0.899666 | 0.652830 | 0.233154 | 0.343595 | 0.788546 | 0.428814 | 265 | 0.040225 | 5754 | 92 | 569 | 173 |
| HistGradientBoosting | Original | 3 | Training_F1 | 0.857620 | 0.404297 | 0.557951 | 0.468856 | 0.788546 | 0.428814 | 1024 | 0.155434 | 5236 | 610 | 328 | 414 |
| HistGradientBoosting | Original | 3 | Training_Precision50 | 0.888282 | 0.505319 | 0.384097 | 0.436447 | 0.788546 | 0.428814 | 564 | 0.085610 | 5567 | 279 | 457 | 285 |
| HistGradientBoosting | Balanced | 3 | Reference_0.50 | 0.838342 | 0.367948 | 0.606469 | 0.458015 | 0.787446 | 0.427418 | 1223 | 0.185641 | 5073 | 773 | 292 | 450 |
| HistGradientBoosting | Balanced | 3 | Training_F1 | 0.855343 | 0.400000 | 0.568733 | 0.469672 | 0.787446 | 0.427418 | 1055 | 0.160140 | 5213 | 633 | 320 | 422 |
| HistGradientBoosting | Balanced | 3 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.787446 | 0.427418 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | RandomUnderSampler | 3 | Reference_0.50 | 0.833940 | 0.360317 | 0.611860 | 0.453546 | 0.779623 | 0.406565 | 1260 | 0.191257 | 5040 | 806 | 288 | 454 |
| HistGradientBoosting | RandomUnderSampler | 3 | Training_F1 | 0.852611 | 0.394275 | 0.575472 | 0.467945 | 0.779623 | 0.406565 | 1083 | 0.164390 | 5190 | 656 | 315 | 427 |
| HistGradientBoosting | RandomUnderSampler | 3 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.779623 | 0.406565 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | Original | 3 | Reference_0.50 | 0.897996 | 0.660550 | 0.194070 | 0.300000 | 0.742708 | 0.403262 | 218 | 0.033090 | 5772 | 74 | 598 | 144 |
| LogisticRegression | Original | 3 | Training_F1 | 0.865665 | 0.417722 | 0.489218 | 0.450652 | 0.742708 | 0.403262 | 869 | 0.131906 | 5340 | 506 | 379 | 363 |
| LogisticRegression | Original | 3 | Training_Precision50 | 0.887675 | 0.502058 | 0.328841 | 0.397394 | 0.742708 | 0.403262 | 486 | 0.073770 | 5604 | 242 | 498 | 244 |
| LogisticRegression | Balanced | 3 | Reference_0.50 | 0.753339 | 0.262251 | 0.656334 | 0.374760 | 0.743582 | 0.402949 | 1857 | 0.281876 | 4476 | 1370 | 255 | 487 |
| LogisticRegression | Balanced | 3 | Training_F1 | 0.839557 | 0.358744 | 0.539084 | 0.430802 | 0.743582 | 0.402949 | 1115 | 0.169247 | 5131 | 715 | 342 | 400 |
| LogisticRegression | Balanced | 3 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.743582 | 0.402949 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | RandomUnderSampler | 3 | Reference_0.50 | 0.753339 | 0.260964 | 0.649596 | 0.372345 | 0.741790 | 0.398305 | 1847 | 0.280358 | 4481 | 1365 | 260 | 482 |
| LogisticRegression | RandomUnderSampler | 3 | Training_F1 | 0.843807 | 0.365511 | 0.525606 | 0.431177 | 0.741790 | 0.398305 | 1067 | 0.161961 | 5169 | 677 | 352 | 390 |
| LogisticRegression | RandomUnderSampler | 3 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.741790 | 0.398305 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | Original | 4 | Reference_0.50 | 0.900273 | 0.683983 | 0.212938 | 0.324769 | 0.802185 | 0.467601 | 231 | 0.035064 | 5773 | 73 | 584 | 158 |
| HistGradientBoosting | Original | 4 | Training_F1 | 0.865665 | 0.432356 | 0.615903 | 0.508060 | 0.802185 | 0.467601 | 1057 | 0.160443 | 5246 | 600 | 285 | 457 |
| HistGradientBoosting | Original | 4 | Training_Precision50 | 0.893898 | 0.543086 | 0.365229 | 0.436745 | 0.802185 | 0.467601 | 499 | 0.075744 | 5618 | 228 | 471 | 271 |
| HistGradientBoosting | Balanced | 4 | Reference_0.50 | 0.851245 | 0.398981 | 0.633423 | 0.489583 | 0.802647 | 0.470286 | 1178 | 0.178810 | 5138 | 708 | 272 | 470 |
| HistGradientBoosting | Balanced | 4 | Training_F1 | 0.867790 | 0.437801 | 0.611860 | 0.510399 | 0.802647 | 0.470286 | 1037 | 0.157407 | 5263 | 583 | 288 | 454 |
| HistGradientBoosting | Balanced | 4 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.802647 | 0.470286 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | RandomUnderSampler | 4 | Reference_0.50 | 0.834092 | 0.367547 | 0.656334 | 0.471214 | 0.802165 | 0.456585 | 1325 | 0.201123 | 5008 | 838 | 255 | 487 |
| HistGradientBoosting | RandomUnderSampler | 4 | Training_F1 | 0.864451 | 0.428300 | 0.607817 | 0.502507 | 0.802165 | 0.456585 | 1053 | 0.159836 | 5244 | 602 | 291 | 451 |
| HistGradientBoosting | RandomUnderSampler | 4 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.802165 | 0.456585 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | Original | 4 | Reference_0.50 | 0.897996 | 0.678571 | 0.179245 | 0.283582 | 0.770552 | 0.425777 | 196 | 0.029751 | 5783 | 63 | 609 | 133 |
| LogisticRegression | Original | 4 | Training_F1 | 0.874165 | 0.449242 | 0.518868 | 0.481551 | 0.770552 | 0.425777 | 857 | 0.130085 | 5374 | 472 | 357 | 385 |
| LogisticRegression | Original | 4 | Training_Precision50 | 0.892835 | 0.541475 | 0.316712 | 0.399660 | 0.770552 | 0.425777 | 434 | 0.065877 | 5647 | 199 | 507 | 235 |
| LogisticRegression | Balanced | 4 | Reference_0.50 | 0.776108 | 0.291880 | 0.692722 | 0.410707 | 0.772475 | 0.420824 | 1761 | 0.267304 | 4599 | 1247 | 228 | 514 |
| LogisticRegression | Balanced | 4 | Training_F1 | 0.856102 | 0.403558 | 0.580863 | 0.476243 | 0.772475 | 0.420824 | 1068 | 0.162113 | 5209 | 637 | 311 | 431 |
| LogisticRegression | Balanced | 4 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.772475 | 0.420824 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| LogisticRegression | RandomUnderSampler | 4 | Reference_0.50 | 0.767456 | 0.283917 | 0.699461 | 0.403891 | 0.772041 | 0.425706 | 1828 | 0.277474 | 4537 | 1309 | 223 | 519 |
| LogisticRegression | RandomUnderSampler | 4 | Training_F1 | 0.843048 | 0.377311 | 0.605121 | 0.464803 | 0.772041 | 0.425706 | 1190 | 0.180631 | 5105 | 741 | 293 | 449 |
| LogisticRegression | RandomUnderSampler | 4 | Training_Precision50 | 0.887371 | 0.000000 | 0.000000 | 0.000000 | 0.772041 | 0.425706 | 0 | 0.000000 | 5846 | 0 | 742 | 0 |
| HistGradientBoosting | Original | 5 | Reference_0.50 | 0.899514 | 0.683258 | 0.203230 | 0.313278 | 0.780853 | 0.452125 | 221 | 0.033546 | 5775 | 70 | 592 | 151 |
| HistGradientBoosting | Original | 5 | Training_F1 | 0.869460 | 0.440969 | 0.588156 | 0.504037 | 0.780853 | 0.452125 | 991 | 0.150425 | 5291 | 554 | 306 | 437 |
| HistGradientBoosting | Original | 5 | Training_Precision50 | 0.892077 | 0.529851 | 0.382234 | 0.444097 | 0.780853 | 0.452125 | 536 | 0.081360 | 5593 | 252 | 459 | 284 |
| HistGradientBoosting | Balanced | 5 | Reference_0.50 | 0.843200 | 0.381729 | 0.629879 | 0.475368 | 0.783681 | 0.454671 | 1226 | 0.186096 | 5087 | 758 | 275 | 468 |
| HistGradientBoosting | Balanced | 5 | Training_F1 | 0.864602 | 0.427740 | 0.593540 | 0.497182 | 0.783681 | 0.454671 | 1031 | 0.156497 | 5255 | 590 | 302 | 441 |
| HistGradientBoosting | Balanced | 5 | Training_Precision50 | 0.887219 | 0.000000 | 0.000000 | 0.000000 | 0.783681 | 0.454671 | 0 | 0.000000 | 5845 | 0 | 743 | 0 |
| HistGradientBoosting | RandomUnderSampler | 5 | Reference_0.50 | 0.831967 | 0.359784 | 0.628533 | 0.457619 | 0.784948 | 0.446098 | 1298 | 0.197025 | 5014 | 831 | 276 | 467 |
| HistGradientBoosting | RandomUnderSampler | 5 | Training_F1 | 0.863084 | 0.425071 | 0.606999 | 0.500000 | 0.784948 | 0.446098 | 1061 | 0.161050 | 5235 | 610 | 292 | 451 |
| HistGradientBoosting | RandomUnderSampler | 5 | Training_Precision50 | 0.887219 | 0.000000 | 0.000000 | 0.000000 | 0.784948 | 0.446098 | 0 | 0.000000 | 5845 | 0 | 743 | 0 |
| LogisticRegression | Original | 5 | Reference_0.50 | 0.900729 | 0.725888 | 0.192463 | 0.304255 | 0.764549 | 0.429507 | 197 | 0.029903 | 5791 | 54 | 600 | 143 |
| LogisticRegression | Original | 5 | Training_F1 | 0.874317 | 0.448107 | 0.493943 | 0.469910 | 0.764549 | 0.429507 | 819 | 0.124317 | 5393 | 452 | 376 | 367 |
| LogisticRegression | Original | 5 | Training_Precision50 | 0.894809 | 0.555556 | 0.336474 | 0.419111 | 0.764549 | 0.429507 | 450 | 0.068306 | 5645 | 200 | 493 | 250 |
| LogisticRegression | Balanced | 5 | Reference_0.50 | 0.764572 | 0.276301 | 0.671602 | 0.391526 | 0.765788 | 0.430457 | 1806 | 0.274135 | 4538 | 1307 | 244 | 499 |
| LogisticRegression | Balanced | 5 | Training_F1 | 0.847298 | 0.382694 | 0.577389 | 0.460300 | 0.765788 | 0.430457 | 1121 | 0.170158 | 5153 | 692 | 314 | 429 |
| LogisticRegression | Balanced | 5 | Training_Precision50 | 0.887219 | 0.000000 | 0.000000 | 0.000000 | 0.765788 | 0.430457 | 0 | 0.000000 | 5845 | 0 | 743 | 0 |
| LogisticRegression | RandomUnderSampler | 5 | Reference_0.50 | 0.755313 | 0.268019 | 0.675639 | 0.383792 | 0.765082 | 0.429917 | 1873 | 0.284305 | 4474 | 1371 | 241 | 502 |
| LogisticRegression | RandomUnderSampler | 5 | Training_F1 | 0.840771 | 0.369898 | 0.585464 | 0.453361 | 0.765082 | 0.429917 | 1176 | 0.178506 | 5104 | 741 | 308 | 435 |
| LogisticRegression | RandomUnderSampler | 5 | Training_Precision50 | 0.887219 | 0.000000 | 0.000000 | 0.000000 | 0.765082 | 0.429917 | 0 | 0.000000 | 5845 | 0 | 743 | 0 |

Five-fold mean ± sample SD (ddof=1); contact counts are per-cohort averages and positive_rate a fraction:

| model | treatment | policy | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | AP mean ± SD | predicted_positives mean ± SD | positive_rate mean ± SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | Reference_0.50 | 0.843868 ± 0.004728 | 0.381950 ± 0.011582 | 0.623550 ± 0.014741 | 0.473696 ± 0.012550 | 0.795498 ± 0.011681 | 0.450883 ± 0.015341 | 1212.000000 ± 21.667949 | 0.183971 ± 0.003289 |
| HistGradientBoosting | Balanced | Training_F1 | 0.862872 ± 0.004590 | 0.422266 ± 0.013920 | 0.589328 ± 0.020497 | 0.491954 ± 0.015733 | 0.795498 ± 0.011681 | 0.450883 ± 0.015341 | 1036.000000 ± 23.043437 | 0.157256 ± 0.003498 |
| HistGradientBoosting | Balanced | Training_Precision50 | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.795498 ± 0.011681 | 0.450883 ± 0.015341 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 |
| HistGradientBoosting | Original | Reference_0.50 | 0.899666 ± 0.000387 | 0.667746 ± 0.015987 | 0.218813 ± 0.014761 | 0.329222 ± 0.014903 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 243.600000 ± 21.835751 | 0.036976 ± 0.003314 |
| HistGradientBoosting | Original | Training_F1 | 0.865270 ± 0.004506 | 0.428506 ± 0.014222 | 0.586634 ± 0.025850 | 0.495146 ± 0.016996 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 1016.200000 ± 33.521635 | 0.154250 ± 0.005088 |
| HistGradientBoosting | Original | Training_Precision50 | 0.891682 ± 0.002083 | 0.527200 ± 0.013837 | 0.379681 ± 0.008766 | 0.441264 ± 0.004494 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 535.000000 ± 24.269322 | 0.081208 ± 0.003684 |
| HistGradientBoosting | RandomUnderSampler | Reference_0.50 | 0.835762 ± 0.004164 | 0.366417 ± 0.006755 | 0.627054 ± 0.021090 | 0.462399 ± 0.006993 | 0.792286 ± 0.010668 | 0.436259 ± 0.019079 | 1270.600000 ± 51.901830 | 0.192866 ± 0.007878 |
| HistGradientBoosting | RandomUnderSampler | Training_F1 | 0.860504 ± 0.004784 | 0.416598 ± 0.013410 | 0.593637 ± 0.019817 | 0.489511 ± 0.014186 | 0.792286 ± 0.010668 | 0.436259 ± 0.019079 | 1058.000000 ± 33.045423 | 0.160595 ± 0.005016 |
| HistGradientBoosting | RandomUnderSampler | Training_Precision50 | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.792286 ± 0.010668 | 0.436259 ± 0.019079 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 |
| LogisticRegression | Balanced | Reference_0.50 | 0.765786 ± 0.008200 | 0.278726 ± 0.011120 | 0.678795 ± 0.019595 | 0.395153 ± 0.014142 | 0.763275 ± 0.012586 | 0.420526 ± 0.011461 | 1808.400000 ± 37.971042 | 0.274499 ± 0.005764 |
| LogisticRegression | Balanced | Training_F1 | 0.848543 ± 0.006429 | 0.383642 ± 0.017876 | 0.566691 ± 0.022102 | 0.457502 ± 0.019462 | 0.763275 ± 0.012586 | 0.420526 ± 0.011461 | 1096.800000 ± 22.365151 | 0.166485 ± 0.003395 |
| LogisticRegression | Balanced | Training_Precision50 | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.763275 ± 0.012586 | 0.420526 ± 0.011461 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 |
| LogisticRegression | Original | Reference_0.50 | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 209.600000 ± 13.722245 | 0.031815 ± 0.002083 |
| LogisticRegression | Original | Training_F1 | 0.871554 ± 0.003530 | 0.438715 ± 0.012656 | 0.500136 ± 0.014471 | 0.467336 ± 0.011666 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 846.400000 ± 24.511222 | 0.128476 ± 0.003721 |
| LogisticRegression | Original | Training_Precision50 | 0.891651 ± 0.002716 | 0.531257 ± 0.020313 | 0.330098 ± 0.012439 | 0.407013 ± 0.012233 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 461.600000 ± 22.018174 | 0.070067 ± 0.003342 |
| LogisticRegression | RandomUnderSampler | Reference_0.50 | 0.758136 ± 0.005758 | 0.271554 ± 0.008972 | 0.681489 ± 0.021588 | 0.388347 ± 0.012460 | 0.762635 ± 0.013194 | 0.419671 ± 0.012471 | 1862.800000 ± 24.406966 | 0.282757 ± 0.003705 |
| LogisticRegression | RandomUnderSampler | Training_F1 | 0.842380 ± 0.001426 | 0.371261 ± 0.005774 | 0.576392 ± 0.032531 | 0.451457 ± 0.014069 | 0.762635 ± 0.013194 | 0.419671 ± 0.012471 | 1151.800000 ± 50.519303 | 0.174833 ± 0.007668 |
| LogisticRegression | RandomUnderSampler | Training_Precision50 | 0.887341 ± 0.000068 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.762635 ± 0.013194 | 0.419671 ± 0.012471 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 |

Ranking comparison, invariant to threshold:

| model | treatment | AP_mean | AP_SD | ROC_AUC_mean | ROC_AUC_SD |
| --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | 0.450883 | 0.015341 | 0.795498 | 0.011681 |
| HistGradientBoosting | Original | 0.448145 | 0.014219 | 0.794911 | 0.011816 |
| HistGradientBoosting | RandomUnderSampler | 0.436259 | 0.019079 | 0.792286 | 0.010668 |
| LogisticRegression | Balanced | 0.420526 | 0.011461 | 0.763275 | 0.012586 |
| LogisticRegression | Original | 0.422429 | 0.011606 | 0.761875 | 0.012192 |
| LogisticRegression | RandomUnderSampler | 0.419671 | 0.012471 | 0.762635 | 0.013194 |

Pooled outer-policy diagnostics (not a substitute for mean-fold values):

| model | treatment | policy | Accuracy | Precision | Recall | F1 | ROC_AUC | AP | predicted_positives | positive_rate | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | Reference_0.50 | 0.899666 | 0.666667 | 0.218809 | 0.329479 | 0.794260 | 0.445335 | 1218 | 0.036976 | 28823 | 406 | 2899 | 812 |
| HistGradientBoosting | Original | Training_F1 | 0.865270 | 0.428459 | 0.586634 | 0.495223 | 0.794260 | 0.445335 | 5081 | 0.154250 | 26325 | 2904 | 1534 | 2177 |
| HistGradientBoosting | Original | Training_Precision50 | 0.891682 | 0.526729 | 0.379682 | 0.441278 | 0.794260 | 0.445335 | 2675 | 0.081208 | 27963 | 1266 | 2302 | 1409 |
| HistGradientBoosting | Balanced | Reference_0.50 | 0.843868 | 0.381848 | 0.623552 | 0.473647 | 0.794982 | 0.446932 | 6060 | 0.183971 | 25483 | 3746 | 1397 | 2314 |
| HistGradientBoosting | Balanced | Training_F1 | 0.862872 | 0.422201 | 0.589329 | 0.491958 | 0.794982 | 0.446932 | 5180 | 0.157256 | 26236 | 2993 | 1524 | 2187 |
| HistGradientBoosting | Balanced | Training_Precision50 | 0.887341 | 0.000000 | 0.000000 | 0.000000 | 0.794982 | 0.446932 | 0 | 0.000000 | 29229 | 0 | 3711 | 0 |
| HistGradientBoosting | RandomUnderSampler | Reference_0.50 | 0.835762 | 0.366284 | 0.627055 | 0.462440 | 0.791972 | 0.432852 | 6353 | 0.192866 | 25203 | 4026 | 1384 | 2327 |
| HistGradientBoosting | RandomUnderSampler | Training_F1 | 0.860504 | 0.416446 | 0.593641 | 0.489501 | 0.791972 | 0.432852 | 5290 | 0.160595 | 26142 | 3087 | 1508 | 2203 |
| HistGradientBoosting | RandomUnderSampler | Training_Precision50 | 0.887341 | 0.000000 | 0.000000 | 0.000000 | 0.791972 | 0.432852 | 0 | 0.000000 | 29229 | 0 | 3711 | 0 |
| LogisticRegression | Original | Reference_0.50 | 0.899180 | 0.686069 | 0.193748 | 0.302164 | 0.761768 | 0.421094 | 1048 | 0.031815 | 28900 | 329 | 2992 | 719 |
| LogisticRegression | Original | Training_F1 | 0.871554 | 0.438563 | 0.500135 | 0.467330 | 0.761768 | 0.421094 | 4232 | 0.128476 | 26853 | 2376 | 1855 | 1856 |
| LogisticRegression | Original | Training_Precision50 | 0.891651 | 0.530763 | 0.330100 | 0.407044 | 0.761768 | 0.421094 | 2308 | 0.070067 | 28146 | 1083 | 2486 | 1225 |
| LogisticRegression | Balanced | Reference_0.50 | 0.765786 | 0.278589 | 0.678793 | 0.395044 | 0.763146 | 0.419079 | 9042 | 0.274499 | 22706 | 6523 | 1192 | 2519 |
| LogisticRegression | Balanced | Training_F1 | 0.848543 | 0.383479 | 0.566694 | 0.457423 | 0.763146 | 0.419079 | 5484 | 0.166485 | 25848 | 3381 | 1608 | 2103 |
| LogisticRegression | Balanced | Training_Precision50 | 0.887341 | 0.000000 | 0.000000 | 0.000000 | 0.763146 | 0.419079 | 0 | 0.000000 | 29229 | 0 | 3711 | 0 |
| LogisticRegression | RandomUnderSampler | Reference_0.50 | 0.758136 | 0.271527 | 0.681487 | 0.388330 | 0.762404 | 0.418117 | 9314 | 0.282757 | 22444 | 6785 | 1182 | 2529 |
| LogisticRegression | RandomUnderSampler | Training_F1 | 0.842380 | 0.371419 | 0.576395 | 0.451742 | 0.762404 | 0.418117 | 5759 | 0.174833 | 25609 | 3620 | 1572 | 2139 |
| LogisticRegression | RandomUnderSampler | Training_Precision50 | 0.887341 | 0.000000 | 0.000000 | 0.000000 | 0.762404 | 0.418117 | 0 | 0.000000 | 29229 | 0 | 3711 | 0 |

## Threshold stability and grid-feasibility

| model | treatment | outer_fold | policy | threshold | training_feasible | training_precision | training_recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | 1 | Reference_0.50 | 0.500000 | True | 0.660063 | 0.213203 |
| HistGradientBoosting | Original | 1 | Training_F1 | 0.200000 | True | 0.429076 | 0.572583 |
| HistGradientBoosting | Original | 1 | Training_Precision50 | 0.350000 | True | 0.527404 | 0.369485 |
| HistGradientBoosting | Balanced | 1 | Reference_0.50 | 0.500000 | True | 0.375489 | 0.614011 |
| HistGradientBoosting | Balanced | 1 | Training_F1 | 0.600000 | True | 0.422070 | 0.581004 |
| HistGradientBoosting | Balanced | 1 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | RandomUnderSampler | 1 | Reference_0.50 | 0.500000 | True | 0.354406 | 0.623105 |
| HistGradientBoosting | RandomUnderSampler | 1 | Training_F1 | 0.600000 | True | 0.408708 | 0.588077 |
| HistGradientBoosting | RandomUnderSampler | 1 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | Original | 1 | Reference_0.50 | 0.500000 | True | 0.682209 | 0.187268 |
| LogisticRegression | Original | 1 | Training_F1 | 0.200000 | True | 0.435503 | 0.495790 |
| LogisticRegression | Original | 1 | Training_Precision50 | 0.350000 | True | 0.524769 | 0.324688 |
| LogisticRegression | Balanced | 1 | Reference_0.50 | 0.500000 | True | 0.279076 | 0.667565 |
| LogisticRegression | Balanced | 1 | Training_F1 | 0.600000 | True | 0.383033 | 0.558100 |
| LogisticRegression | Balanced | 1 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | RandomUnderSampler | 1 | Reference_0.50 | 0.500000 | True | 0.264443 | 0.678343 |
| LogisticRegression | RandomUnderSampler | 1 | Training_F1 | 0.600000 | True | 0.369761 | 0.567531 |
| LogisticRegression | RandomUnderSampler | 1 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | Original | 2 | Reference_0.50 | 0.500000 | True | 0.675761 | 0.216908 |
| HistGradientBoosting | Original | 2 | Training_F1 | 0.200000 | True | 0.430380 | 0.584035 |
| HistGradientBoosting | Original | 2 | Training_Precision50 | 0.350000 | True | 0.519059 | 0.371506 |
| HistGradientBoosting | Balanced | 2 | Reference_0.50 | 0.500000 | True | 0.381169 | 0.621758 |
| HistGradientBoosting | Balanced | 2 | Training_F1 | 0.600000 | True | 0.425340 | 0.589087 |
| HistGradientBoosting | Balanced | 2 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | RandomUnderSampler | 2 | Reference_0.50 | 0.500000 | True | 0.368846 | 0.630852 |
| HistGradientBoosting | RandomUnderSampler | 2 | Training_F1 | 0.600000 | True | 0.414519 | 0.590434 |
| HistGradientBoosting | RandomUnderSampler | 2 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | Original | 2 | Reference_0.50 | 0.500000 | True | 0.674883 | 0.193668 |
| LogisticRegression | Original | 2 | Training_F1 | 0.200000 | True | 0.432063 | 0.500168 |
| LogisticRegression | Original | 2 | Training_Precision50 | 0.350000 | True | 0.536353 | 0.323004 |
| LogisticRegression | Balanced | 2 | Reference_0.50 | 0.500000 | True | 0.280707 | 0.674301 |
| LogisticRegression | Balanced | 2 | Training_F1 | 0.600000 | True | 0.381671 | 0.570899 |
| LogisticRegression | Balanced | 2 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | RandomUnderSampler | 2 | Reference_0.50 | 0.500000 | True | 0.271089 | 0.684069 |
| LogisticRegression | RandomUnderSampler | 2 | Training_F1 | 0.600000 | True | 0.375246 | 0.576962 |
| LogisticRegression | RandomUnderSampler | 2 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | Original | 3 | Reference_0.50 | 0.500000 | True | 0.657603 | 0.219939 |
| HistGradientBoosting | Original | 3 | Training_F1 | 0.200000 | True | 0.436168 | 0.585719 |
| HistGradientBoosting | Original | 3 | Training_Precision50 | 0.350000 | True | 0.517148 | 0.385989 |
| HistGradientBoosting | Balanced | 3 | Reference_0.50 | 0.500000 | True | 0.382922 | 0.626810 |
| HistGradientBoosting | Balanced | 3 | Training_F1 | 0.600000 | True | 0.426432 | 0.594476 |
| HistGradientBoosting | Balanced | 3 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | RandomUnderSampler | 3 | Reference_0.50 | 0.500000 | True | 0.367111 | 0.630852 |
| HistGradientBoosting | RandomUnderSampler | 3 | Training_F1 | 0.600000 | True | 0.415446 | 0.592455 |
| HistGradientBoosting | RandomUnderSampler | 3 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | Original | 3 | Reference_0.50 | 0.500000 | True | 0.683180 | 0.199731 |
| LogisticRegression | Original | 3 | Training_F1 | 0.200000 | True | 0.442967 | 0.504884 |
| LogisticRegression | Original | 3 | Training_Precision50 | 0.350000 | True | 0.536278 | 0.343550 |
| LogisticRegression | Balanced | 3 | Reference_0.50 | 0.500000 | True | 0.282201 | 0.684069 |
| LogisticRegression | Balanced | 3 | Training_F1 | 0.600000 | True | 0.382432 | 0.571910 |
| LogisticRegression | Balanced | 3 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | RandomUnderSampler | 3 | Reference_0.50 | 0.500000 | True | 0.276529 | 0.683732 |
| LogisticRegression | RandomUnderSampler | 3 | Training_F1 | 0.600000 | True | 0.375330 | 0.574941 |
| LogisticRegression | RandomUnderSampler | 3 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | Original | 4 | Reference_0.50 | 0.500000 | True | 0.669734 | 0.220613 |
| HistGradientBoosting | Original | 4 | Training_F1 | 0.150000 | True | 0.413890 | 0.598181 |
| HistGradientBoosting | Original | 4 | Training_Precision50 | 0.350000 | True | 0.535456 | 0.373863 |
| HistGradientBoosting | Balanced | 4 | Reference_0.50 | 0.500000 | True | 0.382742 | 0.614011 |
| HistGradientBoosting | Balanced | 4 | Training_F1 | 0.600000 | True | 0.420416 | 0.585382 |
| HistGradientBoosting | Balanced | 4 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | RandomUnderSampler | 4 | Reference_0.50 | 0.500000 | True | 0.361665 | 0.623442 |
| HistGradientBoosting | RandomUnderSampler | 4 | Training_F1 | 0.600000 | True | 0.411932 | 0.586056 |
| HistGradientBoosting | RandomUnderSampler | 4 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | Original | 4 | Reference_0.50 | 0.500000 | True | 0.691463 | 0.190973 |
| LogisticRegression | Original | 4 | Training_F1 | 0.200000 | True | 0.435169 | 0.495116 |
| LogisticRegression | Original | 4 | Training_Precision50 | 0.350000 | True | 0.530295 | 0.321320 |
| LogisticRegression | Balanced | 4 | Reference_0.50 | 0.500000 | True | 0.276091 | 0.673627 |
| LogisticRegression | Balanced | 4 | Training_F1 | 0.600000 | True | 0.375940 | 0.555743 |
| LogisticRegression | Balanced | 4 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | RandomUnderSampler | 4 | Reference_0.50 | 0.500000 | True | 0.270536 | 0.676659 |
| LogisticRegression | RandomUnderSampler | 4 | Training_F1 | 0.600000 | True | 0.374162 | 0.563826 |
| LogisticRegression | RandomUnderSampler | 4 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | Original | 5 | Reference_0.50 | 0.500000 | True | 0.666667 | 0.221698 |
| HistGradientBoosting | Original | 5 | Training_F1 | 0.200000 | True | 0.427403 | 0.581199 |
| HistGradientBoosting | Original | 5 | Training_Precision50 | 0.350000 | True | 0.513242 | 0.378706 |
| HistGradientBoosting | Balanced | 5 | Reference_0.50 | 0.500000 | True | 0.368536 | 0.626685 |
| HistGradientBoosting | Balanced | 5 | Training_F1 | 0.600000 | True | 0.414576 | 0.590296 |
| HistGradientBoosting | Balanced | 5 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| HistGradientBoosting | RandomUnderSampler | 5 | Reference_0.50 | 0.500000 | True | 0.357183 | 0.635782 |
| HistGradientBoosting | RandomUnderSampler | 5 | Training_F1 | 0.600000 | True | 0.407067 | 0.597709 |
| HistGradientBoosting | RandomUnderSampler | 5 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | Original | 5 | Reference_0.50 | 0.500000 | True | 0.683313 | 0.189016 |
| LogisticRegression | Original | 5 | Training_F1 | 0.200000 | True | 0.433647 | 0.497642 |
| LogisticRegression | Original | 5 | Training_Precision50 | 0.350000 | True | 0.518753 | 0.330863 |
| LogisticRegression | Balanced | 5 | Reference_0.50 | 0.500000 | True | 0.274398 | 0.683962 |
| LogisticRegression | Balanced | 5 | Training_F1 | 0.600000 | True | 0.371647 | 0.574124 |
| LogisticRegression | Balanced | 5 | Training_Precision50 | none feasible | False | not applicable | not applicable |
| LogisticRegression | RandomUnderSampler | 5 | Reference_0.50 | 0.500000 | True | 0.265181 | 0.685647 |
| LogisticRegression | RandomUnderSampler | 5 | Training_F1 | 0.600000 | True | 0.356852 | 0.591307 |
| LogisticRegression | RandomUnderSampler | 5 | Training_Precision50 | none feasible | False | not applicable | not applicable |

| model | treatment | policy | threshold | fold_count |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | Reference_0.50 | 0.500000 | 5 |
| HistGradientBoosting | Balanced | Training_F1 | 0.600000 | 5 |
| HistGradientBoosting | Balanced | Training_Precision50 | none feasible | 5 |
| HistGradientBoosting | Original | Reference_0.50 | 0.500000 | 5 |
| HistGradientBoosting | Original | Training_F1 | 0.150000 | 1 |
| HistGradientBoosting | Original | Training_F1 | 0.200000 | 4 |
| HistGradientBoosting | Original | Training_Precision50 | 0.350000 | 5 |
| HistGradientBoosting | RandomUnderSampler | Reference_0.50 | 0.500000 | 5 |
| HistGradientBoosting | RandomUnderSampler | Training_F1 | 0.600000 | 5 |
| HistGradientBoosting | RandomUnderSampler | Training_Precision50 | none feasible | 5 |
| LogisticRegression | Balanced | Reference_0.50 | 0.500000 | 5 |
| LogisticRegression | Balanced | Training_F1 | 0.600000 | 5 |
| LogisticRegression | Balanced | Training_Precision50 | none feasible | 5 |
| LogisticRegression | Original | Reference_0.50 | 0.500000 | 5 |
| LogisticRegression | Original | Training_F1 | 0.200000 | 5 |
| LogisticRegression | Original | Training_Precision50 | 0.350000 | 5 |
| LogisticRegression | RandomUnderSampler | Reference_0.50 | 0.500000 | 5 |
| LogisticRegression | RandomUnderSampler | Training_F1 | 0.600000 | 5 |
| LogisticRegression | RandomUnderSampler | Training_Precision50 | none feasible | 5 |

| model | treatment | feasible_training_folds | outer_folds |
| --- | --- | --- | --- |
| HistGradientBoosting | Balanced | 0 | 5 |
| HistGradientBoosting | Original | 5 | 5 |
| HistGradientBoosting | RandomUnderSampler | 0 | 5 |
| LogisticRegression | Balanced | 0 | 5 |
| LogisticRegression | Original | 5 | 5 |
| LogisticRegression | RandomUnderSampler | 0 | 5 |

A training constraint does not guarantee outer precision; zero-contact abstentions are reported with precision/recall/F1=0 under zero_division=0. Treat infeasible-grid cases separately from evidence that a treatment cannot ever meet a precision goal. Resampling/weighting changes the fitted score distribution and can change which fixed threshold is appropriate. It does not automatically improve the ranking objective.

## Business targeting at identical capacities

All ranks use nested outer-validation probabilities, never in-sample refit scores. Top 5/10/20% capacities are fixed in advance. K=ceil(fraction*N); descending score with saved-row-position ties independent of outcomes. Precision@K=captured/K; Recall@K=captured/actual positives; Lift@K=precision/cohort prevalence. Every model/treatment uses identical K for a given cohort. capture_minus_original_HGB is the additional historical subscribers versus the original HGB at the same pooled K, not a causal effect.

| model | treatment | fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K | capture_minus_original_HGB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | 0.050000 | 1647 | 1005 | 0.610200 | 0.270816 | 5.416330 | 0 |
| HistGradientBoosting | Original | 0.100000 | 3294 | 1628 | 0.494232 | 0.438696 | 4.386958 | 0 |
| HistGradientBoosting | Original | 0.200000 | 6588 | 2377 | 0.360808 | 0.640528 | 3.202641 | 0 |
| HistGradientBoosting | Balanced | 0.050000 | 1647 | 1018 | 0.618094 | 0.274320 | 5.486392 | 13 |
| HistGradientBoosting | Balanced | 0.100000 | 3294 | 1610 | 0.488767 | 0.433845 | 4.338453 | -18 |
| HistGradientBoosting | Balanced | 0.200000 | 6588 | 2371 | 0.359897 | 0.638911 | 3.194557 | -6 |
| HistGradientBoosting | RandomUnderSampler | 0.050000 | 1647 | 988 | 0.599879 | 0.266236 | 5.324710 | -17 |
| HistGradientBoosting | RandomUnderSampler | 0.100000 | 3294 | 1578 | 0.479053 | 0.425222 | 4.252223 | -50 |
| HistGradientBoosting | RandomUnderSampler | 0.200000 | 6588 | 2348 | 0.356406 | 0.632714 | 3.163568 | -29 |
| LogisticRegression | Original | 0.050000 | 1647 | 962 | 0.584092 | 0.259229 | 5.184586 | -43 |
| LogisticRegression | Original | 0.100000 | 3294 | 1564 | 0.474803 | 0.421450 | 4.214497 | -64 |
| LogisticRegression | Original | 0.200000 | 6588 | 2257 | 0.342593 | 0.608192 | 3.040959 | -120 |
| LogisticRegression | Balanced | 0.050000 | 1647 | 952 | 0.578021 | 0.256535 | 5.130693 | -53 |
| LogisticRegression | Balanced | 0.100000 | 3294 | 1552 | 0.471160 | 0.418216 | 4.182161 | -76 |
| LogisticRegression | Balanced | 0.200000 | 6588 | 2267 | 0.344111 | 0.610887 | 3.054433 | -110 |
| LogisticRegression | RandomUnderSampler | 0.050000 | 1647 | 960 | 0.582878 | 0.258690 | 5.173808 | -45 |
| LogisticRegression | RandomUnderSampler | 0.100000 | 3294 | 1553 | 0.471463 | 0.418486 | 4.184856 | -75 |
| LogisticRegression | RandomUnderSampler | 0.200000 | 6588 | 2250 | 0.341530 | 0.606306 | 3.031528 | -127 |

Fold-local mean/sample SD (less sensitive to cross-model probability calibration shifts across outer folds):

| model | treatment | fraction | captured_mean | captured_SD | Precision_mean | Precision_SD | Recall_mean | Recall_SD | Lift_mean | Lift_SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | 0.050000 | 205.000000 | 2.738613 | 0.621212 | 0.008299 | 0.276205 | 0.003626 | 5.514061 | 0.072379 |
| HistGradientBoosting | Balanced | 0.100000 | 322.000000 | 11.510864 | 0.488619 | 0.017467 | 0.433844 | 0.015464 | 4.337123 | 0.154594 |
| HistGradientBoosting | Balanced | 0.200000 | 474.200000 | 10.917875 | 0.359788 | 0.008284 | 0.638912 | 0.014743 | 3.193590 | 0.073691 |
| HistGradientBoosting | Original | 0.050000 | 202.000000 | 2.000000 | 0.612121 | 0.006061 | 0.272164 | 0.002745 | 5.433389 | 0.054809 |
| HistGradientBoosting | Original | 0.100000 | 325.400000 | 6.503845 | 0.493778 | 0.009869 | 0.438425 | 0.008686 | 4.382921 | 0.086838 |
| HistGradientBoosting | Original | 0.200000 | 474.200000 | 14.272351 | 0.359788 | 0.010829 | 0.638912 | 0.019242 | 3.193588 | 0.096180 |
| HistGradientBoosting | RandomUnderSampler | 0.050000 | 197.400000 | 7.602631 | 0.598182 | 0.023038 | 0.265964 | 0.010192 | 5.309618 | 0.203467 |
| HistGradientBoosting | RandomUnderSampler | 0.100000 | 317.200000 | 16.991174 | 0.481335 | 0.025783 | 0.427374 | 0.022788 | 4.272438 | 0.227808 |
| HistGradientBoosting | RandomUnderSampler | 0.200000 | 469.400000 | 12.033287 | 0.356146 | 0.009130 | 0.632444 | 0.016229 | 3.161262 | 0.081120 |
| LogisticRegression | Balanced | 0.050000 | 192.400000 | 10.597169 | 0.583030 | 0.032113 | 0.259226 | 0.014200 | 5.175092 | 0.283476 |
| LogisticRegression | Balanced | 0.100000 | 312.000000 | 5.958188 | 0.473445 | 0.009041 | 0.420369 | 0.007837 | 4.202415 | 0.078346 |
| LogisticRegression | Balanced | 0.200000 | 453.200000 | 15.417522 | 0.343854 | 0.011698 | 0.610616 | 0.020717 | 3.052151 | 0.103553 |
| LogisticRegression | Original | 0.050000 | 192.600000 | 8.384510 | 0.583636 | 0.025408 | 0.259496 | 0.011221 | 5.180487 | 0.224006 |
| LogisticRegression | Original | 0.100000 | 314.000000 | 5.000000 | 0.476480 | 0.007587 | 0.423066 | 0.006657 | 4.229372 | 0.066547 |
| LogisticRegression | Original | 0.200000 | 451.200000 | 14.754660 | 0.342337 | 0.011195 | 0.607920 | 0.019807 | 3.038680 | 0.099004 |
| LogisticRegression | RandomUnderSampler | 0.050000 | 192.600000 | 8.561542 | 0.583636 | 0.025944 | 0.259496 | 0.011450 | 5.180480 | 0.228581 |
| LogisticRegression | RandomUnderSampler | 0.100000 | 311.000000 | 3.937004 | 0.471927 | 0.005974 | 0.419024 | 0.005203 | 4.188964 | 0.052010 |
| LogisticRegression | RandomUnderSampler | 0.200000 | 449.600000 | 14.135063 | 0.341123 | 0.010725 | 0.605765 | 0.018975 | 3.027905 | 0.094844 |

Pooled scores combine five separately fitted models with potentially different calibration and overlapping training sets. Ceil rounding changes summed fold-local capacities slightly versus pooled. No call costs, incremental revenue, causal outreach response or actual bank budget is known; no financial optimum follows.

## Sampler audit and computational evidence

| model | treatment | role | rows | fits |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | inner search | 21081 | 160 |
| HistGradientBoosting | Balanced | inner search | 21082 | 240 |
| HistGradientBoosting | Balanced | outer-training refit | 26352 | 5 |
| HistGradientBoosting | Balanced | training-side OOF fit | 21081 | 10 |
| HistGradientBoosting | Balanced | training-side OOF fit | 21082 | 15 |
| HistGradientBoosting | Original | outer-training refit | 26352 | 5 |
| HistGradientBoosting | Original | training-side OOF fit | 21081 | 10 |
| HistGradientBoosting | Original | training-side OOF fit | 21082 | 15 |
| HistGradientBoosting | RandomUnderSampler | inner search | 21081 | 160 |
| HistGradientBoosting | RandomUnderSampler | inner search | 21082 | 240 |
| HistGradientBoosting | RandomUnderSampler | outer-training refit | 26352 | 5 |
| HistGradientBoosting | RandomUnderSampler | training-side OOF fit | 21081 | 10 |
| HistGradientBoosting | RandomUnderSampler | training-side OOF fit | 21082 | 15 |
| LogisticRegression | Balanced | inner search | 21081 | 30 |
| LogisticRegression | Balanced | inner search | 21082 | 45 |
| LogisticRegression | Balanced | outer-training refit | 26352 | 5 |
| LogisticRegression | Balanced | training-side OOF fit | 21081 | 10 |
| LogisticRegression | Balanced | training-side OOF fit | 21082 | 15 |
| LogisticRegression | Original | outer-training refit | 26352 | 5 |
| LogisticRegression | Original | training-side OOF fit | 21081 | 10 |
| LogisticRegression | Original | training-side OOF fit | 21082 | 15 |
| LogisticRegression | RandomUnderSampler | inner search | 21081 | 30 |
| LogisticRegression | RandomUnderSampler | inner search | 21082 | 45 |
| LogisticRegression | RandomUnderSampler | outer-training refit | 26352 | 5 |
| LogisticRegression | RandomUnderSampler | training-side OOF fit | 21081 | 10 |
| LogisticRegression | RandomUnderSampler | training-side OOF fit | 21082 | 15 |

Training-only sampling counts, min/max across fitting calls with the same group:

| model | outer_fold | role | before_rows_min | before_rows_max | after_rows_min | after_rows_max | before_no_min | before_no_max | before_yes_min | before_yes_max | after_no_min | after_no_max | after_yes_min | after_yes_max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 1 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| HistGradientBoosting | 1 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 2 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 2 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| HistGradientBoosting | 2 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 3 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 3 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| HistGradientBoosting | 3 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 4 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 4 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| HistGradientBoosting | 4 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| HistGradientBoosting | 5 | inner search | 21081 | 21082 | 4748 | 4750 | 18707 | 18708 | 2374 | 2375 | 2374 | 2375 | 2374 | 2375 |
| HistGradientBoosting | 5 | outer-training refit | 26352 | 26352 | 5936 | 5936 | 23384 | 23384 | 2968 | 2968 | 2968 | 2968 | 2968 | 2968 |
| HistGradientBoosting | 5 | training-side OOF fit | 21081 | 21082 | 4748 | 4750 | 18707 | 18708 | 2374 | 2375 | 2374 | 2375 | 2374 | 2375 |
| LogisticRegression | 1 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 1 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| LogisticRegression | 1 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 2 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 2 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| LogisticRegression | 2 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 3 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 3 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| LogisticRegression | 3 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 4 | inner search | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 4 | outer-training refit | 26352 | 26352 | 5938 | 5938 | 23383 | 23383 | 2969 | 2969 | 2969 | 2969 | 2969 | 2969 |
| LogisticRegression | 4 | training-side OOF fit | 21081 | 21082 | 4750 | 4752 | 18706 | 18707 | 2375 | 2376 | 2375 | 2376 | 2375 | 2376 |
| LogisticRegression | 5 | inner search | 21081 | 21082 | 4748 | 4750 | 18707 | 18708 | 2374 | 2375 | 2374 | 2375 | 2374 | 2375 |
| LogisticRegression | 5 | outer-training refit | 26352 | 26352 | 5936 | 5936 | 23384 | 23384 | 2968 | 2968 | 2968 | 2968 | 2968 | 2968 |
| LogisticRegression | 5 | training-side OOF fit | 21081 | 21082 | 4748 | 4750 | 18707 | 18708 | 2374 | 2375 | 2374 | 2375 | 2374 | 2375 |

| model | treatment | outer_fold | candidates_in_selection_budget | new_inner_search_fits | threshold_OOF_fits | outer_refits | grid_refit_seconds | total_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Original | 1 | 16 | 0 | 5 | 1 | 0.000000 | 4.342511 |
| HistGradientBoosting | Balanced | 1 | 16 | 80 | 5 | 1 | 78.597506 | 82.428790 |
| HistGradientBoosting | RandomUnderSampler | 1 | 16 | 80 | 5 | 1 | 34.917950 | 36.553110 |
| LogisticRegression | Original | 1 | 3 | 0 | 5 | 1 | 0.000000 | 0.906294 |
| LogisticRegression | Balanced | 1 | 3 | 15 | 5 | 1 | 1.888160 | 2.643690 |
| LogisticRegression | RandomUnderSampler | 1 | 3 | 15 | 5 | 1 | 1.317709 | 1.932755 |
| HistGradientBoosting | Original | 2 | 16 | 0 | 5 | 1 | 0.000000 | 4.362590 |
| HistGradientBoosting | Balanced | 2 | 16 | 80 | 5 | 1 | 78.355206 | 82.060617 |
| HistGradientBoosting | RandomUnderSampler | 2 | 16 | 80 | 5 | 1 | 34.535839 | 36.232561 |
| LogisticRegression | Original | 2 | 3 | 0 | 5 | 1 | 0.000000 | 0.859213 |
| LogisticRegression | Balanced | 2 | 3 | 15 | 5 | 1 | 1.991152 | 2.737412 |
| LogisticRegression | RandomUnderSampler | 2 | 3 | 15 | 5 | 1 | 1.338894 | 1.929341 |
| HistGradientBoosting | Original | 3 | 16 | 0 | 5 | 1 | 0.000000 | 4.222468 |
| HistGradientBoosting | Balanced | 3 | 16 | 80 | 5 | 1 | 83.688826 | 87.387070 |
| HistGradientBoosting | RandomUnderSampler | 3 | 16 | 80 | 5 | 1 | 33.543505 | 35.396521 |
| LogisticRegression | Original | 3 | 3 | 0 | 5 | 1 | 0.000000 | 0.806803 |
| LogisticRegression | Balanced | 3 | 3 | 15 | 5 | 1 | 1.912774 | 2.750068 |
| LogisticRegression | RandomUnderSampler | 3 | 3 | 15 | 5 | 1 | 1.485363 | 2.239503 |
| HistGradientBoosting | Original | 4 | 16 | 0 | 5 | 1 | 0.000000 | 4.160662 |
| HistGradientBoosting | Balanced | 4 | 16 | 80 | 5 | 1 | 79.483163 | 82.967560 |
| HistGradientBoosting | RandomUnderSampler | 4 | 16 | 80 | 5 | 1 | 34.046622 | 35.824738 |
| LogisticRegression | Original | 4 | 3 | 0 | 5 | 1 | 0.000000 | 0.965294 |
| LogisticRegression | Balanced | 4 | 3 | 15 | 5 | 1 | 1.855901 | 2.633856 |
| LogisticRegression | RandomUnderSampler | 4 | 3 | 15 | 5 | 1 | 1.399056 | 2.030858 |
| HistGradientBoosting | Original | 5 | 16 | 0 | 5 | 1 | 0.000000 | 4.337631 |
| HistGradientBoosting | Balanced | 5 | 16 | 80 | 5 | 1 | 81.915672 | 85.604136 |
| HistGradientBoosting | RandomUnderSampler | 5 | 16 | 80 | 5 | 1 | 34.164066 | 35.903923 |
| LogisticRegression | Original | 5 | 3 | 0 | 5 | 1 | 0.000000 | 0.857962 |
| LogisticRegression | Balanced | 5 | 3 | 15 | 5 | 1 | 1.896236 | 2.702499 |
| LogisticRegression | RandomUnderSampler | 5 | 3 | 15 | 5 | 1 | 1.392127 | 2.014995 |

| model | treatment | selection_candidates | new_inner_search_fits | threshold_OOF_fits | outer_refits | wall_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Balanced | 16 | 400 | 25 | 5 | 420.448172 |
| HistGradientBoosting | Original | 16 | 0 | 25 | 5 | 21.425863 |
| HistGradientBoosting | RandomUnderSampler | 16 | 400 | 25 | 5 | 179.910852 |
| LogisticRegression | Balanced | 3 | 75 | 25 | 5 | 13.467524 |
| LogisticRegression | Original | 3 | 0 | 25 | 5 | 4.395567 |
| LogisticRegression | RandomUnderSampler | 3 | 75 | 25 | 5 | 10.147452 |

Elapsed through experiments/plots 652.33s. Versions: sklearn 1.8.0, imbalanced-learn 0.14.2, pandas 2.2.3, NumPy 2.3.5. Native threads limited to one; RF is not searched. Runtime includes audit/threshold selection; saved baseline selections make its current cost lower without reducing its original selection budget. Hosted Colab was not directly exercised.

## Technical validation

All 1,130 fresh fitting pipelines and corresponding prediction calls passed; all 535 sampler calls were fitting-only. Fit indices match current inner/OOF training partitions or the selected outer-training refit, disjoint from outer validation and held-out indices. Every prediction is disjoint from its estimator's fitting rows and must match the authorized training-side/outer cohort. Entire development fitting is impossible under allowed partition keys. OneHotEncoder vocabulary equals raw fitting-row levels; LR mean/variance/scale/sample count equals fitting data before sampling; ConditionalRecencyScaler only uses available fitting observations, placeholder standardized values remain zero and availability stays unscaled. HGB numeric/recency values exactly match validation input and 999 never appears. Finite matrices/probabilities/metrics, class mapping [0,1], unchanged fitted state on predict, no validation resampling, unchanged datasets/split/preprocessing and old results were asserted. Threshold selection determinism/no-feasible fallback is tested; original baseline replication provides an additional compatibility check. Existing preprocessing unit tests are run separately.

Warnings/errors during model experiments:

None recorded across all 1,130 current-phase fits.

## Is imbalance treatment worth retaining? Provisional Phase 6 discussion

Use nested AP/ROC and equal-capacity capture to judge ranking improvements, distinct from recall increases caused only by moving probability thresholds. Compare every treatment against the already-evaluated unweighted F1/precision policies, not just .50. A weighted/resampled .50 rule may approximate a lower threshold without increasing AP or subscriber capture. High recall alone, or a best point on these outer plots, is not a policy-selection justification. Do not assume complex imbalance treatment must help. Current AP ordering is HistGradientBoosting / Balanced, HistGradientBoosting / Original, HistGradientBoosting / RandomUnderSampler, LogisticRegression / Original, LogisticRegression / Balanced, LogisticRegression / RandomUnderSampler; statistical significance was not tested.

Retain original HGB and LR as references; any treatment shortlist must be justified by the actual ranking/capture trade-offs and selection uncertainty in these tables, not default preference for balance. No final deployment policy or feature ablation is chosen. Prior whole-development model/grid/shortlist exploration and family selection on outer means remain limitations despite correct within-experiment nesting.

Optional SMOTENC is **deferred, not implemented**. A defensible mixed-type design would resample training-only numerical and categorical representations before final one-hot encoding, mark categorical fields (including the binary availability flag), learn any distance-related scaling only within fitting folds, and preserve recency-availability consistency and legitimate count domains in synthetic records. Vanilla mixed-type interpolation can still create nonzero unavailable recency or fractional counts; extra constraints/validation and approval are needed. Ordinary SMOTE on the full one-hot matrix is not an acceptable substitute. No synthetic records or new encoding strategy were introduced.

All 15 predictors remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Confirm campaign-start customer/status snapshots, historical contact/recency cutoff/reference date, economic publication/revision vintages and target window. Missing customer IDs/timestamps allow repeated-client/temporal overlap; prior full-data EDA also limits claims. Preprocessing/sampling isolation does not eliminate feature-timing leakage or certify future-campaign/unseen-client generalization.

Team decisions for Phase 6: which model/treatment and decision-objective candidates to retain; whether a wider predeclared threshold range or calibration is justified (not changed here); bank capacity, illustrative precision target and error/benefit assumptions; uncertainty analysis; and acceptable timing/client validation evidence. No final feature ablation, held-out evaluation, Phase 6, commit or push occurred.

Deliverables: executed 08_imbalance_treatment.ipynb and this 08_imbalance_treatment_summary.md in the repository. Stop pending review.
