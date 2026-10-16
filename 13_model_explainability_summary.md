# Phase 8A — Frozen-model explainability and interpretation

## Observed findings and interpretation

The strongest individual P1 permutation sensitivities are nr.employed (AP drop 0.176239 ± 0.012367 repeat SD), emp.var.rate (0.118862 ± 0.006869) and euribor3m (0.084485 ± 0.002679). Joint economic sensitivity is 0.335810 ± 0.011211, ahead of previous campaign history (0.083725 ± 0.012011) and customer attributes (0.072181 ± 0.007798). These in-sample perturbation magnitudes must not replace or be added to nested feature-ablation losses.

The leading signed-within-field mean absolute SHAP log-odds contributions are emp.var.rate 0.397556, nr.employed 0.376072 and euribor3m 0.200518. Thus both methods point to macro context, while allocating correlated information differently. The dependence plots do not imply a simple economic law: emp.var.rate has negative observed value/contribution association, whereas nr.employed's association is weaker and positive here. Neither is a causal intervention response.

SHAP was reliable in this environment: maximum logit additivity error 5.33e-15 and probability reconstruction error 1.17e-15. A plotting-only FutureWarning concerned global RNG seeding; seeded jitter was reproducible in the current package version. No classifier modification or fallback was required. Example probabilities high/middle/low are 0.859851 / 0.057087 / 0.015950, selected without outcomes. All explanation observations are development rows.

B1's recency-availability coefficient is +1.737389, emp.var.rate -0.640220 and nr.employed -0.378930 on their approved transformed scales. These conditional linear signs are not causal and need not match nonlinear SHAP dependence. Rare categories, such as education=illiterate (18 cleaned records), particularly limit substantive interpretation of individual category coefficients.

## Scope, integrity and boundaries

Source merged main **92cac1f** includes Phase 7. Release-gate PASS chronology, all four frozen model hashes and archived results digests verified. Only trusted frozen P1 (Full original HGB) and B1 (Full original LR) were loaded. No training, hyperparameter/threshold selection, calibration or held-out evaluation occurred. Fit methods were blocked in this session. Every previous project file is unchanged, and both loaded estimators have unchanged in-memory joblib hashes. Held-out row-level predictions were only byte-hashed for integrity, never parsed; final reporting uses archived aggregate tables only.

All 15 predictors remain Provisional. These explanations do not establish deployment readiness. This is **in-sample descriptive explanation**: final models had already fitted all 32,940 development observations. Neither an explanation sample nor permutation repeats create independent validation.

## Predeclared development sampling and permutation method

Sample: **5000 development rows, 563 positives (0.112600)**, class-count-proportional sampling without replacement, seed 42; development prevalence 0.112659. Frozen P1 sample AP is **0.500152, in-sample**, not a replacement for nested CV or held-out AP. Sample row positions are saved under figures/data/; no held-out positions enter analysis.

Each original raw input field is permuted through the complete unchanged pipeline ten times, using default_rng(42+repeat_zero_based). A repeat's row permutation is shared across all fields/groups, giving paired perturbations. Mean AP reduction = original sample AP minus permuted AP; sample SD (ddof=1) measures Monte Carlo repeat dispersion, not a sampling/generalization confidence interval. Small/negative values are retained, not clipped. Labels and class prevalence stay fixed.

