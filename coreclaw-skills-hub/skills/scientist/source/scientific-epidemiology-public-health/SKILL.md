---
name: scientific-epidemiology-public-health
description: |
 analysisskill。observationresearch（/case/cross-cutting）
 （RR/OR/HR/NNT）standardization（SMR）rate
 （GIS / clustering）causal inference（DAG）
 WHO/CDC/EU dataintegrationpipeline。
 ToolUniverse integration: who_gho。
tu_tools:
 - key: who_gho
 name: WHO GHO
 description: WHO Global Health Observatory API
---

# Scientific Epidemiology & Public Health

research and dataanalysis'spipeline is provided。
researchdesign、、、
、evaluation、databaseintegration systematichandles。

## When to Use

- observationresearch's（RR / OR / HR） is computedand
- ratestandardization（SMR） calculationwhen needed
- （diseaseclusteringGIS mapping） is performedand
- DAG（timesgraph）structure minwhen needed
- WHO / CDC / EU 's data retrievalanalysiswhen needed

---

## Quick Start

## 1. 

```python
import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_risk_measures(a, b, c, d, alpha=0.05):
 """
 2×2 mintablefrom is computed。

 Disease+ Disease-
 Exposed+ a b → a+b
 Exposed- c d → c+d
 a+c b+d N

 :
 - Risk (Incidence): R = cases / total
 - Risk Ratio (RR): R_exposed / R_unexposed（research）
 - Odds Ratio (OR): (a·d) / (b·c)（caseresearch）
 - Risk Difference (RD): R_exposed - R_unexposed
 - NNT (Number Needed to Treat): 1 / |RD|
 - Attributable Fraction (AF): (RR - 1) / RR
 """
 z = norm.ppf(1 - alpha / 2)

 # Risk
 R1 = a / (a + b) # Exposed
 R0 = c / (c + d) # Unexposed

 # Risk Ratio
 RR = R1 / R0
 ln_RR_se = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))
 RR_ci = (RR * np.exp(-z * ln_RR_se), RR * np.exp(z * ln_RR_se))

 # Odds Ratio
 OR = (a * d) / (b * c)
 ln_OR_se = np.sqrt(1/a + 1/b + 1/c + 1/d)
 OR_ci = (OR * np.exp(-z * ln_OR_se), OR * np.exp(z * ln_OR_se))

 # Risk Difference
 RD = R1 - R0
 RD_se = np.sqrt(R1*(1-R1)/(a+b) + R0*(1-R0)/(c+d))
 RD_ci = (RD - z * RD_se, RD + z * RD_se)

 # NNT
 NNT = 1 / abs(RD) if RD != 0 else np.inf

 # Attributable fraction
 AF = (RR - 1) / RR if RR > 0 else 0

 results = {
 "risk_exposed": round(R1, 4),
 "risk_unexposed": round(R0, 4),
 "RR": round(RR, 4), "RR_CI": [round(x, 4) for x in RR_ci],
 "OR": round(OR, 4), "OR_CI": [round(x, 4) for x in OR_ci],
 "RD": round(RD, 4), "RD_CI": [round(x, 4) for x in RD_ci],
 "NNT": round(NNT, 1),
 "AF": round(AF, 4),
 }

 print(f" RR={RR:.3f} ({RR_ci[0]:.3f}–{RR_ci[1]:.3f}), "
 f"OR={OR:.3f} ({OR_ci[0]:.3f}–{OR_ci[1]:.3f})")
 return results
```

## 2. rateSMR

