# Final university presentation outline — 15 slides

Based on 14_final_academic_report.md and preserved approved sources. No explicit course slide-count requirement was found in the supplied planning DOCX; fifteen slides satisfy the requested range. All final test figures use archived aggregates, and all new explanations use development data only. P1 remains sole primary; every predictor remains Provisional.

## Slide 1 — Research question and academic scope

**Main message:** Can frozen models rank historical term-deposit subscribers while making leakage risks explicit?

- Predict subscription propensity before a proposed campaign start.
- P1 Full HGB is the sole primary academic scenario.
- All 15 predictors remain Provisional; no verified deployment or causal claim.

**Suggested visual:** Figure 1: figures/01_research_workflow.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Open with the distinction between prediction and intervention. The project concerns subscription propensity in a historical marketing cohort. It does not identify which customers subscribe because of a call. Explain that the original aim is pre-campaign prioritization, but the supplied records lack the timing evidence needed to certify that use. P1 was designated primary before the final test. The report is a completed academic comparison, not a proposal to tune a model further on its final outcomes. This framing should remain visible when presenting attractive scores or the 412-subscriber result.

## Slide 2 — Dataset and class imbalance

**Main message:** A strong accuracy number can conceal failure to identify subscribers.

- Raw: 41,188 records; cleaned: 41,176.
- Cleaned subscribers: 4,639 (11.2663%); non-subscribers: 36,537.
- Dummy accuracy 0.887341, but recall/F1=0 and AP=0.112659.

**Suggested visual:** Figure 2: figures/02_class_distribution.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Use the class chart to motivate AP and ranking rather than accuracy alone. The majority-class baseline predicts no for every customer and is almost 89% accurate, yet finds no subscribers. State that the counts shown come from archived approved summaries, not new inspection of test rows. Explain the 12-row approved duplicate removal and that the README headline incorrectly says 21 columns while the supplied file has 20. Do not suggest that duplicate removal establishes unique customers: customer identifiers are unavailable. The class imbalance is an observed property, not proof that automatic resampling is required.

## Slide 3 — Leakage-aware feature design

**Main message:** Removing obvious call-time variables reduces exposure but does not verify retained fields.

- Exclude duration, current campaign/contact timing fields and original pdays.
- Preserve unknown categories and approved recency indicator/day representation.
- Customer snapshots, history cutoff and economic release vintages remain unresolved.

**Suggested visual:** Feature-contract table in report Sections 5/10; Figure 1. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Duration cannot be known before a call and is excluded. Campaign count includes current activity; contact/month/day-of-week are not established at campaign start. Describe pdays=999 as unavailable recency under the approved representation, paired with a separate indicator rather than a literal elapsed-day value. All 4,110 previous-positive/sentinel cases remain. The remaining features are not automatically safe: economic values might reflect later releases or campaign periods, and status/history records might have been updated later. Distinguish documented meanings from verified observation and availability times.

## Slide 4 — Split, pipelines and nested validation

**Main message:** Every fitting operation stays within its authorized development partition.

- Fixed saved development 32,940 / held-out 8,236; no new split.
- OHE/scalers fit within complete CV pipelines; conditional recency uses available rows only.
- Five outer and five inner stratified folds; final PASS gate before test opening.

**Suggested visual:** Figure 1: figures/01_research_workflow.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Walk through the separation of design and evaluation. The saved split is hash-bound to row order. Inner CV selects hyperparameters by AP, while outer folds evaluate the selection procedure. Encoders and scalers are never fitted on all development before CV. The final selected pipeline may fit all development only after selection; this does not permit held-out fitting. In Phase 7, 190 candidate-fold fits and four final development refits were completed. Four frozen artifacts reloaded identically on development fixtures and the release gate was saved before the one-time test parser. Random folds still cannot certify customer or temporal independence.

## Slide 5 — Candidate model comparison

**Main message:** Algorithm comparisons must retain their experimental-design labels.

- Untuned AP: HGB 0.439412; LR 0.422181; RF 0.361307; DT 0.180763.
- Tuning-selected CV may be optimistic because the folds selected the configuration.
- Nested CV supplies a separate outer evaluation of the fixed searches.

**Suggested visual:** Figure 3: figures/03_model_comparison.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Show the two panels separately rather than mixing their bars into one ranking. LR supplies a cheap linear reference, DT explicit rules, RF an ensemble of trees, and HGB nonlinear boosted-tree flexibility. Complexity was evaluated rather than assumed better. Explain why a best selected-CV score is not independent performance: it has been optimized using those folds. DT has no Phase 5A nested result and should not be shown as zero or compared as if it does. Historical timing measurements provide context only, because scoring and audit overhead and runtime conditions differ.

## Slide 6 — Why original HGB was shortlisted

**Main message:** HGB leads the nested AP comparison, with a small margin over RF.

- Nested AP: HGB 0.448145; RF 0.443930; LR 0.422429.
- HGB minus RF = 0.004215; RF leads one outer fold.
- P1 was frozen as sole primary; no statistical-significance or deployment claim.

