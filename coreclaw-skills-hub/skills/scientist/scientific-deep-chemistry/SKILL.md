---
name: scientific-deep-chemistry
description: |
 Deep chemistry skill. Graph neural networks for molecular property prediction, molecular generation with VAE/GAN, reaction prediction, and retrosynthesis planning.
---

# Scientific Deep Chemistry

DeepChem utilizingdeep learningmoleculepredictionpipeline is provided。
graphnetwork (GCN/MPNN/AttentiveFP)、MoleculeNet
、 (ChemBERTa/GROVER)。

## When to Use

- molecule's ADMET/properties deep learning predictionwhen needed
- MoleculeNet dataset and
- GCN / MPNN / AttentiveFP trainingwhen needed
- ChemBERTa moleculetable is performedand
- toxicityprediction (Tox21, ToxCast) is performedand
- activityprediction'smoleculefeatures is generatedand

---

## Quick Start

## 1. MoleculeNet dataset

```python
import deepchem as dc
import numpy as np
import pandas as pd


def load_moleculenet(dataset_name="delaney", featurizer="GraphConv",
 split="scaffold"):
 """
 MoleculeNet dataset。

 Parameters:
 dataset_name: str — dataset name
 ("delaney", "tox21", "bbbp", "hiv", "muv", "pcba",
 "sider", "clintox", "freesolv", "lipo")
 featurizer: str — featuresmethod
 ("GraphConv", "ECFP", "Weave", "MolGraphConv")
 split: str — minmethod ("scaffold", "random", "stratified")

 K-Dense: deepchem
 """
 loader_map = {
 "delaney": dc.molnet.load_delaney,
 "tox21": dc.molnet.load_tox21,
 "bbbp": dc.molnet.load_bbbp,
 "hiv": dc.molnet.load_hiv,
 "muv": dc.molnet.load_muv,
 "pcba": dc.molnet.load_pcba,
 "sider": dc.molnet.load_sider,
 "clintox": dc.molnet.load_clintox,
 "freesolv": dc.molnet.load_freesolv,
 "lipo": dc.molnet.load_lipo,
 }

 if dataset_name not in loader_map:
 raise ValueError(f"Unknown dataset: {dataset_name}")

 tasks, datasets, transformers = loader_map[dataset_name](
 featurizer=featurizer, splitter=split
 )
 train, valid, test = datasets

 print(f"MoleculeNet '{dataset_name}':")
 print(f" Tasks: {len(tasks)}")
 print(f" Train: {len(train)}, Valid: {len(valid)}, Test: {len(test)}")
 print(f" Featurizer: {featurizer}, Split: {split}")
 return tasks, (train, valid, test), transformers
```

## 2. GCN training

```python
def train_gcn(train_data, valid_data, tasks, n_epochs=50,
 learning_rate=0.001, batch_size=64):
 """
 Graph Convolutional Network (GCN) training。

 Parameters:
 train_data: dc.data.Dataset — training data
 valid_data: dc.data.Dataset — validation data
 tasks: list — task name list
 n_epochs: int — number of epochs
 """
 model = dc.models.GraphConvModel(
 n_tasks=len(tasks),
 mode="classification" if hasattr(train_data, 'mode') and train_data.mode == 'classification' else ("classification" if any(t in str(tasks).lower for t in ['tox21','bbbp','hiv','clintox','sider','muv','pcba']) else "regression"),
 batch_size=batch_size,
 learning_rate=learning_rate,
 )

 for epoch in range(n_epochs):
 loss = model.fit(train_data, nb_epoch=1)
 if (epoch + 1) % 10 == 0:
 metric = dc.metrics.Metric(
 dc.metrics.roc_auc_score if model.mode == "classification"
 else dc.metrics.pearson_r2_score
 )
 train_score = model.evaluate(train_data, [metric])
 valid_score = model.evaluate(valid_data, [metric])
 print(f" Epoch {epoch+1}: "
 f"train={list(train_score.values)[0]:.4f}, "
 f"valid={list(valid_score.values)[0]:.4f}")

 return model
```

## 3. MPNN training

