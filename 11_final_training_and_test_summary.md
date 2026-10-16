# Phase 7 — Final training, freeze and one-time held-out evaluation

## Completion and fixed primary scenario

Executed from approved merged main **9578ebc**. The user's Phase 7 instruction explicitly approves the Phase 6B four-scenario historical academic protocol, both stages and automatic continuation after a passing gate. Earlier Phase 6B documents retain their original proposed wording unchanged; this new authorization is recorded in models/phase7_protocol.json, the manifest and event log. No material protocol conflict was found.

**P1 remains the sole primary**: original HGB, Full 15 Provisional predictors. S1 is customer-only HGB sensitivity; B1 full LR and B2 customer-only LR are secondary benchmarks. All 15 predictors remain Provisional. These are conditional historical academic results, not verified deployment readiness. No scenario, model, feature set, threshold or capacity was chosen from test performance.

All required Phase 7 outputs are present: executed notebook, this report, preserved pre-test PASS gate, four frozen complete sklearn Pipelines plus manifest/protocol, frozen predictions, point metrics, targeting tables, 2,000 paired stratified metric-bootstrap replicates/intervals and reproducibility/audit metadata. No prior Phase 2C–6B artifact was overwritten. No commit, push, merge or next experiment occurred.

## Final development-only selection and training

- P1: `{"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15}`.
- S1: `{"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15}`.
- B1: `{"classifier__C": 0.1}`.
- B2: `{"classifier__C": 0.1}`.

| scenario | role | group | selected_parameters | CV_AP_selection_only | seconds |
| --- | --- | --- | --- | --- | --- |
| P1 | Sole Primary | Full | {"classifier__l2_regularization": 1.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 200, "classifier__max_leaf_nodes": 15} | 0.448069 | 100.591032 |
| S1 | Secondary Sensitivity | Customer Attributes Only | {"classifier__l2_regularization": 0.0, "classifier__learning_rate": 0.05, "classifier__max_iter": 100, "classifier__max_leaf_nodes": 15} | 0.233785 | 85.355146 |
| B1 | Secondary Benchmark | Full | {"classifier__C": 0.1} | 0.422429 | 2.079500 |
| B2 | Secondary Benchmark | Customer Attributes Only | {"classifier__C": 0.1} | 0.202251 | 1.738402 |

Each scenario independently searched the exact approved grid with StratifiedKFold(5, shuffle=True, random_state=42), positive-class predict_proba AP scorer, refit='AP', n_jobs=1, error_score='raise'. HGB grid 16 candidates; LR C grid 3. Highest unrounded mean AP wins; exact ties use first ParameterGrid order. Detailed 38 candidates × five folds are in results/development_cv_candidates.csv. **190 candidate-fold fits +4 permitted all-development winner refits =194 model fits**; all input rows are saved development records. CV selection AP above is a tuning estimate, not independent test performance. Training/search/freezing time: 189.76s, including audits; not a controlled hardware benchmark.

Full uses exact original FEATURES order; customer-only uses age, job, marital, education, default, housing, loan. The exact approved Phase 6A subset adapter was extracted as a single function from its digest-verified notebook, not reimplemented or its modeling cells rerun. Full adapter output/statistics match the original approved factory on development-only fixtures. Customer-only removes excluded columns and the recency component entirely. No constant stand-ins or new features.

HGB: unscaled approved tree preprocessing, numeric full one-hot, categorical_features=None, early_stopping=False, class_weight=None, seed42. LR: approved training-only StandardScaler and observed-only ConditionalRecencyScaler when Full, lbfgs, max_iter1000, default L2, class_weight=None, seed42. sklearn 1.8 represents default L2 with l1_ratio=0 and a deprecated penalty sentinel; leaving the approved default unchanged avoids an unnecessary deprecation warning. No calibration, learned threshold, sampling or class weighting.

