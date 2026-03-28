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
