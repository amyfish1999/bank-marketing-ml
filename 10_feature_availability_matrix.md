# Phase 6B — Feature availability contract and evidence matrix

Version 1.0 proposed for team approval, 16 October 2026 (Asia/Singapore). Source: merged main `7d8678d`. Companion: [final model-selection plan](10_final_model_selection_plan.md). This document records requirements and evidence; it does not verify missing timestamps, alter predictors or authorize held-out access.

## Contract and status definitions

The proposed prediction time **t0** is the instant the bank freezes the eligible outreach cohort and scores it before the current campaign's first marketing action. The bank must confirm campaign identity, start time/timezone, cohort eligibility, scoring frequency and whether historical rows represent customers, contacts or campaign episodes. No such operational definition or row-aligned timestamps are supplied. A timestamp before a customer's last call is insufficient evidence of availability before campaign start.

A predictor must have both an effective/reference date appropriate to t0 and evidence that its recorded value was accessible to the bank by t0. Later corrections, publications, backfills and retrospective status changes must not enter a reconstructed historical snapshot. No existing values will be recomputed, lagged or replaced under this planning phase.

- **Verified:** row-aligned source lineage and effective/availability timestamps establish the retained value was usable at t0, with data-owner confirmation. A variable definition, approval to experiment, or good CV score does not qualify.
- **Provisional:** meaning/representation is documented but availability at t0 is not established. It may be used only in explicitly conditional academic/historical scenarios with approved limitations.
- **Excluded:** omitted from a particular scenario or from the approved predictor universe. Scenario exclusion does not imply the source field is erroneous or unusable in every setting.

**Current result: all 15 predictors are Provisional; none is Verified.** No current feature set supports a verified deployment-readiness claim without the relevant evidence. The status column below describes the approved predictor universe; the scenario definitions separately identify exclusions.

## Evidence references

- **R:** [README.md](README.md), Feature Categories, Missing Values and Duration Caveat: meanings, coding and economic frequencies; no as-of timestamps or publication vintages.
- **C:** [02_data_cleaning_summary.md](02_data_cleaning_summary.md), Unknown-value handling, recency representation and unresolved timing: approved deterministic mapping/formulas and preserved history cases.
- **P:** [03_preprocessing_summary.md](03_preprocessing_summary.md), Feature availability table and final review, and [preprocessing.py](preprocessing.py): all variables Provisional; approved fitting behavior, not source-timing proof.
- **A:** [09_feature_ablation_summary.md](09_feature_ablation_summary.md), feature definitions and availability analysis: predictive sensitivity only.
- **D:** `MSI5001 Project Bank Telemarketing .docx`: asks for defensible preprocessing and separate development/final evaluation; does not supply row-level time provenance.

## All 15 predictors