Serialized artifacts are plain complete sklearn Pipelines containing the already-fitted approved preprocessing and classifier; the experiment-only audit wrapper is omitted without refitting or changing learned steps. Four trusted locally created artifacts reloaded with **bit-identical probabilities on 256 development-only fixture records** before release. No untrusted pickle was loaded. Joblib artifacts require a compatible trusted environment and preprocessing.py.

## Release gate before test access

**PASS — All requirements satisfied.** [12_pre_holdout_release_gate.md](12_pre_holdout_release_gate.md) was written at 2026-10-16T01:52:21.438245+00:00 UTC before any test parser invocation. Gate document SHA-256 `b12f5252aef6794c635a041506a01ae388b141e9f91973afb612d155bb07ba89` is preserved unchanged. models/model_manifest.json SHA-256 `84aad6db0ad97b619fdf27c4e6fccdef3263ac65c178ca4f9898a0b0b773d96a` and protocol/code digests were recorded before exposure. results/phase7_events.jsonl and test_access_started.json record the ordered events.

Training isolation checked every candidate/refit row set, fold-specific category levels, selected numerical means/population variances/scales and available-only recency statistics. Unavailable transformed recency days remain zero; availability stays unscaled; original 999 never enters numeric recency. Customer-only has no recency transformer. Validation transforms did not change fitted signatures; finite outputs and [0,1] class mapping passed. Full adapter equivalence, synthetic targeting/tie/metric checks and **four existing preprocessing tests passed**. No unexpected training or prediction warnings occurred. Original datasets, saved indices and preprocessing.py retain approved digests.

Gate passage continued automatically under existing authorization. The exact saved **8,236** test observations were parsed once, restored to saved ordered cleaned-row positions and never dropped, rebalanced, relabelled or used for fitting. **Exactly one predict_proba call per scenario** generated all four vectors before any test metric was calculated. No test fit/fit_transform, vocabulary update, scaling update, threshold fitting or calibration occurred. Immutable predictions are in results/heldout_predictions.csv, with row positions, y and four positive-class probability columns. The test partition is now evaluated/exposed, not available for new model selection.

## Held-out predictive and .50 reference results

Observed prevalence: **0.112676** (928 subscribers / 8236 records). This is post-release evaluation context only, not a selection input. Positive class is 1; classification uses probability>=.50, zero_division=0. AP is sklearn Average Precision, not trapezoidal PR area; ROC-AUC uses the same positive probabilities.

| scenario | role | AP | ROC_AUC | Accuracy | Precision | Recall | F1 | predicted_positive_count | predicted_positive_fraction | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Sole Primary | 0.451334 | 0.807608 | 0.896552 | 0.619497 | 0.212284 | 0.316212 | 318 | 0.038611 | 7187 | 121 | 731 | 197 |
| S1 | Secondary Sensitivity | 0.230981 | 0.669764 | 0.887688 | 0.615385 | 0.008621 | 0.017003 | 13 | 0.001578 | 7303 | 5 | 920 | 8 |
| B1 | Secondary Benchmark | 0.431032 | 0.777331 | 0.898009 | 0.676000 | 0.182112 | 0.286927 | 250 | 0.030355 | 7227 | 81 | 759 | 169 |
| B2 | Secondary Benchmark | 0.200407 | 0.648536 | 0.887324 | 0.000000 | 0.000000 | 0.000000 | 0 | 0.000000 | 7308 | 0 | 928 | 0 |

Confusion matrices follow **[[TN, FP], [FN, TP]]**, actual rows [0,1], predicted columns [0,1]; corresponding counts are above and in results/heldout_metrics.csv. P1 AP=0.451334, ROC-AUC=0.807608. Observed descending held-out AP order is P1, B1, S1, B2. This descriptive ordering does not change P1's sole-primary status or select a deployment model.