| kind | feature_or_group | mean_AP_reduction | sample_SD | minimum | maximum |
| --- | --- | --- | --- | --- | --- |
| individual | nr.employed | 0.176239 | 0.012367 | 0.153569 | 0.191672 |
| individual | emp.var.rate | 0.118862 | 0.006869 | 0.110704 | 0.130365 |
| individual | euribor3m | 0.084485 | 0.002679 | 0.079850 | 0.087501 |
| individual | recency_available | 0.060935 | 0.010651 | 0.048604 | 0.085530 |
| individual | age | 0.046798 | 0.007833 | 0.035083 | 0.062832 |
| individual | cons.conf.idx | 0.022663 | 0.002875 | 0.017913 | 0.026385 |
| individual | education | 0.018104 | 0.003620 | 0.011044 | 0.022723 |
| individual | job | 0.015972 | 0.001917 | 0.012960 | 0.019190 |
| individual | previous | 0.013001 | 0.002083 | 0.009249 | 0.016397 |
| individual | recency_days | 0.012304 | 0.002423 | 0.009449 | 0.017134 |
| individual | marital | 0.009630 | 0.003388 | 0.004396 | 0.015249 |
| individual | cons.price.idx | 0.008801 | 0.001909 | 0.005053 | 0.011219 |
| individual | default | 0.006102 | 0.001679 | 0.003065 | 0.008499 |
| individual | housing | 0.005735 | 0.001121 | 0.004228 | 0.007980 |
| individual | loan | 0.004770 | 0.001441 | 0.002371 | 0.007101 |

![Individual permutation importance](figures/09_permutation_individual.png)

**Figure 9.** Original-column permutation AP reductions; development-only in-sample; ten repeats ± repeat SD. Source: Phase 8 frozen P1.

## Joint-group permutation sensitivity

| kind | feature_or_group | mean_AP_reduction | sample_SD | minimum | maximum |
| --- | --- | --- | --- | --- | --- |
| group | Economic indicators | 0.335810 | 0.011211 | 0.312852 | 0.347088 |
| group | Previous campaign history | 0.083725 | 0.012011 | 0.069889 | 0.111219 |
| group | Customer attributes | 0.072181 | 0.007798 | 0.064194 | 0.086425 |

![Joint permutation](figures/10_permutation_groups.png)

**Figure 10.** Joint-group permutation, development-only in-sample. One shared row order moves all group columns together, preserving within-group relationships.

Economic group: emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed. History group: previous, recency_available, recency_days. Customer group: age, job, marital, education, default, housing, loan. Joint permutations preserve within-group structure but break relationships with the outcome and other groups. Individual recency-field shuffling can create impossible availability/day combinations; such AP reductions are model perturbation sensitivities, not valid customer interventions. The joint history group is more coherent for this reason. Economics are correlated and can substitute/shared-information; small individual values need not imply no joint contribution. Do not sum individual drops as the group contribution.

Phase 6A separately retuned/refit models after removing feature groups, with nested out-of-sample evaluation: HGB AP 0.448145 Full, 0.351146 without economics, 0.389129 without history, 0.232569 customer-only. Those losses (0.096999 /0.059017 /0.215576) are **not numerically interchangeable** with frozen-model in-sample permutation drops. Compare qualitative reliance only; the estimator, refitting allowance, cohort and evaluation design differ. No new ablation was performed.

## SHAP compatibility, output scale and mapping

SHAP support: **True**; version 0.50.0; issue None. SHAP was initially absent; shap0.50.0 plus numba0.63.1, llvmlite0.46.0, slicer0.0.8, tqdm4.67.1 and cloudpickle3.1.2 were installed in scratch space. Approved sklearn1.8.0/NumPy2.3.5/pandas2.2.3 and frozen files were not changed. Colab instructions pin compatible versions. Hosted Colab itself was not exercised.

TreeExplainer uses tree_path_dependent training-node cover and model_output='raw'. Binary output is **positive-class log-odds**, not probability units. Sum of base and transformed SHAP values was checked against the frozen HGB decision_function, and its logistic transform against class-1 probability. No interventional background sample or causal interpretation is claimed. Training-path reference is not the population mean probability and depends on the fitted model/training distribution.

The global explanation sample has 300 random development-sample observations (seed 42). Additional high/middle/low score-selected examples bring unique explained rows to 303; global summaries use only the random 300, not deliberately added extremes. Transformed names/order were validated against learned encoder categories and the manifest, then mapped to all 15 original fields. Mapping is saved in figures/data/13_transformed_feature_mapping.csv.

