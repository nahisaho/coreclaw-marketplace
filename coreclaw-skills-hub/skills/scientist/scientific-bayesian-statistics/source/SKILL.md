---
name: scientific-bayesian-statistics
description: |
 Bayesian statistics skill. PyMC/Stan/ArviZ-based Bayesian regression, hierarchical models, MCMC sampling, Bayesian optimization, posterior predictive checks, and model comparison.
tu_tools:
 - key: biotools
 name: bio.tools
 description: Bayesian statistics tool registry search
---

# Scientific Bayesian Statistics

Bayesianinferenceforanalysisskill。ratelog
framework（PyMC, Stan, NumPyro）utilizing
parameterscomparisonsupport is performed。

## When to Use

- parameters's posterior distribution
- Bayesian（）
- BayesianregressionBayesianclassification
- MCMC diagnosis（Rhat, ESS, plot）
- comparison（WAIC, LOO-CV, Bayesian）
- Bayesianoptimization（Gaussian Process）
- prediction

## Quick Start

### Bayesiananalysispipeline

```
Phase 1: Model Specification
 - likelihoodnumber/count'sselection (Normal, Poisson, Binomial, etc.)
 - prior distribution's settings (informationprior distributionrecommended)
 - parameters'sdefinition
 ↓
Phase 2: Prior Predictive Check
 - predictionsimulation
 - prior distribution'sverification
 - and 'sverification
 ↓
Phase 3: MCMC Sampling
 - NUTS (No-U-Turn Sampler) 
 - number/countnumber/countsettings (chains≥4, draws≥2000)
 - convergencediagnosis (Rhat < 1.01, ESS > 400)
 ↓
Phase 4: Posterior Analysis
 - posterior distributionvisualization (forest, trace, pair plot)
 - 95% HDI (Highest Density Interval)
 - prediction (PPC)
 ↓
Phase 5: Model Comparison
 - WAIC / LOO-CV 
 - Bayes Factor calculation
 - mean (Stacking)
 ↓
Phase 6: Reporting
 - valuesummarytable
 - posterior distributionplot
 - results'sreportgeneration
```

## Workflow

### 1. PyMC: Bayesianlineshaperegression

```python
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# === datageneration (example) ===
np.random.seed(42)
N = 100
X = np.random.randn(N)
true_alpha, true_beta, true_sigma = 1.0, 2.5, 0.5
y = true_alpha + true_beta * X + np.random.normal(0, true_sigma, N)

# === Bayesianlineshaperegression ===
with pm.Model as linear_model:
 # prior distribution
 alpha = pm.Normal("alpha", mu=0, sigma=10)
 beta = pm.Normal("beta", mu=0, sigma=10)
 sigma = pm.HalfNormal("sigma", sigma=5)

 # likelihood
 mu = alpha + beta * X
 y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

 # MCMC sampling (NUTS)
 trace = pm.sample(
 draws=2000,
 tune=1000,
 chains=4,
 cores=4,
 target_accept=0.95,
 return_inferencedata=True,
 )

# === convergencediagnosis ===
print(az.summary(trace, var_names=["alpha", "beta", "sigma"]))
# Rhat < 1.01 && ESS > 400 verification

# === plot ===
az.plot_trace(trace, var_names=["alpha", "beta", "sigma"])
plt.savefig("figures/bayesian_trace.png", dpi=300, bbox_inches="tight")
plt.show
```

### 2. Bayesian（）

```python
import pandas as pd

# === Bayesianregression  ===
# example: multiple's 'sprediction
# school_id: loopnumber/count
# x: predictionnumber/count, y: objective variable

def hierarchical_model(df):
 school_ids = df["school_id"].unique
 school_idx = df["school_id"].map({s: i for i, s in enumerate(school_ids)}).values
 n_schools = len(school_ids)

 with pm.Model as hier_model:
 # Hyper-priors (allmean)
 mu_alpha = pm.Normal("mu_alpha", mu=0, sigma=10)
 sigma_alpha = pm.HalfNormal("sigma_alpha", sigma=5)
 mu_beta = pm.Normal("mu_beta", mu=0, sigma=10)
 sigma_beta = pm.HalfNormal("sigma_beta", sigma=5)

 # 'sparameters (partial)
 alpha = pm.Normal("alpha", mu=mu_alpha, sigma=sigma_alpha, shape=n_schools)
 beta = pm.Normal("beta", mu=mu_beta, sigma=sigma_beta, shape=n_schools)

 # residual
 sigma = pm.HalfNormal("sigma", sigma=5)

 # likelihood
 mu = alpha[school_idx] + beta[school_idx] * df["x"].values
 y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=df["y"].values)

 # sampling
 trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.95,
 return_inferencedata=True)

 return trace

# === Forest Plot（parameterscomparison）===
# az.plot_forest(trace, var_names=["alpha", "beta"], combined=True)
```

