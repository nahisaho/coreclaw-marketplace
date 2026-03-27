---
name: scientific-graph-neural-networks
description: |
  Graph neural networks skill. GNN architectures (GCN/GAT/GraphSAGE), molecular graph learning, knowledge graph embeddings, and graph-level prediction tasks.
---

# Scientific Graph Neural Networks

グラフニューラルネットワーク (GNN) のための解析スキル。
分子グラフ、タンパク質構造、知識グラフなどの構造化データに対する
深層学習を支援する。

## When to Use

- 分子特性予測（溶解度・毒性・ADMET・活性）
- タンパク質機能予測・相互作用予測
- 知識グラフ埋め込み・リンク予測
- ノード分類・グラフ分類・グラフ回帰
- 分子生成・レトロシンセシス計画
- ソーシャル/バイオネットワーク解析

## Quick Start

### GNN パイプライン

```
Phase 1: Graph Construction
  - 分子 SMILES → 分子グラフ変換
  - タンパク質 PDB → 接触マップグラフ
  - ノード/エッジ特徴量設計
    ↓
Phase 2: Model Selection
  - GCN / GAT / GIN / GraphSAGE / SchNet
  - Message Passing 方式選択
  - プーリング戦略 (mean, sum, attention)
    ↓
Phase 3: Training
  - データ分割 (scaffold split 推奨)
  - ミニバッチローダー設定
  - 学習率スケジューラ
    ↓
Phase 4: Evaluation
  - ROC-AUC / RMSE / MAE
  - 5-fold CV or scaffold split
  - MoleculeNet ベンチマーク比較
    ↓
Phase 5: Interpretation
  - GNNExplainer / Attention 可視化
  - 分子部分構造の寄与分析
  - SHAP for graphs
    ↓
Phase 6: Deployment
  - モデルエクスポート (ONNX)
  - バッチ推論パイプライン
  - 予測レポート生成
```

## Workflow

### 1. PyTorch Geometric: 分子特性予測

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, GINConv, global_mean_pool
from torch_geometric.data import Data, DataLoader
from torch_geometric.datasets import MoleculeNet
from rdkit import Chem
import numpy as np

