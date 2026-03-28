---
name: scientific-pharmacovigilance
description: |
 Pharmacovigilance skill. Adverse event signal detection, FAERS/VAERS data analysis, disproportionality analysis, and drug safety signal evaluation.
---

# Scientific Pharmacovigilance

all（）foranalysisskill。
FDA FAERS（FDA Adverse Event Reporting System）and
alldata's integrationmin is supported。

## When to Use

- adverse event data's min（Signal Detection）
- 'ssafety profileevaluation
- MedDRA using'ssystematicclassification
- time seriesby/via's
- （）'sanalysis
- drug's allcomparison

## Quick Start

### analysispipeline

```
Phase 1: Data Acquisition
 - FAERS / EudraVigilance / VigiBase from's Data Retrieval
 - min'snormalization
 - 's（Case ID ）
 ↓
Phase 2: MedDRA Coding & Hierarchy
 - LLT → PT → HLT → HLGT → SOC mapping
 - Preferred Term (PT) 's
 - SMQ (Standardised MedDRA Query) for
 ↓
Phase 3: Disproportionality Analysis
 - PRR (Proportional Reporting Ratio) 
 - ROR (Reporting Odds Ratio) 
 - IC (Information Component, Bayesian) 
 - EBGM (Empirical Bayes Geometric Mean) 
 - threshold
 ↓
Phase 4: Temporal & Demographic Analysis
 - Time-to-Onset distributionanalysis
 - 
 - 
 - Rechallenge / Dechallenge min
 ↓
Phase 5: Signal Evaluation & Reporting
 - 
 - min
 - evaluation（WHO-UMC / Naranjo ）
 - allreportgeneration
 ↓
Phase 6: Risk-Benefit Assessment
 - NNH (Number Needed to Harm) 
 - -evaluation
 - REMS / RiskMAP 
 ↓
Phase 7: Regulatory Communication
 - PBRER / PSUR support
 - summarygeneration
 - 
```

## Workflow

### 1. FAERS Data Retrievalpreprocessing

```python
import pandas as pd
import numpy as np
from scipy import stats

# === FAERS Loading data ===
# FAERS ASCII file: DEMO, DRUG, REAC, OUTC, INDI, THER, RPSR
demo = pd.read_csv("faers/DEMO.txt", sep="$", dtype=str)
drug = pd.read_csv("faers/DRUG.txt", sep="$", dtype=str)
reac = pd.read_csv("faers/REAC.txt", sep="$", dtype=str)

# : primaryid latest's
demo = demo.sort_values("fda_dt", ascending=False).drop_duplicates(subset=["caseid"], keep="first")

# Drug-Reaction construction
merged = drug.merge(reac, on="primaryid", how="inner")
merged = merged.merge(demo[["primaryid", "age", "sex", "wt", "reporter_country"]], on="primaryid", how="left")

# 'sfilter
target_drug = "ACETAMINOPHEN"
target_df = merged[merged["drugname"].str.upper.str.contains(target_drug)]
print(f"Target drug reports: {len(target_df):,}")
```

### 2. MedDRA mapping

```python
# === MedDRA ===
# LLT → PT → HLT → HLGT → SOC
meddra_pt = pd.read_csv("meddra/pt.asc", sep="$", header=None,
 names=["pt_code", "pt_name", "null_field",
 "pt_soc_code", "null2", "null3"])
meddra_soc = pd.read_csv("meddra/soc.asc", sep="$", header=None,
 names=["soc_code", "soc_name", "soc_abbrev", "null1"])

# PT Reaction table
merged["pt_name_clean"] = merged["pt"].str.strip.str.upper

# SOC 
soc_summary = merged.merge(meddra_pt, left_on="pt_name_clean", right_on="pt_name")
soc_counts = soc_summary.groupby("pt_soc_code").size.reset_index(name="count")
soc_counts = soc_counts.merge(meddra_soc, left_on="pt_soc_code", right_on="soc_code")
soc_counts = soc_counts.sort_values("count", ascending=False)
print("Top SOC categories:")
print(soc_counts[["soc_name", "count"]].head(10).to_string(index=False))
```

### 3. min（Disproportionality Analysis）