**Suggested visual:** Figure 3 nested panel; Phase 5A table in report Section 8. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Interpret the measured advantage at the scale of fold variability. HGB sample SD is 0.014219 and RF SD is 0.018936, and the overlapping training folds are not independent trials. A small mean difference does not establish significance. HGB also captured 1,628 historical subscribers at pooled development top 10%, compared with RF 1,588 and LR 1,564 among 3,294 contacts. These are development diagnostics across separately fitted outer models. The shortlist incorporated ranking, targeting and interpretability considerations before final testing, and did not mean that all timing concerns had been resolved.

## Slide 7 — Threshold policy trade-offs

**Main message:** Changing decisions can improve recall/F1 without improving ranking.

- HGB recall: 0.218813 at .50 to 0.586634 under training-F1 selection.
- Precision falls 0.667746 to 0.428506; F1 rises 0.329222 to 0.495146.
- AP/ROC-AUC stay unchanged; policies contact different numbers of records.

**Suggested visual:** Figure 4: figures/04_threshold_tradeoff.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Explain that thresholds were fitted only from outer-training-side probabilities and frozen before outer evaluation. The F1 rule selects a larger positive group, raising recall at a precision/contact-volume cost. It does not make probabilities rank subscribers better. A separate illustrative precision-constrained rule selected .35 in original-model folds but did not establish a future lower precision guarantee. Neither these fold thresholds nor full-feature thresholds were copied to reduced final models. The final protocol retained .50 as a reference and fixed-capacity ranking for business reporting, without new held-out threshold optimization.

## Slide 8 — Class weighting and undersampling

**Main message:** Imbalance correction did not consistently beat the original threshold-only strategies.

- Balanced HGB AP 0.450883 versus original 0.448145.
- Equal-capacity capture change: +13 / -18 / -6 at 5% / 10% / 20%.
- HGB undersampling AP 0.436259; original unweighted models retained.

**Suggested visual:** Figure 5: figures/05_imbalance_ap.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Present balancing as an empirical question. The AP gain was small, and targeting gains depended on capacity rather than being uniformly positive. Random undersampling discarded majority information and performed worse in the tested HGB configuration searches. Both LR treatments lowered mean AP. Weighted/sampled scores shifted enough that F1 thresholds reached the approved grid boundary and the illustrative precision constraint was infeasible within that grid. This does not prove no higher threshold could work, but no post-result expansion was made. The conclusions apply to the tested full-feature grids, not every possible imbalance method or reduced feature set.

## Slide 9 — Feature ablation and availability

**Main message:** Information requirements materially change predictive performance.

- HGB nested AP: Full 0.448145; no economics 0.351146.
- No history 0.389129; customer-only 0.232569.
- All retained fields remain Provisional; ablation is not timing verification.

**Suggested visual:** Figure 6: figures/06_feature_ablation.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Each subset received its own inner AP search rather than inheriting the full-feature winner. Removing economics or previous campaign information therefore measures the performance of a different permitted information set with retraining. Losses need not add because predictors share information and interact. At development top 5%, no-economics HGB can capture more than no-history HGB despite lower overall AP, showing why capacity matters. The feature contract, not the largest score, determines whether inputs could be used prospectively. Customer-only is conservative in information requirements but still needs verified snapshot and outcome timing.

## Slide 10 — Final held-out performance

**Main message:** The frozen primary scenario retains its historical ranking advantage on this cohort.

- P1 AP 0.451334; ROC-AUC 0.807608.
- S1 AP 0.230981; B1 AP 0.431032; B2 AP 0.200407.
- P1 remains primary; 2,000 paired stratified metric-bootstrap intervals are conditional.

**Suggested visual:** Figure 7: figures/07_heldout_performance.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** These values are read from the frozen Phase 7 aggregates; no test probabilities were regenerated. P1 AP interval is 0.420577–0.485339 and ROC-AUC interval 0.790575–0.824540. P1 nested AP was 0.448145, close to its test value, but that proximity does not establish future-campaign validity. Customer-only HGB AP was 0.232569 in nested development and 0.230981 on test. The models trained on more development data for the final refit than in outer-fold training. Bootstrap intervals omit model-selection uncertainty and unknown customer/time clustering, so avoid significance or guaranteed-future-performance language.

## Slide 11 — Fixed-capacity customer targeting

**Main message:** An illustrative 10% capacity identifies 412 historical subscribers among 824 selected records.

- P1 top 10%: precision 50.00%, recall 44.40%, lift 4.44.
- P1 top 5%: 248/412; top 20%: 610/1,648.
- 412 subscribers were identified historically, not caused by the marketing policy.

