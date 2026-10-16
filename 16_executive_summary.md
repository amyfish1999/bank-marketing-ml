# Executive summary — MSI5001 Bank Telemarketing study

**Objective.** Predict historical term-deposit subscription and assess fixed-capacity customer prioritization while documenting leakage risks. This is an academic study, **not verified deployment-ready pre-campaign targeting**. All 15 predictors remain Provisional.

**Data and methods.** Approved cleaning reduced 41,188 raw records to 41,176, including 4,639 subscribers (11.2663%). A saved stratified split reserved 32,940 development and 8,236 held-out rows. Complete pipelines kept encoding/scaling within fitting partitions. LR, DT, RF and HGB were compared; nested CV, training-selected thresholds, imbalance treatments and four feature-availability scenarios informed a protocol fixed before final testing. Exactly 194 final development fits preceded a saved PASS gate and one four-scenario test batch. Phase 8 adds only development explanations and aggregate reporting.

**Final archived outcomes.** Full original HGB (P1) remains the sole primary. Other scenarios are secondary, not test-selected replacements.

| Scenario | Held-out AP | Held-out ROC-AUC | Historical subscribers at top 10% (824 contacts) |
| --- | ---: | ---: | ---: |
| P1 Full HGB | 0.451334 | 0.807608 | 412 |
| S1 Customer-only HGB | 0.230981 | 0.669764 | 224 |
| B1 Full LR | 0.431032 | 0.777331 | 396 |
| B2 Customer-only LR | 0.200407 | 0.648536 | 190 |

P1 top 10% precision is 50.00%, recall 44.40% and predictive lift 4.44. Top 5% identifies 248 among 412; top 20% identifies 610 among 1,648. Ten percent is an illustrative reporting capacity, not an established bank requirement. Captured subscribers are historical identifications, **not subscriptions caused by calls**. No financial ROI is estimated.

**Methodological findings.** HGB nested AP 0.448145 exceeded RF0.443930 and LR0.422429 without a significance claim. Training-side threshold selection improved HGB recall/F1 at a precision/volume cost, not AP/ROC-AUC. Balanced HGB gains were small and capacity-dependent; undersampling generally reduced ranking quality. Removing economics/history reduced nested AP, and customer-only performance was substantially lower.

**Explanations.** Frozen P1 permutation analysis used 5,000 development rows and 10 repeats; macroeconomic indicators dominated, with joint economic AP reduction0.335810. This is **in-sample descriptive sensitivity**, not validation. TreeSHAP logit/probability reconstruction passed; its leading fields were emp.var.rate, nr.employed and euribor3m. Signed dummy aggregation, correlation and reference limits are documented. Frozen LR coefficients provide a conditional linear contrast, not causal intervention effects.

**Uncertainty and limitations.** P1 recorded 95% bootstrap intervals are AP [0.420577, 0.485339] and ROC-AUC [0.790575, 0.824540]. These 2,000 paired stratified metric-bootstrap intervals condition on fitted models/class balance; they do not resolve model selection, customer/time overlap or future shift. Missing IDs, campaign dates, snapshot/history reference times, economic publication vintages and outcome-window metadata prevent prospective claims. Prior full-data EDA and development exploration also limit independence.

**Implications.** Prioritize source/time verification, independent future/group validation and real capacity/cost objectives before any operational consideration. Causal outreach value requires separate evidence. Frozen models/results are unchanged; no retraining, held-out re-evaluation, post-test tuning or new predictive experiment occurred. The package includes the explainability notebook/summary, standalone report, 15-slide outline and 17 source-labelled figures. No PowerPoint, commit or push was created.
