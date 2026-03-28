---
name: scientific-graph-neural-networks
description: |
 graphnetwork (GNN) skill。PyTorch GeometricTorchDrug
 DeepChem utilizing、moleculepredictionproteinknowledge graphinference
 node/graphclassification support。
 「GNN molecule prediction」「graphclassification」「graphinference」 。
---

# Scientific Graph Neural Networks

graphnetwork (GNN) foranalysisskill。
moleculegraph、proteinstructure、knowledge graphetc.'s structuredatafor/against
deep learning is supported。

## When to Use

- moleculeprediction（degreetoxicityADMETactivity）
- proteinpredictioninteractionprediction
- knowledge graphprediction
- nodeclassificationgraphclassificationgraphregression
- moleculegenerationdesign
- /networkanalysis

## Quick Start

### GNN pipeline

```
Phase 1: Graph Construction
 - molecule SMILES → moleculegraphtransformation
 - protein PDB → graph
 - node/edgefeaturesdesign
 ↓
Phase 2: Model Selection
 - GCN / GAT / GIN / GraphSAGE / SchNet
 - Message Passing formulaselection
 - (mean, sum, attention)
 ↓
Phase 3: Training
 - datamin (scaffold split recommended)
 - batchsettings
 - learning rate
 ↓
Phase 4: Evaluation
 - ROC-AUC / RMSE / MAE
 - 5-fold CV or scaffold split
 - MoleculeNet comparison
 ↓
Phase 5: Interpretation
 - GNNExplainer / Attention visualization
 - moleculepartialstructure's min
 - SHAP for graphs
 ↓
Phase 6: Deployment
 - export (ONNX)
 - batchinferencepipeline
 - predictionreportgeneration
```

## Workflow

### 1. PyTorch Geometric: moleculeprediction

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, GINConv, global_mean_pool
from torch_geometric.data import Data, DataLoader
from torch_geometric.datasets import MoleculeNet
from rdkit import Chem
import numpy as np

# === molecule → graphtransformation ===
def smiles_to_graph(smiles):
 """SMILES → PyG Data """
 mol = Chem.MolFromSmiles(smiles)
 if mol is None:
 return None

 # nodefeatures 
 atom_features = []
 for atom in mol.GetAtoms:
 features = [
 atom.GetAtomicNum,
 atom.GetDegree,
 atom.GetFormalCharge,
 int(atom.GetHybridization),
 int(atom.GetIsAromatic),
 atom.GetTotalNumHs,
 atom.GetNumRadicalElectrons,
 ]
 atom_features.append(features)

 x = torch.tensor(atom_features, dtype=torch.float)

 # edge (binding)
 edge_index = []
 for bond in mol.GetBonds:
 i, j = bond.GetBeginAtomIdx, bond.GetEndAtomIdx
 edge_index.extend([[i, j], [j, i]]) # direction

 edge_index = torch.tensor(edge_index, dtype=torch.long).t.contiguous

 return Data(x=x, edge_index=edge_index)


# === GCN ===
class MolGCN(torch.nn.Module):
 def __init__(self, in_channels, hidden_channels, out_channels, n_layers=3):
 super.__init__
 self.convs = torch.nn.ModuleList
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

 # graphtable (Readout)
 x = global_mean_pool(x, batch)
 x = self.lin(x)
 return x


