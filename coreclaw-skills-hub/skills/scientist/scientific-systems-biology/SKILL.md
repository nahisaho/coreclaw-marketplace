---
name: scientific-systems-biology
description: |
 Systems biology skill. Network modeling, flux balance analysis, dynamical systems simulation, and multi-scale biological system analysis.
---

# Scientific Systems Biology

's quantitativepipeline is provided。
ODE 's 、analysis（FBA）、
genenetwork（GRN）、parametersdegreeanalysis、
BioModelsReactomeKEGGBiGG 's integrationutilizing is supported。

## When to Use

- pathway's（ODE）when needed
- metabolismnetwork'sanalysis（FBA） is performedand
- genenetwork（GRN） is estimatedand
- BioModels / SBML 's retrievalsimulation is performedand
- parameters's degreeanalysis is performedand

---

## Quick Start

## 1. SBML simulation

```python
import numpy as np
import pandas as pd

def simulate_sbml_model(sbml_file, duration=100, n_points=1000):
 """
 SBML 'ssimulation。

 SBML (Systems Biology Markup Language):
 's standard。BioModels DB 1,000+ 。

 procedure:
 1. SBML → RoadRunner 
 2. initialconditionsettings
 3. timesimulation
 4. resultsextractionvisualization

 support:
 - ODE （）
 - Stochastic（Gillespie SSA）
 - Hybrid
 """
 import roadrunner

 rr = roadrunner.RoadRunner(sbml_file)
 result = rr.simulate(0, duration, n_points)

 df = pd.DataFrame(result, columns=result.colnames)
 species = [c for c in df.columns if c != "time"]

 print(f" SBML: {len(species)} species simulated over t=[0, {duration}]")
 print(f" Species: {', '.join(species[:5])}{'...' if len(species) > 5 else ''}")
 return df, rr


def steady_state_analysis(rr):
 """
 statusanalysis。

 status: dx/dt = f(x, p) = 0
 J 's value → :
 - Re(λᵢ) < 0 ∀i: point
 - ∃i: Re(λᵢ) > 0: 
 """
 rr.steadyState
 species_ids = rr.getFloatingSpeciesIds
 ss_values = rr.getFloatingSpeciesConcentrations

 # 
 jac = rr.getFullJacobian
 eigenvalues = np.linalg.eigvals(jac)
 stable = all(np.real(eigenvalues) < 0)

 ss_dict = dict(zip(species_ids, ss_values))
 ss_dict["stable"] = stable
 ss_dict["eigenvalues"] = eigenvalues.tolist

 print(f" Steady state: {'Stable' if stable else 'Unstable'}")
 return ss_dict
```

## 2. analysis（FBA）

```python
def flux_balance_analysis(model_path, objective="biomass", method="fba"):
 """
 metabolismanalysis。

 FBA formula:
 max c^T · v (objective function、 biomass)
 s.t. S · v = 0 (status)
 vₘᵢₙ ≤ v ≤ vₘₐₓ (range)

 method:
 - "fba": standard FBA — LP distribution
 - "pfba": Parsimonious FBA — optimization
 - "fva": Flux Variability Analysis — eachreaction's range
 - "loopless": loop FBA

 input: SBML / JSON / YAML shapeformula's genomemetabolism（GEM）
 BiGG Models DB: 100+ organism/species's GEM 
 """
 import cobra

 model = cobra.io.read_sbml_model(model_path)
 print(f" Model: {model.id} — {len(model.reactions)} reactions, "
 f"{len(model.metabolites)} metabolites, {len(model.genes)} genes")

 if method == "fba":
 solution = model.optimize
 elif method == "pfba":
 solution = cobra.flux_analysis.pfba(model)
 elif method == "fva":
 fva_result = cobra.flux_analysis.flux_variability_analysis(
 model, fraction_of_optimum=0.9)
 return fva_result
 elif method == "loopless":
 from cobra.flux_analysis.loopless import loopless_solution
 solution = loopless_solution(model)
 objective_value = solution.objective_value
 fluxes = solution.fluxes
 print(f" Loopless FBA: objective={objective_value:.4f}")
 result = {
 "objective_value": objective_value,
 "n_active_reactions": (fluxes.abs > 1e-6).sum,
 }
 return result, fluxes

 # results
 objective_value = solution.objective_value
 fluxes = solution.fluxes

 # Essential genes (single gene knockouts)
 essential = []
 for gene in model.genes:
 with model:
 gene.knock_out
 ko_sol = model.optimize
 if ko_sol.objective_value < 0.01 * objective_value:
 essential.append(gene.id)

 print(f" FBA: objective={objective_value:.4f}, "
 f"{len(essential)} essential genes")

 result = {
 "objective_value": objective_value,
 "n_active_reactions": (fluxes.abs > 1e-6).sum,
 "n_essential_genes": len(essential),
 "essential_genes": essential,
 }
 return result, fluxes
```

## 3. genenetwork（GRN）