# === 分子 → グラフ変換 ===
def smiles_to_graph(smiles):
    """SMILES → PyG Data オブジェクト"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # ノード特徴量 (原子特徴)
    atom_features = []
    for atom in mol.GetAtoms():
        features = [
            atom.GetAtomicNum(),
            atom.GetDegree(),
            atom.GetFormalCharge(),
            int(atom.GetHybridization()),
            int(atom.GetIsAromatic()),
            atom.GetTotalNumHs(),
            atom.GetNumRadicalElectrons(),
        ]
        atom_features.append(features)

    x = torch.tensor(atom_features, dtype=torch.float)

    # エッジ (結合)
    edge_index = []
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        edge_index.extend([[i, j], [j, i]])  # 双方向

    # エッジ特徴量 (結合特徴)
    edge_attr = []
    for bond in mol.GetBonds():
        bond_features = [
            bond.GetBondTypeAsDouble(),
            bond.GetIsConjugated(),
            bond.GetIsAromatic(),
            bond.IsInRing(),
        ]
        edge_attr.extend([bond_features, bond_features])  # both directions

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)

    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)


# === GCN モデル ===
class MolGCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, n_layers=3):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.convs.append(GCNConv(in_channels, hidden_channels))
        for _ in range(n_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
        self.convs.append(GCNConv(hidden_channels, hidden_channels))
        self.lin = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index, batch):
        for conv in self.convs:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=0.2, training=self.training)

        # グラフレベル表現 (Readout)
        x = global_mean_pool(x, batch)
        x = self.lin(x)
        return x


# === GAT (Graph Attention Network) ===
class MolGAT(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, heads=4):
        super().__init__()
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=0.3)
        self.conv2 = GATConv(hidden_channels * heads, hidden_channels, heads=1, dropout=0.3)
        self.lin = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index, batch):
        x = F.elu(self.conv1(x, edge_index))
        x = F.elu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        x = self.lin(x)
        return x
```

### 2. GIN (Graph Isomorphism Network)

```python
from torch_geometric.nn import GINConv, global_add_pool

class MolGIN(torch.nn.Module):
    """GIN: 最大表現力を持つ GNN (WL test 等価)"""
    def __init__(self, in_channels, hidden_channels, out_channels, n_layers=5):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.batch_norms = torch.nn.ModuleList()

        for i in range(n_layers):
            in_ch = in_channels if i == 0 else hidden_channels
            mlp = torch.nn.Sequential(
                torch.nn.Linear(in_ch, hidden_channels),
                torch.nn.BatchNorm1d(hidden_channels),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_channels, hidden_channels),
            )
            self.convs.append(GINConv(mlp, train_eps=True))
            self.batch_norms.append(torch.nn.BatchNorm1d(hidden_channels))

        self.lin1 = torch.nn.Linear(hidden_channels, hidden_channels)
        self.lin2 = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index, batch):
        for conv, bn in zip(self.convs, self.batch_norms):
            x = conv(x, edge_index)
            x = bn(x)
            x = F.relu(x)

        x = global_add_pool(x, batch)
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin2(x)
        return x
```

### 3. TorchDrug: 分子特性予測

```python
import torchdrug
from torchdrug import datasets, models, tasks, core

# === TorchDrug: MoleculeNet ベンチマーク ===
# BBBP (Blood-Brain Barrier Penetration) 分類
dataset = datasets.BBBP("data/bbbp/", atom_feature="default", bond_feature="default")

# Scaffold split (推奨: 化学的多様性を考慮)
train_set, valid_set, test_set = dataset.split(ratios=[0.8, 0.1, 0.1])

# GIN モデル
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256, 256],
    batch_norm=True,
    short_cut=True,
    readout="mean",
)

# タスク定義
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=("auprc", "auroc"),
)

# トレーニング
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
solver = core.Engine(
    task,
    train_set, valid_set, test_set,
    optimizer,
    batch_size=128,
    gpus=[0],
)
solver.train(num_epoch=100)
solver.evaluate("valid")
```

### 4. 知識グラフ推論

```python
from torchdrug import datasets as td_datasets, models as td_models, tasks as td_tasks

# === 知識グラフ埋め込み ===
# 例: Hetionet (疾患-遺伝子-薬物 KG)
# dataset = td_datasets.Hetionet("data/hetionet/")

# TransE / RotatE / ComplEx モデル
class KGEModel:
    """Knowledge Graph Embedding wrapper"""

    MODELS = {
        "transe": {"embedding_dim": 256, "margin": 6.0},
        "rotate": {"embedding_dim": 256},
        "complex": {"embedding_dim": 256},
    }

    def __init__(self, model_name, num_entities, num_relations):
        self.model_name = model_name
        self.num_entities = num_entities
        self.num_relations = num_relations
        config = self.MODELS[model_name]
        dim = config["embedding_dim"]
        self.margin = config.get("margin", 6.0)
        self.entity_emb = torch.nn.Embedding(num_entities, dim)
        self.relation_emb = torch.nn.Embedding(num_relations, dim)
        torch.nn.init.xavier_uniform_(self.entity_emb.weight)
        torch.nn.init.xavier_uniform_(self.relation_emb.weight)

    def _score(self, h, r, t):
        """TransE scoring: -||h + r - t||"""
        return -torch.norm(h + r - t, p=2, dim=-1)

    def train_and_evaluate(self, train_triples, valid_triples, test_triples,
                           n_epochs=100, lr=0.01, neg_ratio=10):
        """KGE トレーニングと評価 (negative sampling)"""
        optimizer = torch.optim.Adam(
            list(self.entity_emb.parameters()) +
            list(self.relation_emb.parameters()), lr=lr,
        )
        train_t = torch.tensor(train_triples, dtype=torch.long)

        for epoch in range(n_epochs):
            optimizer.zero_grad()
            h = self.entity_emb(train_t[:, 0])
            r = self.relation_emb(train_t[:, 1])
            t = self.entity_emb(train_t[:, 2])
            pos_score = self._score(h, r, t)

            # Negative sampling: corrupt tail entities
            neg_tails = torch.randint(0, self.num_entities,
                                      (len(train_t) * neg_ratio,))
            h_neg = h.repeat(neg_ratio, 1)
            r_neg = r.repeat(neg_ratio, 1)
            t_neg = self.entity_emb(neg_tails)
            neg_score = self._score(h_neg, r_neg, t_neg)

            loss = F.relu(
                self.margin - pos_score.repeat(neg_ratio) + neg_score
            ).mean()
            loss.backward()
            optimizer.step()

        return self._evaluate(test_triples)

    def _evaluate(self, test_triples):
        """Compute MRR and Hits@K metrics"""
        test_t = torch.tensor(test_triples, dtype=torch.long)
        ranks = []
        with torch.no_grad():
            all_entities = self.entity_emb.weight
            for triple in test_t:
                h = self.entity_emb(triple[0].unsqueeze(0))
                r = self.relation_emb(triple[1].unsqueeze(0))
                scores = self._score(
                    h.expand(self.num_entities, -1),
                    r.expand(self.num_entities, -1),
                    all_entities,
                )
                rank = (scores >= scores[triple[2]]).sum().item()
                ranks.append(rank)

        ranks = np.array(ranks, dtype=float)
        return {
            "mrr": round(float(np.mean(1.0 / ranks)), 4),
            "hits@1": round(float(np.mean(ranks <= 1)), 4),
            "hits@3": round(float(np.mean(ranks <= 3)), 4),
            "hits@10": round(float(np.mean(ranks <= 10)), 4),
        }

    def predict_links(self, head, relation, top_k=10):
        """リンク予測: (h, r, ?) → top-k tail entities"""
        with torch.no_grad():
            h = self.entity_emb(torch.tensor([head]))
            r = self.relation_emb(torch.tensor([relation]))
            all_entities = self.entity_emb.weight
            scores = self._score(
                h.expand(self.num_entities, -1),
                r.expand(self.num_entities, -1),
                all_entities,
            )
            top_scores, top_indices = torch.topk(scores, top_k)
        return list(zip(top_indices.tolist(), top_scores.tolist()))

    def drug_repurposing_candidates(self, disease_entity, treats_relation):
        """薬物リポジショニング候補のスコアリング"""
        return self.predict_links(disease_entity, treats_relation, top_k=10)
```

### 5. トレーニング・評価ループ

```python
from sklearn.metrics import roc_auc_score, mean_squared_error
from torch_geometric.loader import DataLoader

def train_gnn(model, train_loader, optimizer, criterion, device="cpu"):
    """GNN トレーニング 1 エポック"""
    model.train()
    total_loss = 0
    for batch in train_loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index, batch.batch)
        loss = criterion(out.squeeze(), batch.y.float())
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * batch.num_graphs
    return total_loss / len(train_loader.dataset)


@torch.no_grad()
def evaluate_gnn(model, loader, device="cpu"):
    """GNN 評価"""
    model.eval()
    y_true, y_pred = [], []
    for batch in loader:
        batch = batch.to(device)
        out = model(batch.x, batch.edge_index, batch.batch)
        y_true.extend(batch.y.cpu().numpy())
        y_pred.extend(out.squeeze().cpu().numpy())

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    if len(np.unique(y_true)) == 2:  # 分類
        auc = roc_auc_score(y_true, y_pred)
        return {"auroc": round(auc, 4)}
    else:  # 回帰
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return {"rmse": round(rmse, 4)}


def scaffold_split(dataset, train_ratio=0.8, val_ratio=0.1):
    """
    Scaffold Split: 化学構造の Murcko scaffold ベースでデータ分割。
    train/val/test が異なる scaffold を持つことを保証。
    """
    from rdkit.Chem.Scaffolds.MurckoScaffold import MurckoScaffoldSmiles
    scaffolds = {}
    for idx, data in enumerate(dataset):
        smiles = data.smiles if hasattr(data, "smiles") else ""
        scaffold = MurckoScaffoldSmiles(smiles=smiles) if smiles else str(idx)
        scaffolds.setdefault(scaffold, []).append(idx)

    scaffold_sets = sorted(scaffolds.values(), key=len, reverse=True)

    train_idx, val_idx, test_idx = [], [], []
    n = len(dataset)
    for s in scaffold_sets:
        if len(train_idx) / n < train_ratio:
            train_idx.extend(s)
        elif len(val_idx) / n < val_ratio:
            val_idx.extend(s)
        else:
            test_idx.extend(s)

    return train_idx, val_idx, test_idx
```

---

## Best Practices

1. **Scaffold Split 必須**: 分子タスクでは random split ではなく scaffold split を使用
2. **Message Passing 層数**: 3-5 層が最適。深すぎると over-smoothing
3. **Readout 関数**: 分類→mean pool、検出→sum pool、注意→attention pool
4. **ノード特徴量**: 原子番号・次数・芳香族性・形式電荷・混成軌道を含める
5. **3D 情報活用**: SchNet/DimeNet で 3D 座標を持つ分子は距離情報を活用
6. **MoleculeNet ベンチマーク**: 新手法は BBBP/BACE/HIV/Tox21 での比較を報告
7. **GNNExplainer**: 予測根拠の可視化により化学的解釈性を担保

## Completeness Checklist

- [ ] 分子/グラフデータの前処理完了
- [ ] ノード・エッジ特徴量の設計
- [ ] GNN アーキテクチャ選定 (GCN/GAT/GIN)
- [ ] Scaffold split でデータ分割
- [ ] トレーニング収束確認
- [ ] ROC-AUC / RMSE でベンチマーク比較
- [ ] GNNExplainer で解釈性分析
- [ ] 予測レポート生成

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/gnn_predictions.json` | GNN 予測結果（JSON） | 推論完了時 |
| `results/gnn_benchmark.json` | ベンチマーク比較（JSON） | 評価完了時 |
| `figures/gnn_training_curve.png` | 学習曲線プロット | トレーニング完了時 |
| `figures/gnn_explanation.png` | GNNExplainer 可視化 | 解釈性分析時 |

### Available Tools

> [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP 経由で利用可能な外部ツール。

| カテゴリ | 主要ツール | 用途 |
|---|---|---|
| PubChem | `PubChem_get_compound_properties_by_CID` | 分子物性取得 |
| ChEMBL | `ChEMBL_get_molecule` | 分子情報取得 |
| ChEMBL | `ChEMBL_get_activity` | バイオアッセイデータ |
| UniProt | `UniProt_get_entry_by_accession` | タンパク質グラフ構築用 |
| BindingDB | `BindingDB_get_ligands_by_uniprot` | リガンド-ターゲットデータ |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-cheminformatics` | ← SMILES 前処理・分子記述子 |
| `scientific-drug-target-profiling` | → 標的予測・活性予測の GNN 応用 |
| `scientific-admet-pharmacokinetics` | → ADMET 予測モデル |
| `scientific-network-analysis` | ← グラフ構造解析 |
| `scientific-deep-learning` | ← NN アーキテクチャ設計・トレーニング手法 |
| `scientific-explainable-ai` | → GNN 予測の説明可能性 |
| `scientific-protein-structure-analysis` | ← タンパク質グラフの構築 |

---

## Verification Loop (v0.3.0)

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