AP is prioritized because subscribers are the minority and positive ranking quality matters; a mostly-negative classifier can have high accuracy. The .50 rule is a reference, not a calibrated, cost-optimal or capacity-preserving decision. Threshold changes alone can change precision/recall/F1/contact volume but cannot change AP/ROC-AUC for fixed scores. No alternative cutoff was selected here.

## Primary illustrative business capacity — top 10%

**824 contacts for every scenario**, fixed before test access; not a bank-confirmed operational budget.

| scenario | fraction | capacity_role | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 0.100000 | Primary illustrative | 824 | 412 | 0.500000 | 0.443966 | 4.437500 |
| S1 | 0.100000 | Primary illustrative | 824 | 224 | 0.271845 | 0.241379 | 2.412621 |
| B1 | 0.100000 | Primary illustrative | 824 | 396 | 0.480583 | 0.426724 | 4.265170 |
| B2 | 0.100000 | Primary illustrative | 824 | 190 | 0.230583 | 0.204741 | 2.046420 |

P1 identifies **412 historical subscribers**, conversion concentration/Precision@824=0.500000, Recall@824=0.443966, Lift@824=4.437500. These counts describe historical subscriber identification, not subscribers caused by calls or guaranteed future conversions.

## Predefined secondary capacities — top 5% and 20%

| scenario | fraction | capacity_role | contacts | captured_subscribers | Precision_at_K | Recall_at_K | Lift_at_K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 0.050000 | Secondary | 412 | 248 | 0.601942 | 0.267241 | 5.342233 |
| P1 | 0.200000 | Secondary | 1648 | 610 | 0.370146 | 0.657328 | 3.285042 |
| S1 | 0.050000 | Secondary | 412 | 156 | 0.378641 | 0.168103 | 3.360437 |
| S1 | 0.200000 | Secondary | 1648 | 338 | 0.205097 | 0.364224 | 1.820237 |
| B1 | 0.050000 | Secondary | 412 | 240 | 0.582524 | 0.258621 | 5.169903 |
| B1 | 0.200000 | Secondary | 1648 | 586 | 0.355583 | 0.631466 | 3.155795 |
| B2 | 0.050000 | Secondary | 412 | 123 | 0.298544 | 0.132543 | 2.649575 |
| B2 | 0.200000 | Secondary | 1648 | 312 | 0.189320 | 0.336207 | 1.680218 |

Contact counts are exactly 412 / 824 / 1,648. Rank descending score, ties ascending immutable cleaned-row position, independent of outcome. Precision@K=captured/K; Recall@K=captured/total positives; Lift@K=Precision@K/prevalence. Same K across scenarios. Broader capacity trades contact volume for subscriber coverage; use actual results rather than infer a financially optimal budget. No call costs, incremental value, experimental treatment effect or ROI is known.

## Feature and model contrasts — descriptive, no test-driven reselection

| comparison | AP_difference | ROC_AUC_difference | Top10_capture_difference |
| --- | --- | --- | --- |
| HGB Full minus Customer Only | 0.220353 | 0.137844 | 188 |
| LR Full minus Customer Only | 0.230626 | 0.128794 | 206 |
| Full HGB minus Full LR | 0.020302 | 0.030278 | 16 |
| Customer HGB minus Customer LR | 0.030575 | 0.021228 | 34 |

The Full-versus-Customer contrasts quantify this frozen pair of models on this cohort, including their development-selected configurations. They do not isolate causal effects of economic/history variables or establish remaining feature timing. The HGB-versus-LR contrasts show whether the historical ranking advantage persists here, without a statistical-significance/winner claim. Do not add the untested No Economic/No History subsets or new models to explain a surprising result.

Prior Phase 5B-2 balanced HGB offered only small, capacity-dependent gains (+13/-18/-6 historical subscribers at development 5/10/20%) and a 0.002738 mean AP increase. RandomUnderSampler reduced HGB AP and capture. Original threshold-only F1 strategies already changed recall substantially. Therefore the pre-test plan retained original unweighted models, not an assumption that imbalance treatments never help. No treatment was reconsidered after test results.

