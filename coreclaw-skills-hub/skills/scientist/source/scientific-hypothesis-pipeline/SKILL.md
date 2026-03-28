---
name: scientific-hypothesis-pipeline
description: |
 's（researchdata）fromhypothesis、
 verificationfor's analysispipelineautomatedgeneratesskill。PICO/PECO frameworkby/via
 hypothesisstructure、testing'sselection、pipelinegeneration is performed。
 「hypothesis」「's data？」「analysispipeline」 。
---

# Scientific Hypothesis-Driven Pipeline Generator

inputfromresearchhypothesis、
hypothesisverificationforallanalysispipelineautomatedgeneratesskill。

## When to Use

- research and data's overview input and
- datafromverificationpossiblehypothesiswhen needed
- hypothesisanalysispipelineautomatedconstructionwhen needed
- search/explorationdataminfromhypothesistype's minwhen needed
- researchdesign's support and

## Quick Start

## 1. analysis and hypothesis

```

 ├─ Phase 1: analysis
 │ ├─ research'sextraction
 │ ├─ data's typestructure's
 │ └─ number/count（）'s
 ├─ Phase 2: hypothesis
 │ ├─ PICO/PECO frameworkstructure
 │ ├─ null hypothesis (H₀) / alternative hypothesis (H₁) 's formula
 │ └─ multiplehypothesis's
 ├─ Phase 3: pipelinedesign
 │ ├─ skill's selection
 │ ├─ testing'sselection
 │ └─ sample sizepower's also
 └─ Phase 4: generation
 ├─ scientific-pipeline-scaffold 'sgeneration
 ├─ each Step correspondingskill's
 └─ JSON summaryhypothesisverificationresults
```

## 2. analysistemplate

'sfrombelow/following's element is extracted。

```markdown
## analysis

### input
> ['s input 's]

### extractionelement

| Element | Description |
|---|---|
| **research** | [min → min] |
| **research** | [data] |
| **number/count (X)** | [conditiongroupminnumber/count] |
| **number/count (Y)** | [measurementnumber/count] |
| **** | [covariates] |
| **datatype** | [ / / time series / / ] |
| **sample size** | [knowncase。] |
| **comparisonstructure** | [2group / group / / correlation / regression / classification] |
```

## 3. PICO/PECO frameworkby/viahypothesisstructure

```markdown
## hypothesisstructuretemplate

### PICO (intervention research)
| Element | Definition | Entry |
|---|---|---|
| **P** (Population) | | [example: 2024synthesis Ti-6Al-4V ] |
| **I** (Intervention) | | [example: temperature 500-900°C ] |
| **C** (Comparison) | comparison | [example: (as-cast) ] |
| **O** (Outcome) | | [example: (HV)] |

### PECO (observationresearch)
| Element | Definition | Entry |
|---|---|---|
| **P** (Population) | | [example: cancerpatient (n=500)] |
| **E** (Exposure) | factor | [example: 's (Shannon index)] |
| **C** (Comparison) | comparison | [example: group] |
| **O** (Outcome) | | [example: 5rate] |

### hypothesis's formula
**researchhypothesis (H₁)**: [PICO/PECO 's I/E O significant items]
**null hypothesis (H₀)**: [I/E O （）]

### hypothesis（）
- H₁ₐ: [hypothesis 1]
- H₁ᵦ: [hypothesis 2]
```

## 3.1 hypothesisdefinition's filesave

hypothesispoint 、below/following's 2 shapeformula file.
than 、's pipelinepaperwriting hypothesis referencepossible.

### 3.1.1 Markdown shapeformula（）

`docs/hypothesis.md` save.

