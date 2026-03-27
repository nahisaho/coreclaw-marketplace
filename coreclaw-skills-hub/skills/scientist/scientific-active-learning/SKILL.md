---
name: scientific-active-learning
description: |
  Active learning skill. Uncertainty sampling, Query-by-Committee, expected model change, pool-based/stream-based, batch active learning, GP-based active learning with ARD-RBF kernel, dimension-adaptive convergence, stopping criteria, and model improvement pipeline.
tu_tools:
  - key: openml
    name: OpenML
    description: 能動学習データセット・評価指標
---

# Scientific Active Learning

ラベル付けコストを最小化しながらモデル精度を最大化する
アクティブラーニング戦略の設計・実行・評価パイプラインを提供する。

## When to Use

- 少量のラベル付きデータで効率的にモデルを改善するとき
- ラベル付けコストが高い実験データを扱うとき
- 不確実性サンプリングでモデルの弱点を特定するとき
- Query-by-Committee で意見が分かれるサンプルを選択するとき
- バッチアクティブラーニングで複数サンプルを同時取得するとき
- 停止基準 (パフォーマンス収束) を判定するとき

---

## Quick Start

## 1. 不確実性サンプリング

```python
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def uncertainty_sampling(model, X_pool, strategy="entropy"):
    """
    不確実性ベース サンプリング。

    Parameters:
        model: fitted sklearn classifier
        X_pool: np.ndarray — ラベルなしプール
        strategy: str — "entropy" / "margin" / "least_confident"
    Returns:
        indices: np.ndarray — 不確実性降順のインデックス
    """
    proba = model.predict_proba(X_pool)

    if strategy == "entropy":
        scores = -np.sum(proba * np.log(proba + 1e-10), axis=1)
    elif strategy == "margin":
        sorted_p = np.sort(proba, axis=1)
        scores = 1.0 - (sorted_p[:, -1] - sorted_p[:, -2])
    elif strategy == "least_confident":
        scores = 1.0 - np.max(proba, axis=1)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    indices = np.argsort(scores)[::-1]
    print(f"Uncertainty ({strategy}): top score = {scores[indices[0]]:.4f}")
    return indices


def query_by_committee(models, X_pool, n_members=5):
    """
    Query-by-Committee サンプリング。

    Parameters:
        models: list — 学習済み分類器リスト
        X_pool: np.ndarray — ラベルなしプール
        n_members: int — 委員会メンバ数
    """
    predictions = np.array([m.predict(X_pool) for m in models[:n_members]])
    # Vote entropy
    n_samples = X_pool.shape[0]
    n_classes = len(np.unique(predictions))
    scores = np.zeros(n_samples)

    for i in range(n_samples):
        votes = predictions[:, i]
        _, counts = np.unique(votes, return_counts=True)
        proba = counts / len(votes)
        scores[i] = -np.sum(proba * np.log(proba + 1e-10))

    indices = np.argsort(scores)[::-1]
    print(f"QBC: top disagreement = {scores[indices[0]]:.4f}")
    return indices
```

## 2. バッチアクティブラーニング

```python
def batch_active_learning(model, X_pool, batch_size=10,
                          strategy="entropy", diversity_weight=0.5):
    """
    多様性を考慮したバッチアクティブラーニング。

    Parameters:
        model: fitted classifier
        X_pool: np.ndarray — ラベルなしプール
        batch_size: int — バッチサイズ
        strategy: str — 不確実性戦略
        diversity_weight: float — 多様性重み (0-1)
    """
    from sklearn.metrics.pairwise import euclidean_distances

    # 不確実性スコア
    indices = uncertainty_sampling(model, X_pool, strategy)

    # 候補プール (上位 batch_size * 3)
    candidate_size = min(batch_size * 3, len(indices))
    candidates = indices[:candidate_size]

    # 多様性ベース選択 (k-center greedy)
    selected = [candidates[0]]
    for _ in range(batch_size - 1):
        remaining = [c for c in candidates if c not in selected]
        if not remaining:
            break

        dists = euclidean_distances(
            X_pool[remaining], X_pool[selected])
        min_dists = dists.min(axis=1)

        # 不確実性ランクを正規化
        uncertainty_ranks = np.array([
            np.where(indices == r)[0][0] for r in remaining])
        uncertainty_scores = 1.0 - uncertainty_ranks / len(indices)

        # 複合スコア
        combined = (diversity_weight * min_dists / (min_dists.max() + 1e-10)
                    + (1 - diversity_weight) * uncertainty_scores)

        best_idx = remaining[np.argmax(combined)]
        selected.append(best_idx)

    print(f"Batch AL: selected {len(selected)} diverse-uncertain samples")
    return np.array(selected)
```