## Comparison with previous nested development CV

| scenario | role | prior_nested_AP_mean_SD | heldout_AP | AP_test_minus_prior_nested_mean | prior_nested_ROC_AUC_mean_SD | heldout_ROC_AUC | ROC_AUC_test_minus_prior_nested_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Sole Primary | 0.448145 ± 0.014219 | 0.451334 | 0.003189 | 0.794911 ± 0.011816 | 0.807608 | 0.012697 |
| S1 | Secondary Sensitivity | 0.232569 ± 0.009506 | 0.230981 | -0.001588 | 0.663736 ± 0.005367 | 0.669764 | 0.006028 |
| B1 | Secondary Benchmark | 0.422429 ± 0.011606 | 0.431032 | 0.008603 | 0.761875 ± 0.012192 | 0.777331 | 0.015456 |
| B2 | Secondary Benchmark | 0.202251 ± 0.015223 | 0.200407 | -0.001844 | 0.646807 ± 0.008145 | 0.648536 | 0.001729 |

Prior full-feature values come from Phase 5A and its Phase 6A replication; customer-only values from Phase 6A's own nested searches. Differences are test point estimates minus prior five-fold means. Read them as apparent generalization differences across partitions/training procedures, not a paired test, confidence bound or proof of distributional stability. Final models were selected/refitted on all development whereas nested models fit less data per outer fold. Prior CV SD is descriptive fold spread; it is not a test CI. Full-development best-CV selection scores are separately labelled above and are not substituted for this comparison.

## Bootstrap uncertainty

Exactly **2,000 stratified paired metric-bootstrap replicates**, NumPy default_rng(42)/PCG64. Draw with replacement within each observed class, preserving original counts; use the identical draws for all four frozen scenarios. No model fitting, prediction, transform, recalibration or threshold fitting in bootstrap. Recompute .50 metrics and Top-K using cohort length/ceil capacity and deterministic ties: score, original row position, duplicate draw-occurrence position. Original outcomes do not break ties. Draw digests and 8,000 scenario-replicate rows are saved.

Selected AP/ROC and primary-capacity intervals:

| scenario | metric | estimate | lower_95 | upper_95 | method |
| --- | --- | --- | --- | --- | --- |
| P1 | AP | 0.451334 | 0.420577 | 0.485339 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | ROC_AUC | 0.807608 | 0.790575 | 0.824540 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_captured_subscribers | 412.000000 | 386.000000 | 435.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Precision_at_K | 0.500000 | 0.468447 | 0.527913 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Recall_at_K | 0.443966 | 0.415948 | 0.468750 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Lift_at_K | 4.437500 | 4.157464 | 4.685225 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | AP | 0.230981 | 0.211086 | 0.254719 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | ROC_AUC | 0.669764 | 0.651039 | 0.687616 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_captured_subscribers | 224.000000 | 202.000000 | 247.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Precision_at_K | 0.271845 | 0.245146 | 0.299757 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Recall_at_K | 0.241379 | 0.217672 | 0.266164 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Lift_at_K | 2.412621 | 2.175667 | 2.660346 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | AP | 0.431032 | 0.400841 | 0.463371 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | ROC_AUC | 0.777331 | 0.759071 | 0.796171 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_captured_subscribers | 396.000000 | 373.000000 | 421.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Precision_at_K | 0.480583 | 0.452670 | 0.510922 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Recall_at_K | 0.426724 | 0.401940 | 0.453664 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Lift_at_K | 4.265170 | 4.017445 | 4.534436 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | AP | 0.200407 | 0.183810 | 0.221354 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | ROC_AUC | 0.648536 | 0.630318 | 0.665504 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_captured_subscribers | 190.000000 | 168.000000 | 210.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Precision_at_K | 0.230583 | 0.203883 | 0.254885 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Recall_at_K | 0.204741 | 0.181034 | 0.226320 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Lift_at_K | 2.046420 | 1.809466 | 2.262102 | 2000 paired stratified percentile; conditional on fitted model/class counts |