### 3. Posterior predictive check (PPC)

```python
def posterior_predictive_check(model, trace, observed_y):
 """prediction: 's degreeverification"""
 with model:
 ppc = pm.sample_posterior_predictive(trace, random_seed=42)

 fig, axes = plt.subplots(1, 3, figsize=(16, 5))

 # 1. degree
 az.plot_ppc(az.from_pymc(posterior_predictive=ppc, model=model),
 ax=axes[0], kind="kde")
 axes[0].set_title("Posterior Predictive: KDE")

 # 2. amountcomparison (mean)
 ppc_mean = ppc.posterior_predictive["y_obs"].mean(dim=("chain", "draw")).values
 axes[1].hist(ppc_mean, bins=30, alpha=0.7, label="PPC mean")
 axes[1].axvline(observed_y.mean, color="red", linestyle="--", label="Observed mean")
 axes[1].set_title("PPC: Mean Comparison")
 axes[1].legend

 # 3. residual
 ppc_median = np.median(ppc.posterior_predictive["y_obs"].values, axis=(0, 1))
 residuals = observed_y - ppc_median
 axes[2].scatter(ppc_median, residuals, alpha=0.5, s=10)
 axes[2].axhline(0, color="red", linestyle="--")
 axes[2].set_title("PPC Residuals")

 plt.tight_layout
 plt.savefig("figures/bayesian_ppc.png", dpi=300, bbox_inches="tight")
 plt.show
```

### 4. comparison (WAIC / LOO-CV)

```python
def bayesian_model_comparison(models_dict):
 """
 WAIC / LOO-CV Bayesiancomparison。
 models_dict: {"model_name": (model, trace)} 's
 """
 comparison_data = {}

 for name, (model, trace) in models_dict.items:
 # WAIC
 waic = az.waic(trace)
 # LOO-CV (PSIS-LOO)
 loo = az.loo(trace)

 comparison_data[name] = {
 "waic": round(waic.waic, 2),
 "waic_se": round(waic.waic_se, 2),
 "p_waic": round(waic.p_waic, 2),
 "loo": round(loo.loo, 2),
 "loo_se": round(loo.loo_se, 2),
 "p_loo": round(loo.p_loo, 2),
 }

 # ArviZ comparison
 comp_df = az.compare(
 {name: trace for name, (_, trace) in models_dict.items},
 ic="loo",
 )
 print("Model Comparison (LOO-CV):")
 print(comp_df)

 # comparisonplot
 az.plot_compare(comp_df)
 plt.savefig("figures/bayesian_model_comparison.png", dpi=300, bbox_inches="tight")
 plt.show

 return comparison_data
```

### 5. Bayesianoptimization (Gaussian Process)

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from scipy.optimize import minimize
from scipy.stats import norm, qmc