```python
def disproportionality_analysis(drug_reactions_df, all_reactions_df, target_drug):
 """
 PRR, ROR, IC (Information Component) 。

 2x2 mintable:
 Target AE Other AE
 Target Drug a b
 Other Drugs c d
 """
 results = []

 target_pts = drug_reactions_df[
 drug_reactions_df["drugname"].str.upper.str.contains(target_drug)
 ]["pt"].value_counts

 total_target = drug_reactions_df[
 drug_reactions_df["drugname"].str.upper.str.contains(target_drug)
 ]["primaryid"].nunique

 total_all = all_reactions_df["primaryid"].nunique
 total_other = total_all - total_target

 for pt, a in target_pts.items:
 # b: target drug, other AE
 b = total_target - a
 # c: other drugs, same AE
 c_total = all_reactions_df[all_reactions_df["pt"] == pt]["primaryid"].nunique
 c = c_total - a
 # d: other drugs, other AE
 d = total_other - c

 # PRR
 if (a + b) > 0 and (c + d) > 0 and c > 0:
 prr = (a / (a + b)) / (c / (c + d))
 # PRR 's 95% CI
 se_ln_prr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d)) if a > 0 else np.inf
 prr_lower = np.exp(np.log(prr) - 1.96 * se_ln_prr) if prr > 0 else 0
 else:
 prr, prr_lower = 0, 0

 # ROR
 if b > 0 and c > 0 and d > 0:
 ror = (a * d) / (b * c)
 se_ln_ror = np.sqrt(1/a + 1/b + 1/c + 1/d) if a > 0 else np.inf
 ror_lower = np.exp(np.log(ror) - 1.96 * se_ln_ror) if ror > 0 else 0
 else:
 ror, ror_lower = 0, 0

 # IC (Information Component) - Bayesian
 expected = (a + b) * (a + c) / (a + b + c + d) if (a + b + c + d) > 0 else 1
 ic = np.log2((a + 0.5) / (expected + 0.5)) if expected > 0 else 0

 # Chi-square
 chi2, p_value = 0, 1
 if a + b + c + d > 0:
 try:
 chi2, p_value, _, _ = stats.chi2_contingency([[a, b], [c, d]])
 except ValueError:
 pass

 # Signal criteria
 is_signal = (prr >= 2 and chi2 >= 4 and a >= 3)
 is_signal_ror = (ror_lower > 1 and a >= 3)
 is_signal_ic = (ic > 0 and a >= 3)

 results.append({
 "pt": pt, "a": a, "b": b, "c": c, "d": d,
 "prr": round(prr, 3), "prr_lower": round(prr_lower, 3),
 "ror": round(ror, 3), "ror_lower": round(ror_lower, 3),
 "ic": round(ic, 3),
 "chi2": round(chi2, 3), "p_value": round(p_value, 6),
 "signal_prr": is_signal,
 "signal_ror": is_signal_ror,
 "signal_ic": is_signal_ic,
 })

 return pd.DataFrame(results).sort_values("prr", ascending=False)

signals = disproportionality_analysis(merged, merged, target_drug)
print(f"Signals detected (PRR≥2, χ²≥4, N≥3): {signals['signal_prr'].sum}")
print(signals[signals["signal_prr"]].head(20))
```

### 4. time seriesmin

```python
import matplotlib.pyplot as plt

def temporal_trend_analysis(drug_df, target_drug, target_pt=None):
 """and Time-to-Onset distribution"""
 target = drug_df[drug_df["drugname"].str.upper.str.contains(target_drug)].copy
 if target_pt:
 target = target[target["pt"].str.upper.str.contains(target_pt)]

 # 
 target["report_date"] = pd.to_datetime(target["fda_dt"], format="%Y%m%d", errors="coerce")
 target["quarter"] = target["report_date"].dt.to_period("Q")
 quarterly = target.groupby("quarter").size

 fig, axes = plt.subplots(1, 2, figsize=(14, 5))

 # 
 quarterly.plot(kind="bar", ax=axes[0], color="#2196F3")
 axes[0].set_title(f"Quarterly Reports: {target_drug}")
 axes[0].set_ylabel("Report Count")
 axes[0].tick_params(axis="x", rotation=45)

 # Time-to-Onset
 if "event_dt" in target.columns and "start_dt" in target.columns:
 target["event_date"] = pd.to_datetime(target["event_dt"], format="%Y%m%d", errors="coerce")
 target["start_date"] = pd.to_datetime(target["start_dt"], format="%Y%m%d", errors="coerce")
 target["tto_days"] = (target["event_date"] - target["start_date"]).dt.days
 valid_tto = target["tto_days"].dropna
 valid_tto = valid_tto[(valid_tto >= 0) & (valid_tto <= 365)]
 axes[1].hist(valid_tto, bins=30, color="#FF9800", edgecolor="black")
 axes[1].set_title("Time-to-Onset Distribution")
 axes[1].set_xlabel("Days")
 axes[1].set_ylabel("Frequency")

 plt.tight_layout
 plt.savefig("figures/pv_temporal_trend.png", dpi=300, bbox_inches="tight")
 plt.show

temporal_trend_analysis(merged, target_drug)
```

### 5. min