## 3. アクティブラーニングループ

```python
def active_learning_loop(X_labeled, y_labeled, X_pool, y_pool_true,
                         X_test, y_test,
                         model=None, n_rounds=20, batch_size=10,
                         strategy="entropy"):
    """
    アクティブラーニング実験ループ。

    Parameters:
        X_labeled: np.ndarray — 初期ラベル付きデータ
        y_labeled: np.ndarray — 初期ラベル
        X_pool: np.ndarray — ラベルなしプール
        y_pool_true: np.ndarray — プールの真ラベル (Oracle)
        X_test: np.ndarray — テストデータ
        y_test: np.ndarray — テストラベル
        model: sklearn classifier (default: RF)
        n_rounds: int — ラウンド数
        batch_size: int — バッチサイズ
        strategy: str — サンプリング戦略
    """
    if model is None:
        model = RandomForestClassifier(n_estimators=100, random_state=42)

    X_l = X_labeled.copy()
    y_l = y_labeled.copy()
    X_p = X_pool.copy()
    y_p = y_pool_true.copy()

    history = []
    for rnd in range(n_rounds):
        m = clone(model).fit(X_l, y_l)
        acc = accuracy_score(y_test, m.predict(X_test))
        history.append({
            "round": rnd,
            "n_labeled": len(y_l),
            "accuracy": round(acc, 4),
            "pool_size": len(y_p),
        })

        if len(X_p) == 0:
            break

        # バッチ選択
        selected = batch_active_learning(
            m, X_p, batch_size, strategy)

        # Oracle に問い合わせ
        X_l = np.vstack([X_l, X_p[selected]])
        y_l = np.concatenate([y_l, y_p[selected]])

        mask = np.ones(len(X_p), dtype=bool)
        mask[selected] = False
        X_p = X_p[mask]
        y_p = y_p[mask]

    df = pd.DataFrame(history)
    improvement = df["accuracy"].iloc[-1] - df["accuracy"].iloc[0]
    print(f"AL loop: {n_rounds} rounds, "
          f"acc {df['accuracy'].iloc[0]:.3f} → {df['accuracy'].iloc[-1]:.3f} "
          f"(+{improvement:.3f})")
    return df


def compare_strategies(X_labeled, y_labeled, X_pool, y_pool_true,
                       X_test, y_test, n_rounds=20, batch_size=10):
    """
    複数アクティブラーニング戦略の比較。

    Parameters: (同上)
    """
    strategies = ["entropy", "margin", "least_confident"]
    results = {}

    for strat in strategies:
        history = active_learning_loop(
            X_labeled, y_labeled, X_pool, y_pool_true,
            X_test, y_test,
            n_rounds=n_rounds, batch_size=batch_size,
            strategy=strat)
        results[strat] = history

    # ランダムベースライン
    np.random.seed(42)
    random_history = active_learning_loop(
        X_labeled, y_labeled,
        X_pool[np.random.permutation(len(X_pool))],
        y_pool_true[np.random.permutation(len(y_pool_true))],
        X_test, y_test,
        n_rounds=n_rounds, batch_size=batch_size,
        strategy="least_confident")
    results["random"] = random_history

    print(f"Strategy comparison: {len(strategies) + 1} methods evaluated")
    return results
```

## 4. GP-Based Active Learning with ARD-RBF Kernel

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel


def gp_active_learning(X_labeled, y_labeled, X_pool,
                       n_rounds=20, batch_size=5):
    """
    Gaussian Process active learning with ARD-RBF kernel.

    ARD-RBF assigns a per-dimension length_scale, enabling
    automatic relevance determination for high-dimensional spaces
    (d >= 10).  Isotropic RBF or Matern kernels fail to converge
    in such settings because they cannot distinguish informative
    from uninformative dimensions.

    Parameters:
        X_labeled: np.ndarray (n, d)
        y_labeled: np.ndarray (n,)
        X_pool: np.ndarray (m, d)
        n_rounds: int
        batch_size: int
    Returns:
        dict with gp_model, history, X_final, y_final
    """
    d = X_labeled.shape[1]
    # ARD-RBF: one length_scale per dimension
    kernel = RBF(length_scale=np.ones(d)) + WhiteKernel(noise_level=1e-3)

    X_l = X_labeled.copy()
    y_l = y_labeled.copy()
    X_p = X_pool.copy()

    history = []
    for rnd in range(n_rounds):
        gp = GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=5, random_state=42)
        gp.fit(X_l, y_l)

        mu, sigma = gp.predict(X_p, return_std=True)
        mean_var = np.mean(sigma ** 2)

        # dimension-adaptive convergence threshold
        threshold = 0.3 * d
        history.append({
            "round": rnd,
            "n_labeled": len(y_l),
            "mean_variance": round(float(mean_var), 6),
            "threshold": threshold,
            "pool_remaining": len(X_p),
        })

        if mean_var < threshold:
            print(f"GP-AL converged at round {rnd}: "
                  f"mean_var={mean_var:.4f} < threshold={threshold:.1f}")
            break

        if len(X_p) < batch_size:
            print(f"Pool exhausted at round {rnd}")
            break

        # Select highest-variance points
        top_idx = np.argsort(sigma)[::-1][:batch_size]
        X_l = np.vstack([X_l, X_p[top_idx]])
        y_l = np.concatenate([y_l, mu[top_idx]])  # surrogate label

        mask = np.ones(len(X_p), dtype=bool)
        mask[top_idx] = False
        X_p = X_p[mask]

    print(f"GP-AL: {len(history)} rounds, "
          f"final mean_var={history[-1]['mean_variance']:.4f}, "
          f"ARD length_scales={gp.kernel_.k1.length_scale}")
    return {
        "gp_model": gp,
        "history": pd.DataFrame(history),
        "X_final": X_l,
        "y_final": y_l,
    }
```

## 5. 停止基準判定

```python
def stopping_criterion(history_df, patience=5, min_improvement=0.001,
                       n_dims=None):
    """
    アクティブラーニング停止基準判定。

    Parameters:
        history_df: pd.DataFrame — AL 履歴
        patience: int — 改善なしラウンド数
        min_improvement: float — 最小改善幅
        n_dims: int or None — 入力次元数 (variance-based convergence)
    """
    # variance-based convergence (for GP-AL)
    if "mean_variance" in history_df.columns and n_dims is not None:
        threshold = 0.3 * n_dims
        last_var = history_df["mean_variance"].iloc[-1]
        if last_var < threshold:
            return True, (f"variance converged: {last_var:.4f} "
                          f"< threshold={threshold:.1f} (d={n_dims})")

    # accuracy-based convergence
    if "accuracy" in history_df.columns:
        accs = history_df["accuracy"].values
        if len(accs) < patience + 1:
            return False, "insufficient rounds"

        recent = accs[-patience:]
        best_before = accs[:-patience].max()
        improvement = recent.max() - best_before

        if improvement < min_improvement:
            return True, (f"converged: improvement {improvement:.5f} "
                          f"< threshold {min_improvement}")

        return False, f"continuing: improvement {improvement:.5f}"

    return False, "no convergence metric found"
```

---

## Pipeline Integration

```
eda-correlation → active-learning → ml-classification
  (データ探索)     (サンプル選択)     (モデル構築)
       │                │                ↓
  missing-data ─────────┘     ensemble-methods
    (欠損値処理)               (アンサンブル)
                                    ↓
                          uncertainty-quantification
                            (不確実性定量化)
```

## Pipeline Output

| ファイル | 説明 | 次スキル |
|---------|------|---------|
| `al_history.csv` | AL ラウンド履歴 | → 停止判定 |
| `gp_al_history.csv` | GP-AL (ARD-RBF) ラウンド履歴 | → 停止判定 |
| `selected_samples.csv` | 選択サンプル | → ラベル付け |
| `strategy_comparison.csv` | 戦略比較 | → advanced-visualization |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `openml` | OpenML | 能動学習データセット・評価指標 |

---

## Verification Loop (v0.2.2)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY  → check outputs against quality gates
REPORT  → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show())
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