```python
def save_hypothesis_markdown(hypothesis, filepath=None):
 """
 hypothesisdefinition Markdown fileassave.
 
 Args:
 hypothesis: dict — HYPOTHESIS definition
 filepath: Path — save（: docs/hypothesis.md）
 """
 import datetime
 
 if filepath is None:
 filepath = BASE_DIR / "docs" / "hypothesis.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 content = f"""# researchhypothesisdefinition

> generationdatetime: {datetime.datetime.now.strftime('%Y-%m-%d %H:%M')}

## framework: {hypothesis['framework']}

| Element | Description |
|---|---|
| **P** (Population) | {hypothesis['population']} |
| **{'I' if hypothesis['framework'] == 'PICO' else 'E'}** ({'Intervention' if hypothesis['framework'] == 'PICO' else 'Exposure'}) | {hypothesis['intervention_or_exposure']} |
| **C** (Comparison) | {hypothesis['comparison']} |
| **O** (Outcome) | {hypothesis['outcome']} |

## hypothesis

- **researchhypothesis (H₁)**: {hypothesis['H1']}
- **null hypothesis (H₀)**: {hypothesis['H0']}

## parameters

- significance level α = {hypothesis['alpha']}
- targetpower = {hypothesis['power_target']}
"""
 # hypothesis addition
 if hypothesis.get('sub_hypotheses'):
 content += "\n## hypothesis\n\n"
 for sub_id, sub_desc in hypothesis['sub_hypotheses'].items:
 content += f"- **{sub_id}**: {sub_desc}\n"
 
 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)
 
 print(f" → hypothesisdefinitionsave: {filepath}")
 return filepath
```

### 3.1.2 JSON shapeformula（）

`docs/hypothesis.json` save.pipelineskillreference.

```python
def save_hypothesis_json(hypothesis, filepath=None):
 """
 hypothesisdefinition JSON fileassave.
 skill（critical-review, academic-writing） reference.
 """
 import datetime
 
 if filepath is None:
 filepath = BASE_DIR / "docs" / "hypothesis.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 data = {
 "version": "1.0",
 "created_at": datetime.datetime.now.isoformat,
 "hypothesis": hypothesis,
 }
 
 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(data, f, indent=2, ensure_ascii=False, default=str)
 
 print(f" → hypothesisdefinition JSON save: {filepath}")
 return filepath
```

### 3.1.3 existinghypothesisfile'sload

```python
def load_hypothesis(filepath=None):
 """
 save's hypothesisdefinitionloads。
 pipelineand for。
 """
 if filepath is None:
 filepath = BASE_DIR / "docs" / "hypothesis.json"
 
 if not filepath.exists:
 print(f" ⚠ hypothesisfileitems: {filepath}")
 return None
 
 with open(filepath, "r", encoding="utf-8") as f:
 data = json.load(f)
 
 print(f" → hypothesisdefinition load: {filepath}")
 print(f" H₁: {data['hypothesis']['H1']}")
 return data['hypothesis']
```

## 4. hypothesisfromanalysismethod to 'sautomatedmapping

```markdown
## analysismethodselection

### comparisonstructure × datatype → recommendedmethod

| comparisonstructure | number/count | number/count | recommendedmethod | referenceskill |
|---|---|---|---|---|
| 2groupcomparison |  | | Welch t testing | statistical-testing |
| 2groupcomparison |  | | Mann-Whitney U | statistical-testing |
| groupcomparison |  | | ANOVA + Tukey | statistical-testing |
| groupcomparison |  | | Kruskal-Wallis + Dunn | statistical-testing |
| correlation | | | Pearson / Spearman | eda-correlation |
| regression | | / | Linear / Ridge / RF | ml-regression |
| classification | | / | RF / SVM / XGBoost | ml-classification |
| time series | | time | STLdegradation / ARIMA | time-series |
| | time | | Kaplan-Meier / Cox PH | survival-clinical |
| causal inference | /value | | PSM / DiD / IV | causal-inference |
| foramount | | | RSM / GP | process-optimization |
| dimensionality reduction | | — | PCA / t-SNE / UMAP | pca-tsne |
```

## 4.1 workflowdesign's filesave

pipelinedesign（workflow） `docs/workflow_design.md` and 
`docs/workflow_design.json`.than design's change Git 、
paper's Methods writing workflow reference。

### 4.1.1 workflow Markdown save

```python
def save_workflow_design(hypothesis, steps, filepath=None):
 """
 pipeline's workflowdesign Markdown fileassave.
 
 Args:
 hypothesis: dict — hypothesisdefinition
 steps: list[dict] — pipelinestep
 eachstep: {"id": "step_1", "name": "Loading data",
 "skill": "data-preprocessing", "params": {...},
 "inputs": [...], "outputs": [...]}
 filepath: Path — save（: docs/workflow_design.md）
 """
 import datetime
 
 if filepath is None:
 filepath = BASE_DIR / "docs" / "workflow_design.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 content = f"""# workflowdesign

> generationdatetime: {datetime.datetime.now.strftime('%Y-%m-%d %H:%M')}

## verification'shypothesis

- **H₁**: {hypothesis['H1']}
- **H₀**: {hypothesis['H0']}

## pipelineoverview

```
"""
 # chartgeneration
 for i, step in enumerate(steps):
 prefix = "├─" if i < len(steps) - 1 else "└─"
 content += f" {prefix} Step {i+1}: {step['name']}\n"
 if step.get('skill'):
 content += f" │ └─ Skill: {step['skill']}\n"
 
 content += "```\n\n## stepdetails\n\n"
 
 for i, step in enumerate(steps):
 content += f"""### Step {i+1}: {step['name']}