```python
def age_standardization(observed_df, standard_pop, method="direct"):
 """
 rate and standardization。

 method:
 - "direct": method — standard's configuration
 ASR = Σ(rateᵢ × standardratioᵢ)
 - "indirect": method — SMR (Standardized Mortality Ratio)
 SMR = observationnumber/count / number/count
 number/count = Σ(standardrateᵢ × ᵢ)

 SMR 's 95% CI（Byar's approximation）:
 SMR_lower = SMR × (1 - 1/(9·O) - z/(3·√O))³
 SMR_upper = (O+1)/E × (1 - 1/(9·(O+1)) + z/(3·√(O+1)))³
 """
 if method == "direct":
 # methodrate
 merged = observed_df.merge(standard_pop, on="age_group")
 merged["weighted_rate"] = merged["rate"] * merged["std_proportion"]
 asr = merged["weighted_rate"].sum

 # variance（term）
 merged["var_component"] = (merged["std_proportion"] ** 2 *
 merged["rate"] * (1 - merged["rate"]) /
 merged["population"])
 se = np.sqrt(merged["var_component"].sum)

 return {
 "ASR": round(asr, 6),
 "ASR_per_100k": round(asr * 1e5, 2),
 "SE": round(se, 6),
 "CI_95": [round((asr - 1.96*se)*1e5, 2), round((asr + 1.96*se)*1e5, 2)],
 }

 elif method == "indirect":
 # method SMR
 merged = observed_df.merge(standard_pop, on="age_group",
 suffixes=("_obs", "_std"))
 merged["expected"] = merged["rate_std"] * merged["population_obs"]
 O = merged["deaths_obs"].sum
 E = merged["expected"].sum

 SMR = O / E
 z = 1.96

 # Byar's approximation
 lower = SMR * (1 - 1/(9*O) - z/(3*np.sqrt(O)))**3
 upper = ((O+1)/E) * (1 - 1/(9*(O+1)) + z/(3*np.sqrt(O+1)))**3

 print(f" SMR={SMR:.3f} ({lower:.3f}–{upper:.3f}), O={O}, E={E:.1f}")
 return {"SMR": round(SMR, 4), "CI_95": [round(lower, 4), round(upper, 4)],
 "observed": O, "expected": round(E, 1)}
```

## 3. diseaseclustering

```python
def spatial_cluster_detection(cases_gdf, population_gdf, method="kulldorff"):
 """
 diseaseclustering。

 method:
 - "kulldorff": Kulldorff's spatial scan statistic（SaTScan）
 H₀: λ(s) = number/count（）
 H₁: ∃ shape Z λ_in > λ_out
 LLR = (O_Z/E_Z)^{O_Z} × ((O-O_Z)/(O-E_Z))^{O-O_Z}
 - "moran": Local Moran's I（correlation）
 Iᵢ = zᵢ Σⱼ wᵢⱼ zⱼ
 - "getis_ord": Getis-Ord Gi* — 

 for:
 - disease's（）'s
 - / 's
 """
 import geopandas as gpd
 from libpysal.weights import Queen
 from esda.moran import Moran_Local
 from esda.getisord import G_Local

 if method == "moran":
 W = Queen.from_dataframe(cases_gdf)
 W.transform = "r"
 rates = cases_gdf["cases"] / cases_gdf["population"]
 lisa = Moran_Local(rates.values, W)

 cases_gdf["local_moran_I"] = lisa.Is
 cases_gdf["local_moran_p"] = lisa.p_sim
 cases_gdf["cluster_type"] = classify_lisa(lisa)

 n_hotspots = (cases_gdf["cluster_type"] == "HH").sum
 n_coldspots = (cases_gdf["cluster_type"] == "LL").sum
 print(f" LISA: {n_hotspots} hotspots, {n_coldspots} coldspots")

 elif method == "getis_ord":
 W = Queen.from_dataframe(cases_gdf)
 W.transform = "b"
 rates = cases_gdf["cases"] / cases_gdf["population"]
 g_local = G_Local(rates.values, W)

 cases_gdf["gi_star"] = g_local.Zs
 cases_gdf["gi_p"] = g_local.p_sim
 cases_gdf["hotspot"] = (g_local.Zs > 1.96) & (g_local.p_sim < 0.05)

 return cases_gdf


def classify_lisa(lisa, p_threshold=0.05):
 """LISA classification（HH/HL/LH/LL/NS）。"""
 types = []
 for i in range(len(lisa.Is)):
 if lisa.p_sim[i] > p_threshold:
 types.append("NS")
 elif lisa.q[i] == 1:
 types.append("HH")
 elif lisa.q[i] == 2:
 types.append("LH")
 elif lisa.q[i] == 3:
 types.append("LL")
 elif lisa.q[i] == 4:
 types.append("HL")
 return types
```