| Retained variable | Original variable name | Meaning | Required availability time | Potential timing/leakage concern | Existing project evidence | Missing evidence needed for verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| age | age | Age in years | Customer-record age effective and accessible at t0 | Age may be measured at a later record/contact date | R gives age meaning; C preserves values; P/A mark timing unresolved | Age reference date or permitted DOB-to-age rule, record capture/availability dates and t0-aligned snapshot | Provisional |
| job | job | Job/occupation category | Latest valid occupation snapshot known by t0 | Later occupation update/backfill or unknown status reflecting later collection | R categories; C preserves exact categories/unknown; P | Effective and ingestion dates, source history, snapshot identity and data-owner confirmation | Provisional |
| marital | marital | Marital category; divorced includes widowed in documentation | Status effective and accessible by t0 | Later marriage/divorce/widowhood update | R definition/category caveat; C retains values; P | Status change/capture dates and t0 snapshot | Provisional |
| education | education | Education category | Recorded education known by t0 | Retrospective attainment or completion of missing records | R categories; C retains unknown; P | Record effective/availability dates, update history and t0 snapshot | Provisional |
| default | default | Whether credit is in default; unknown is a category | Credit-status snapshot available by t0 | Later delinquency/outcome-related update; unknown can reflect collection timing | R codes -1/0/1; C relabels unknown/no/yes without imputation; P | Default-status definition, assessment/effective date, report delivery date, revisions and t0 snapshot | Provisional |
| housing | housing | Whether customer has a housing loan | Loan-status snapshot accessible by t0 | Loans initiated/closed after t0 or later database refresh | R codes/meaning; C relabels unknown/no/yes; P | Loan-state effective dates, source refresh/availability dates and t0 snapshot | Provisional |
| loan | loan | Whether customer has a personal loan | Loan-status snapshot accessible by t0 | Post-start loan change/backfill | R codes/meaning; C relabels unknown/no/yes; P | Loan-state effective dates, source refresh/availability dates and t0 snapshot | Provisional |
| previous | previous | Count of contacts before this campaign | Only eligible prior-campaign events strictly before t0, count available by t0 | Current/future events accidentally included; campaign boundaries/history scope unknown | R says contacts before current campaign; C retains all 4,110 previous>0/pdays=999 records; P | Campaign IDs, event timestamps, counting scope, extraction cutoff and snapshot availability; explanation of mixed-history scope | Provisional |
| emp.var.rate | emp.var.rate | Quarterly employment variation rate | Relevant historical release actually published/accessible by t0 | Quarter's eventual value or revised release may postdate t0; period proxy across random folds | R quarterly frequency; P/A identify vintage concerns | Reference period, first-release timestamp, revision vintages, source and t0 as-of join/approved lag evidence | Provisional |
| cons.price.idx | cons.price.idx | Monthly consumer price index | Release available by t0, using the then-known vintage | Current-month final/revised index may not yet have been published | R monthly frequency; P/A | Reference month, release/ingestion dates, revisions and historical as-of mapping | Provisional |
| cons.conf.idx | cons.conf.idx | Monthly consumer confidence index | Release accessible by t0 | Publication lag/revision or later campaign-period value | R monthly frequency; P/A | Survey/reference period, publication/availability timestamps, revision history and t0 mapping | Provisional |
| euribor3m | euribor3m | Daily three-month Euribor rate | Published fixing accessible before scoring at t0 | Same-day fixing may publish after scoring; later-day rate or corrected fixing | R daily frequency; P/A | Fixing date/time/timezone, publication/availability time, correction policy and t0 lookup | Provisional |
| nr.employed | nr.employed | Quarterly number-employed indicator | Historical release/vintage accessible by t0 | Later quarterly estimate/revision and shared-period overlap | R quarterly frequency; P/A | Reference quarter, publication/availability and revision dates, source units and t0 as-of mapping | Provisional |
| recency_available | pdays (derived; original pdays is excluded) | 1 iff original pdays !=999; otherwise 0, indicating available recency | Historical-recency snapshot and its availability known by t0 | Recency availability may be defined at a later contact; unavailable does not prove never contacted | R pdays definition/sentinel; C exact formula and 4,110 retained mixed-history cases; P preserves binary indicator | pdays reference/capture date, history cutoff/scope, sentinel definition and t0-aligned snapshot | Provisional |
| recency_days | pdays (derived; original pdays is excluded) | Original elapsed days if available; otherwise fixed 0 placeholder | Elapsed interval must refer to t0, derived from eligible earlier contact known by t0 | Days computed relative to later call; real zero-day interval differs from unavailable placeholder | C formula, actual-zero distinction, 0–27 observed range; P approved conditional scaler; A | Reference timestamp, last qualifying contact timestamp, rounding/timezone rule, capture time and t0-aligned lineage | Provisional |

Unknown categories are retained as approved; treating them as categories does not establish when their missingness was recorded. Recency availability is not a replacement for `previous`: mixed history was preserved deliberately, not corrected as an error. Original 999 is never a numeric elapsed-day input. Evidence of a feature's frequency or semantic definition establishes neither publication timing nor row-specific availability.

## Cross-cutting evidence required