| Item | Description |
|---|---|
| **forskill** | {step.get('skill', 'N/A')} |
| **input** | {', '.join(step.get('inputs', ['—']))} |
| **output** | {', '.join(step.get('outputs', ['—']))} |
| **parameters** | {step.get('params', '—')} |

"""
 
 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)
 
 print(f" → workflowdesignsave: {filepath}")
 return filepath
```

### 4.1.2 workflow JSON save

```python
def save_workflow_json(hypothesis, steps, filepath=None):
 """
 pipeline's workflowdesign JSON assave.
 pipeline's constructionfixreference.
 """
 import datetime
 
 if filepath is None:
 filepath = BASE_DIR / "docs" / "workflow_design.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 data = {
 "version": "1.0",
 "created_at": datetime.datetime.now.isoformat,
 "hypothesis_ref": {
 "H1": hypothesis["H1"],
 "H0": hypothesis["H0"],
 "framework": hypothesis["framework"],
 },
 "pipeline": {
 "total_steps": len(steps),
 "steps": steps,
 },
 }
 
 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(data, f, indent=2, ensure_ascii=False, default=str)
 
 print(f" → workflowdesign JSON save: {filepath}")
 return filepath
```

### 4.1.3 existingworkflowdesign'sload

```python
def load_workflow_design(filepath=None):
 """
 save's workflowdesignloads。
 pipeline's fix for。
 """
 if filepath is None:
 filepath = BASE_DIR / "docs" / "workflow_design.json"
 
 if not filepath.exists:
 print(f" ⚠ workflowdesignfileitems: {filepath}")
 return None
 
 with open(filepath, "r", encoding="utf-8") as f:
 data = json.load(f)
 
 print(f" → workflowdesign load: {filepath}")
 print(f" steps: {data['pipeline']['total_steps']}")
 return data
```

## 5. pipelineautomatedgeneration

### 5.1 generation'sstructure

'sfrombelow/following's structure'sautomatedgenerates。

```python
#!/usr/bin/env python3
"""
Hypothesis-Driven Analysis Pipeline
Generated from user prompt by scientific-hypothesis-pipeline skill