```python
def demographic_stratification(drug_df, target_drug, target_pt):
 """'s min"""
 target = drug_df[
 (drug_df["drugname"].str.upper.str.contains(target_drug)) &
 (drug_df["pt"].str.upper.str.contains(target_pt))
 ].copy

 # 
 target["age_num"] = pd.to_numeric(target["age"], errors="coerce")
 target["age_group"] = pd.cut(target["age_num"],
 bins=[0, 18, 40, 65, 85, 120],
 labels=["<18", "18-40", "40-65", "65-85", "85+"])

 # distribution
 sex_dist = target["sex"].value_counts

 # Weight-based analysis
 target["wt_num"] = pd.to_numeric(target["wt"], errors="coerce")

 fig, axes = plt.subplots(1, 3, figsize=(16, 5))

 # Age distribution
 target["age_group"].value_counts.sort_index.plot(
 kind="bar", ax=axes[0], color="#4CAF50")
 axes[0].set_title(f"Age Distribution: {target_drug} + {target_pt}")
 axes[0].set_ylabel("Count")

 # Sex distribution
 sex_dist.plot(kind="pie", ax=axes[1], autopct="%1.1f%%",
 colors=["#2196F3", "#E91E63", "#9E9E9E"])
 axes[1].set_title("Sex Distribution")

 # Outcome severity
 if "outc_cod" in target.columns:
 outcome_map = {"DE": "Death", "LT": "Life-Threatening",
 "HO": "Hospitalization", "DS": "Disability",
 "CA": "Congenital Anomaly", "OT": "Other"}
 target["outcome_label"] = target["outc_cod"].map(outcome_map)
 target["outcome_label"].value_counts.plot(
 kind="barh", ax=axes[2], color="#F44336")
 axes[2].set_title("Outcome Distribution")

 plt.tight_layout
 plt.savefig("figures/pv_demographics.png", dpi=300, bbox_inches="tight")
 plt.show

 return target

demographic_stratification(merged, target_drug, "HEPATOTOXICITY")
```

### 6. evaluation

```python
def naranjo_assessment(case_data):
 """
 Naranjo Adverse Drug Reaction Probability Scale
 : ≥9 = Definite, 5-8 = Probable, 1-4 = Possible, ≤0 = Doubtful
 """
 questions = [
 ("previous reaction", 1, 0, 0),
 ("", 2, -1, 0),
 ("improvement (Dechallenge)", 1, 0, 0),
 (" (Rechallenge)", 2, -1, 0),
 ("'s", -1, 2, 0),
 ("also", -1, 1, 0),
 ("degree", 1, 0, 0),
 ("foramountdependency", 1, 0, 0),
 ("", 1, 0, 0),
 ("verification", 1, 0, 0),
 ]

 total_score = 0
 assessment = []
 for q, yes_score, no_score, dk_score in questions:
 # 's datafrom
 answer = case_data.get(q, "dk")
 if answer == "yes":
 score = yes_score
 elif answer == "no":
 score = no_score
 else:
 score = dk_score
 total_score += score
 assessment.append({"question": q, "answer": answer, "score": score})

 if total_score >= 9:
 category = "Definite"
 elif total_score >= 5:
 category = "Probable"
 elif total_score >= 1:
 category = "Possible"
 else:
 category = "Doubtful"

 return {
 "total_score": total_score,
 "category": category,
 "details": assessment,
 }
```

### 7. EBGM (Empirical Bayes Geometric Mean)

```python
def calculate_ebgm(contingency_df, shrinkage_prior=0.5):
 """
 EBGM (Multi-item Gamma Poisson Shrinker) by/via
 。FDA OPIS for。

 EBGM = exp(E[log(λ)|N])
 EB05 = EBGM 's 5% limitations
 """
 results = []
 N_total = contingency_df[["a", "b", "c", "d"]].sum.sum

 for _, row in contingency_df.iterrows:
 a = row["a"]
 E = ((row["a"] + row["b"]) * (row["a"] + row["c"])) / N_total
 if E > 0:
 # EBGM (full GPS EM )
 ebgm = (a + shrinkage_prior) / (E + shrinkage_prior)
 # EB05 (Poisson )
 from scipy.stats import poisson
 eb05 = poisson.ppf(0.05, a + shrinkage_prior) / (E + shrinkage_prior)
 else:
 ebgm, eb05 = 0, 0

 results.append({
 "pt": row["pt"],
 "observed": a,
 "expected": round(E, 3),
 "ebgm": round(ebgm, 3),
 "eb05": round(eb05, 3),
 "signal_ebgm": eb05 >= 2, # EB05 ≥ 2 criteria
 })

 return pd.DataFrame(results).sort_values("ebgm", ascending=False)

ebgm_results = calculate_ebgm(signals)
print(f"EBGM signals (EB05≥2): {ebgm_results['signal_ebgm'].sum}")
```

### 8. allreportgeneration