```python
def train_mpnn(train_data, valid_data, tasks, n_epochs=50,
 learning_rate=0.001):
 """
 Message Passing Neural Network (MPNN) training。

 Parameters:
 train_data: dc.data.Dataset — GraphConv featurestraining data
 valid_data: dc.data.Dataset — validation data
 tasks: list — task name list
 """
 model = dc.models.MPNNModel(
 n_tasks=len(tasks),
 mode="classification" if hasattr(train_data, 'mode') and train_data.mode == 'classification' else ("classification" if any(t in str(tasks).lower for t in ['tox21','bbbp','hiv','clintox','sider','muv','pcba']) else "regression"),
 learning_rate=learning_rate,
 node_out_feats=64,
 edge_hidden_feats=128,
 num_step_message_passing=3,
 )

 model.fit(train_data, nb_epoch=n_epochs)

 metric = dc.metrics.Metric(
 dc.metrics.roc_auc_score if model.mode == "classification"
 else dc.metrics.pearson_r2_score
 )
 valid_score = model.evaluate(valid_data, [metric])
 print(f"MPNN: valid score = {list(valid_score.values)[0]:.4f}")
 return model
```

## 4. AttentiveFP training

```python
def train_attentivefp(train_data, valid_data, tasks, n_epochs=50,
 learning_rate=0.001, num_layers=2):
 """
 AttentiveFP (Attention-based Fingerprint) training。

 Parameters:
 train_data: dc.data.Dataset — training data
 valid_data: dc.data.Dataset — validation data
 tasks: list — task
 num_layers: int — GATlayernumber/count
 """
 model = dc.models.AttentiveFPModel(
 n_tasks=len(tasks),
 mode="classification" if hasattr(train_data, 'mode') and train_data.mode == 'classification' else ("classification" if any(t in str(tasks).lower for t in ['tox21','bbbp','hiv','clintox','sider','muv','pcba']) else "regression"),
 learning_rate=learning_rate,
 num_layers=num_layers,
 graph_feat_size=200,
 num_timesteps=2,
 )

 model.fit(train_data, nb_epoch=n_epochs)

 metric = dc.metrics.Metric(
 dc.metrics.roc_auc_score if model.mode == "classification"
 else dc.metrics.pearson_r2_score
 )
 valid_score = model.evaluate(valid_data, [metric])
 print(f"AttentiveFP: valid score = {list(valid_score.values)[0]:.4f}")
 return model
```

## 4.1 's save andload

```python
def save_model(model, model_dir="results/model"):
 """
 training DeepChem save.
 """
 import os
 os.makedirs(model_dir, exist_ok=True)
 model.save_checkpoint(model_dir=model_dir)
 print(f" Model saved to: {model_dir}")
 return model_dir


def load_model(model_class, model_dir="results/model", **model_kwargs):
 """
 save DeepChem loads。

 Parameters:
 model_class: DeepChem (e.g., dc.models.GraphConvModel)
 model_dir: str — savedirectory
 **model_kwargs: initialparameters (n_tasks, mode etc.)
 """
 model = model_class(**model_kwargs)
 model.restore(model_dir=model_dir)
 print(f" Model loaded from: {model_dir}")
 return model
```

## 5. ChemBERTa moleculetable

```python
def chemberta_embeddings(smiles_list, model_name="seyonec/ChemBERTa-zinc-base-v1"):
 """
 ChemBERTa SMILES → molecule。

 Parameters:
 smiles_list: list — SMILES 
 model_name: str — HuggingFace model name
 """
 from transformers import AutoTokenizer, AutoModel
 import torch

 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = AutoModel.from_pretrained(model_name)
 model.eval

 embeddings = []
 batch_size = 32

 for i in range(0, len(smiles_list), batch_size):
 batch = smiles_list[i:i+batch_size]
 inputs = tokenizer(batch, padding=True, truncation=True,
 max_length=512, return_tensors="pt")

 with torch.no_grad:
 outputs = model(**inputs)
 # CLS 
 cls_emb = outputs.last_hidden_state[:, 0, :].numpy
 embeddings.append(cls_emb)

 embeddings = np.vstack(embeddings)
 print(f"ChemBERTa: {len(smiles_list)} molecules → "
 f"{embeddings.shape[1]}D embeddings")
 return embeddings
```

