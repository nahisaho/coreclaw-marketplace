---
name: scientific-adaptive-experiments
description: |
 Adaptive experiment design skill. Sequential experiment optimization, Bayesian optimization, multi-armed bandit, response-adaptive randomization, and interim analysis for efficient experimental workflows.
---

# Scientific Adaptive Experiments

experiment's data Experimental Design fix
Experimental Designpipeline is provided。

## When to Use

- A/B testing's is performedand
- search/explorationand utilizingoptimizationwhen needed
- analysis is performedand
- Bayesiandesign foramountsearch/explorationwhen needed
- Response-Adaptive Randomization clinical trial is designedand

---

## Quick Start

## 1. 

```python
import numpy as np
import pandas as pd
from typing import List, Dict


class ThompsonSamplingBandit:
 """
 Thompson Sampling -。
 """

 def __init__(self, n_arms, prior_alpha=1.0, prior_beta=1.0):
 """
 Parameters:
 n_arms: int — number/count
 prior_alpha: float — Beta prior distribution's α
 prior_beta: float — Beta prior distribution's β
 """
 self.n_arms = n_arms
 self.alphas = np.full(n_arms, prior_alpha)
 self.betas = np.full(n_arms, prior_beta)
 self.history = []

 def select_arm(self):
 samples = np.array([
 np.random.beta(a, b)
 for a, b in zip(self.alphas, self.betas)])
 return int(np.argmax(samples))

 def update(self, arm, reward):
 if reward > 0:
 self.alphas[arm] += 1
 else:
 self.betas[arm] += 1
 self.history.append({"arm": arm, "reward": reward})

 def get_summary(self):
 records = []
 for i in range(self.n_arms):
 a, b = self.alphas[i], self.betas[i]
 samples = np.random.beta(a, b, 10000)
 records.append({
 "arm": i,
 "alpha": a, "beta": b,
 "mean": a / (a + b),
 "n_pulls": int(a + b - 2),
 "95%_lower": float(np.percentile(samples, 2.5)),
 "95%_upper": float(np.percentile(samples, 97.5)),
 })
 return pd.DataFrame(records)


def run_bandit_experiment(true_rates, n_rounds=1000,
 algorithm="thompson", seed=42):
 """
 experimentsimulation。

 Parameters:
 true_rates: list[float] — each's 's successrate
 n_rounds: int — number of rounds
 algorithm: str — "thompson" / "ucb" / "epsilon_greedy"
 seed: int — random seed
 """
 rng = np.random.default_rng(seed)
 n_arms = len(true_rates)

 if algorithm == "thompson":
 bandit = ThompsonSamplingBandit(n_arms)
 for t in range(n_rounds):
 arm = bandit.select_arm
 reward = int(rng.random < true_rates[arm])
 bandit.update(arm, reward)
 elif algorithm == "ucb":
 counts = np.zeros(n_arms)
 values = np.zeros(n_arms)
 history = []
 for t in range(n_rounds):
 if t < n_arms:
 arm = t
 else:
 ucb = values + np.sqrt(2 * np.log(t) / (counts + 1e-10))
 arm = int(np.argmax(ucb))
 reward = int(rng.random < true_rates[arm])
 counts[arm] += 1
 values[arm] += (reward - values[arm]) / counts[arm]
 history.append({"arm": arm, "reward": reward})
 bandit = type("UCB", , {
 "history": history,
 "get_summary": lambda self: pd.DataFrame([
 {"arm": i, "n_pulls": int(counts[i]),
 "mean": values[i]} for i in range(n_arms)])
 })
 else: # epsilon_greedy
 epsilon = 0.1
 counts = np.zeros(n_arms)
 values = np.zeros(n_arms)
 history = []
 for t in range(n_rounds):
 if rng.random < epsilon:
 arm = rng.integers(n_arms)
 else:
 arm = int(np.argmax(values))
 reward = int(rng.random < true_rates[arm])
 counts[arm] += 1
 values[arm] += (reward - values[arm]) / counts[arm]
 history.append({"arm": arm, "reward": reward})
 bandit = type("EG", , {
 "history": history,
 "get_summary": lambda self: pd.DataFrame([
 {"arm": i, "n_pulls": int(counts[i]),
 "mean": values[i]} for i in range(n_arms)])
 })

 summary = bandit.get_summary
 best_arm = summary.loc[summary["mean"].idxmax, "arm"]
 print(f"Bandit ({algorithm}, {n_rounds} rounds):")
 print(f" Best arm: {best_arm} (est. rate={summary.loc[summary['arm']==best_arm, 'mean'].values[0]:.3f})")
 print(f" True best: {np.argmax(true_rates)} (rate={max(true_rates):.3f})")
 return bandit, summary
```

