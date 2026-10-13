# Phase 1 EDA summary

Scope: descriptive EDA only; no models, row removal, encoding, scaling, SMOTE or final preprocessing. Notebook executed successfully against the supplied CSV. Dataframe and original file integrity checks passed.

Sources reviewed: README.md and dataset.csv. MSI5001 Project Bank Telemarketing.docx was absent; its requirements remain unverified.

## Observed findings
- 41,188 rows, 20 columns: 19 predictors plus y. README describes 20 predictors plus y, a schema discrepancy requiring clarification.
- y=0: 36,548 (88.7346%); y=1: 4,640 (11.2654%). No unknown targets.
- No pandas-null values. Unknown job: 330; marital: 80; education: 1,731. Encoded unknown (-1): default 8,597; housing 990; loan 990. These integer columns are categorical statuses.
- pdays=999: 39,673 (96.32%), meaning not previously contacted per README. Actual recency exists for 1,515 records. Do not interpret the overall pdays mean as average elapsed days.
- 12 exact duplicates beyond first occurrences; record identity cannot be verified without client IDs. No identical-predictor groups have conflicting targets.
- 4,110 records have previous>0 and pdays=999. Clarify history scope before treating this as an error. No previous=0 records have actual recency.
- Age spans 17–98; campaign 1–56; duration 0–4,918 seconds. Four duration=0 rows all have y=0. Extremes are not proven errors.
- Sparse categories: default=1 occurs 3 times; illiterate education 18 times. January/February are absent; only ten months appear.
- Economic correlations: employment variation/Euribor 0.972; Euribor/number employed 0.945; employment variation/number employed 0.907. Shared period indicators warrant redundancy and temporal checks.

## Leakage and interpretation
Duration is unavailable before the call and is a documented leakage risk for pre-call prediction. EDA retains it solely for inspection. Last-call campaign count/month/day/channel also need an availability audit against the intended prediction time. Economic publication timing, repeat clients and period overlap may affect later evaluation; dates/year/client IDs are unavailable.

Notebook includes semantic feature dictionary, every-column missing/sentinel audit, domain checks, duplicate review, distributions of all numerical/categorical predictors, outcome-stratified boxplots, categorical rates with group sizes and Wilson intervals, focused age/campaign/pdays plots, socioeconomic analysis and a data-quality treatment-proposal table. Plot bins/subsets do not modify the dataset.

## Hypotheses, not established conclusions
Age/customer mix, economic regime and contact selection may explain observed response-rate differences. Associations do not establish causality, an optimal contact frequency or predictive performance. Wilson intervals assume independence, which may not hold.

## Team approvals needed
Define prediction time and duration policy; resolve schema/source brief/history semantics; decide unknown/sentinel representation, categorical encoding, rare groups, scaling/transformations, duplicate/extreme handling, temporal/client/stratified split design, held-out size and five-fold validation, metrics/business costs/thresholds, imbalance strategy, model families/tuning and economic feature selection. Any future learned treatments must be confined to training folds. None are implemented here.

## Running in Colab
Open 01_eda.ipynb in Colab and run all cells; upload the unchanged dataset.csv when prompted, or set DATA_PATH to a mounted Drive path. Required analysis packages are included in standard Colab. Runtime analysis is recomputed from the loaded file; static findings refer to the supplied dataset.

Source CSV SHA-256: 81fd5eb4b659dddbc704edd90376c32714c3f6a43b887cb686762903bc793f0d