## 6. comparison

```python
def benchmark_models(dataset_name="tox21", models_to_test=None,
 n_epochs=30):
 """
 multiple'scomparison。

 Parameters:
 dataset_name: str — MoleculeNet dataset
 models_to_test: list — testing
 n_epochs: int — number of epochs
 """
 if models_to_test is None:
 models_to_test = ["GCN", "MPNN", "AttentiveFP"]

 results = {}

 for model_name in models_to_test:
 featurizer = "GraphConv" if model_name != "ECFP_RF" else "ECFP"
 tasks, (train, valid, test), transformers = load_moleculenet(
 dataset_name, featurizer=featurizer
 )

 is_classification = len(tasks) > 1 or dataset_name in [
 "tox21", "bbbp", "hiv", "sider", "clintox"
 ]

 if model_name == "GCN":
 model = train_gcn(train, valid, tasks, n_epochs=n_epochs)
 elif model_name == "MPNN":
 model = train_mpnn(train, valid, tasks, n_epochs=n_epochs)
 elif model_name == "AttentiveFP":
 model = train_attentivefp(train, valid, tasks, n_epochs=n_epochs)
 else:
 continue

 metric = dc.metrics.Metric(
 dc.metrics.roc_auc_score if is_classification
 else dc.metrics.pearson_r2_score
 )
 test_score = model.evaluate(test, [metric])
 results[model_name] = list(test_score.values)[0]

 print(f"\nBenchmark on '{dataset_name}':")
 for name, score in sorted(results.items, key=lambda x: -x[1]):
 print(f" {name}: {score:.4f}")
 return results
```

## 7. moleculepredictionpipeline

```python
def molecular_prediction_pipeline(smiles_list, property_name="solubility",
 model_type="AttentiveFP"):
 """
 SMILES → moleculeprediction integrationpipeline。

 Parameters:
 smiles_list: list — SMILES 
 property_name: str — predictionproperties
 model_type: str — for
 """
 # datasetmapping
 property_dataset = {
 "solubility": "delaney",
 "toxicity": "tox21",
 "bbb_penetration": "bbbp",
 "hiv_activity": "hiv",
 "lipophilicity": "lipo",
 "solvation_energy": "freesolv",
 }

 dataset_name = property_dataset.get(property_name, "delaney")

 # 1) datatraining
 tasks, (train, valid, test), transformers = load_moleculenet(
 dataset_name, featurizer="GraphConv"
 )

 if model_type == "GCN":
 model = train_gcn(train, valid, tasks)
 elif model_type == "AttentiveFP":
 model = train_attentivefp(train, valid, tasks)
 else:
 model = train_mpnn(train, valid, tasks)

 # 2) novelmoleculeprediction
 featurizer = dc.feat.MolGraphConvFeaturizer
 features = featurizer.featurize(smiles_list)
 pred_dataset = dc.data.NumpyDataset(X=features)
 predictions = model.predict(pred_dataset)

 results = []
 for smi, pred in zip(smiles_list, predictions):
 results.append({
 "smiles": smi,
 "prediction": float(pred[0]) if pred.ndim > 1 else float(pred),
 "property": property_name,
 "model": model_type,
 })

 df = pd.DataFrame(results)
 print(f"Predictions: {len(df)} molecules, property='{property_name}'")
 return df
```

---

## Pipeline Integration

```
cheminformatics → deep-chemistry → drug-target-profiling
 (RDKit/SMILES) (GCN/MPNN/FP) (ChEMBL/)
 │ │ ↓
molecular-docking ───────┘ admet-pharmacokinetics
 (AutoDock/Vina) │ (ADMETprediction)
 ↓
 md-simulation
 (molecular dynamicsverification)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/predictions.csv` | moleculepredictionvalue | → drug-target-profiling |
| `results/benchmark.json` | results | — |
| `results/embeddings.npy` | ChemBERTa | → cheminformatics |
| `results/model/` | training | → admet-pharmacokinetics |

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

---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