All predefined metric intervals (2.5th/97.5th percentiles, NumPy linear quantiles):

| scenario | metric | estimate | lower_95 | upper_95 | method |
| --- | --- | --- | --- | --- | --- |
| P1 | AP | 0.451334 | 0.420577 | 0.485339 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | ROC_AUC | 0.807608 | 0.790575 | 0.824540 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Accuracy | 0.896552 | 0.892788 | 0.900559 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Precision | 0.619497 | 0.570571 | 0.670117 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Recall | 0.212284 | 0.186422 | 0.238147 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | F1 | 0.316212 | 0.281758 | 0.348791 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | predicted_positive_count | 318.000000 | 288.000000 | 350.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | predicted_positive_fraction | 0.038611 | 0.034968 | 0.042499 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | TN | 7187.000000 | 7165.000000 | 7207.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | FP | 121.000000 | 100.975000 | 143.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | FN | 731.000000 | 707.000000 | 755.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | TP | 197.000000 | 173.000000 | 221.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top5_contacts | 412.000000 | 412.000000 | 412.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top5_captured_subscribers | 248.000000 | 230.000000 | 267.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top5_Precision_at_K | 0.601942 | 0.558252 | 0.648058 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top5_Recall_at_K | 0.267241 | 0.247845 | 0.287716 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top5_Lift_at_K | 5.342233 | 4.954490 | 5.751517 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_contacts | 824.000000 | 824.000000 | 824.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_captured_subscribers | 412.000000 | 386.000000 | 435.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Precision_at_K | 0.500000 | 0.468447 | 0.527913 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Recall_at_K | 0.443966 | 0.415948 | 0.468750 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top10_Lift_at_K | 4.437500 | 4.157464 | 4.685225 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top20_contacts | 1648.000000 | 1648.000000 | 1648.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top20_captured_subscribers | 610.000000 | 585.000000 | 637.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top20_Precision_at_K | 0.370146 | 0.354976 | 0.386529 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top20_Recall_at_K | 0.657328 | 0.630388 | 0.686422 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| P1 | Top20_Lift_at_K | 3.285042 | 3.150410 | 3.430446 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | AP | 0.230981 | 0.211086 | 0.254719 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | ROC_AUC | 0.669764 | 0.651039 | 0.687616 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Accuracy | 0.887688 | 0.886838 | 0.888538 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Precision | 0.615385 | 0.333333 | 0.888889 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Recall | 0.008621 | 0.003233 | 0.015086 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | F1 | 0.017003 | 0.006403 | 0.029536 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | predicted_positive_count | 13.000000 | 6.000000 | 21.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | predicted_positive_fraction | 0.001578 | 0.000729 | 0.002550 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | TN | 7303.000000 | 7298.975000 | 7307.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | FP | 5.000000 | 1.000000 | 9.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | FN | 920.000000 | 914.000000 | 925.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | TP | 8.000000 | 3.000000 | 14.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top5_contacts | 412.000000 | 412.000000 | 412.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top5_captured_subscribers | 156.000000 | 136.000000 | 173.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top5_Precision_at_K | 0.378641 | 0.330097 | 0.419903 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top5_Recall_at_K | 0.168103 | 0.146552 | 0.186422 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top5_Lift_at_K | 3.360437 | 2.929612 | 3.726638 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_contacts | 824.000000 | 824.000000 | 824.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_captured_subscribers | 224.000000 | 202.000000 | 247.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Precision_at_K | 0.271845 | 0.245146 | 0.299757 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Recall_at_K | 0.241379 | 0.217672 | 0.266164 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top10_Lift_at_K | 2.412621 | 2.175667 | 2.660346 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top20_contacts | 1648.000000 | 1648.000000 | 1648.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top20_captured_subscribers | 338.000000 | 313.000000 | 366.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top20_Precision_at_K | 0.205097 | 0.189927 | 0.222087 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top20_Recall_at_K | 0.364224 | 0.337284 | 0.394397 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| S1 | Top20_Lift_at_K | 1.820237 | 1.685604 | 1.971025 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | AP | 0.431032 | 0.400841 | 0.463371 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | ROC_AUC | 0.777331 | 0.759071 | 0.796171 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Accuracy | 0.898009 | 0.894609 | 0.901530 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Precision | 0.676000 | 0.621414 | 0.732000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Recall | 0.182112 | 0.159483 | 0.206897 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | F1 | 0.286927 | 0.254947 | 0.319207 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | predicted_positive_count | 250.000000 | 223.000000 | 278.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | predicted_positive_fraction | 0.030355 | 0.027076 | 0.033754 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | TN | 7227.000000 | 7209.000000 | 7244.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | FP | 81.000000 | 64.000000 | 99.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | FN | 759.000000 | 736.000000 | 780.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | TP | 169.000000 | 148.000000 | 192.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top5_contacts | 412.000000 | 412.000000 | 412.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top5_captured_subscribers | 240.000000 | 220.000000 | 258.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top5_Precision_at_K | 0.582524 | 0.533981 | 0.626214 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top5_Recall_at_K | 0.258621 | 0.237069 | 0.278017 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top5_Lift_at_K | 5.169903 | 4.739078 | 5.557646 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_contacts | 824.000000 | 824.000000 | 824.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_captured_subscribers | 396.000000 | 373.000000 | 421.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Precision_at_K | 0.480583 | 0.452670 | 0.510922 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Recall_at_K | 0.426724 | 0.401940 | 0.453664 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top10_Lift_at_K | 4.265170 | 4.017445 | 4.534436 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top20_contacts | 1648.000000 | 1648.000000 | 1648.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top20_captured_subscribers | 586.000000 | 560.000000 | 612.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top20_Precision_at_K | 0.355583 | 0.339806 | 0.371359 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top20_Recall_at_K | 0.631466 | 0.603448 | 0.659483 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B1 | Top20_Lift_at_K | 3.155795 | 3.015777 | 3.295813 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | AP | 0.200407 | 0.183810 | 0.221354 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | ROC_AUC | 0.648536 | 0.630318 | 0.665504 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Accuracy | 0.887324 | 0.887324 | 0.887324 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Precision | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Recall | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | F1 | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | predicted_positive_count | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | predicted_positive_fraction | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | TN | 7308.000000 | 7308.000000 | 7308.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | FP | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | FN | 928.000000 | 928.000000 | 928.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | TP | 0.000000 | 0.000000 | 0.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top5_contacts | 412.000000 | 412.000000 | 412.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top5_captured_subscribers | 123.000000 | 105.000000 | 140.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top5_Precision_at_K | 0.298544 | 0.254854 | 0.339867 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top5_Recall_at_K | 0.132543 | 0.113147 | 0.150889 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top5_Lift_at_K | 2.649575 | 2.261833 | 3.016315 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_contacts | 824.000000 | 824.000000 | 824.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_captured_subscribers | 190.000000 | 168.000000 | 210.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Precision_at_K | 0.230583 | 0.203883 | 0.254885 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Recall_at_K | 0.204741 | 0.181034 | 0.226320 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top10_Lift_at_K | 2.046420 | 1.809466 | 2.262102 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top20_contacts | 1648.000000 | 1648.000000 | 1648.000000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top20_captured_subscribers | 312.000000 | 287.000000 | 339.025000 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top20_Precision_at_K | 0.189320 | 0.174150 | 0.205719 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top20_Recall_at_K | 0.336207 | 0.309267 | 0.365329 | 2000 paired stratified percentile; conditional on fitted model/class counts |
| B2 | Top20_Lift_at_K | 1.680218 | 1.545586 | 1.825757 | 2000 paired stratified percentile; conditional on fitted model/class counts |

