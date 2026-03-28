---
name: scientific-reinforcement-learning
description: |
 reinforcement learningskill。Stable-Baselines3 by/via RL training、
 Gymnasium environmentconstruction、PufferLib large-scale、
 application (moleculegenerationexperimentoptimization) pipeline。
tu_tools:
 - key: papers_with_code
 name: Papers with Code
 description: reinforcement learningenvironmentsearch
---

# Scientific Reinforcement Learning

Stable-Baselines3 / PufferLib / Gymnasium utilizing
reinforcement learningpipeline is provided。

## When to Use

- RL trainingevaluationwhen needed
- custom Gymnasium environment is builtand
- moleculedesign RL is appliedand
- experimentparameters's optimization RL and
- reinforcement learning is executedand
- 'swhen needed

---

## Quick Start

## 1. Stable-Baselines3 basictraining

```python
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO, SAC, A2C, DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback


def train_rl_agent(env_id, algorithm="PPO", total_timesteps=100_000,
 n_envs=4, hyperparams=None):
 """
 Stable-Baselines3 RL training。

 Parameters:
 env_id: str — Gymnasium environment ID (e.g., "CartPole-v1", "LunarLander-v3")
 algorithm: str — "PPO", "SAC", "A2C", "DQN"
 total_timesteps: int — trainingsteps
 n_envs: int — environmentnumber/count
 hyperparams: dict — hyperparameters override

 K-Dense: stable-baselines3 — RL training framework
 """
 algo_map = {"PPO": PPO, "SAC": SAC, "A2C": A2C, "DQN": DQN}
 AlgoClass = algo_map.get(algorithm, PPO)

 # Vectorized environments
 env = DummyVecEnv([lambda: gym.make(env_id) for _ in range(n_envs)])

 # Default hyperparams per algorithm
 default_params = {
 "PPO": {"learning_rate": 3e-4, "n_steps": 2048, "batch_size": 64},
 "SAC": {"learning_rate": 3e-4, "buffer_size": 1_000_000},
 "A2C": {"learning_rate": 7e-4, "n_steps": 5},
 "DQN": {"learning_rate": 1e-4, "buffer_size": 100_000},
 }
 params = default_params.get(algorithm, {})
 if hyperparams:
 params.update(hyperparams)

 model = AlgoClass("MlpPolicy", env, verbose=1, **params)

 # Callbacks
 eval_env = gym.make(env_id)
 eval_callback = EvalCallback(
 eval_env, best_model_save_path="./models/best/",
 log_path="./logs/", eval_freq=10_000,
 )
 checkpoint_callback = CheckpointCallback(
 save_freq=25_000, save_path="./models/checkpoints/",
 )

 model.learn(
 total_timesteps=total_timesteps,
 callback=[eval_callback, checkpoint_callback],
 )

 # Evaluation
 mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=20)
 print(f"RL Training ({algorithm} on {env_id}): "
 f"reward = {mean_reward:.2f} ± {std_reward:.2f}")

 return model, {"mean_reward": mean_reward, "std_reward": std_reward}
```

## 2. custom Gymnasium environment

```python
class MoleculeDesignEnv(gym.Env):
 """
 moleculedesignforcustom RL environment。

 status: molecule (Morgan FP)
 : /binding's additiondeletionchange
 : drug (QED) + bindingprediction
 """
 metadata = {"render_modes": ["human"]}

 def __init__(self, max_atoms=50, target_property="qed"):
 super.__init__
 self.max_atoms = max_atoms
 self.target_property = target_property

 # Action space: discrete (add atom types, add bonds, remove)
 self.action_space = gym.spaces.Discrete(10)

 # Observation space: molecular fingerprint
 self.observation_space = gym.spaces.Box(
 low=0, high=1, shape=(2048,), dtype=np.float32,
 )

 self.current_mol = None
 self.step_count = 0

 def reset(self, seed=None, options=None):
 super.reset(seed=seed)
 self.current_mol = None # Start from scratch
 self.step_count = 0
 obs = np.zeros(2048, dtype=np.float32)
 return obs, {}

 def step(self, action):
 self.step_count += 1

 # Apply action to modify molecule
 reward = self._calculate_reward
 terminated = self.step_count >= self.max_atoms
 truncated = False
 obs = self._get_observation

 return obs, reward, terminated, truncated, {}

 def _calculate_reward(self):
 """Calculate reward based on molecular properties."""
 if self.current_mol is None:
 return 0.0
 # Placeholder: QED score
 return np.random.uniform(0, 1)

 def _get_observation(self):
 return np.zeros(2048, dtype=np.float32)


def train_molecule_designer(total_timesteps=50_000):
 """moleculedesign RL training。"""
 env = MoleculeDesignEnv
 model = PPO("MlpPolicy", env, verbose=1, learning_rate=1e-4)
 model.learn(total_timesteps=total_timesteps)

 mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
 print(f"Molecule Designer: reward = {mean_reward:.2f} ± {std_reward:.2f}")
 return model
```

