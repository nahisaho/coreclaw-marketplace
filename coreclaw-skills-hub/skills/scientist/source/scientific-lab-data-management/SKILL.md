---
name: scientific-lab-data-management
description: |
 dataskill。Benchling (ELN/DNA design/registry)、
 DNAnexus ( PaaS)、LatchBio (workflow)、
 OMERO 、Protocols.io (protocol)
 integrationdatapipeline。
---

# Scientific Lab Data Management

experimentfromdatato/until、
data's generationanalysis integrationpipeline。

## When to Use

- experiment (ELN) protocolresultswhen needed
- DNA sequencedesigndesignwhen needed
- large-scaledata PaaS analysiswhen needed
- data structurewhen needed
- experimentprotocolwhen needed

---

## Quick Start

## 1. Benchling ELN / DNA design

```python
import json
import requests


class BenchlingClient:
 """
 Benchling API 。

 Benchling :
 - ELN (Electronic Lab Notebook): experiment
 - Molecular Biology: DNA sequencedesign, design, 
 - Registry: registry
 - Inventory: 
 """

 def __init__(self, api_key, tenant_url):
 self.base_url = f"https://{tenant_url}/api/v2"
 self.headers = {
 "Authorization": f"Basic {api_key}",
 "Content-Type": "application/json",
 }

 def create_dna_sequence(self, name, bases, folder_id,
 annotations=None):
 """
 DNA sequence's 。

 Parameters:
 - name: sequence
 - bases: sequence (ATCG)
 - folder_id: savefolder
 - annotations: annotation [{name, start, end, type, strand}]
 """
 payload = {
 "name": name,
 "bases": bases,
 "folderId": folder_id,
 "isCircular": False,
 "annotations": annotations or [],
 }

 print(f" Benchling DNA sequence: {name}")
 print(f" Length: {len(bases)} bp")
 if annotations:
 print(f" Annotations: {len(annotations)}")

 return payload

 def search_registry(self, query, schema_id=None, page_size=50):
 """
 Benchling Registry search。

 registry:
 -,, antibody, cell, compound
 """
 params = {
 "query": query,
 "pageSize": page_size,
 }
 if schema_id:
 params["schemaId"] = schema_id

 print(f" Benchling registry search: '{query}'")

 return params

 def create_entry(self, name, folder_id, template_id=None):
 """
 ELN entry (experiment) 。
 """
 payload = {
 "name": name,
 "folderId": folder_id,
 }
 if template_id:
 payload["entryTemplateId"] = template_id

 print(f" Benchling ELN entry: {name}")

 return payload
```

## 2. DNAnexus PaaS

```python
import json


class DNAnexusClient:
 """
 DNAnexus Platform API 。

 DNAnexus :
 - data: FASTQ, BAM, VCF 'slarge-scalefile
 - workflow: WDL/CWL/Applet 
 - : HIPAA, GxP, FedRAMP
 - : 's
 """

 def __init__(self, token):
 self.token = token
 self.base_url = "https://api.dnanexus.com"

 def upload_file(self, local_path, project_id, folder="/"):
 """
 file。

 supportshapeformula: FASTQ(.gz), BAM, CRAM, VCF, BED, etc.
 """
 print(f" DNAnexus upload: {local_path}")
 print(f" Project: {project_id}")
 print(f" Destination: {folder}")

 return {"local_path": local_path, "project_id": project_id}

 def run_workflow(self, workflow_id, project_id, inputs):
 """
 workflow。

 workflowexample:
 - GATK Best Practices (germline/somatic)
 - RNA-STAR alignment + featureCounts
 - DeepVariant caller
 - Structural variant calling
 """
 print(f" DNAnexus workflow: {workflow_id}")
 print(f" Project: {project_id}")
 print(f" Inputs: {len(inputs)} parameters")

 return {
 "workflow_id": workflow_id,
 "project_id": project_id,
 "inputs": inputs,
 }

 def list_project_files(self, project_id, folder="/", name_glob=None):
 """
 filelist。
 """
 params = {"folder": folder}
 if name_glob:
 params["name"] = {"glob": name_glob}

 print(f" DNAnexus list: {project_id}{folder}")

 return params
```