def bayesian_optimization(objective_func, bounds, n_init=5, n_iter=25):
 """
 Gaussian Process (ARD-RBF kernel) 'sBayesianoptimization。
 Expected Improvement (EI) number/countasfor。
 """
 dim = len(bounds)

 # initialsampling (Latin Hypercube Sampling)
 sampler = qmc.LatinHypercube(d=dim, seed=42)
 X_unit = sampler.random(n=n_init)
 l_bounds = np.array([b[0] for b in bounds])
 u_bounds = np.array([b[1] for b in bounds])
 X_samples = qmc.scale(X_unit, l_bounds, u_bounds)
 y_samples = np.array([objective_func(x) for x in X_samples])

 # GP (ARD-RBF kernel)
 kernel = RBF(length_scale=np.ones(dim)) + WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-5, 1e1))
 gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, normalize_y=True)

 history = {"X": list(X_samples), "y": list(y_samples)}

 for i in range(n_iter):
 gp.fit(np.array(history["X"]), np.array(history["y"]))

 # Expected Improvement
 def neg_ei(x):
 mu, sigma = gp.predict(x.reshape(1, -1), return_std=True)
 best_y = np.min(history["y"])
 z = (best_y - mu) / (sigma + 1e-8)
 ei = (best_y - mu) * norm.cdf(z) + sigma * norm.pdf(z)
 return -ei[0]

 # 'ssearch/explorationpoint
 best_x = None
 best_ei = np.inf
 for _ in range(20):
 x0 = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
 result = minimize(neg_ei, x0, bounds=bounds, method="L-BFGS-B")
 if result.fun < best_ei:
 best_ei = result.fun
 best_x = result.x

 new_y = objective_func(best_x)
 history["X"].append(best_x)
 history["y"].append(new_y)

 print(f"Iter {i+1}: x = {best_x}, y = {new_y:.4f}, best = {min(history['y']):.4f}")

 return history
```

### 6. Stan by/via

```python
# === CmdStanPy interface ===
import cmdstanpy

def fit_stan_model(stan_code, data_dict, **kwargs):
 """Stan 's and"""
 model = cmdstanpy.CmdStanModel(stan_file=None, stan_file_path=None,
 model_code=stan_code)
 fit = model.sample(data=data_dict, chains=4, iter_sampling=2000,
 iter_warmup=1000, **kwargs)

 # ArviZ transformation
 idata = az.from_cmdstanpy(fit)
 return idata

# Stan example: 
STAN_HIERARCHICAL = """
data {
 int<lower=0> N;
 int<lower=0> J;
 array[N] int<lower=1,upper=J> group;
 vector[N] x;
 vector[N] y;
}
parameters {
 real mu_alpha;
 real mu_beta;
 real<lower=0> sigma_alpha;
 real<lower=0> sigma_beta;
 real<lower=0> sigma;
 vector[J] alpha;
 vector[J] beta;
}
model {
 mu_alpha ~ normal(0, 10);
 mu_beta ~ normal(0, 10);
 sigma_alpha ~ half_normal(5);
 sigma_beta ~ half_normal(5);
 sigma ~ half_normal(5);
 alpha ~ normal(mu_alpha, sigma_alpha);
 beta ~ normal(mu_beta, sigma_beta);
 y ~ normal(alpha[group] + beta[group].* x, sigma);
}
"""
```

---

## Best Practices

1. **informationprior distribution**: data。degree informationprior distribution
2. **convergencediagnosisrequired**: Rhat < 1.01, ESS > 400/chain, 
3. **prediction**: 's degree PPC verification
4. **LOO-CV **: comparison WAIC than LOO-CV (PSIS-LOO) 
5. ****: non-centered parameterization 
6. **reproducibility**: random_seed 
7. **sensitivity analysis**: prior distributionresults'sverification

## Completeness Checklist

- [ ] Model specification (likelihood and priors)
- [ ] Prior predictive check
- [ ] MCMC sampling complete
- [ ] Convergence diagnostics (Rhat, ESS, divergences)
- [ ] Posterior summary (mean, HDI)
- [ ] Posterior predictive check (PPC)
- [ ] Model comparison (LOO-CV / WAIC)
- [ ] Result report and plot generation

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | Bayesian statistics tool registry search |

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/bayesian_summary.json` | posterior distributionsummary（JSON） | samplingcompletion |
| `figures/bayesian_trace.png` | plot | MCMC completion |
| `figures/bayesian_ppc.png` | predictionfigure | PPC completion |
| `figures/bayesian_model_comparison.png` | comparisonplot | comparisoncompletion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-statistical-testing` | ← frequencytesting and 's comparison |
| `scientific-ml-regression` | ← regression's Bayesian |
| `scientific-doe` | ← Experimental Design'sBayesianoptimization |
| `scientific-causal-inference` | ← Bayesian |
| `scientific-quantum-computing` | → VQE parameters's Bayesianoptimization |
| `scientific-meta-analysis` | ← Bayesianmin |

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