For original-field summaries, **sum SIGNED dummy SHAP values within a field per row, then compute mean absolute sums**. This preserves the local total logit decomposition, but is an aggregation of the encoded-feature game, not an exact new original-variable coalition SHAP calculation. It can cancel opposing dummy contributions; it differs from summing arbitrary mean absolute dummy values. Correlation/reference choices and off-manifold feature coalitions constrain interpretation.

| feature | mean_abs_signed_group_logodds |
| --- | --- |
| emp.var.rate | 0.397556 |
| nr.employed | 0.376072 |
| euribor3m | 0.200518 |
| cons.conf.idx | 0.102447 |
| cons.price.idx | 0.096185 |
| age | 0.070380 |
| recency_available | 0.052469 |
| previous | 0.046534 |
| education | 0.042158 |
| default | 0.034844 |
| recency_days | 0.031156 |
| housing | 0.026034 |
| job | 0.024775 |
| marital | 0.015469 |
| loan | 0.006804 |

![SHAP beeswarm](figures/11_shap_beeswarm.png)

**Figure 11.** Encoded-feature SHAP beeswarm, raw log-odds, random 300 development observations; dummy color indicates indicator values, not ordered category meaning. Source: frozen P1, Phase 8.

![Grouped signed SHAP](figures/12_shap_grouped_bar.png)

**Figure 12.** Mean absolute signed-within-original-field aggregation on the same 300 rows; not independent contribution validation.

![SHAP dependence](figures/13_shap_dependence.png)

**Figure 13.** Observed development numerical values versus signed original-field logit contributions; recency availability colors; associations, not effects of changing a customer's value.

## Representative local explanations

| example | cleaned_row_position | predicted_probability | base_log_odds | sum_contributions_log_odds | reconstructed_probability | leading_signed_contributions |
| --- | --- | --- | --- | --- | --- | --- |
| high | 40181 | 0.859851 | -2.503824 | 4.317877 | 0.859851 | nr.employed: +2.1633; recency_available: +0.5566; emp.var.rate: +0.5145; recency_days: +0.4189; euribor3m: +0.2334 |
| medium | 18081 | 0.057087 | -2.503824 | -0.300582 | 0.057087 | emp.var.rate: -0.4434; euribor3m: +0.2317; nr.employed: -0.1661; cons.price.idx: +0.0845; age: +0.0440 |
| low | 1415 | 0.015950 | -2.503824 | -1.618390 | 0.015950 | emp.var.rate: -0.4452; nr.employed: -0.3898; loan: -0.2464; education: -0.2226; cons.price.idx: -0.1377 |

Examples use only P1 predicted probability ranks and immutable cleaned-row tie breaks: high=maximum, medium=middle ordered score, low=minimum in the 5,000-row explanation sample. Observed y does not choose or validate examples. The local sum reconstructs the frozen model prediction, not why a real customer acted or what changing one attribute would cause.

![High propensity](figures/14_shap_local_high.png)

**Figure 14.** Highest-scored development example, grouped signed log-odds decomposition.

![Middle propensity](figures/15_shap_local_medium.png)

**Figure 15.** Middle-scored development example, same predeclared procedure.

![Low propensity](figures/16_shap_local_low.png)

**Figure 16.** Lowest-scored development example, not an outcome-selected example.

## Frozen B1 coefficient interpretation

All 42 transformed coefficients align exactly to approved output names. Reconstructed transformed dot-product logits and logistic probabilities match B1 outputs on development data. Intercept: -2.466572.