| Requirement | Proposed contract | Evidence currently available | Unresolved evidence / approval |
| --- | --- | --- | --- |
| Campaign start | One bank-defined t0 before first current-campaign marketing action, with campaign ID/timezone and cohort definition | Project objective; R distinguishes current/prior contacts | No row-level campaign IDs/start dates or scoring schedule; bank/data owner must define them |
| Prior history cutoff | Include only approved historical campaigns/events strictly before t0 and accessible by scoring; distinguish event time from ingestion time | R `previous`/`pdays` meanings; C preserved representation | No event ledger, cutoff, historical scope or row-aligned availability evidence |
| Recency reference | Elapsed days anchored to t0 under an approved rounding rule; original cleaned representation otherwise remains frozen | C deterministic formulas; P transformation tests | No reference-date metadata; do not assume last-contact reference equals campaign start |
| Economic vintage | Use only releases available at t0, with period/release/revision/ingestion lineage | R indicator frequencies | No vintage archive or historical as-of join. Obtaining evidence does not authorize silently replacing frozen CSV values |
| Customer/status snapshots | Effective values and unknown states accessible by t0 | R variable meanings; C/P representations | No transaction-time/effective-time snapshots or update history |
| Outcome window | Define subscription endpoint, window (t0, t0+H], eligible population, existing subscribers and follow-up/censoring before claims of prospective prediction | R defines y as term-deposit subscription; D requires held-out evaluation | H, label construction date, current/prior subscriptions and follow-up completeness are unspecified; do not invent a horizon or relabel y |
| Evaluation unit | Preserve frozen CSV rows for this academic evaluation; do not equate row IDs with unique customers | Saved positional split and approved duplicate removal | Customer IDs/campaign timestamps missing; repeated-client/time overlap cannot be ruled out |

The proposed outcome interval is a requirement to confirm, not an assertion that existing y was constructed that way. If the label window or source timing cannot be established, retain the historical binary-outcome interpretation and state that prospective campaign-start validity is unresolved.

## Exact conditional feature groups

Order is the approved input order filtered to group membership, not alphabetic order. All six categorical variables remain present in each group.

| Group | Ordered input columns | Count | Conditional recommendation |
| --- | --- | --- | --- |
| Full | age, job, marital, education, default, housing, loan, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, recency_available, recency_days | 15 | Operational candidate only if customer, history and economic inputs and label contract are verified; otherwise explicitly conditional historical/academic reference |
| No Economic Indicators | age, job, marital, education, default, housing, loan, previous, recency_available, recency_days | 10 | Candidate if customer/history evidence is verified and economic evidence is not; does not resolve history timing |
| No Previous Campaign History | age, job, marital, education, default, housing, loan, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed | 12 | Candidate if customer/economic evidence is verified and history is not; does not resolve economic publication timing |
| Customer Attributes Only | age, job, marital, education, default, housing, loan | 7 | Conservative information-requirement sensitivity; operational candidacy still requires verification of all seven snapshots and the label contract |

Currently no group qualifies as verified deployment-ready. These conditional recommendations depend on external evidence obtained before final protocol approval, not held-out scores. The companion plan proposes Full HGB as the primary conditional academic scenario and Customer Attributes Only HGB as the conservative sensitivity. The middle two groups remain development-evidence alternatives, not automatically added held-out experiments. Any amendment must precede test access and fix scenario roles in writing.

## Exclusions already approved

| Original field | Status | Reason / scope |
| --- | --- | --- |
| duration | Excluded | Last-call duration is unavailable before the call; not reintroduced even for final academic scoring |
| campaign | Excluded | Count includes current-campaign contacts; incompatible with the stated pre-start objective without a different definition |
| contact, month, day_of_week | Excluded | Last/current contact mode and timing not established before campaign start; no new timing features |
| pdays | Excluded as original predictor | Replaced by the two approved recency fields; 999 is not actual elapsed days |

## Required sign-off and change control

The team/data owner must record evidence references, row coverage, t0/outcome definitions, source vintages, remaining exceptions, reviewer and approval date before promoting a field to Verified. No reviewer or verification date is invented here. Academic use of Provisional features requires explicit acknowledgment of the research-only interpretation; it does not change their status.

Availability evidence can narrow the pre-test shortlist, but an ablation result, large AP or small CV SD cannot verify availability. If evidence contradicts retained values, stop and document a separate data/protocol revision before any held-out access. Do not repair, rederive, drop held-out rows or switch scenarios after outcomes are seen. Approval of these documents does not by itself run fitting or authorize deployment.
