# Phase 5B-1 — Threshold and business decision-policy analysis

## Scope, latest-main provenance and economical reuse

Started from latest fetched main **8587eb4**, including merged Phase 5A; local branch fast-forwarded without creating a commit. Reviewed preprocessing.py, cleaned data/saved split, Phase 3/4/4B summaries and Phase 5A notebook/summary. No prior artifacts are modified.

Phase 5A persisted neither fitted estimators nor row-level probability artifacts. It did persist each outer fold's hyperparameters, selected by inner five-fold AP on outer-training data only. We verified its executed code uses search.fit(outer_X,outer_y), records search.best_params_, and uses the same fold recipe. Those approved parameter decisions are reused exactly; every saved value belongs to the exact approved Phase 5A grids. No final parameters are selected from outer outcomes. Repeating the same grids is unnecessary, so only the selected pipelines are regenerated: **50 training-side OOF fits and 10 outer-training refits = 60 fits**, versus 535 fits if the LR/HGB grids were repeated. RF is imported as a historical comparison, not rerun.

The 0.50 outer-fold scores reproduced all six Phase 5A metrics at their published six-decimal precision; pooled Top-K counts/metrics also reproduced Phase 5A. This consistency check validates regeneration and does not change parameters based on outer scores.

## Data integrity and leakage boundaries

Cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49` matched saved split before applying positions, binding row ordering and values. Saved development=32,940, held-out=8,236; positions verified unique/disjoint/exhaustive. Only development CSV rows were parsed. Outer StratifiedKFold(5,shuffle=True,random_state=42), checksum `6016ca88c4c344724075ade804828d47f03a69bf7337f5287cee0f4a444457c4`, matches Phase 5A. No new train-test split. Original CSV if present was only byte-hashed, not parsed for modeling.

Inside each outer-training partition, we regenerated selected-model OOF probabilities using five training-side folds (same inner configuration). Each prediction excludes its own row from fitting; preprocessing is fresh per fit. Hyperparameters were selected previously using all of that outer-training partition, including training-side OOF labels during earlier inner scoring. Thus these probabilities are cross-fitted conditional on training-selected hyperparameters, **not an unbiased inner performance estimate**. They are used solely to fit the threshold, never as final evaluation. Outer-validation labels influence neither hyperparameters nor thresholds. Both threshold policies are frozen before outer predictions and label evaluation. The outer layer evaluates the complete reused-HP-selection-plus-threshold procedure; prior development exploration and shortlist choice remain limitations.

LR reuses approved one-hot, ordinary StandardScaler and available-only ConditionalRecencyScaler unchanged. HGB reuses unscaled tree one-hot/numerical factory, categorical_features=None, early_stopping=False. All seeds=42, weights=None. Numeric guards do not transform values. No whole-development preprocessing, resampling, feature selection, new model family or RF search. Threshold rule is probability >=t, consistent with prior >=0.50 convention.

## Predeclared threshold objectives and rules

Grid: [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]; 0.50 retained unchanged. F1 policy maximizes training-side OOF F1, exact ties choose the highest threshold. Precision-constrained policy maximizes recall among thresholds with positive contact volume and empirical training-side precision >=50%; ties choose higher precision, then higher threshold. The **50% target is an illustrative research assumption, not a bank policy or guaranteed future precision**.

If no candidate is feasible, record none feasible and abstain (zero contacts) on that outer cohort; precision is reported with zero_division=0, not as satisfying the constraint. Synthetic tests verified this branch and deterministic tie-breaking. In all cases outer precision can fall below the training target; report actual validation behavior rather than silently retuning. Repeating selector calls on identical training-side predictions reproduced thresholds.

## Selected thresholds and stability — training-side decisions only

| model | outer_fold | policy | threshold | training_feasible | training_OOF_precision | training_OOF_recall | best_parameters |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | Reference_0.50 | 0.500000 | True | 0.660063 | 0.213203 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 1 | Training_F1 | 0.200000 | True | 0.429076 | 0.572583 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 1 | Training_Precision50 | 0.350000 | True | 0.527404 | 0.369485 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| LogisticRegression | 1 | Reference_0.50 | 0.500000 | True | 0.682209 | 0.187268 | {"classifier__C": 0.1} |
| LogisticRegression | 1 | Training_F1 | 0.200000 | True | 0.435503 | 0.495790 | {"classifier__C": 0.1} |
| LogisticRegression | 1 | Training_Precision50 | 0.350000 | True | 0.524769 | 0.324688 | {"classifier__C": 0.1} |
| HistGradientBoosting | 2 | Reference_0.50 | 0.500000 | True | 0.675761 | 0.216908 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 2 | Training_F1 | 0.200000 | True | 0.430380 | 0.584035 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 2 | Training_Precision50 | 0.350000 | True | 0.519059 | 0.371506 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| LogisticRegression | 2 | Reference_0.50 | 0.500000 | True | 0.674883 | 0.193668 | {"classifier__C": 0.1} |
| LogisticRegression | 2 | Training_F1 | 0.200000 | True | 0.432063 | 0.500168 | {"classifier__C": 0.1} |
| LogisticRegression | 2 | Training_Precision50 | 0.350000 | True | 0.536353 | 0.323004 | {"classifier__C": 0.1} |
| HistGradientBoosting | 3 | Reference_0.50 | 0.500000 | True | 0.657603 | 0.219939 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 3 | Training_F1 | 0.200000 | True | 0.436168 | 0.585719 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 3 | Training_Precision50 | 0.350000 | True | 0.517148 | 0.385989 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| LogisticRegression | 3 | Reference_0.50 | 0.500000 | True | 0.683180 | 0.199731 | {"classifier__C": 0.1} |
| LogisticRegression | 3 | Training_F1 | 0.200000 | True | 0.442967 | 0.504884 | {"classifier__C": 0.1} |
| LogisticRegression | 3 | Training_Precision50 | 0.350000 | True | 0.536278 | 0.343550 | {"classifier__C": 0.1} |
| HistGradientBoosting | 4 | Reference_0.50 | 0.500000 | True | 0.669734 | 0.220613 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 4 | Training_F1 | 0.150000 | True | 0.413890 | 0.598181 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 4 | Training_Precision50 | 0.350000 | True | 0.535456 | 0.373863 | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| LogisticRegression | 4 | Reference_0.50 | 0.500000 | True | 0.691463 | 0.190973 | {"classifier__C": 0.1} |
| LogisticRegression | 4 | Training_F1 | 0.200000 | True | 0.435169 | 0.495116 | {"classifier__C": 0.1} |
| LogisticRegression | 4 | Training_Precision50 | 0.350000 | True | 0.530295 | 0.321320 | {"classifier__C": 0.1} |
| HistGradientBoosting | 5 | Reference_0.50 | 0.500000 | True | 0.666667 | 0.221698 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 5 | Training_F1 | 0.200000 | True | 0.427403 | 0.581199 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| HistGradientBoosting | 5 | Training_Precision50 | 0.350000 | True | 0.513242 | 0.378706 | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} |
| LogisticRegression | 5 | Reference_0.50 | 0.500000 | True | 0.683313 | 0.189016 | {"classifier__C": 0.1} |
| LogisticRegression | 5 | Training_F1 | 0.200000 | True | 0.433647 | 0.497642 | {"classifier__C": 0.1} |
| LogisticRegression | 5 | Training_Precision50 | 0.350000 | True | 0.518753 | 0.330863 | {"classifier__C": 0.1} |

Training_OOF_precision/recall here are threshold-fitting diagnostics, not unbiased evaluation.

| model | policy | threshold | fold_count |
| --- | --- | --- | --- |
| HistGradientBoosting | Reference_0.50 | 0.500000 | 5 |
| HistGradientBoosting | Training_F1 | 0.150000 | 1 |
| HistGradientBoosting | Training_F1 | 0.200000 | 4 |
| HistGradientBoosting | Training_Precision50 | 0.350000 | 5 |
| LogisticRegression | Reference_0.50 | 0.500000 | 5 |
| LogisticRegression | Training_F1 | 0.200000 | 5 |
| LogisticRegression | Training_Precision50 | 0.350000 | 5 |

All training-side candidate threshold scores (for audit, not independent performance):

| model | outer_fold | threshold | Precision | Recall | F1 | predicted_positives |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | 0.100000 | 0.342072 | 0.641630 | 0.446240 | 5569 |
| HistGradientBoosting | 1 | 0.150000 | 0.411627 | 0.591445 | 0.485418 | 4266 |
| HistGradientBoosting | 1 | 0.200000 | 0.429076 | 0.572583 | 0.490550 | 3962 |
| HistGradientBoosting | 1 | 0.250000 | 0.440173 | 0.547659 | 0.488068 | 3694 |
| HistGradientBoosting | 1 | 0.300000 | 0.476485 | 0.467497 | 0.471948 | 2913 |
| HistGradientBoosting | 1 | 0.350000 | 0.527404 | 0.369485 | 0.434541 | 2080 |
| HistGradientBoosting | 1 | 0.400000 | 0.579051 | 0.296059 | 0.391799 | 1518 |
| HistGradientBoosting | 1 | 0.450000 | 0.629505 | 0.252947 | 0.360884 | 1193 |
| HistGradientBoosting | 1 | 0.500000 | 0.660063 | 0.213203 | 0.322301 | 959 |
| HistGradientBoosting | 1 | 0.550000 | 0.683887 | 0.187268 | 0.294024 | 813 |
| HistGradientBoosting | 1 | 0.600000 | 0.705146 | 0.170765 | 0.274946 | 719 |
| LogisticRegression | 1 | 0.100000 | 0.258085 | 0.688110 | 0.375379 | 7916 |
| LogisticRegression | 1 | 0.150000 | 0.353609 | 0.587403 | 0.441463 | 4932 |
| LogisticRegression | 1 | 0.200000 | 0.435503 | 0.495790 | 0.463695 | 3380 |
| LogisticRegression | 1 | 0.250000 | 0.463947 | 0.444257 | 0.453889 | 2843 |
| LogisticRegression | 1 | 0.300000 | 0.492940 | 0.388009 | 0.434225 | 2337 |
| LogisticRegression | 1 | 0.350000 | 0.524769 | 0.324688 | 0.401165 | 1837 |
| LogisticRegression | 1 | 0.400000 | 0.574721 | 0.260357 | 0.358368 | 1345 |
| LogisticRegression | 1 | 0.450000 | 0.634653 | 0.215898 | 0.322192 | 1010 |
| LogisticRegression | 1 | 0.500000 | 0.682209 | 0.187268 | 0.293869 | 815 |
| LogisticRegression | 1 | 0.550000 | 0.708628 | 0.168744 | 0.272579 | 707 |
| LogisticRegression | 1 | 0.600000 | 0.719436 | 0.154598 | 0.254505 | 638 |
| HistGradientBoosting | 2 | 0.100000 | 0.343994 | 0.652071 | 0.450390 | 5628 |
| HistGradientBoosting | 2 | 0.150000 | 0.416901 | 0.599865 | 0.491921 | 4272 |
| HistGradientBoosting | 2 | 0.200000 | 0.430380 | 0.584035 | 0.495570 | 4029 |
| HistGradientBoosting | 2 | 0.250000 | 0.435965 | 0.556079 | 0.488751 | 3787 |
| HistGradientBoosting | 2 | 0.300000 | 0.464081 | 0.491748 | 0.477514 | 3146 |
| HistGradientBoosting | 2 | 0.350000 | 0.519059 | 0.371506 | 0.433059 | 2125 |
| HistGradientBoosting | 2 | 0.400000 | 0.589980 | 0.301448 | 0.399019 | 1517 |
| HistGradientBoosting | 2 | 0.450000 | 0.638119 | 0.255978 | 0.365385 | 1191 |
| HistGradientBoosting | 2 | 0.500000 | 0.675761 | 0.216908 | 0.328404 | 953 |
| HistGradientBoosting | 2 | 0.550000 | 0.695396 | 0.198383 | 0.308700 | 847 |
| HistGradientBoosting | 2 | 0.600000 | 0.701473 | 0.176490 | 0.282024 | 747 |
| LogisticRegression | 2 | 0.100000 | 0.259171 | 0.697204 | 0.377875 | 7987 |
| LogisticRegression | 2 | 0.150000 | 0.352188 | 0.601886 | 0.444362 | 5074 |
| LogisticRegression | 2 | 0.200000 | 0.432063 | 0.500168 | 0.463628 | 3437 |
| LogisticRegression | 2 | 0.250000 | 0.459327 | 0.441226 | 0.450094 | 2852 |
| LogisticRegression | 2 | 0.300000 | 0.498700 | 0.387673 | 0.436233 | 2308 |
| LogisticRegression | 2 | 0.350000 | 0.536353 | 0.323004 | 0.403195 | 1788 |
| LogisticRegression | 2 | 0.400000 | 0.590594 | 0.257999 | 0.359119 | 1297 |
| LogisticRegression | 2 | 0.450000 | 0.645472 | 0.225665 | 0.334415 | 1038 |
| LogisticRegression | 2 | 0.500000 | 0.674883 | 0.193668 | 0.300968 | 852 |
| LogisticRegression | 2 | 0.550000 | 0.703605 | 0.177501 | 0.283486 | 749 |
| LogisticRegression | 2 | 0.600000 | 0.706505 | 0.157292 | 0.257300 | 661 |
| HistGradientBoosting | 3 | 0.100000 | 0.346465 | 0.648703 | 0.451689 | 5559 |
| HistGradientBoosting | 3 | 0.150000 | 0.421596 | 0.604917 | 0.496888 | 4260 |
| HistGradientBoosting | 3 | 0.200000 | 0.436168 | 0.585719 | 0.500000 | 3987 |
| HistGradientBoosting | 3 | 0.250000 | 0.443460 | 0.556079 | 0.493425 | 3723 |
| HistGradientBoosting | 3 | 0.300000 | 0.468246 | 0.499158 | 0.483208 | 3165 |
| HistGradientBoosting | 3 | 0.350000 | 0.517148 | 0.385989 | 0.442044 | 2216 |
| HistGradientBoosting | 3 | 0.400000 | 0.579146 | 0.310542 | 0.404297 | 1592 |
| HistGradientBoosting | 3 | 0.450000 | 0.629934 | 0.257999 | 0.366069 | 1216 |
| HistGradientBoosting | 3 | 0.500000 | 0.657603 | 0.219939 | 0.329631 | 993 |
| HistGradientBoosting | 3 | 0.550000 | 0.679724 | 0.198720 | 0.307532 | 868 |
| HistGradientBoosting | 3 | 0.600000 | 0.697051 | 0.175143 | 0.279946 | 746 |
| LogisticRegression | 3 | 0.100000 | 0.261143 | 0.698552 | 0.380167 | 7942 |
| LogisticRegression | 3 | 0.150000 | 0.354390 | 0.600876 | 0.445833 | 5034 |
| LogisticRegression | 3 | 0.200000 | 0.442967 | 0.504884 | 0.471903 | 3384 |
| LogisticRegression | 3 | 0.250000 | 0.466298 | 0.454362 | 0.460252 | 2893 |
| LogisticRegression | 3 | 0.300000 | 0.498092 | 0.395756 | 0.441066 | 2359 |
| LogisticRegression | 3 | 0.350000 | 0.536278 | 0.343550 | 0.418805 | 1902 |
| LogisticRegression | 3 | 0.400000 | 0.577495 | 0.274840 | 0.372433 | 1413 |
| LogisticRegression | 3 | 0.450000 | 0.632163 | 0.230381 | 0.337694 | 1082 |
| LogisticRegression | 3 | 0.500000 | 0.683180 | 0.199731 | 0.309096 | 868 |
| LogisticRegression | 3 | 0.550000 | 0.701102 | 0.171438 | 0.275507 | 726 |
| LogisticRegression | 3 | 0.600000 | 0.716952 | 0.155271 | 0.255260 | 643 |
| HistGradientBoosting | 4 | 0.100000 | 0.338241 | 0.642304 | 0.443128 | 5638 |
| HistGradientBoosting | 4 | 0.150000 | 0.413890 | 0.598181 | 0.489256 | 4291 |
| HistGradientBoosting | 4 | 0.200000 | 0.426496 | 0.573594 | 0.489227 | 3993 |
| HistGradientBoosting | 4 | 0.250000 | 0.440898 | 0.549006 | 0.489049 | 3697 |
| HistGradientBoosting | 4 | 0.300000 | 0.473826 | 0.475581 | 0.474702 | 2980 |
| HistGradientBoosting | 4 | 0.350000 | 0.535456 | 0.373863 | 0.440301 | 2073 |
| HistGradientBoosting | 4 | 0.400000 | 0.595904 | 0.294038 | 0.393775 | 1465 |
| HistGradientBoosting | 4 | 0.450000 | 0.642298 | 0.248569 | 0.358426 | 1149 |
| HistGradientBoosting | 4 | 0.500000 | 0.669734 | 0.220613 | 0.331898 | 978 |
| HistGradientBoosting | 4 | 0.550000 | 0.692671 | 0.197373 | 0.307208 | 846 |
| HistGradientBoosting | 4 | 0.600000 | 0.699104 | 0.183900 | 0.291200 | 781 |
| LogisticRegression | 4 | 0.100000 | 0.256655 | 0.688447 | 0.373914 | 7964 |
| LogisticRegression | 4 | 0.150000 | 0.353824 | 0.587403 | 0.441631 | 4929 |
| LogisticRegression | 4 | 0.200000 | 0.435169 | 0.495116 | 0.463211 | 3378 |
| LogisticRegression | 4 | 0.250000 | 0.458861 | 0.439542 | 0.448994 | 2844 |
| LogisticRegression | 4 | 0.300000 | 0.493339 | 0.386662 | 0.433535 | 2327 |
| LogisticRegression | 4 | 0.350000 | 0.530295 | 0.321320 | 0.400168 | 1799 |
| LogisticRegression | 4 | 0.400000 | 0.580425 | 0.257663 | 0.356893 | 1318 |
| LogisticRegression | 4 | 0.450000 | 0.648111 | 0.219603 | 0.328050 | 1006 |
| LogisticRegression | 4 | 0.500000 | 0.691463 | 0.190973 | 0.299287 | 820 |
| LogisticRegression | 4 | 0.550000 | 0.705234 | 0.172449 | 0.277131 | 726 |
| LogisticRegression | 4 | 0.600000 | 0.713396 | 0.154261 | 0.253669 | 642 |
| HistGradientBoosting | 5 | 0.100000 | 0.337927 | 0.652628 | 0.445287 | 5732 |
| HistGradientBoosting | 5 | 0.150000 | 0.405161 | 0.603100 | 0.484701 | 4418 |
| HistGradientBoosting | 5 | 0.200000 | 0.427403 | 0.581199 | 0.492576 | 4036 |
| HistGradientBoosting | 5 | 0.250000 | 0.437720 | 0.543464 | 0.484894 | 3685 |
| HistGradientBoosting | 5 | 0.300000 | 0.467216 | 0.477763 | 0.472430 | 3035 |
| HistGradientBoosting | 5 | 0.350000 | 0.513242 | 0.378706 | 0.435828 | 2190 |
| HistGradientBoosting | 5 | 0.400000 | 0.583333 | 0.294811 | 0.391674 | 1500 |
| HistGradientBoosting | 5 | 0.450000 | 0.631535 | 0.252358 | 0.360616 | 1186 |
| HistGradientBoosting | 5 | 0.500000 | 0.666667 | 0.221698 | 0.332743 | 987 |
| HistGradientBoosting | 5 | 0.550000 | 0.682987 | 0.188005 | 0.294848 | 817 |
| HistGradientBoosting | 5 | 0.600000 | 0.707756 | 0.172170 | 0.276965 | 722 |
| LogisticRegression | 5 | 0.100000 | 0.258185 | 0.698787 | 0.377057 | 8033 |
| LogisticRegression | 5 | 0.150000 | 0.345068 | 0.601078 | 0.438437 | 5170 |
| LogisticRegression | 5 | 0.200000 | 0.433647 | 0.497642 | 0.463445 | 3406 |
| LogisticRegression | 5 | 0.250000 | 0.459910 | 0.446429 | 0.453069 | 2881 |
| LogisticRegression | 5 | 0.300000 | 0.491789 | 0.393531 | 0.437208 | 2375 |
| LogisticRegression | 5 | 0.350000 | 0.518753 | 0.330863 | 0.404032 | 1893 |
| LogisticRegression | 5 | 0.400000 | 0.569666 | 0.264488 | 0.361252 | 1378 |
| LogisticRegression | 5 | 0.450000 | 0.653728 | 0.215633 | 0.324297 | 979 |
| LogisticRegression | 5 | 0.500000 | 0.683313 | 0.189016 | 0.296120 | 821 |
| LogisticRegression | 5 | 0.550000 | 0.698087 | 0.172170 | 0.276216 | 732 |
| LogisticRegression | 5 | 0.600000 | 0.715180 | 0.153976 | 0.253396 | 639 |

## Proper outer-validation policy results

Each selected policy is evaluated once per outer fold. Accuracy/precision/recall/F1 and contact counts depend on threshold; ROC-AUC/AP use the unchanged positive probabilities. AP is Average Precision, not trapezoidal PR area. zero_division=0 throughout. Confusion matrices use actual rows no/yes, predicted columns no/yes: [[TN,FP],[FN,TP]].

| model | outer_fold | policy | Accuracy | Precision | Recall | F1 | ROC_AUC | AP | predicted_positives | positive_rate | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | Reference_0.50 | 0.899666 | 0.650558 | 0.235849 | 0.346192 | 0.810998 | 0.450109 | 269 | 0.040832 | 5752 | 94 | 567 | 175 |
| HistGradientBoosting | 1 | Training_F1 | 0.867183 | 0.435749 | 0.607817 | 0.507597 | 0.810998 | 0.450109 | 1035 | 0.157104 | 5262 | 584 | 291 | 451 |
| HistGradientBoosting | 1 | Training_Precision50 | 0.891621 | 0.525547 | 0.388140 | 0.446512 | 0.810998 | 0.450109 | 548 | 0.083182 | 5586 | 260 | 454 | 288 |
| LogisticRegression | 1 | Reference_0.50 | 0.899211 | 0.671053 | 0.206199 | 0.315464 | 0.773340 | 0.432797 | 228 | 0.034608 | 5771 | 75 | 589 | 153 |
| LogisticRegression | 1 | Training_F1 | 0.871281 | 0.438799 | 0.512129 | 0.472637 | 0.773340 | 0.432797 | 866 | 0.131451 | 5360 | 486 | 362 | 380 |
| LogisticRegression | 1 | Training_Precision50 | 0.892532 | 0.535270 | 0.347709 | 0.421569 | 0.773340 | 0.432797 | 482 | 0.073163 | 5622 | 224 | 484 | 258 |
| HistGradientBoosting | 2 | Reference_0.50 | 0.899211 | 0.668103 | 0.208895 | 0.318275 | 0.791971 | 0.442077 | 232 | 0.035216 | 5769 | 77 | 587 | 155 |
| HistGradientBoosting | 2 | Training_F1 | 0.866424 | 0.429158 | 0.563342 | 0.487179 | 0.791971 | 0.442077 | 974 | 0.147845 | 5290 | 556 | 324 | 418 |
| HistGradientBoosting | 2 | Training_Precision50 | 0.892532 | 0.532197 | 0.378706 | 0.442520 | 0.791971 | 0.442077 | 528 | 0.080146 | 5599 | 247 | 461 | 281 |
| LogisticRegression | 2 | Reference_0.50 | 0.899970 | 0.698565 | 0.196765 | 0.307045 | 0.758226 | 0.420805 | 209 | 0.031724 | 5783 | 63 | 596 | 146 |
| LogisticRegression | 2 | Training_F1 | 0.872344 | 0.439708 | 0.486523 | 0.461932 | 0.758226 | 0.420805 | 821 | 0.124621 | 5386 | 460 | 381 | 361 |
| LogisticRegression | 2 | Training_Precision50 | 0.890407 | 0.521930 | 0.320755 | 0.397329 | 0.758226 | 0.420805 | 456 | 0.069217 | 5628 | 218 | 504 | 238 |
| HistGradientBoosting | 3 | Reference_0.50 | 0.899666 | 0.652830 | 0.233154 | 0.343595 | 0.788546 | 0.428814 | 265 | 0.040225 | 5754 | 92 | 569 | 173 |
| HistGradientBoosting | 3 | Training_F1 | 0.857620 | 0.404297 | 0.557951 | 0.468856 | 0.788546 | 0.428814 | 1024 | 0.155434 | 5236 | 610 | 328 | 414 |
| HistGradientBoosting | 3 | Training_Precision50 | 0.888282 | 0.505319 | 0.384097 | 0.436447 | 0.788546 | 0.428814 | 564 | 0.085610 | 5567 | 279 | 457 | 285 |
| LogisticRegression | 3 | Reference_0.50 | 0.897996 | 0.660550 | 0.194070 | 0.300000 | 0.742708 | 0.403262 | 218 | 0.033090 | 5772 | 74 | 598 | 144 |
| LogisticRegression | 3 | Training_F1 | 0.865665 | 0.417722 | 0.489218 | 0.450652 | 0.742708 | 0.403262 | 869 | 0.131906 | 5340 | 506 | 379 | 363 |
| LogisticRegression | 3 | Training_Precision50 | 0.887675 | 0.502058 | 0.328841 | 0.397394 | 0.742708 | 0.403262 | 486 | 0.073770 | 5604 | 242 | 498 | 244 |
| HistGradientBoosting | 4 | Reference_0.50 | 0.900273 | 0.683983 | 0.212938 | 0.324769 | 0.802185 | 0.467601 | 231 | 0.035064 | 5773 | 73 | 584 | 158 |
| HistGradientBoosting | 4 | Training_F1 | 0.865665 | 0.432356 | 0.615903 | 0.508060 | 0.802185 | 0.467601 | 1057 | 0.160443 | 5246 | 600 | 285 | 457 |
| HistGradientBoosting | 4 | Training_Precision50 | 0.893898 | 0.543086 | 0.365229 | 0.436745 | 0.802185 | 0.467601 | 499 | 0.075744 | 5618 | 228 | 471 | 271 |
| LogisticRegression | 4 | Reference_0.50 | 0.897996 | 0.678571 | 0.179245 | 0.283582 | 0.770552 | 0.425777 | 196 | 0.029751 | 5783 | 63 | 609 | 133 |
| LogisticRegression | 4 | Training_F1 | 0.874165 | 0.449242 | 0.518868 | 0.481551 | 0.770552 | 0.425777 | 857 | 0.130085 | 5374 | 472 | 357 | 385 |
| LogisticRegression | 4 | Training_Precision50 | 0.892835 | 0.541475 | 0.316712 | 0.399660 | 0.770552 | 0.425777 | 434 | 0.065877 | 5647 | 199 | 507 | 235 |
| HistGradientBoosting | 5 | Reference_0.50 | 0.899514 | 0.683258 | 0.203230 | 0.313278 | 0.780853 | 0.452125 | 221 | 0.033546 | 5775 | 70 | 592 | 151 |
| HistGradientBoosting | 5 | Training_F1 | 0.869460 | 0.440969 | 0.588156 | 0.504037 | 0.780853 | 0.452125 | 991 | 0.150425 | 5291 | 554 | 306 | 437 |
| HistGradientBoosting | 5 | Training_Precision50 | 0.892077 | 0.529851 | 0.382234 | 0.444097 | 0.780853 | 0.452125 | 536 | 0.081360 | 5593 | 252 | 459 | 284 |
| LogisticRegression | 5 | Reference_0.50 | 0.900729 | 0.725888 | 0.192463 | 0.304255 | 0.764549 | 0.429507 | 197 | 0.029903 | 5791 | 54 | 600 | 143 |
| LogisticRegression | 5 | Training_F1 | 0.874317 | 0.448107 | 0.493943 | 0.469910 | 0.764549 | 0.429507 | 819 | 0.124317 | 5393 | 452 | 376 | 367 |
| LogisticRegression | 5 | Training_Precision50 | 0.894809 | 0.555556 | 0.336474 | 0.419111 | 0.764549 | 0.429507 | 450 | 0.068306 | 5645 | 200 | 493 | 250 |

Five-fold mean ± sample SD (ddof=1); counts are average contacts per outer-validation cohort, positive_rate is a fraction:

| model | policy | Accuracy mean ± SD | Precision mean ± SD | Recall mean ± SD | F1 mean ± SD | ROC_AUC mean ± SD | AP mean ± SD | predicted_positives mean ± SD | positive_rate mean ± SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Reference_0.50 | 0.899666 ± 0.000387 | 0.667746 ± 0.015987 | 0.218813 ± 0.014761 | 0.329222 ± 0.014903 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 243.600000 ± 21.835751 | 0.036976 ± 0.003314 |
| HistGradientBoosting | Training_F1 | 0.865270 ± 0.004506 | 0.428506 ± 0.014222 | 0.586634 ± 0.025850 | 0.495146 ± 0.016996 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 1016.200000 ± 33.521635 | 0.154250 ± 0.005088 |
| HistGradientBoosting | Training_Precision50 | 0.891682 ± 0.002083 | 0.527200 ± 0.013837 | 0.379681 ± 0.008766 | 0.441264 ± 0.004494 | 0.794911 ± 0.011816 | 0.448145 ± 0.014219 | 535.000000 ± 24.269322 | 0.081208 ± 0.003684 |
| LogisticRegression | Reference_0.50 | 0.899180 ± 0.001207 | 0.686925 ± 0.025841 | 0.193749 ± 0.009698 | 0.302069 ± 0.011779 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 209.600000 ± 13.722245 | 0.031815 ± 0.002083 |
| LogisticRegression | Training_F1 | 0.871554 ± 0.003530 | 0.438715 ± 0.012656 | 0.500136 ± 0.014471 | 0.467336 ± 0.011666 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 846.400000 ± 24.511222 | 0.128476 ± 0.003721 |
| LogisticRegression | Training_Precision50 | 0.891651 ± 0.002716 | 0.531257 ± 0.020313 | 0.330098 ± 0.012439 | 0.407013 ± 0.012233 | 0.761875 ± 0.012192 | 0.422429 ± 0.011606 | 461.600000 ± 22.018174 | 0.070067 ± 0.003342 |

Pooled outer-policy diagnostics, aggregating predictions made with each fold's own frozen threshold:

| model | policy | Accuracy | Precision | Recall | F1 | ROC_AUC | AP | predicted_positives | positive_rate | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | Reference_0.50 | 0.899666 | 0.666667 | 0.218809 | 0.329479 | 0.794260 | 0.445335 | 1218 | 0.036976 | 28823 | 406 | 2899 | 812 |
| HistGradientBoosting | Training_F1 | 0.865270 | 0.428459 | 0.586634 | 0.495223 | 0.794260 | 0.445335 | 5081 | 0.154250 | 26325 | 2904 | 1534 | 2177 |
| HistGradientBoosting | Training_Precision50 | 0.891682 | 0.526729 | 0.379682 | 0.441278 | 0.794260 | 0.445335 | 2675 | 0.081208 | 27963 | 1266 | 2302 | 1409 |
| LogisticRegression | Reference_0.50 | 0.899180 | 0.686069 | 0.193748 | 0.302164 | 0.761768 | 0.421094 | 1048 | 0.031815 | 28900 | 329 | 2992 | 719 |
| LogisticRegression | Training_F1 | 0.871554 | 0.438563 | 0.500135 | 0.467330 | 0.761768 | 0.421094 | 4232 | 0.128476 | 26853 | 2376 | 1855 | 1856 |
| LogisticRegression | Training_Precision50 | 0.891651 | 0.530763 | 0.330100 | 0.407044 | 0.761768 | 0.421094 | 2308 | 0.070067 | 28146 | 1083 | 2486 | 1225 |

Pooled counts are integer totals; pooled precision/F1 need not equal mean fold metrics. For the same fixed probabilities, changing threshold **does not change ROC-AUC or AP**. Assertions verify identical ranking metrics across policies within each outer fold and all descriptive curves. No ranking gain is attributed to threshold movement.

Illustrative constraint achieved on outer folds (not a guaranteed policy):

| model | folds_at_or_above_50 | outer_folds |
| --- | --- | --- |
| HistGradientBoosting | 5 | 5 |
| LogisticRegression | 5 | 5 |

## Descriptive threshold curves — not a policy-selection score

The following fixed-grid results use pooled outer-OOF probabilities and their labels only to describe the precision/recall/F1/volume trade-off. No threshold is selected from this table or plotted maxima and called unbiased performance. The actual policy thresholds above were fixed training-side before outer evaluation. These views must remain distinct.

| model | threshold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP | predicted_positives | positive_rate | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 0.100000 | 0.823315 | 0.347550 | 0.647804 | 0.452390 | 0.794260 | 0.445335 | 6917 | 0.209988 | 24716 | 4513 | 1307 | 2404 |
| HistGradientBoosting | 0.150000 | 0.859957 | 0.415952 | 0.601455 | 0.491792 | 0.794260 | 0.445335 | 5366 | 0.162902 | 26095 | 3134 | 1479 | 2232 |
| HistGradientBoosting | 0.200000 | 0.866485 | 0.431396 | 0.582053 | 0.495526 | 0.794260 | 0.445335 | 5007 | 0.152004 | 26382 | 2847 | 1551 | 2160 |
| HistGradientBoosting | 0.250000 | 0.870097 | 0.439677 | 0.557801 | 0.491745 | 0.794260 | 0.445335 | 4708 | 0.142927 | 26591 | 2638 | 1641 | 2070 |
| HistGradientBoosting | 0.300000 | 0.880237 | 0.469324 | 0.482350 | 0.475748 | 0.794260 | 0.445335 | 3814 | 0.115786 | 27205 | 2024 | 1921 | 1790 |
| HistGradientBoosting | 0.350000 | 0.891682 | 0.526729 | 0.379682 | 0.441278 | 0.794260 | 0.445335 | 2675 | 0.081208 | 27963 | 1266 | 2302 | 1409 |
| HistGradientBoosting | 0.400000 | 0.897571 | 0.590155 | 0.297224 | 0.395341 | 0.794260 | 0.445335 | 1869 | 0.056740 | 28463 | 766 | 2608 | 1103 |
| HistGradientBoosting | 0.450000 | 0.898998 | 0.629905 | 0.250876 | 0.358836 | 0.794260 | 0.445335 | 1478 | 0.044869 | 28682 | 547 | 2780 | 931 |
| HistGradientBoosting | 0.500000 | 0.899666 | 0.666667 | 0.218809 | 0.329479 | 0.794260 | 0.445335 | 1218 | 0.036976 | 28823 | 406 | 2899 | 812 |
| HistGradientBoosting | 0.550000 | 0.900000 | 0.699522 | 0.196982 | 0.307401 | 0.794260 | 0.445335 | 1045 | 0.031724 | 28915 | 314 | 2980 | 731 |
| HistGradientBoosting | 0.600000 | 0.899120 | 0.707265 | 0.178389 | 0.284915 | 0.794260 | 0.445335 | 936 | 0.028415 | 28955 | 274 | 3049 | 662 |
| LogisticRegression | 0.100000 | 0.741894 | 0.259174 | 0.694691 | 0.377508 | 0.761768 | 0.421094 | 9947 | 0.301973 | 21860 | 7369 | 1133 | 2578 |
| LogisticRegression | 0.150000 | 0.831967 | 0.354127 | 0.596605 | 0.444444 | 0.761768 | 0.421094 | 6252 | 0.189800 | 25191 | 4038 | 1497 | 2214 |
| LogisticRegression | 0.200000 | 0.871554 | 0.438563 | 0.500135 | 0.467330 | 0.761768 | 0.421094 | 4232 | 0.128476 | 26853 | 2376 | 1855 | 1856 |
| LogisticRegression | 0.250000 | 0.878901 | 0.461086 | 0.443816 | 0.452286 | 0.761768 | 0.421094 | 3572 | 0.108440 | 27304 | 1925 | 2064 | 1647 |
| LogisticRegression | 0.300000 | 0.886733 | 0.496552 | 0.388036 | 0.435638 | 0.761768 | 0.421094 | 2900 | 0.088039 | 27769 | 1460 | 2271 | 1440 |
| LogisticRegression | 0.350000 | 0.891651 | 0.530763 | 0.330100 | 0.407044 | 0.761768 | 0.421094 | 2308 | 0.070067 | 28146 | 1083 | 2486 | 1225 |
| LogisticRegression | 0.400000 | 0.895446 | 0.578761 | 0.264349 | 0.362930 | 0.761768 | 0.421094 | 1695 | 0.051457 | 28515 | 714 | 2730 | 981 |
| LogisticRegression | 0.450000 | 0.898330 | 0.640310 | 0.222582 | 0.330334 | 0.761768 | 0.421094 | 1290 | 0.039162 | 28765 | 464 | 2885 | 826 |
| LogisticRegression | 0.500000 | 0.899180 | 0.686069 | 0.193748 | 0.302164 | 0.761768 | 0.421094 | 1048 | 0.031815 | 28900 | 329 | 2992 | 719 |
| LogisticRegression | 0.550000 | 0.898573 | 0.702851 | 0.172730 | 0.277309 | 0.761768 | 0.421094 | 912 | 0.027687 | 28958 | 271 | 3070 | 641 |
| LogisticRegression | 0.600000 | 0.897662 | 0.707317 | 0.156292 | 0.256014 | 0.761768 | 0.421094 | 820 | 0.024894 | 28989 | 240 | 3131 | 580 |

## Policy A: fixed contact capacity — outer OOF rankings

Rank top 5%,10%,20% with K=ceil(fraction*N), descending probability and saved cleaned-row position for deterministic outcome-independent ties. Precision@K=captured/K, Recall@K=captured/actual subscribers, Lift@K=Precision/cohort prevalence. A fixed probability threshold is not needed. All models contact equal numbers within each comparison view. Include RF's unchanged Phase 5A results; no RF search or new predictions.

| model | fraction | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | 0.050000 | 1647 | 1005 | 0.610200 | 0.270816 | 5.416330 |
| HistGradientBoosting | 0.100000 | 3294 | 1628 | 0.494232 | 0.438696 | 4.386958 |
| HistGradientBoosting | 0.200000 | 6588 | 2377 | 0.360808 | 0.640528 | 3.202641 |
| LogisticRegression | 0.050000 | 1647 | 962 | 0.584092 | 0.259229 | 5.184586 |
| LogisticRegression | 0.100000 | 3294 | 1564 | 0.474803 | 0.421450 | 4.214497 |
| LogisticRegression | 0.200000 | 6588 | 2257 | 0.342593 | 0.608192 | 3.040959 |
| RandomForest | 0.050000 | 1647 | 999 | 0.606557 | 0.269200 | 5.383994 |
| RandomForest | 0.100000 | 3294 | 1588 | 0.482089 | 0.427917 | 4.279170 |
| RandomForest | 0.200000 | 6588 | 2341 | 0.355343 | 0.630827 | 3.154136 |

Fold-local mean/SD, including historical RF reference:

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

Pooled probabilities originate from five fitted models and may differ in calibration; fold-local rankings are cleaner per-cohort comparisons. Ceil rounding means pooled and summed fold-local capacities differ slightly. These are historical subscriber-identification metrics, not causal effects of outreach. No known costs, incremental revenue or operational capacity were assumed.

## Policy B: fixed probability rule versus fixed capacity

Reference .50 and both training-selected rules above produce **variable contact volume** by model/fold. F1 maximization balances precision/recall implicitly, not bank profit. The 50% precision-constrained rule sacrifices coverage for an illustrative empirical precision target that is not guaranteed out of sample. Neither rule is financially optimal without costs, incremental value and bank constraints.

If the operational goal is a firm call budget (e.g. contact only 5–20%), a top-K policy directly enforces that capacity and permits like-for-like model comparisons. It is not automatically universally better: a genuinely calibrated probability plus validated utility/cost rule may suit a different objective. No calibration experiment or financial threshold was run. Compare the observed contact rates and capture/precision tables before a team chooses a policy.

RF .50 historical fold metrics for reference only (no threshold adjustment or RF tuning):

| model | outer_fold | Accuracy | Precision | Recall | F1 | ROC_AUC | AP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RandomForest | 1 | 0.899818 | 0.683036 | 0.206199 | 0.316770 | 0.804058 | 0.442925 |
| RandomForest | 2 | 0.899362 | 0.670996 | 0.208895 | 0.318602 | 0.788798 | 0.444596 |
| RandomForest | 3 | 0.898907 | 0.679245 | 0.194070 | 0.301887 | 0.781868 | 0.414406 |
| RandomForest | 4 | 0.899514 | 0.698020 | 0.190027 | 0.298729 | 0.798528 | 0.466453 |
| RandomForest | 5 | 0.899970 | 0.705882 | 0.193809 | 0.304118 | 0.778870 | 0.451270 |

## Technical checks, warnings and cost

| model | role | rows | fits |
| --- | --- | --- | --- |
| HistGradientBoosting | outer-training refit | 26352 | 5 |
| HistGradientBoosting | training-side OOF fit | 21081 | 10 |
| HistGradientBoosting | training-side OOF fit | 21082 | 15 |
| LogisticRegression | outer-training refit | 26352 | 5 |
| LogisticRegression | training-side OOF fit | 21081 | 10 |
| LogisticRegression | training-side OOF fit | 21082 | 15 |

| model | role | calls |
| --- | --- | --- |
| HistGradientBoosting | outer validation | 5 |
| HistGradientBoosting | training-side OOF | 25 |
| LogisticRegression | outer validation | 5 |
| LogisticRegression | training-side OOF | 25 |

| model | outer_fold | training_OOF_fits | outer_refits | wall_seconds |
| --- | --- | --- | --- | --- |
| HistGradientBoosting | 1 | 5 | 1 | 4.149055 |
| LogisticRegression | 1 | 5 | 1 | 0.804798 |
| HistGradientBoosting | 2 | 5 | 1 | 4.325518 |
| LogisticRegression | 2 | 5 | 1 | 0.920465 |
| HistGradientBoosting | 3 | 5 | 1 | 4.500505 |
| LogisticRegression | 3 | 5 | 1 | 0.826069 |
| HistGradientBoosting | 4 | 5 | 1 | 4.262828 |
| LogisticRegression | 4 | 5 | 1 | 0.812872 |
| HistGradientBoosting | 5 | 5 | 1 | 4.177991 |
| LogisticRegression | 5 | 5 | 1 | 0.772249 |

| model | training_OOF_fits | outer_refits | wall_seconds |
| --- | --- | --- | --- |
| HistGradientBoosting | 25 | 5 | 21.415897 |
| LogisticRegression | 25 | 5 | 4.136453 |

Elapsed through experiments/plots: 27.60s, sklearn 1.8.0, pandas 2.2.3, NumPy 2.3.5; local execution, not a live hosted Colab session. threadpoolctl limits native threads to one. Standard Colab packages with sklearn >=1.2 suffice; required uploads are listed in the notebook. No previous grids were rerun.

All 60 fits started fresh and were restricted to training-side folds or the current outer-training refit. Every OHE vocabulary equals fitting-row levels; LR mean/variance/scale/sample counts match fit rows; ConditionalRecencyScaler statistics use only available fitting recencies, with zero unavailable standardized values and an unscaled indicator. HGB numbers/recency exactly equal validation input; no 999 sentinel. Probability column mapped by classes_=[0,1]. Each prediction is disjoint from its estimator's fitting rows. Outer prediction is blocked until thresholds are frozen. No whole-development or held-out fitting, no NaN/infinity, no changes in fitted parameters on transform. Hashes and development equality confirm raw/cleaned data, split, approved preprocessing and earlier results unchanged. All four existing standalone preprocessing tests passed when rerun separately.

Warnings/errors:

None recorded across all 60 fits.

## Observed policy trade-offs and stability

Mean outer-fold HGB recall rises from 21.88% at 0.50 to 58.66% under training-side F1 selection, with precision falling from 66.77% to 42.85% and F1 rising from 0.3292 to 0.4951. Mean contact rate rises from 3.70% to 15.43%. LR recall rises from 19.37% to 50.01%, precision falls from 68.69% to 43.87%, and F1 rises from 0.3021 to 0.4673; contact rate rises from 3.18% to 12.85%. These are evaluated frozen-policy effects on decisions, not improvements in AP/ROC-AUC or causal outreach response.

F1 selects 0.20 for LR in all five folds; HGB selects 0.20 in four and 0.15 in one. The research precision constraint selects 0.35 in every fold for both models. All training partitions had a feasible candidate, and every outer cohort empirically achieved at least 50% precision. Mean HGB precision/recall at that policy is 52.72%/37.97%, versus LR 53.13%/33.01%; mean contact rates are 8.12% and 7.01%. Passing five observed cohorts is not a guaranteed lower precision bound on new customers.

Pooled HGB contact volume changes from 1,218 at 0.50 to 5,081 under F1 selection, capturing 2,177 versus 812 historical subscribers. The precision-constrained policy contacts 2,675 and captures 1,409. If an illustrative budget were exactly 10% (3,294), top-K HGB instead captures 1,628 with 49.42% precision and 43.87% recall; it enforces capacity directly, while the precision/F1 rules pursue different objectives and contact different numbers. That conditional comparison does not establish a known bank budget or a financially optimal policy.

Use this phase's threshold-only gains as a reference before adding imbalance-treatment complexity. Next approved experiments should distinguish ranking improvements (AP/ROC-AUC) from decision-rule effects and compare policies at a bank-approved capacity or objective; simply lowering a threshold is already a substantial recall/precision trade-off.

## Interpretation, limitations and Phase 5B-2 recommendations

Use measured outer-fold mean/SD and pooled confusion/volume tables to judge recall gains and precision cost. Selected thresholds are research policy experiments, not final deployment choices. No best pooled-diagnostic threshold is declared. Outer ranking metrics remain exactly those of the fixed probability predictions.

All 15 predictors remain Provisional: age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days. Historical recency/contact cutoff, campaign-start customer/status snapshots, economic publication/revision vintages and outcome window still need timestamped confirmation. Missing customer IDs/dates permit repeated-client/temporal overlap in random stratified CV. Prior full-data EDA and development-based family/grid/shortlist exploration also limit generalization claims. Threshold isolation controls direct fitting/evaluation leakage; it does not certify feature timing, unseen-client/future-period performance, deployment readiness or causal call impact.

For a separately approved Phase 5B-2, compare class weighting against these threshold-only references under the same outer isolation, and consider resampling only with appropriate mixed-type methods and training-fold-only application. Any sampling method must respect categorical indicators and avoid standard SMOTE generating invalid fractional category combinations. No improvement is claimed before experiments. Do not change saved holdout, fit globally before CV, or use threshold changes to claim AP improvement. Team approval needed for imbalance methods, model/policy shortlist, business capacity/error costs, illustrative precision target and timing assumptions. No SMOTE, undersampling, class weighting, feature selection, held-out evaluation, commit/push or Phase 5B-2 was performed.

Deliverables: executed 07_threshold_decision_analysis.ipynb and this 07_threshold_decision_summary.md, saved in the repository; stop pending review.