```python
def infer_grn(expression_matrix, method="genie3", n_top=1000):
 """
 genenetwork（GRN）。

 method:
 - "genie3": GENIE3 — Random Forest 
 eachgene gⱼ 's allgene regression、
 featuresimportantdegree 's and.
 - "scenic": SCENIC — cis-regulatory analysisintegration
 - "granger": Granger — time series data

 GENIE3 :
 For each target gene gⱼ:
 Train RF: gⱼ = f(g₁,..., gⱼ₋₁, gⱼ₊₁,..., gₚ)
 Weight wᵢⱼ = importance of gᵢ for predicting gⱼ
 """
 from arboreto.algo import genie3
 import warnings

 # GENIE3
 if method == "genie3":
 network = genie3(expression_matrix.values,
 gene_names=expression_matrix.columns.tolist)
 network = network.sort_values("importance", ascending=False).head(n_top)
 elif method in ("scenic", "granger"):
 warnings.warn(f"Method '{method}' requires external setup. Falling back to GENIE3.")
 network = genie3(expression_matrix.values,
 gene_names=expression_matrix.columns.tolist)
 network = network.sort_values("importance", ascending=False).head(n_top)

 # networkconstruction
 import networkx as nx
 G = nx.DiGraph
 for _, row in network.iterrows:
 G.add_edge(row["TF"], row["target"], weight=row["importance"])

 # TF（number/count）
 out_degrees = sorted(G.out_degree, key=lambda x: x[1], reverse=True)
 top_tfs = out_degrees[:10]

 print(f" GRN: {G.number_of_nodes} nodes, {G.number_of_edges} edges")
 print(f" Top TFs: {', '.join([tf for tf, _ in top_tfs[:5]])}")
 return G, network
```

## 4. parametersdegreeanalysis

```python
from scipy.optimize import differential_evolution
from SALib.sample import saltelli
from SALib.analyze import sobol

def parameter_estimation(model_func, data, param_bounds, method="de"):
 """
 ODE parameters。

 method:
 - "de": Differential Evolution（optimization）
 - "mcmc": MCMC — pymc/emcee（posterior distribution）

 objective function: Σ (y_data - y_model)² / σ² → minimize
 """
 def objective(params):
 y_pred = model_func(params)
 residuals = (data["y_obs"] - y_pred) ** 2
 return np.sum(residuals / data.get("sigma", 1) ** 2)

 if method == "de":
 result = differential_evolution(objective, bounds=param_bounds,
 seed=42, maxiter=1000, tol=1e-8)
 return {
 "params": result.x,
 "cost": result.fun,
 "success": result.success,
 "message": result.message,
 }
 elif method in ("nelder-mead", "l-bfgs-b"):
 from scipy.optimize import minimize
 x0 = np.mean(param_bounds, axis=1)
 result = minimize(objective, x0, method=method,
 bounds=param_bounds if method == "l-bfgs-b" else None,
 options={"maxiter": 1000})
 return {
 "params": result.x,
 "cost": result.fun,
 "success": result.success,
 "message": result.message,
 }
 else:
 from scipy.optimize import minimize
 x0 = np.mean(param_bounds, axis=1)
 result = minimize(objective, x0, method=method,
 bounds=param_bounds,
 options={"maxiter": 1000})
 return {
 "params": result.x,
 "cost": result.fun,
 "success": result.success,
 "message": result.message,
 }


def global_sensitivity_analysis(model_func, param_names, param_bounds,
 n_samples=1024):
 """
 Sobol degreeanalysis。

 :
 - S1: degree（main effect）
 - ST: alldegree（main effect＋interactionall）
 - S2: degree（interaction）

 S1 + interaction = ST
 ΣS1 < 1 case、interaction.
 """
 problem = {
 "num_vars": len(param_names),
 "names": param_names,
 "bounds": param_bounds,
 }

 param_values = saltelli.sample(problem, n_samples)
 Y = np.array([model_func(p) for p in param_values])

 Si = sobol.analyze(problem, Y)

 sa_df = pd.DataFrame({
 "parameter": param_names,
 "S1": Si["S1"],
 "S1_conf": Si["S1_conf"],
 "ST": Si["ST"],
 "ST_conf": Si["ST_conf"],
 })

 print(f" Sensitivity: top parameter = {sa_df.loc[sa_df['ST'].idxmax, 'parameter']} "
 f"(ST={sa_df['ST'].max:.3f})")
 return sa_df, Si
```

## References

### Output Files

| File | Format |
|---|---|
| `results/simulation_timecourse.csv` | CSV |
| `results/fba_fluxes.csv` | CSV |
| `results/grn_network.csv` | CSV |
| `results/sensitivity_analysis.csv` | CSV |
| `results/parameter_estimates.json` | JSON |
| `figures/timecourse_plot.png` | PNG |
| `figures/flux_map.png` | PNG |
| `figures/grn_graph.png` | PNG |

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

### Related Skills

| Skill | Integration |
|---|---|
| [scientific-network-analysis](../scientific-network-analysis/SKILL.md) | GRN networkanalysis |
| [scientific-multi-omics](../scientific-multi-omics/SKILL.md) | multi-omicsdataintegration |
| [scientific-bayesian-statistics](../scientific-bayesian-statistics/SKILL.md) | Bayesianparameters |
| [scientific-doe](../scientific-doe/SKILL.md) | Experimental Designdegreeanalysis |
| [scientific-metabolomics](../scientific-metabolomics/SKILL.md) | metabolism-metabolomeintegration |

#### Dependencies

- cobra (cobrapy), roadrunner (libroadrunner), arboreto, SALib, scipy, networkx
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria

Before execution, define:
- [ ] **Objective**: specific, measurable outcome
- [ ] **Input requirements**: data format, size, quality
- [ ] **Output specification**: expected files, formats, metrics
- [ ] **Success threshold**: quantitative pass/fail criteria

#### Pass Criteria
- All specified outputs produced and validated
- Results reproducible with same inputs and seed
- Error cases handled gracefully with informative messages
- Performance within acceptable time/memory bounds
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