## 3. PufferLib large-scale

```python
def setup_pufferlib_training(env_name, num_agents=8, algorithm="PPO"):
 """
 PufferLib RL settings。

 Parameters:
 env_name: str — PufferLib supportenvironment
 num_agents: int — number/count
 algorithm: str — "PPO", "IMPALA"

 K-Dense: pufferlib — Scalable multi-agent RL
 """
 try:
 import pufferlib
 import pufferlib.environments

 config = {
 "env": env_name,
 "num_agents": num_agents,
 "algorithm": algorithm,
 "total_timesteps": 1_000_000,
 "batch_size": 256,
 "learning_rate": 2.5e-4,
 "num_envs": 16,
 "num_steps": 128,
 }
 print(f"PufferLib config: {config}")
 return config

 except ImportError:
 print("PufferLib not installed. Install with: pip install pufferlib")
 return None
```

## 4. experimentparametersoptimization

```python
def rl_experiment_optimizer(parameter_ranges, objective_fn,
 total_episodes=100, algorithm="PPO"):
 """
 RL by/viaexperimentparametersoptimization。

 Parameters:
 parameter_ranges: dict — {param_name: (min, max)}
 objective_fn: callable — objective function (params → score)
 total_episodes: int — optimizationnumber/count
 """
 n_params = len(parameter_ranges)
 param_names = list(parameter_ranges.keys)

 class ExperimentEnv(gym.Env):
 def __init__(self):
 super.__init__
 self.action_space = gym.spaces.Box(
 low=-1, high=1, shape=(n_params,), dtype=np.float32,
 )
 self.observation_space = gym.spaces.Box(
 low=-np.inf, high=np.inf,
 shape=(n_params + 1,), dtype=np.float32,
 )
 self.best_score = -np.inf
 self.history = []

 def reset(self, seed=None, options=None):
 super.reset(seed=seed)
 self.current_params = np.zeros(n_params, dtype=np.float32)
 return np.zeros(n_params + 1, dtype=np.float32), {}

 def step(self, action):
 # Scale action to parameter ranges
 params = {}
 for i, name in enumerate(param_names):
 lo, hi = parameter_ranges[name]
 params[name] = lo + (action[i] + 1) / 2 * (hi - lo)

 score = objective_fn(params)
 self.history.append({"params": params, "score": score})

 if score > self.best_score:
 self.best_score = score

 obs = np.append(action, [score]).astype(np.float32)
 return obs, score, False, False, {}

 env = ExperimentEnv
 model = SAC("MlpPolicy", env, verbose=0) if algorithm == "SAC" else PPO("MlpPolicy", env, verbose=0)
 model.learn(total_timesteps=total_episodes)

 best_idx = max(range(len(env.history)), key=lambda i: env.history[i]["score"])
 best = env.history[best_idx]
 print(f"RL Optimization: best score = {best['score']:.4f}")
 print(f" Best params: {best['params']}")
 return best, env.history
```

---

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `models/rl_model.zip` | training RL | → deep-learning (integration) |
| `results/rl_training_log.json` | trainingcurvelinemetrics | → publication-figures |
| `results/rl_optimization.json` | optimizationparameters | → doe, process-optimization |
| `figures/rl_reward_curve.png` | curveline | → presentation-design |

## Pipeline Integration

```
doe ──→ reinforcement-learning ──→ lab-automation
 (Experimental Design) (optimization) 
 │
 ├──→ drug-target-profiling (moleculedesign RL)
 ├──→ protein-design (structureoptimization RL)
 └──→ deep-learning (DRL pipeline)
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `papers_with_code` | Papers with Code | reinforcement learningenvironmentsearch |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (ML/AI)

Before execution, define:
- [ ] **Task type**: classification / regression / generation / ranking
- [ ] **Baseline**: naive baseline metric to beat
- [ ] **Target metric**: specific threshold (e.g., AUC > 0.85, RMSE < 0.1)
- [ ] **Data split**: train/val/test ratios, stratification method

#### Pass Criteria
- Model performance exceeds baseline by defined margin
- Train/val/test metrics all reported (no data leakage)
- Hyperparameters logged with search method
- Overfitting check: train-val gap < 10% relative
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
