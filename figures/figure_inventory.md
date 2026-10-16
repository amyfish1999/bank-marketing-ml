# Phase 8 figure inventory

| figure | filename | caption | source |
| --- | --- | --- | --- |
| 1 | 01_research_workflow.png | Research workflow: development modeling/explanations and separately gated one-time held-out evaluation. | Approved Phases 2C–8; schematic, not a new experiment |
| 2 | 02_class_distribution.png | Approved cleaned class counts from Phase 2B; no new inspection of held-out rows. | 02_data_cleaning_summary.md; archived counts |
| 3 | 03_model_comparison.png | Untuned CV and nested CV are separate designs; no nested DT estimate exists; sample SD is not a significance test. | Phases 4/4B and 5A approved summary means |
| 4 | 04_threshold_tradeoff.png | Frozen training-selected threshold policies evaluated on outer validation; connected points are policies, not an optimized test curve. | 07_threshold_decision_summary.md; development outer-fold means |
| 5 | 05_imbalance_ap.png | Symmetric-grid nested imbalance-treatment comparison; small balanced-HGB gain is not a significance conclusion. | 08_imbalance_treatment_summary.md |
| 6 | 06_feature_ablation.png | Each prespecified subset independently tuned in nested CV; ablation does not certify feature availability. | 09_feature_ablation_summary.md |
| 7 | 07_heldout_performance.png | One-time held-out point estimates and conditional 95% paired-stratified bootstrap intervals; P1 remains primary. | Stored results/heldout_metrics.csv and bootstrap_intervals.csv; no test predictions rerun |
| 8 | 08_topk_targeting.png | Fixed capacities 412/824/1648; top 10% is illustrative primary reporting, not a known bank requirement or causal uplift. | Stored results/heldout_topk.csv only |
| 9 | 09_permutation_individual.png | P1 individual raw-column permutation; development-only in-sample, ten repeats; SD is permutation dispersion, not a generalization CI. | Phase 8; frozen P1, no refitting |
| 10 | 10_permutation_groups.png | P1 joint-group permutation; development-only in-sample, ten repeats; SD is permutation dispersion, not a generalization CI. | Phase 8; frozen P1, no refitting |
| 11 | 11_shap_beeswarm.png | TreeSHAP encoded-feature beeswarm; raw log-odds for class 1; color is transformed feature value. | Phase 8; tree-path-dependent reference; development in-sample |
| 12 | 12_shap_grouped_bar.png | Mean absolute signed-within-field SHAP sums; encoded-game aggregation, not a recomputed original-variable Shapley game. | Phase 8; development in-sample |
| 13 | 13_shap_dependence.png | Observed numerical value versus signed original-field contribution; color indicates recency availability; associations, not intervention responses. | Phase 8; 300 development observations |
| 14 | 14_shap_local_high.png | Local high predicted-propensity example chosen by predeclared score rank, not observed outcome; grouped signed log-odds contributions. | Phase 8; development only; no causal intervention |
| 15 | 15_shap_local_medium.png | Local medium predicted-propensity example chosen by predeclared score rank, not observed outcome; grouped signed log-odds contributions. | Phase 8; development only; no causal intervention |
| 16 | 16_shap_local_low.png | Local low predicted-propensity example chosen by predeclared score rank, not observed outcome; grouped signed log-odds contributions. | Phase 8; development only; no causal intervention |
| 17 | 17_lr_coefficients.png | B1 coefficients on standardized numerical/full-one-hot scale; not causal effects or unadjusted original-unit importance. | Phase 8; frozen B1, alignment checked with development logits |
