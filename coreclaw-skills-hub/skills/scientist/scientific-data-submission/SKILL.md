---
name: scientific-data-submission
description: |
 Data submission skill. GEO/SRA/ENA/DDBJ data deposition, metadata preparation, compliance with FAIR principles, and repository-specific format conversion.
---

# Scientific Data Submission

GenBank / SRA / ENA / GEO / BioProject utilizingdata's
pipeline is provided。FAIR principles
sequencedataexpressiondatadata's。

## When to Use

- sequencedata GenBank/DDBJ/ENA when needed
- RNA-seq/WGS data SRA when needed
- GEO /RNA-seq expressiondatawhen needed
- BioProject/BioSample data structurewhen needed
- paperdataaccessionnumberwhen needed
- FAIR principles (Findable, Accessible, Interoperable, Reusable) when needed

---

## Quick Start

## 1. BioProject/BioSample data

```python
import json
import pandas as pd
from pathlib import Path
from datetime import date


def create_bioproject_metadata(title, description, organism,
 data_type="Genome Sequencing",
 relevance="Medical"):
 """
 BioProject data XML/JSON generation。

 Parameters:
 title: str — title
 description: str — 
 organism: str — organism/species
 data_type: str — datatype
 relevance: str — min
 """
 bioproject = {
 "Project": {
 "ProjectID": {"ArchiveID": {"accession": "PRJNA_PENDING"}},
 "Descriptor": {
 "Title": title,
 "Description": description,
 "Relevance": relevance,
 },
 "ProjectType": {
 "ProjectTypeSubmission": {
 "Target": {
 "Organism": {"OrganismName": organism},
 },
 "Method": {"MethodType": data_type},
 "Objectives": {"Data": {"DataType": data_type}},
 }
 },
 }
 }

 print(f"BioProject metadata created:")
 print(f" Title: {title}")
 print(f" Organism: {organism}")
 print(f" Data type: {data_type}")
 return bioproject


def create_biosample_table(samples, organism, package="Generic"):
 """
 BioSample TSV templategeneration。

 Parameters:
 samples: list[dict] — information
 organism: str — organism/species
 package: str — BioSample package
 """
 required_fields = [
 "sample_name", "organism", "collection_date",
 "geo_loc_name", "tissue", "description",
 ]

 rows = []
 for s in samples:
 row = {
 "sample_name": s.get("name", ""),
 "organism": organism,
 "collection_date": s.get("date", str(date.today)),
 "geo_loc_name": s.get("location", "not collected"),
 "tissue": s.get("tissue", "not applicable"),
 "description": s.get("description", ""),
 }
 row.update({k: v for k, v in s.items
 if k not in ["name", "date", "location"]})
 rows.append(row)

 df = pd.DataFrame(rows)
 print(f"BioSample table: {len(df)} samples, package='{package}'")
 return df
```

## 2. GenBank sequence

```python
def prepare_genbank_submission(sequences, annotations, output_dir="submission"):
 """
 GenBank sequencefor.sqn file。

 Parameters:
 sequences: dict — {seq_id: sequence_string}
 annotations: dict — {seq_id: {gene, product, organism,...}}
 output_dir: str — output directory
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # FASTA generation
 fasta_path = output_dir / "sequences.fsa"
 with open(fasta_path, "w") as f:
 for seq_id, seq in sequences.items:
 ann = annotations.get(seq_id, {})
 organism = ann.get("organism", "Unknown organism")
 f.write(f">{seq_id} [organism={organism}]\n")
 # 80
 for i in range(0, len(seq), 80):
 f.write(seq[i:i+80] + "\n")

 # Feature Table generation
 tbl_path = output_dir / "sequences.tbl"
 with open(tbl_path, "w") as f:
 for seq_id, ann in annotations.items:
 f.write(f">Feature {seq_id}\n")
 if "gene" in ann:
 f.write(f"1\t{len(sequences[seq_id])}\tgene\n")
 f.write(f"\t\t\tgene\t{ann['gene']}\n")
 if "product" in ann:
 f.write(f"1\t{len(sequences[seq_id])}\tCDS\n")
 f.write(f"\t\t\tproduct\t{ann['product']}\n")

 # Template generation
 template = {
 "source": {
 "organism": list(annotations.values)[0].get("organism", ""),
 "mol_type": "genomic DNA",
 },
 "submitter": {
 "name": "AutoSubmission",
 },
 }

 template_path = output_dir / "template.json"
 with open(template_path, "w") as f:
 json.dump(template, f, indent=2)

 print(f"GenBank submission prepared: {len(sequences)} sequences")
 print(f" FASTA: {fasta_path}")
 print(f" Feature Table: {tbl_path}")
 return {"fasta": str(fasta_path), "tbl": str(tbl_path)}
```

## 3. SRA data & 

