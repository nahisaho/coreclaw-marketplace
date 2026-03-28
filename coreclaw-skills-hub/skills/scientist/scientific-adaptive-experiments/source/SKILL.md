---
name: scientific-adaptive-experiments
description: |
 Adaptive experiment design skill. Sequential experiment optimization, Bayesian optimization, multi-armed bandit, response-adaptive randomization, and interim analysis for efficient experimental workflows.
tu_tools:
 - key: biotools
 name: bio.tools
 description: Experimental Designtoolsearch
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | Experimental Designtoolsearch |

---

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
