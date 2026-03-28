---
name: scientific-human-protein-atlas
description: |
 Human Protein Atlas (HPA) integrationskill。tissue/cellproteinexpression、
 cancerprognosisbiomarker、RNA expressionfile、cell、
 proteininteraction's searchanalysispipeline。
---

# Scientific Human Protein Atlas

HPA REST API utilizingtissuecell's
proteinexpressionpipeline is provided。

## When to Use

- gene/protein's tissueexpression is investigatedand
- cancerprognosisbiomarker is evaluatedand
- cell (subcellular localization) is verifiedand
- cell'sexpressioncomparison is performedand
- RNA expressiondata (HPA/GTEx/FANTOM5) integrationwhen needed

---

## Quick Start

## 1. HPA genebasicinformationretrieval

```python
import requests
import pandas as pd

HPA_API = "https://www.proteinatlas.org/api"


def get_hpa_gene_info(ensembl_id):
 """
 HPA genebasicinformationretrieval。

 Parameters:
 ensembl_id: str — Ensembl gene ID (e.g., "ENSG00000141510")

 """
 url = f"https://www.proteinatlas.org/{ensembl_id}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 info = {
 "ensembl_id": ensembl_id,
 "gene_name": data.get("Gene", ""),
 "gene_description": data.get("Gene description", ""),
 "uniprot_id": data.get("Uniprot", []),
 "chromosome": data.get("Chromosome", ""),
 "protein_class": data.get("Protein class", []),
 "evidence": data.get("Evidence", ""),
 }

 print(f"HPA gene: {info['gene_name']} ({ensembl_id})")
 return info, data
```

## 2. tissue RNA expressionfile

```python
def get_tissue_rna_expression(gene_name):
 """
 HPA tissue RNA expressionData Retrieval。

 """
 url = f"https://www.proteinatlas.org/{gene_name}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 rna_data = data.get("RNA tissue specific nTPM", [])
 results = []
 for entry in rna_data:
 results.append({
 "tissue": entry.get("Tissue", ""),
 "cell_type": entry.get("Cell type", ""),
 "ntpm": float(entry.get("nTPM", 0)),
 "detection": entry.get("Detection", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("ntpm", ascending=False)

 print(f"HPA RNA expression '{gene_name}': {len(df)} tissue entries")
 return df
```

## 3. cancerprognosisbiomarkeranalysis

```python
def get_cancer_prognostics(gene_name):
 """
 HPA cancerprognosisData Retrieval。

 """
 url = f"https://www.proteinatlas.org/{gene_name}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 prognostics = data.get("Pathology prognostics", [])
 results = []
 for entry in prognostics:
 results.append({
 "cancer_type": entry.get("Cancer type", ""),
 "prognostic_type": entry.get("Prognostic type", ""),
 "is_prognostic": entry.get("Is prognostic", False),
 "p_value": float(entry.get("p-value", 1.0)),
 "high_expression_favorable": entry.get(
 "High expression is favorable", None
 ),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("p_value")
 significant = df[df["p_value"] < 0.05]
 print(f"HPA cancer prognostics '{gene_name}': "
 f"{len(significant)}/{len(df)} significant")
 else:
 print(f"HPA cancer prognostics '{gene_name}': no data")
 return df
```

## 4. cell

```python
def get_subcellular_location(gene_name):
 """
 HPA cellData Retrieval。

 """
 url = f"https://www.proteinatlas.org/{gene_name}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 sc = data.get("Subcellular location", [])
 results = []
 for entry in sc:
 results.append({
 "location": entry.get("Location", ""),
 "reliability": entry.get("Reliability", ""),
 "enhanced": entry.get("Enhanced", False),
 "supported": entry.get("Supported", False),
 "cell_lines": entry.get("Cell lines", []),
 })

 df = pd.DataFrame(results)
 print(f"HPA subcellular '{gene_name}': {len(df)} locations")
 return df
```

## 5. proteininteractionnetwork (HPA)

```python
def get_hpa_protein_interactions(gene_name):
 """
 HPA proteininteractionData Retrieval。

 """
 url = f"https://www.proteinatlas.org/{gene_name}.json"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 interactions = data.get("Protein interaction partners", [])
 results = []
 for partner in interactions:
 results.append({
 "partner_gene": partner.get("Gene", ""),
 "partner_ensembl": partner.get("Ensembl", ""),
 "confidence": partner.get("Confidence", ""),
 "source": partner.get("Source", ""),
 })

 df = pd.DataFrame(results)
 print(f"HPA interactions '{gene_name}': {len(df)} partners")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/hpa_gene_info.json` | JSON |
| `results/hpa_tissue_expression.csv` | CSV |
| `results/hpa_cancer_prognostics.csv` | CSV |
| `results/hpa_subcellular.csv` | CSV |
| `results/hpa_interactions.csv` | CSV |

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
3. Write `report.md` summarizing methods, results, and interpretation

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-gene-expression-transcriptomics` | GEO/GTEx expressionanalysis |
| `scientific-proteomics-mass-spectrometry` | proteomics |
| `scientific-cancer-genomics` | cancer genomics |
| `scientific-protein-interaction-network` | PPI network |
| `scientific-pathway-enrichment` | pathway |

### Dependencies

`requests`, `pandas`
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Bioinformatics)

Before execution, define:
- [ ] **Organism/assembly**: genome build, annotation version
- [ ] **Input format**: FASTQ/BAM/VCF/GFF/AnnData expected schema
- [ ] **Quality thresholds**: min read quality, min coverage, FDR cutoff
- [ ] **Normalization**: method and justification

#### Pass Criteria
- QC metrics reported (read quality, mapping rate, duplication rate)
- All gene/protein IDs mapped to standard nomenclature
- Multiple testing correction applied (BH/Bonferroni)
- Biological replicates handled appropriately
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