## 4. DAG min

```python
def dag_confounding_analysis(dag_edges, exposure, outcome):
 """
 DAG（timesgraph）'s min。

 pipeline:
 1. DAG construction
 2. 
 3. （Sufficient Adjustment Set）
 4. d-min

 Pearl 's criteria:
 number/count Z criteria ⟺
 Z X→Y 's all block、
 Z X 's
 """
 import networkx as nx
 from dowhy import CausalModel

 G = nx.DiGraph
 G.add_edges_from(dag_edges)

 # 
 backdoor_paths = find_backdoor_paths(G, exposure, outcome)

 # 
 adjustment_sets = find_adjustment_sets(G, exposure, outcome)

 result = {
 "n_backdoor_paths": len(backdoor_paths),
 "backdoor_paths": backdoor_paths,
 "adjustment_sets": adjustment_sets,
 "minimal_adjustment": min(adjustment_sets, key=len) if adjustment_sets else [],
 }

 print(f" DAG: {len(backdoor_paths)} backdoor paths, "
 f"minimal adjustment = {result['minimal_adjustment']}")
 return result


def find_backdoor_paths(G, source, target):
 """（X ←... → Y）."""
 undirected = G.to_undirected
 all_paths = list(nx.all_simple_paths(undirected, source, target))
 backdoor = [p for p in all_paths if G.has_edge(p[1], source)]
 return backdoor


def find_adjustment_sets(G, exposure, outcome):
 """min（implementation）。"""
 from itertools import combinations
 nodes = set(G.nodes) - {exposure, outcome}
 sets = []
 for r in range(len(nodes) + 1):
 for combo in combinations(nodes, r):
 if blocks_all_backdoor(G, exposure, outcome, set(combo)):
 sets.append(list(combo))
 return sets


def blocks_all_backdoor(G, X, Y, Z):
 """Z 's block。"""
 # d-separation 
 return True # allimplementation
```

## References

### Output Files

| File | Format |
|---|---|
| `results/risk_measures.json` | JSON |
| `results/age_standardized_rates.csv` | CSV |
| `results/spatial_clusters.geojson` | GeoJSON |
| `results/dag_analysis.json` | JSON |
| `figures/disease_map.png` | PNG |
| `figures/dag_diagram.png` | PNG |
| `figures/forest_plot.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| WHO | `who_gho_get_data` | WHO GHO Data Retrieval |
| WHO | `who_gho_query_health_data` | WHO |
| CDC | `cdc_data_search_datasets` | CDC dataset search |
| CDC | `cdc_data_get_dataset` | CDC data retrieval |
| EUHealthInfo | `euhealthinfo_search_surveillance_mortality_rates` | ratedata |
| EUHealthInfo | `euhealthinfo_search_healthcare_expenditure` | data |
| EUHealthInfo | `euhealthinfo_search_population_health_survey` | investigationdata |
| HealthDisparities | `health_disparities_get_svi_info` | |
| HealthDisparities | `health_disparities_get_county_rankings_info` | |
| ClinicalTrials | `search_clinical_trials` | clinical trial search |
| PubMed | `PubMed_Guidelines_Search` | |

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-causal-inference](../scientific-causal-inference/SKILL.md) | causal inference |
| [scientific-survival-clinical](../scientific-survival-clinical/SKILL.md) | analysisCox regression |
| [scientific-meta-analysis](../scientific-meta-analysis/SKILL.md) | systematic review |
| [scientific-infectious-disease](../scientific-infectious-disease/SKILL.md) | infectious disease |
| [scientific-bayesian-statistics](../scientific-bayesian-statistics/SKILL.md) | Bayesian |
| [scientific-clinical-trials-analytics](../scientific-clinical-trials-analytics/SKILL.md) | clinical trialregistry |

#### Dependencies

- geopandas, libpysal, esda, dowhy, lifelines, scipy, statsmodels
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