# === GAT (Graph Attention Network) ===
class MolGAT(torch.nn.Module):
 def __init__(self, in_channels, hidden_channels, out_channels, heads=4):
 super.__init__
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
 """GIN: table items GNN (WL test )"""
 def __init__(self, in_channels, hidden_channels, out_channels, n_layers=5):
 super.__init__
 self.convs = torch.nn.ModuleList
 self.batch_norms = torch.nn.ModuleList

 for i in range(n_layers):
 in_ch = in_channels if i == 0 else hidden_channels
 mlp = torch.nn.Sequential(
 torch.nn.Linear(in_ch, hidden_channels),
 torch.nn.BatchNorm1d(hidden_channels),
 torch.nn.ReLU,
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

### 3. TorchDrug: moleculeprediction

```python
import torchdrug
from torchdrug import datasets, models, tasks, core

# === TorchDrug: MoleculeNet ===
# BBBP (Blood-Brain Barrier Penetration) classification
dataset = datasets.BBBP("data/bbbp/", atom_feature="default", bond_feature="default")

# Scaffold split (recommended: )
train_set, valid_set, test_set = dataset.split(ratios=[0.8, 0.1, 0.1])

# GIN 
model = models.GIN(
 input_dim=dataset.node_feature_dim,
 hidden_dims=[256, 256, 256, 256],
 batch_norm=True,
 short_cut=True,
 readout="mean",
)

# taskdefinition
task = tasks.PropertyPrediction(
 model,
 task=dataset.tasks,
 criterion="bce",
 metric=("auprc", "auroc"),
)

# 
optimizer = torch.optim.Adam(task.parameters, lr=1e-3)
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

### 4. knowledge graphinference

```python
from torchdrug import datasets as td_datasets, models as td_models, tasks as td_tasks

# === knowledge graph ===
# example: Hetionet (disease-gene-drug KG)
# dataset = td_datasets.Hetionet("data/hetionet/")

# TransE / RotatE / ComplEx 
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

 def train_and_evaluate(self, train_triples, valid_triples, test_triples):
 """KGE andevaluation"""
 # evaluationmetrics
 # MRR (Mean Reciprocal Rank)
 # Hits@1, Hits@3, Hits@10
 pass

 def predict_links(self, head, relation, top_k=10):
 """prediction: (h, r, ?) → top-k tail entities"""
 pass

 def drug_repurposing_candidates(self, disease_entity, treats_relation):
 """drug's"""
 pass
```

### 5. evaluationloop

```python
from sklearn.metrics import roc_auc_score, mean_squared_error
from torch_geometric.loader import DataLoader

def train_gnn(model, train_loader, optimizer, criterion, device="cpu"):
 """GNN 1 """
 model.train
 total_loss = 0
 for batch in train_loader:
 batch = batch.to(device)
 optimizer.zero_grad
 out = model(batch.x, batch.edge_index, batch.batch)
 loss = criterion(out.squeeze, batch.y.float)
 loss.backward
 optimizer.step
 total_loss += loss.item * batch.num_graphs
 return total_loss / len(train_loader.dataset)


@torch.no_grad
def evaluate_gnn(model, loader, device="cpu"):
 """GNN evaluation"""
 model.eval
 y_true, y_pred = [], []
 for batch in loader:
 batch = batch.to(device)
 out = model(batch.x, batch.edge_index, batch.batch)
 y_true.extend(batch.y.cpu.numpy)
 y_pred.extend(out.squeeze.cpu.numpy)

 y_true = np.array(y_true)
 y_pred = np.array(y_pred)

 if len(np.unique(y_true)) == 2: # classification
 auc = roc_auc_score(y_true, y_pred)
 return {"auroc": round(auc, 4)}
 else: # regression
 rmse = np.sqrt(mean_squared_error(y_true, y_pred))
 return {"rmse": round(rmse, 4)}


def scaffold_split(dataset, train_ratio=0.8, val_ratio=0.1):
 """
 Scaffold Split: structure's Murcko scaffold datamin。
 train/val/test different scaffold items and 。
 """
 from rdkit.Chem.Scaffolds.MurckoScaffold import MurckoScaffoldSmiles
 scaffolds = {}
 for idx, data in enumerate(dataset):
 smiles = data.smiles if hasattr(data, "smiles") else ""
 scaffold = MurckoScaffoldSmiles(smiles=smiles) if smiles else str(idx)
 scaffolds.setdefault(scaffold, []).append(idx)

 scaffold_sets = sorted(scaffolds.values, key=len, reverse=True)

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

1. **Scaffold Split required**: moleculetask random split scaffold split for
2. **Message Passing number/count**: 3-5 。 and over-smoothing
3. **Readout number/count**: classification→mean pool、→sum pool、caution→attention pool
4. **nodefeatures**: numbernumber/countshapeformula
5. **3D informationutilizing**: SchNet/DimeNet 3D coordinatesitemsmolecule informationutilizing
6. **MoleculeNet **: method BBBP/BACE/HIV/Tox21 's comparison
7. **GNNExplainer**: predictionbasis's visualization than

## Completeness Checklist

- [ ] molecule/graphdata's preprocessingcompletion
- [ ] nodeedgefeatures'sdesign
- [ ] GNN (GCN/GAT/GIN)
- [ ] Scaffold split datamin
- [ ] Training convergence check
- [ ] ROC-AUC / RMSE comparison
- [ ] GNNExplainer min
- [ ] predictionreportgeneration

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/gnn_predictions.json` | GNN predictionresults（JSON） | inferencecompletion |
| `results/gnn_benchmark.json` | comparison（JSON） | evaluationcompletion |
| `figures/gnn_training_curve.png` | curvelineplot | completion |
| `figures/gnn_explanation.png` | GNNExplainer visualization | min |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| PubChem | `PubChem_get_compound_properties_by_CID` | moleculepropertiesretrieval |
| ChEMBL | `ChEMBL_get_molecule` | molecule information retrieval |
| ChEMBL | `ChEMBL_get_activity` | bioassay data |
| UniProt | `UniProt_get_entry_by_accession` | proteingraphconstructionfor |
| BindingDB | `BindingDB_get_ligands_by_uniprot` | ligand-data |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-cheminformatics` | ← SMILES preprocessingmolecule |
| `scientific-drug-target-profiling` | → predictionactivityprediction's GNN application |
| `scientific-admet-pharmacokinetics` | → ADMET prediction |
| `scientific-network-analysis` | ← graphstructureanalysis |
| `scientific-deep-learning` | ← NN Design Method |
| `scientific-explainable-ai` | → GNN prediction's explainability |
| `scientific-protein-structure-analysis` | ← proteingraph's construction |
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