```python
import json

def generate_pv_report(target_drug, signals_df, ebgm_df, output_dir="results"):
 """allreport'sintegrationgeneration"""

 # integration
 combined = signals_df.merge(ebgm_df[["pt", "ebgm", "eb05", "signal_ebgm"]], on="pt")
 combined["consensus_signal"] = (
 combined["signal_prr"] & combined["signal_ror"] & combined["signal_ebgm"]
 )

 report = {
 "drug": target_drug,
 "analysis_date": pd.Timestamp.now.isoformat,
 "total_reports": int(signals_df["a"].sum),
 "unique_pts_analyzed": len(signals_df),
 "signals_prr": int(signals_df["signal_prr"].sum),
 "signals_ror": int(signals_df["signal_ror"].sum),
 "signals_ic": int(signals_df["signal_ic"].sum),
 "signals_ebgm": int(ebgm_df["signal_ebgm"].sum),
 "consensus_signals": int(combined["consensus_signal"].sum),
 "top_signals": combined[combined["consensus_signal"]].nlargest(20, "prr").to_dict("records"),
 "summary": {
 "method": "PRR + ROR + IC + EBGM consensus",
 "thresholds": {
 "prr": "≥2, χ²≥4, N≥3",
 "ror": "lower 95% CI > 1, N≥3",
 "ic": "IC > 0, N≥3",
 "ebgm": "EB05 ≥ 2",
 },
 },
 }

 with open(f"{output_dir}/pv_signal_report.json", "w") as f:
 json.dump(report, f, indent=2, default=str)

 # Markdown report
 md = f"# Pharmacovigilance Signal Report: {target_drug}\n\n"
 md += f"**Analysis Date**: {report['analysis_date']}\n\n"
 md += f"## Summary\n\n"
 md += f"| Metric | Value |\n|---|---|\n"
 md += f"| Total Reports | {report['total_reports']:,} |\n"
 md += f"| PTs Analyzed | {report['unique_pts_analyzed']} |\n"
 md += f"| PRR Signals | {report['signals_prr']} |\n"
 md += f"| ROR Signals | {report['signals_ror']} |\n"
 md += f"| IC Signals | {report['signals_ic']} |\n"
 md += f"| EBGM Signals | {report['signals_ebgm']} |\n"
 md += f"| **Consensus Signals** | **{report['consensus_signals']}** |\n\n"
 md += f"## Top Consensus Signals\n\n"
 md += "| PT | N | PRR | ROR | IC | EBGM |\n|---|---|---|---|---|---|\n"
 for s in report["top_signals"]:
 md += f"| {s['pt']} | {s['a']} | {s['prr']} | {s['ror']} | {s['ic']} | {s['ebgm']} |\n"

 with open(f"{output_dir}/pv_signal_report.md", "w") as f:
 f.write(md)

 return report
```

---

## Best Practices

1. **multiplemethod's**: PRR/ROR/IC/EBGM for、2 methodabove/more
2. **MedDRA PT **: LLT degree 、SOC 
3. **criteria N≥3**: number/count's
4. **Weber caution**: large
5. **Notoriety Bias **: possible
6. **'s**: FAERS many（ 10-15%）。Case ID latest
7. **'s**: indication-reaction 's caution

## Completeness Checklist

- [ ] FAERS Data Retrievaland preprocessingcompletion
- [ ] MedDRA mappingfor
- [ ] PRR/ROR/IC/EBGM 
- [ ] threshold（formula）
- [ ] Time-to-Onset distributionmin
- [ ] （）
- [ ] evaluation（Naranjo / WHO-UMC）
- [ ] allreport（JSON + Markdown）generation

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/pv_signal_report.json` | results（JSON） | mincompletion |
| `results/pv_signal_report.md` | report（Markdown） | reportgeneration |
| `figures/pv_temporal_trend.png` | time seriesfigure | min |
| `figures/pv_demographics.png` | distributionfigure | min |

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
3. Write `report.md` summarizing methods, results, and interpretation

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-survival-clinical` | ← allanalysis |
| `scientific-statistical-testing` | ← χ² testingmultiple comparisoncorrection |
| `scientific-drug-target-profiling` | ← filebackground |
| `scientific-admet-pharmacokinetics` | ← toxicitypredictionmetabolic pathwayinformation |
| `scientific-clinical-decision-support` | → information'sclinical decision supportto 's |
| `scientific-deep-research` | ← allliterature's |
| `scientific-clinical-trials-analytics` | ← clinical trialdatabase |
| `scientific-regulatory-science` | → FDA/FAERS dataintegration |
| `scientific-pharmacogenomics` | ← PGx metabolismtypeallevaluation |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
  |-- Generate report.md with all sections
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
| G5 | All figure/table text is English-only | MUST |
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