These are **descriptive 95% intervals conditional on the fitted models and observed class balance**. They omit uncertainty from prior development-driven family/feature/grid selection, fitting variation, unknown customer clustering, temporal overlap, source timing, prevalence change and future deployment shift. Row-wise resampling may be optimistic with repeated customers/shared periods. No significance test or multiplicity-free inference is claimed; intervals and secondary scenarios do not reselect the primary model. They are not guaranteed future ranges and do not establish causal campaign uplift.

## Reproducibility and frozen artifacts

- 11_final_training_and_test.ipynb includes development fitting/freezing, gate, one-time evaluation, bootstrap and four figures. **Default replay mode** reads digest-verified frozen prediction/results files, recomputes deterministic point tables/figures and loads saved bootstrap intervals/replicates; it does not refit, predict from models or reopen raw held-out records. Initial mode refuses existing freeze/gate/access artifacts.
- models/P1_pipeline.joblib, S1_pipeline.joblib, B1_pipeline.joblib, B2_pipeline.joblib: trusted frozen complete pipelines. model_manifest.json records exact parameters, preprocessing signatures, schemas/classes, versions/seeds/source/model hashes; phase7_protocol.json records the pre-test rules/approval and execution-code hash.
- results/: development candidates/audits/tests; final parameters; immutable heldout_predictions.csv; heldout_metrics.csv and heldout_topk.csv; bootstrap_intervals.csv, bootstrap_replicate_metrics.csv.gz, bootstrap_draw_digests.csv and metadata; release-gate/access/prediction audits; event log and evaluation_complete.json containing frozen file digests and counts.
- Source cleaned SHA-256 `c1a19ca755279a5f22ba22e06b8d5ca22797d9b6351c69fe4cfafd2b47041d49`; split SHA-256 `397e6e9c66ba3b6b5f6bef6232e00dc392c9ae9d77fdfda28a2d7dc02693596b`; preprocessing SHA-256 `3959b4db9a561be5bf7373dfcf82ab85c24a288250e26180599a403b7e551ed8`. Complete raw/source/plan hashes are in the manifest. No saved split or previous notebook/data/module was changed.
- Versions: {"joblib": "1.5.3", "numpy": "2.3.5", "pandas": "2.2.3", "python": "3.12.14", "scipy": "1.17.0", "sklearn": "1.8.0"}. GridSearch/native threads bounded to one. Hosted Colab was not directly exercised; portable repository/Drive loading and pinned tested versions are documented. Execution code digest excludes notebook outputs so saving results does not alter frozen algorithm identity.

## Research limitations and final implications

All 15 predictors remain Provisional, including customer-only fields. Campaign-start snapshots, previous-campaign cutoff, recency reference date, economic release/revision vintages and the outcome window remain unverified. Strong Full performance cannot make those fields deployable. This is conditional historical prediction in the provided marketing cohort, not verified prospective pre-campaign targeting, causal uplift or financial impact.

Missing customer IDs and campaign dates prevent grouped-customer and forward-time validation and can permit repeated-client or temporal overlap across the saved random split. Prior whole-dataset EDA and development-based model/grid/shortlist selection limit any pristine-holdout claim, even though no held-out predictive fitting/tuning occurred. All scenario roles/policies were fixed before exposure; the holdout has now been used once for its authorized batch and must not become a new development set for repeated experimentation.

Use these results to document the frozen academic comparison and its business-capacity trade-offs. Deployment would require verified time-aligned inputs/labels, customer/time validation, real operational objectives/costs and prospective evidence in a separately authorized study. Do not change models, add experiments or choose another primary based on these results. **Stop after Phase 7; no commit or push pending review.**
