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
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
