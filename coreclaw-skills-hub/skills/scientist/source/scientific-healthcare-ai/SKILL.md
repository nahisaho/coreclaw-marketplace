---
name: scientific-healthcare-ai
description: |
 AI skill。PyHealth ML pipeline、
 (FlowIO) analysis、 (EHR) 、
 predictionconstruction's。
---

# Scientific Healthcare AI

dataanalysismachine learningpipeline is provided。
PyHealth framework、analysistoolutilizing。

## When to Use

- prediction (prediction, rateprediction) is builtand
- EHR  data's preprocessingfeatures is performedand
- (FACS) dataloadanalysiswhen needed
- task's ML pipeline is designedand
- (ICD-10, SNOMED, ATC) 's mapping is performedand

---

## Quick Start

## 1. PyHealth predictionpipeline

```python
"""
PyHealth by/viapredictionconstruction。
pip install pyhealth

K-Dense-AI reference: pyhealth — ML framework
"""
from pyhealth.datasets import MIMIC3Dataset
from pyhealth.tasks import readmission_prediction_mimic3_fn


def build_clinical_pipeline(
 mimic3_root,
 tables=("DIAGNOSES_ICD", "PROCEDURES_ICD", "PRESCRIPTIONS"),
 code_mapping=None,
):
 """
 MIMIC-III datasetfrompredictionpipelineconstruction。

 Parameters:
 mimic3_root: str — MIMIC-III CSV directory
 tables: tuple — fortable
 code_mapping: dict | None — mappingsettings
 """
 # Step 1: Dataset loading
 if code_mapping is None:
 code_mapping = {
 "NDC": ("ATC", {"target_kwargs": {"level": 3}}),
 "ICD9CM": "CCSCM",
 "ICD9PROC": "CCSPROC",
 }

 dataset = MIMIC3Dataset(
 root=mimic3_root,
 tables=tables,
 code_mapping=code_mapping,
 )

 print(f"MIMIC-III dataset: {len(dataset.patients)} patients")
 return dataset


def apply_clinical_task(dataset, task_fn=None):
 """
 tasknumber/count forgeneration。
 """
 from pyhealth.datasets import split_by_patient

 if task_fn is None:
 task_fn = readmission_prediction_mimic3_fn

 samples = dataset.set_task(task_fn)
 train, val, test = split_by_patient(samples, [0.8, 0.1, 0.1])

 print(f"Clinical task samples: "
 f"train={len(train)}, val={len(val)}, test={len(test)}")
 return train, val, test
```

## 2. PyHealth 

```python
def train_clinical_model(
 train_dataset,
 val_dataset,
 model_type="Transformer",
 epochs=20,
 batch_size=64,
):
 """
 PyHealth 's 。

 Parameters:
 train_dataset: SampleDataset
 val_dataset: SampleDataset
 model_type: str — "Transformer", "RETAIN", "GRU", "CNN"
 epochs: int — training epochs
 """
 from pyhealth.models import Transformer
 from pyhealth.trainer import Trainer

 model_classes = {
 "Transformer": Transformer,
 }
 ModelClass = model_classes.get(model_type, Transformer)

 model = ModelClass(
 dataset=train_dataset,
 feature_keys=["conditions", "procedures", "drugs"],
 label_key="label",
 mode="binary",
 )

 trainer = Trainer(model=model)
 trainer.train(
 train_dataloader=train_dataset,
 val_dataloader=val_dataset,
 epochs=epochs,
 monitor="pr_auc",
 )

 print(f"Clinical model ({model_type}): trained for {epochs} epochs")
 return model, trainer
```

## 3. analysis

```python
def read_fcs_file(fcs_path):
 """
 FCS file's load andpreprocessing。
 pip install flowio

 K-Dense-AI reference: flowio — FCS file I/O

 Parameters:
 fcs_path: str — FCS file path
 """
 import flowio
 import numpy as np
 import pandas as pd

 fcs_data = flowio.FlowData(fcs_path)

 # Extract channel names
 channels = []
 for i in range(1, fcs_data.channel_count + 1):
 name = fcs_data.channels.get(f"P{i}N", f"Channel_{i}")
 channels.append(name)

 # Convert to DataFrame
 events = np.array(fcs_data.events).reshape(-1, fcs_data.channel_count)
 df = pd.DataFrame(events, columns=channels)

 print(f"FCS '{fcs_path}': {len(df)} events x {len(channels)} channels")
 return df, fcs_data


def gate_fcs_data(df, channel, low=None, high=None):
 """
 shape。

 Parameters:
 df: pd.DataFrame — FCS data
 channel: str — 
 low: float | None — 
 high: float | None — 
 """
 mask = pd.Series([True] * len(df))
 if low is not None:
 mask &= df[channel] >= low
 if high is not None:
 mask &= df[channel] <= high

 gated = df[mask]
 pct = len(gated) / len(df) * 100
 print(f"Gate '{channel}' [{low},{high}]: "
 f"{len(gated)}/{len(df)} events ({pct:.1f}%)")
 return gated
```

## 4. mapping

```python
def map_medical_codes(codes, source_system, target_system):
 """
 'smapping。

 Parameters:
 codes: list[str] — 's
 source_system: str — "ICD9CM", "ICD10CM", "NDC", "ATC", "SNOMED"
 target_system: str — transformationsystem
 """
 try:
 from pyhealth.medcode import CrossMap

 mapper = CrossMap(source_system, target_system)
 results = {}
 for code in codes:
 mapped = mapper.map(code)
 results[code] = mapped

 mapped_count = sum(1 for v in results.values if v)
 print(f"Code mapping {source_system}→{target_system}: "
 f"{mapped_count}/{len(codes)} mapped")
 return results

 except ImportError:
 print("pyhealth.medcode not available; install pyhealth")
 return {}
```

## 5. evaluation

```python
def evaluate_clinical_model(trainer, test_dataset):
 """
 prediction'sevaluation。

 Parameters:
 trainer: Trainer — Trainer
 test_dataset: SampleDataset — test data
 """
 metrics = trainer.evaluate(test_dataset)

 print("Clinical model evaluation:")
 for metric_name, value in metrics.items:
 print(f" {metric_name}: {value:.4f}")

 return metrics
```

## References

### Output Files

| File | Format |
|---|---|
| `results/clinical_predictions.csv` | CSV |
| `results/clinical_metrics.json` | JSON |
| `results/fcs_processed.csv` | CSV |
| `results/code_mapping.json` | JSON |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| (K-Dense) | `pyhealth` | ML framework |
| (K-Dense) | `flowio` | FCS file I/O |

> **note**: papersskill ToolUniverse tool、
> K-Dense-AI Scientific Skills from's reference's。

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-clinical-nlp` | NLP |
| `scientific-biostatistics-survival` | timeanalysis |
| `scientific-single-cell-rnaseq` | singlecellanalysis |
| `scientific-machine-learning-omics` | ML x omics |
| `scientific-biothings-idmapping` | ID mapping |

### Dependencies

`pyhealth`, `flowio`, `numpy`, `pandas`, `scikit-learn`