| transformed_position | transformed_name | original_feature | display_name | coefficient | absolute_coefficient | interpretation_unit |
| --- | --- | --- | --- | --- | --- | --- |
| 41 | recency__recency_available | recency_available | recency_available | 1.737389 | 1.737389 | one unscaled binary indicator |
| 35 | numerical__emp.var.rate | emp.var.rate | emp.var.rate | -0.640220 | 0.640220 | one training-fitted standard deviation; recency conditional on available |
| 39 | numerical__nr.employed | nr.employed | nr.employed | -0.378930 | 0.378930 | one training-fitted standard deviation; recency conditional on available |
| 5 | categorical__job_retired | job | job=retired | 0.344794 | 0.344794 | one encoded category indicator (valid substitution requires coefficient difference) |
| 8 | categorical__job_student | job | job=student | 0.317715 | 0.317715 | one encoded category indicator (valid substitution requires coefficient difference) |
| 36 | numerical__cons.price.idx | cons.price.idx | cons.price.idx | 0.285707 | 0.285707 | one training-fitted standard deviation; recency conditional on available |
| 20 | categorical__education_illiterate | education | education=illiterate | 0.275833 | 0.275833 | one encoded category indicator (valid substitution requires coefficient difference) |
| 1 | categorical__job_blue-collar | job | job=blue-collar | -0.204580 | 0.204580 | one encoded category indicator (valid substitution requires coefficient difference) |
| 18 | categorical__education_basic.9y | education | education=basic.9y | -0.185861 | 0.185861 | one encoded category indicator (valid substitution requires coefficient difference) |
| 25 | categorical__default_unknown | default | default=unknown | -0.166392 | 0.166392 | one encoded category indicator (valid substitution requires coefficient difference) |
| 7 | categorical__job_services | job | job=services | -0.162402 | 0.162402 | one encoded category indicator (valid substitution requires coefficient difference) |
| 24 | categorical__default_no | default | default=no | 0.155572 | 0.155572 | one encoded category indicator (valid substitution requires coefficient difference) |
| 40 | recency__recency_days | recency_days | recency_days | -0.154484 | 0.154484 | one training-fitted standard deviation; recency conditional on available |
| 12 | categorical__marital_divorced | marital | marital=divorced | -0.133932 | 0.133932 | one encoded category indicator (valid substitution requires coefficient difference) |
| 11 | categorical__job_unknown | job | job=unknown | -0.123288 | 0.123288 | one encoded category indicator (valid substitution requires coefficient difference) |

![LR coefficients](figures/17_lr_coefficients.png)

**Figure 17.** Largest absolute frozen B1 coefficients with sign; standardized numerical/full-one-hot representation.

A positive coefficient raises the fitted conditional log-odds holding other encoded inputs fixed; negative lowers it. Numerical coefficients refer to one training-fitted standard deviation, with recency scaling estimated only where available; availability is a separate unscaled bit. Full one-hot includes every level, so individual dummy coefficients have no omitted reference category and are regularization-dependent alongside the intercept. A valid category contrast uses the difference of category coefficients. Do not read coefficient magnitude as unadjusted original-unit importance or treat category flags as independent interventions. Correlated macro indicators can redistribute/flip conditional coefficients; signs do not establish causal economic effects. L2 shrinkage and model linearity differ from HGB's nonlinear attribution behavior.

## Validity, source timing and business implications

Explainability can reveal predictive reliance on macro context/history/customer records, not confirm campaign-start availability. Economic values can proxy shared campaign periods; correlations can distribute importance. Missing IDs/dates prevent verifying unique-customer and future-period generalization. Customer/status snapshots, history cutoff, recency reference date, economic release/revision vintage and target window remain unresolved in 10_feature_availability_matrix.md. No importance value verifies fairness, robustness, availability or causality.

For limited outreach resources, explanations help communicate the frozen ranking's information requirements and data-governance priorities. They do not recommend changing a customer's demographic/status/history to obtain a subscription, prove incrementality, justify ROI or select a new policy. The original P1 remains sole primary; archived final performance and predeclared top-10% illustrative policy remain unchanged.

Detailed sample indices, repeat-level APs, mappings, signed SHAP arrays, local records, coefficients and audit metadata are in figures/data/. Previous models/results/source files remain byte-identical. No retraining, held-out record parsing/scoring, post-test tuning, commit or push occurred. Stop after interpretation/reporting.