## 3. OMERO 

```python
import json


class OMEROClient:
 """
 OMERO (Open Microscopy Environment Remote Objects) 。

 OMERO :
 - data: 150+ (Bio-Formats)
 - data: Key-Value,, ROI
 - analysisintegration: ImageJ/Fiji, CellProfiler, napari
 - : /loop
 """

 def __init__(self, host, port=4064):
 self.host = host
 self.port = port

 def import_images(self, file_paths, dataset_id):
 """
 import。

 support (Bio-Formats):
 - OME-TIFF, ND2 (Nikon), CZI (Zeiss), LIF (Leica)
 - VSI (Olympus), SVS (Aperio), DICOM
 """
 print(f" OMERO import: {len(file_paths)} images → Dataset {dataset_id}")

 return {"files": file_paths, "dataset_id": dataset_id}

 def create_roi(self, image_id, shapes):
 """
 ROI (Region of Interest) 。

 Shape :
 - Rectangle, Ellipse, Polygon
 - Line, Polyline, Point
 - Mask (binary mask)
 """
 print(f" OMERO ROI: Image {image_id}, {len(shapes)} shapes")

 return {"image_id": image_id, "shapes": shapes}

 def query_images(self, project=None, dataset=None,
 key_value_pairs=None):
 """
 search (database)。

 filter:
 - /dataset
 - Key-Value annotation
 - 
 - retrieval, 
 """
 print(f" OMERO query:")
 if project:
 print(f" Project: {project}")
 if key_value_pairs:
 print(f" Key-Value: {key_value_pairs}")

 return {"project": project, "dataset": dataset}
```

## 4. Protocols.io protocol

```python
import json


def create_protocol(title, description, steps, reagents=None,
 doi_prefix="dx.doi.org/10.17504"):
 """
 Protocols.io protocol。

 Protocols.io:
 - DOI by/viacitationpossibleprotocol
 - 
 - 
 - JOVE, Nature Protocol Exchange integration
 """
 protocol = {
 "title": title,
 "description": description,
 "steps": [],
 "reagents": reagents or [],
 }

 for i, step in enumerate(steps, 1):
 protocol["steps"].append({
 "step_number": i,
 "description": step.get("description", ""),
 "duration": step.get("duration"),
 "temperature": step.get("temperature"),
 "critical_step": step.get("critical", False),
 "expected_result": step.get("expected_result"),
 })

 print(f" Protocol: {title}")
 print(f" Steps: {len(steps)}")
 if reagents:
 print(f" Reagents: {len(reagents)}")
 print(f" DOI: {doi_prefix}/protocols.io...")

 return protocol


def fork_protocol(original_protocol_id, modifications):
 """
 existingprotocol's and。

 - changepoint's
 - protocol to 's
 - number's automated
 """
 print(f" Forking protocol: {original_protocol_id}")
 print(f" Modifications: {len(modifications)}")

 return {
 "forked_from": original_protocol_id,
 "modifications": modifications,
 }
```

## References

### Output Files

| File | Format |
|---|---|
| `results/benchling_sequences.json` | JSON |
| `results/benchling_registry.json` | JSON |
| `results/dnanexus_workflow_output.json` | JSON |
| `results/omero_image_metadata.json` | JSON |
| `results/protocol.json` | JSON |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

 — each's REST API use。

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-bioinformatics` | dataanalysis |
| `scientific-image-analysis` | analysis |
| `scientific-gene-expression-transcriptomics` | RNA-seq data |
| `scientific-single-cell-genomics` | scRNA-seq data |
| `scientific-data-preprocessing` | datapreprocessing |

### Dependencies

`requests`, `json`, `pandas` (each SDK: `benchling-sdk`, `dxpy`, `omero-py`)
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