```python
def prepare_sra_metadata(samples, library_strategy="WGS",
 library_source="GENOMIC",
 platform="ILLUMINA",
 instrument_model="Illumina NovaSeq 6000"):
 """
 SRA data TSV generation。

 Parameters:
 samples: list[dict] — {biosample, title, file_r1, file_r2}
 library_strategy: str — WGS/RNA-Seq/AMPLICON/etc.
 library_source: str — GENOMIC/TRANSCRIPTOMIC/etc.
 platform: str — ILLUMINA/OXFORD_NANOPORE/etc.
 """
 rows = []
 for s in samples:
 rows.append({
 "biosample_accession": s.get("biosample", "SAMN_PENDING"),
 "library_ID": s.get("library_id", s.get("title", "")),
 "title": s.get("title", ""),
 "library_strategy": library_strategy,
 "library_source": library_source,
 "library_selection": s.get("selection", "RANDOM"),
 "library_layout": "paired" if s.get("file_r2") else "single",
 "platform": platform,
 "instrument_model": instrument_model,
 "filetype": "fastq",
 "filename": s.get("file_r1", ""),
 "filename2": s.get("file_r2", ""),
 })

 df = pd.DataFrame(rows)
 print(f"SRA metadata: {len(df)} runs, strategy={library_strategy}")
 return df


def sra_upload_ascp(files, destination, ascp_key=None):
 """
 Aspera (ascp) by/via SRA datahigh-speed。

 Parameters:
 files: list — file
 destination: str — SRA 
 ascp_key: str — Aspera SSH 
 """
 import subprocess

 if ascp_key is None:
 ascp_key = Path.home / ".aspera/connect/etc/asperaweb_id_dsa.openssh"

 for f in files:
 cmd = [
 "ascp", "-i", str(ascp_key),
 "-QT", "-l", "300m", "-k", "1",
 str(f), destination,
 ]
 print(f"Uploading: {f}")
 subprocess.run(cmd, check=True)

 print(f"SRA upload complete: {len(files)} files")
```

## 4. GEO expressiondata

```python
def prepare_geo_submission(expression_matrix, sample_metadata,
 platform="GPL16791", output_dir="geo_submission"):
 """
 GEO SOFT shapeformula。

 Parameters:
 expression_matrix: pd.DataFrame — gene × 
 sample_metadata: pd.DataFrame — data
 platform: str — GEO ID
 output_dir: str — output directory
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # SOFT template
 soft_path = output_dir / "submission.soft"
 with open(soft_path, "w") as f:
 # Series section
 f.write("^SERIES\n")
 f.write("!Series_title = \n")
 f.write("!Series_summary = \n")
 f.write(f"!Series_platform_id = {platform}\n")

 # Sample sections
 for col in expression_matrix.columns:
 meta = sample_metadata[sample_metadata["sample_id"] == col]
 f.write(f"\n^SAMPLE = {col}\n")
 f.write(f"!Sample_title = {col}\n")
 if len(meta) > 0:
 for key, val in meta.iloc[0].items:
 if key != "sample_id":
 f.write(f"!Sample_characteristics_ch1 = {key}: {val}\n")

 # Matrix file
 matrix_path = output_dir / "expression_matrix.txt"
 expression_matrix.to_csv(matrix_path, sep="\t")

 # Raw data files list
 raw_files_path = output_dir / "raw_files.txt"
 with open(raw_files_path, "w") as f:
 for col in expression_matrix.columns:
 f.write(f"{col}.fastq.gz\n")

 print(f"GEO submission: {expression_matrix.shape[1]} samples, "
 f"{expression_matrix.shape[0]} genes")
 return {"soft": str(soft_path), "matrix": str(matrix_path)}
```

## 5. FAIR dataverification

```python
def fair_checklist(submission_package):
 """
 FAIR principles。

 Parameters:
 submission_package: dict — packageinformation
 """
 checks = {
 "Findable": {
 "F1_persistent_id": bool(submission_package.get("accession")),
 "F2_metadata_rich": bool(submission_package.get("metadata")),
 "F3_id_in_metadata": True,
 "F4_searchable_registry": bool(submission_package.get("repository")),
 },
 "Accessible": {
 "A1_retrievable_protocol": bool(submission_package.get("access_url")),
 "A1_1_open_protocol": True,
 "A2_metadata_persists": True,
 },
 "Interoperable": {
 "I1_formal_language": bool(submission_package.get("format")),
 "I2_fair_vocabularies": bool(submission_package.get("ontology_terms")),
 "I3_qualified_references": bool(submission_package.get("references")),
 },
 "Reusable": {
 "R1_usage_license": bool(submission_package.get("license")),
 "R1_1_community_standards": bool(submission_package.get("standard")),
 "R1_2_provenance": bool(submission_package.get("methods")),
 },
 }

 total = 0
 passed = 0
 for principle, items in checks.items:
 for check, status in items.items:
 total += 1
 if status:
 passed += 1

 score = passed / total * 100 if total > 0 else 0
 print(f"FAIR checklist: {passed}/{total} ({score:.0f}%)")
 for principle, items in checks.items:
 n_pass = sum(items.values)
 print(f" {principle}: {n_pass}/{len(items)}")

 return checks
```

---

## Pipeline Integration

```
bioinformatics → data-submission → literature-search
 (analysiscompletion) (data) (paper)
 │ │ ↓
lab-data-management ───┘ academic-writing
 (Benchling/OMERO) │ (paperwriting)
 ↓
 ebi-databases
 (ENA/BioStudies integration)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `submission/sequences.fsa` | GenBank for FASTA | → bioinformatics |
| `submission/sra_metadata.tsv` | SRA data | → ebi-databases |
| `geo_submission/submission.soft` | GEO SOFT template | → gene-expression |
| `submission/fair_report.json` | FAIR results | → academic-writing |

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