Hypothesis: [H₁ 's]
Null Hypothesis: [H₀ 's]
Framework: [PICO / PECO]

Author: [Name]
Date: [YYYY-MM-DD]
"""

import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import json
import time

# === Reproducibility Settings ===
SEED = 42
np.random.seed(SEED)

# === Directory Structure ===
BASE_DIR = Path(__file__).resolve.parent
DATA_DIR = BASE_DIR / "data"
FIG_DIR = BASE_DIR / "figures"
RESULTS_DIR = BASE_DIR / "results"

for d in [DATA_DIR, FIG_DIR, RESULTS_DIR]:
 d.mkdir(parents=True, exist_ok=True)

# === Publication-Quality Style ===
# ⚠️ RULE: All graph text (titles, axis labels, legends, annotations) MUST be in English.
plt.rcParams.update({
 "font.family": "sans-serif",
 "font.sans-serif": ["Noto Sans CJK JP", "IPAGothic", "Arial", "Helvetica", "DejaVu Sans"],
 "font.size": 10,
 "axes.titlesize": 12,
 "axes.labelsize": 11,
 "axes.spines.top": False,
 "axes.spines.right": False,
 "savefig.dpi": 300,
 "savefig.bbox": "tight",
 "figure.facecolor": "white",
})


# ============================================================
# Hypothesis Definition
# ============================================================
HYPOTHESIS = {
 "framework": "PICO", # or "PECO"
 "population": "[]",
 "intervention_or_exposure": "[or]",
 "comparison": "[comparison]",
 "outcome": "[]",
 "H1": "[alternative hypothesis's]",
 "H0": "[null hypothesis's]",
 "alpha": 0.05,
 "power_target": 0.80,
}


def main:
 start_time = time.time
 print("=" * 60)
 print("Hypothesis-Driven Analysis Pipeline")
 print(f"H₁: {HYPOTHESIS['H1']}")
 print("=" * 60)

 # ──── Step 0: hypothesisworkflowdesign'ssave ────
 print("\n[Step 0] Saving hypothesis/workflow definitions...")
 save_hypothesis_markdown(HYPOTHESIS)
 save_hypothesis_json(HYPOTHESIS)

 # workflowdesign's definition
 workflow_steps = [
 {"id": "step_1", "name": "Data loading / generation",
 "skill": "data-preprocessing", "inputs": ["raw data"],
 "outputs": ["data/dataset.csv"]},
 {"id": "step_2", "name": "data",
 "skill": "data-preprocessing", "inputs": ["data/dataset.csv"],
 "outputs": ["results/data_quality.json"]},
 {"id": "step_3", "name": "search/explorationdataanalysis",
 "skill": "eda-correlation", "inputs": ["data/dataset.csv"],
 "outputs": ["figures/eda_*.png"]},
 {"id": "step_4", "name": "preprocessing",
 "skill": "data-preprocessing", "inputs": ["data/dataset.csv"],
 "outputs": ["data/dataset_processed.csv"]},
 {"id": "step_5", "name": "hypothesisverification",
 "skill": "[automatedselection]", "inputs": ["data/dataset_processed.csv"],
 "outputs": ["results/test_results.json"]},
 {"id": "step_6", "name": "results'svisualization",
 "skill": "publication-figures", "inputs": ["results/"],
 "outputs": ["figures/*.png"]},
 {"id": "step_7", "name": "hypothesis",
 "skill": "hypothesis-pipeline", "inputs": ["results/test_results.json"],
 "outputs": ["results/hypothesis_verdict.json"]},
 {"id": "step_8", "name": "summarygeneration",
 "skill": "pipeline-scaffold", "inputs": ["results/"],
 "outputs": ["results/analysis_summary.json"]},
 ]
 save_workflow_design(HYPOTHESIS, workflow_steps)
 save_workflow_json(HYPOTHESIS, workflow_steps)

 # ──── Step 1: Data loading / generation ────
 print("\n[Step 1] Loading data...")
 # df = pd.read_csv(DATA_DIR / "dataset.csv")
 # → scientific-data-simulation datagenerates:
 # df = generate_synthetic_data
 # df.to_csv(DATA_DIR / "dataset.csv", index=False)

 # ──── Step 2: data ────
 print("\n[Step 2] data...")
 # → scientific-data-preprocessing: data_quality_report(df)

 # ──── Step 3: search/explorationdataanalysis (EDA) ────
 print("\n[Step 3] search/explorationdataanalysis...")
 # → scientific-eda-correlation: descriptive_statistics, plot_distributions
 # → scientific-eda-correlation: plot_correlation_heatmap

 # ──── Step 4: preprocessing ────
 print("\n[Step 4] preprocessing...")
 # → scientific-data-preprocessing: handle_missing_values, scale_data

 # ──── Step 5: hypothesisverification ────
 print("\n[Step 5] hypothesisverification...")
 # [hypothesistesting / / analysis]
 # example: 2groupcomparisoncase
 # result = two_group_test(group1, group2)
 # example: regressioncase
 # result = train_evaluate_regression(X_train, y_train, X_test, y_test)

 # ──── Step 6: results'svisualization ────
 print("\n[Step 6] results'svisualization...")
 # → scientific-publication-figures: hypothesisfigures/tables generation
 # figure figures/ save、paper possible

 # ──── Step 7: hypothesis ────
 print("\n[Step 7] hypothesis...")
 # hypothesis_verdict = evaluate_hypothesis(result, HYPOTHESIS)

 # ──── Step 8: summarygeneration ────
 elapsed = time.time - start_time
 print(f"\n[Step 8] summarygeneration... (elapsed: {elapsed:.1f}s)")

 # summary = generate_hypothesis_summary(
 # hypothesis=HYPOTHESIS,
 # test_results=result,
 # verdict=hypothesis_verdict,
 # elapsed=elapsed,
 # )

 print("\n" + "=" * 60)
 print(f"Done! ({elapsed:.1f} sec)")
 print("=" * 60)


if __name__ == "__main__":
 main
```

### 5.2 hypothesis

```python
def evaluate_hypothesis(test_results, hypothesis):
 """
 testing's results hypothesis.

 Returns:
 dict: results（verdict, evidence_level, interpretation）
 """
 alpha = hypothesis["alpha"]
 p_value = test_results.get("p_value")
 effect_size = test_results.get("cohens_d") or test_results.get("effect_size_value")

 # 
 if p_value is None:
 verdict = "INCONCLUSIVE"
 evidence = "testingresults"
 elif p_value < alpha:
 verdict = "REJECT_H0"
 evidence = f"H₀ (p = {p_value:.4f} < α = {alpha})"
 else:
 verdict = "FAIL_TO_REJECT_H0"
 evidence = f"H₀ (p = {p_value:.4f} ≥ α = {alpha})"

 # effect size's
 if effect_size is not None:
 effect_interp = (
 "large" if abs(effect_size) > 0.8 else
 "degree's" if abs(effect_size) > 0.5 else
 "small" if abs(effect_size) > 0.2 else
 ""
 )
 else:
 effect_interp = "effect size"

 result = {
 "verdict": verdict,
 "p_value": p_value,
 "alpha": alpha,
 "effect_size": effect_size,
 "effect_interpretation": effect_interp,
 "evidence": evidence,
 "interpretation": _generate_interpretation(verdict, hypothesis, test_results),
 }

 print(f" hypothesis: {verdict}")
 print(f" {evidence}")
 print(f" effect size: {effect_interp}")

 return result


def _generate_interpretation(verdict, hypothesis, results):
 """hypothesis's is generated。"""
 if verdict == "REJECT_H0":
 return (
 f"significantresults。"
 f"{hypothesis['H1']}."
 f"however、significant forsignificant。"
 f"effect size and confidence intervalalso and 。"
 )
 elif verdict == "FAIL_TO_REJECT_H0":
 return (
 f"significant。"
 f"「 」 and 's 、"
 f"「's data」 and."
 f"sample size's and powermin and。"
 )
 else:
 return "testingresults min。data's verification necessary。"
```

### 5.3 powerminsample sizecalculation

```python
from scipy import stats as sp_stats

def power_analysis(effect_size, alpha=0.05, power=0.80, test_type="two_sample_t"):
 """
 powerminby/viasample sizecalculation。

 effect_size: Cohen's d（=0.2, =0.5, =0.8）
 """
 if test_type == "two_sample_t":
 # formula: n ≈ (z_α/2 + z_β)² × 2 / d²
 z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
 z_beta = sp_stats.norm.ppf(power)
 n_per_group = int(np.ceil(2 * ((z_alpha + z_beta) / effect_size) ** 2))
 elif test_type == "one_sample_t":
 z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
 z_beta = sp_stats.norm.ppf(power)
 n_per_group = int(np.ceil(((z_alpha + z_beta) / effect_size) ** 2))
 elif test_type == "chi_square":
 # Cochran 's formula's
 z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
 z_beta = sp_stats.norm.ppf(power)
 n_per_group = int(np.ceil(((z_alpha + z_beta) / effect_size) ** 2))
 else:
 raise ValueError(f"Unsupported test type: {test_type}")

 result = {
 "test_type": test_type,
 "effect_size": effect_size,
 "alpha": alpha,
 "power": power,
 "n_per_group": n_per_group,
 "total_n": n_per_group * 2 if "two" in test_type else n_per_group,
 }

 print(f" powermin:")
 print(f" effect size d = {effect_size}, α = {alpha}, power = {power}")
 print(f" → necessarysample size: {result['n_per_group']}/group ( {result['total_n']})")

 return result
```

### 5.4 hypothesissummary JSON generation

```python
def generate_hypothesis_summary(hypothesis, test_results, verdict,
 elapsed, output_path=None):
 """
 hypothesisverificationresultsincluding analysis_summary.json is generated。
 """
 import datetime

 summary = {
 "experiment": "Hypothesis-Driven Analysis",
 "timestamp": datetime.datetime.now.isoformat,
 "elapsed_seconds": round(elapsed, 2),
 "environment": {
 "python": __import__("sys").version,
 "seed": SEED,
 },
 "hypothesis": {
 "framework": hypothesis["framework"],
 "population": hypothesis["population"],
 "intervention_or_exposure": hypothesis["intervention_or_exposure"],
 "comparison": hypothesis["comparison"],
 "outcome": hypothesis["outcome"],
 "H1": hypothesis["H1"],
 "H0": hypothesis["H0"],
 "alpha": hypothesis["alpha"],
 },
 "results": {
 "test_name": test_results.get("test"),
 "statistic": test_results.get("statistic"),
 "p_value": test_results.get("p_value"),
 "effect_size": test_results.get("cohens_d"),
 },
 "verdict": {
 "decision": verdict["verdict"],
 "evidence": verdict["evidence"],
 "effect_interpretation": verdict["effect_interpretation"],
 "interpretation": verdict["interpretation"],
 },
 }

 if output_path is None:
 output_path = RESULTS_DIR / "analysis_summary.json"

 with open(output_path, "w", encoding="utf-8") as f:
 json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

 print(f" → Summary saved: {output_path}")
 return summary
```

## 6. example andgenerationpipelinesupporttable

| example | generationhypothesis | forskill |
|---|---|---|
| 「temperature 's」 | H₁: temperature significant | pipeline-scaffold + eda + statistical-testing + doe |
| 「gene expressiondatafromcancer's classification」 | H₁: gene expressionthan | pipeline-scaffold + preprocessing + pca-tsne + ml-classification |
| 「's amount and 's optimization」 | H₁: amount and 's significantforamount | pipeline-scaffold + doe + process-optimization + ml-regression |
| 「patient's rate factor」 | H₁: 's factor rate significant items | pipeline-scaffold + survival-clinical + feature-importance |
| 「spectrumdatafrom's prediction」 | H₁: spectrumfeaturesfromhigh-accuracyprediction | pipeline-scaffold + spectral-signal + ml-regression |
| 「metabolomedata diseasegroup and group comparison」 | H₁: diseasegroup and group metabolitefile significant | pipeline-scaffold + metabolomics + statistical-testing + pca-tsne |

## 7. multiplehypothesis's

```python
def manage_hypotheses(hypotheses_list):
 """
 multiplehypothesis.

 hypotheses_list: [
 {"id": "H1a", "description": "...", "priority": "primary",
 "test_type": "two_sample_t", "variables": ("X", "Y")},
 {"id": "H1b", "description": "...", "priority": "secondary",...},
 ]
 """
 # 
 priority_order = {"primary": 0, "secondary": 1, "exploratory": 2}
 sorted_h = sorted(hypotheses_list,
 key=lambda h: priority_order.get(h["priority"], 99))

 print("=== hypothesislist ===")
 for h in sorted_h:
 print(f" [{h['priority'].upper}] {h['id']}: {h['description']}")

 # multiple comparisoncorrection's for
 n_tests = len([h for h in sorted_h if h["priority"] != "exploratory"])
 if n_tests > 1:
 corrected_alpha = 0.05 / n_tests # Bonferroni
 print(f"\n ⚠ {n_tests} units'stesting → Bonferroni correction: α' = {corrected_alpha:.4f}")
 print(f" or FDR (Benjamini-Hochberg) correction recommended")

 return sorted_h
```

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `docs/hypothesis.md` | hypothesisdefinition（Markdown） | Phase 2 completion |
| `docs/hypothesis.json` | hypothesisdefinition（JSON） | Phase 2 completion |
| `docs/workflow_design.md` | workflowdesign（Markdown） | Phase 3 completion |
| `docs/workflow_design.json` | workflowdesign（JSON） | Phase 3 completion |
| `exp_analysis.py` | hypothesispipeline | Phase 4 completion |
| `results/analysis_summary.json` | hypothesisverificationresultsincluding JSON summary | completion |
| `figures/*.png` | analysisresults'sfigures/tables | completion |
| `results/hypothesis_tests.csv` | testingresultslist | completion |
| `results/power_analysis.csv` | powerminresults | completion |

### Related Skills

| skill | |
|---|---|
| `scientific-pipeline-scaffold` | pipeline's（directorystructurelogsummary） |
| `scientific-data-preprocessing` | datapreprocessing |
| `scientific-eda-correlation` | search/explorationdataanalysiscorrelationmin |
| `scientific-statistical-testing` | hypothesistestingmultiple comparison |
| `scientific-ml-regression` | regression（hypothesisregressiontypecase） |
| `scientific-ml-classification` | classification（hypothesisclassificationtypecase） |
| `scientific-publication-figures` | paper'sfigures/tablesgeneration |
| `scientific-academic-writing` | paperwriting（hypothesisverificationresults's paper） |
| `scientific-critical-review` | paper's（hypothesisand conclusion'sverification） |

```
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Experimental Design)

Before execution, define:
- [ ] **Factors and levels**: complete factor list with ranges
- [ ] **Response variable**: measurement method, precision
- [ ] **Design type**: factorial / fractional / RSM / sequential
- [ ] **Sample size**: power analysis with effect size justification

#### Pass Criteria
- Design matrix is orthogonal or near-orthogonal
- All factors have >= 2 levels with scientific justification
- Randomization order specified
- Blocking/stratification applied for known confounders
- Statistical model specified before data collection
### Verification Loop

```
Phase 1: PLAN
  |-- Define eval criteria (above checklist)
  |-- Confirm input data availability and format
  |-- Select analysis methods with justification
  +-- Estimate resource requirements (time, memory, API calls)

Phase 2: EXECUTE
  |-- Run analysis pipeline step-by-step
  |-- Save intermediate results after each major step
  |-- Log execution time per step
  +-- Capture warnings/errors without stopping

Phase 3: VERIFY
  |-- Check all Pass Criteria (above)
  |-- Validate output file existence and non-empty
  |-- Cross-check numeric results for sanity (ranges, signs, units)
  |-- Verify figures are readable and correctly labeled
  +-- Run regression check: did existing outputs break?

Phase 4: RECOVER (on failure)
  |-- Identify failed phase and root cause
  |-- Isolate minimum reproducer
  |-- Apply fix and re-run only failed phase
  |-- Log fix as reusable pattern
  +-- If unrecoverable: document limitation and partial results

Phase 5: REPORT
  |-- Generate report.md with all sections in the user's input language
  |-- Embed all figures with captions
  |-- Save numeric results as JSON/CSV
  |-- List all generated files
  +-- Record execution metadata (duration, versions, seed)
```

### Quality Gates

| Gate | Check | Required |
|------|-------|----------|
| G1 | All figures saved to `figures/` (not `plt.show()`) | MUST |
| G2 | All figures embedded in `report.md` | MUST |
| G3 | Numeric results saved as JSON/CSV in `results/` | MUST |
| G4 | Report includes methods, results, discussion | MUST |
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
| G6 | No hardcoded paths (use `Path` / config) | MUST |
| G7 | Random seed set and documented | MUST |
| G8 | Execution time logged | RECOMMENDED |
| G9 | Input validation performed | RECOMMENDED |
| G10 | Error messages are actionable | RECOMMENDED |

### Model Routing

| Task Complexity | Model Tier | Examples |
|----------------|-----------|----------|
| Mechanical | `fast` (haiku-class) | Data formatting, file I/O, unit conversion |
| Implementation | `standard` (sonnet-class) | Analysis code, pipeline execution, plotting |
| Reasoning | `premium` (opus-class) | Hypothesis generation, result interpretation, review |

### Sub-Agent Orchestration

When the task is complex, split into parallel sub-agents:

```
Orchestrator (this skill)
|-- Agent 1: Data preparation and validation
|-- Agent 2: Core analysis / computation
|-- Agent 3: Visualization and figure generation
+-- Agent 4: Report writing and quality check
```

Each sub-agent receives:
- Specific scope (what to do)
- Input specification (what data to use)
- Output specification (what files to produce)
- Quality gate subset (which gates to check)

### Token Optimization

- Load only the sub-skill needed for the current task
- Compact context after each major phase (discard intermediate logs)
- Use structured output (JSON) over prose for intermediate results
- Prefer code templates over natural language descriptions
- Cache expensive computations (API calls, model training)

### Error Recovery Protocol

```python
def execute_with_recovery(pipeline_steps, max_retries=2):
    results = {}
    for step in pipeline_steps:
        for attempt in range(max_retries + 1):
            try:
                results[step.name] = step.execute()
                break
            except Exception as e:
                if attempt < max_retries:
                    log(f"Step '{step.name}' failed (attempt {attempt+1}): {e}")
                    step.adjust_params()  # reduce batch size, increase timeout
                else:
                    log(f"Step '{step.name}' unrecoverable: {e}")
                    results[step.name] = {"status": "failed", "error": str(e)}
    return results
```
