# Replay the published final results in Google Colab

This is an archive viewer, not another ML experiment. It displays the approved final tables, confidence intervals and charts without loading models or individual customer records. It does not train, predict, repeat held-out testing, bootstrap, SHAP or permutation importance.

## Open and run

1. Open https://colab.research.google.com/ and choose **File → Upload notebook**. Upload `replay_final_results.ipynb` from this repository. Once this notebook is merged into main, you can also use https://colab.research.google.com/github/amyfish1999/bank-marketing-ml/blob/main/replay_final_results.ipynb .
2. Use a standard Python CPU runtime. No GPU is needed.
3. Choose **Runtime → Run all**. The first cell clones the whole public repository's main branch into `/content/bank-marketing-ml` if it is absent. Existing folders are never updated or overwritten.
4. Wait for the visible **PASS** archive check. Scroll through sections A–F: model definitions and hyperparameters; final AP/ROC-AUC and intervals; all predefined Top-K results; earlier Development research; static explanations; final interpretation.

P1 remains the sole primary scenario. Top 10% is an illustrative reporting capacity. Tables, regenerated charts and source links appear inline; the notebook does not save charts over original files. Notebook outputs can be saved using Colab's File menu.

## Private repository or ZIP

Use authorized GitHub access provided by your institution, without embedding tokens or passwords. Alternatively download one approved repository ZIP, upload it using Colab's Files panel and extract it into `/content`. Set `PROJECT_DIR_OVERRIDE` in the first code cell to its root, for example `/content/bank-marketing-ml-main`. Keep the entire folder structure, including `results/`, `models/model_manifest.json`, `figures/` and Markdown summaries. You do not need separate uploads for each file. ZIP inputs should come from trusted approved sources.

For a local checkout, set `PROJECT_DIR_OVERRIDE` to the repository's absolute path before running. The notebook otherwise looks for `bank-marketing-ml` under the current directory.

## Dependencies and provenance

Runtime dependencies are Python standard library, pandas, matplotlib and IPython. Fresh Colab normally supplies all of them; setup installs only missing packages. Neither scikit-learn, SHAP nor imbalanced-learn is needed. Git is used only for the optional clone.

Sources were verified against merged main commit `d41bd3450b17370c8f364c895f3771e5b0a093f4`. The notebook pins exact archived-file SHA-256 values rather than silently accepting a later changed result. It reads only an explicit list of aggregate CSV/JSON, documentation and PNG assets. It never opens datasets, model binaries or row-level prediction files. Source links below outputs point to that immutable approved commit.

Important sources:

- `results/heldout_metrics.csv`: final point estimates and classification results.
- `results/bootstrap_intervals.csv`: recorded conditional 95% percentile intervals.
- `results/heldout_topk.csv`: fixed capacities and captured historical subscribers.
- `results/final_selected_parameters.csv` and `models/model_manifest.json`: configurations.
- `results/evaluation_complete.json`, `results/release_gate.json`: provenance checks.
- `06_nested_cv_targeting_summary.md` through `09_feature_ablation_summary.md`: earlier aggregate research tables, preserving published precision.
- `figures/figure_inventory.md` and `figures/data/figure_inventory.json`: figure captions and experimental contexts.

## If validation fails

Stop on **FAIL**. The error names the missing or changed file. Check `PROJECT_DIR_OVERRIDE` and the extracted folder layout. Obtain a complete approved repository copy, including binary PNG files, rather than regenerating results. If a SHA-256 or aggregate interval estimate disagrees, ask the team to review the source version. Do not edit archived numbers, weaken the checks or recompute from test predictions. If the approved sources are intentionally updated in future, the notebook requires a separate reviewed provenance update.

## Interpretation

Newly drawn comparison charts use archived aggregate tables only. Explanation images are approved static Development-only, in-sample descriptions. Neither represents a fresh experiment. Bootstrap intervals are conditional on frozen fitted models and do not capture selection uncertainty or resolve temporal/customer overlap. All predictors remain Provisional. Historical subscriber capture is not causal marketing uplift or financial ROI.

## Verification performed for this notebook

All seven code cells executed successfully in a fresh temporary `content/bank-marketing-ml` directory containing only the explicit permitted archive inputs. Tables and 16 inline images rendered (two newly drawn aggregate charts plus 14 approved static images). Archive write guards and forbidden-artifact access guards passed. Missing-file and altered-file fixtures both stopped with clear errors. Static code checks found no model fitting, transformation or inference calls. All pre-existing repository files remained byte-identical. Saved outputs contain no errors. This was a local Colab-path simulation, not a hosted Colab session; automatic public cloning uses standard Git and requires network access.