## 2. testing (SPRT)

```python
def sequential_probability_ratio_test(data_stream,
 h0_rate=0.5,
 h1_rate=0.6,
 alpha=0.05, beta=0.2):
 """
 Wald 's ratetesting (SPRT)。

 Parameters:
 data_stream: iterable — data (0/1)
 h0_rate: float — null hypothesis's successrate
 h1_rate: float — alternative hypothesis's successrate
 alpha: float — 1 type's rate
 beta: float — 2 type's rate
 """
 A = np.log((1 - beta) / alpha) # H1 
 B = np.log(beta / (1 - alpha)) # H0 

 log_lr = 0.0
 history = []

 for i, x in enumerate(data_stream):
 # number/countlikelihood's
 if x == 1:
 log_lr += np.log(h1_rate / h0_rate)
 else:
 log_lr += np.log((1 - h1_rate) / (1 - h0_rate))

 decision = None
 if log_lr >= A:
 decision = "reject_H0"
 elif log_lr <= B:
 decision = "accept_H0"

 history.append({
 "step": i + 1, "observation": x,
 "log_lr": log_lr,
 "upper_bound": A, "lower_bound": B,
 "decision": decision,
 })

 if decision is not None:
 print(f"SPRT: {decision} at step {i+1} "
 f"(log_LR={log_lr:.3f})")
 break

 df = pd.DataFrame(history)
 if df["decision"].iloc[-1] is None:
 print(f"SPRT: Inconclusive after {len(df)} observations")
 return df
```

## 3. Bayesianapplicationamountsearch/exploration

```python
def bayesian_adaptive_dose_finding(dose_levels, n_patients=30,
 target_toxicity=0.33,
 prior_alpha=1.0,
 prior_beta=1.0, cohort_size=3,
 seed=42):
 """
 Bayesianapplicationamountsearch/exploration (CRM )。

 Parameters:
 dose_levels: list[float] — foramount
 n_patients: int — patientnumber/count
 target_toxicity: float — targettoxicityrate
 prior_alpha: float — Beta prior distribution α
 prior_beta: float — Beta prior distribution β
 cohort_size: int — （foramount patientnumber/count）
 seed: int — random seed
 """
 rng = np.random.default_rng(seed)
 n_doses = len(dose_levels)
 alphas = np.full(n_doses, prior_alpha)
 betas = np.full(n_doses, prior_beta)
 history = []

 # 's toxicityrate (simulationfor)
 true_tox = np.linspace(0.05, 0.60, n_doses)

 current_dose = 0
 for patient in range(n_patients):
 toxicity = int(rng.random < true_tox[current_dose])

 if toxicity:
 alphas[current_dose] += 1
 else:
 betas[current_dose] += 1

 history.append({
 "patient": patient + 1,
 "dose_level": current_dose,
 "dose_value": dose_levels[current_dose],
 "toxicity": toxicity,
 })

 # 's foramountselection (: cohort_size and)
 if (patient + 1) % cohort_size == 0:
 means = alphas / (alphas + betas)
 distances = np.abs(means - target_toxicity)
 current_dose = int(np.argmin(distances))

 # MTD 
 final_means = alphas / (alphas + betas)
 mtd_idx = int(np.argmin(np.abs(final_means - target_toxicity)))

 summary = pd.DataFrame({
 "dose_level": range(n_doses),
 "dose_value": dose_levels,
 "est_toxicity": final_means,
 "n_treated": [sum(1 for h in history
 if h["dose_level"] == i)
 for i in range(n_doses)],
 })

 print(f"Bayesian adaptive: MTD = dose {mtd_idx} "
 f"(value={dose_levels[mtd_idx]}, "
 f"est_tox={final_means[mtd_idx]:.3f})")
 return summary, pd.DataFrame(history)
```

---

## Pipeline Integration

```
[experimentpurpose] → adaptive-experiments → statistical-testing
 (design) (analysis)
 │
 doe ← statistical-simulation
 (design) (powermin)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `bandit_summary.csv` | results | → |
| `sprt_history.csv` | SPRT testing | → results |
| `dose_finding.csv` | foramountsearch/explorationresults | → MTD |

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