**Suggested visual:** Figure 8: figures/08_topk_targeting.png. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** State the denominator before the numerator: the policy selects 824 records, of which 412 were historical subscribers. It does not create 412 subscriptions. Top 10% is a study scenario rather than a confirmed bank capacity. Full LR captures 396 and customer-only HGB 224 at the same 824 contacts. Broader contact capacity captures more subscribers while lowering precision in these archived results. A bank with limited resources can enforce a count directly through ranking; a fixed .50 probability cutoff does not guarantee that count. No costs, incremental value or experimental treatment effects support a financial ROI estimate.

## Slide 12 — Frozen-model explainability

**Main message:** Macroeconomic reliance is descriptive and carries an availability obligation.

- Development sample: 5,000 rows; P1 in-sample AP 0.500152, not validation.
- Largest permutation fields: nr.employed, emp.var.rate, euribor3m; economic group drop 0.335810.
- SHAP reconstructs class-1 log-odds/probabilities; aggregation and correlation limits are explicit.

**Suggested visual:** Figures 9/12: figures/09_permutation_individual.png and figures/12_shap_grouped_bar.png; optional local Figure 14. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Emphasize the in-sample label before showing importance. The final HGB already fitted all development observations. Ten repeats assess perturbation dispersion, not out-of-sample uncertainty. Joint economic permutation moves the five indicators together, preserving internal correlation but breaking their other associations. Individual recency shuffling can create inconsistent day/availability pairs. TreeSHAP uses a training-path reference and raw log-odds; signed dummy contributions are summed within each field before taking mean absolute values. This preserves local totals but is not a newly computed original-field coalition game. The same three macro fields lead both methods, although order differs. No explanation proves causal economic influence.

## Slide 13 — Practical implications and information governance

**Main message:** The model may support academic prioritization only under clearly stated source assumptions.

- Verify customer snapshots, prior-history cutoff and recency reference date.
- Obtain economic release/revision vintages and define campaign start/outcome window.
- Keep fixed primary/secondary scenarios and separate prediction from outreach incrementality.

**Suggested visual:** Feature-availability matrix in report Section 10; Figure 1 handoff. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Translate importance into data-governance priorities rather than customer interventions. If the model relies heavily on economic context, the team needs proof that the exact retained vintage was accessible at the intended scoring time. A useful predictor may still be invalid for the operational objective. The customer-only scenario estimates a stricter information requirement at lower performance; it is not an automatic deployment substitute. Any real decision policy also needs capacity, costs, operational constraints and prospective validation. Those inputs were not supplied, and this study does not silently invent them or change the frozen model in response to the test.

## Slide 14 — Limitations and future research

**Main message:** Random stratification and precise intervals cannot repair missing temporal/customer evidence.

- No customer IDs/campaign timestamps; repeated-client and shared-period overlap possible.
- All features Provisional; prior full-data EDA/development selection exposure persists.
- Bootstrap is conditional; explainability is in-sample and non-causal.

**Suggested visual:** Concise limitations table from report Section 15; avoid a new quantitative claim. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Keep limitations prominent rather than apologetic fine print. Preprocessing isolation is a real technical safeguard but does not verify feature timing. Row-wise bootstrap preserves class counts and can underestimate uncertainty when customers or periods cluster. Earlier full-data EDA and repeated development exploration qualify any pristine-holdout claim, even though no test-informed model fitting occurred. Explanations are also reference/sample dependent and can allocate correlated information differently. Future work should obtain timestamped lineage and identifiers, conduct genuinely independent forward/group validation and study actual outreach incrementality. These are separate future studies, not extra experiments on the now-exposed test set.

## Slide 15 — Conclusion and academic handoff

**Main message:** The study delivers a reproducible historical ranking comparison, not a deployment or causal claim.

- P1: test AP 0.4513, ROC-AUC 0.8076; 412/824 top-10% historical capture.
- Customer-only HGB AP 0.2310 quantifies the information-requirement trade-off.
- Frozen artifacts, source-labelled figures, report and limitations support transparent academic review.

**Suggested visual:** Figure 7 plus three-number callout from archived Phase 7 aggregates. Use the numbered source/context caption from the report or figures/figure_inventory.md.

**Speaker notes:** Close by repeating the exact meaning of the headline findings. P1 remains the sole primary because it was chosen before final evaluation, and all four scenarios are reported rather than choosing a new test winner. The result is reproducible from preserved artifacts and aggregates. Macroeconomic/history information improves historical prediction, while explainability makes its importance and provenance obligations visible. The proposed ten-percent reporting capacity is illustrative. Do not say the calls generated the captured subscriptions or that performance is deployment-ready. Invite questions about validation design, the availability contract and causal limitations rather than offering post-test tuning or operational ROI estimates.

## Presentation quality checks

Distinguish untuned/tuning-selected/nested/threshold/ablation/held-out designs by slide label. Show conditional 95% intervals without significance-winner language. Keep the Development/in-sample label visible on explanation figures. Never call 412 a causal incremental gain, top 10% a bank requirement, or any Provisional scenario deployment-ready. Use exact archived values behind rounded slide numbers; all figures have numbered captions and sources in the report/inventory. Do not add a PowerPoint file, rerun evaluation or start new model development.
