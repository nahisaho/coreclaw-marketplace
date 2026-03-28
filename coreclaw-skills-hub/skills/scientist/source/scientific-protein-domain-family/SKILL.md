---
name: scientific-protein-domain-family
description: |
 proteinanalysisskill。InterPro annotationsearch、
 InterProScan by/viaprediction、Pfam/SMART/CDD
 classification、visualization、phylogenyconstruction。
---

# Scientific Protein Domain & Family Analysis

InterPro / InterProScan and proteinanalysis
andclassificationpipeline is provided。

## When to Use

- unknownprotein's configurationwhen needed
- InterPro/Pfam annotationclassificationwhen needed
- comparisonvisualizationwhen needed
- InterProScan batchanalysiswhen needed
- evolutionsave is evaluatedand

---

## Quick Start

## 1. InterPro search

```python
import requests
import pandas as pd
import json


INTERPRO_API = "https://www.ebi.ac.uk/interpro/api"


def search_interpro_domains(query, db_filter=None):
 """
 InterPro REST API search。

 Parameters:
 query: str — orkeyword (e.g., "kinase", "SH3")
 db_filter: str — "pfam", "smart", "cdd", "prosite" etc.

 ToolUniverse:
 InterPro_search_domains(query=query)
 """
 url = f"{INTERPRO_API}/entry/interpro"
 params = {"search": query, "page_size": 25}

 if db_filter:
 url = f"{INTERPRO_API}/entry/{db_filter}"

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for entry in data.get("results", []):
 meta = entry.get("metadata", {})
 results.append({
 "accession": meta.get("accession", ""),
 "name": meta.get("name", ""),
 "type": meta.get("type", ""),
 "source_database": meta.get("source_database", "interpro"),
 "description": (meta.get("description", [{}])[0].get("text", "")[:200]
 if meta.get("description") else ""),
 "member_databases": meta.get("member_databases", {}),
 })

 df = pd.DataFrame(results)
 print(f"InterPro search '{query}': {len(df)} entries found")
 return df
```

## 2. protein'sretrieval

```python
def get_protein_domains(uniprot_id):
 """
 UniProt protein's domain annotation retrieval。

 Parameters:
 uniprot_id: str — UniProt accession (e.g., "P04637")

 ToolUniverse:
 InterPro_get_protein_domains(uniprot_id=uniprot_id)
 """
 url = f"{INTERPRO_API}/protein/uniprot/{uniprot_id}"
 params = {"page_size": 50}

 resp = requests.get(url, params=params)
 resp.raise_for_status
 data = resp.json

 domains = []
 for entry in data.get("results", []):
 meta = entry.get("metadata", {})
 # each's information
 for protein_info in entry.get("proteins", []):
 for loc in protein_info.get("entry_protein_locations", []):
 for frag in loc.get("fragments", []):
 domains.append({
 "accession": meta.get("accession", ""),
 "name": meta.get("name", ""),
 "type": meta.get("type", ""),
 "start": frag.get("start", 0),
 "end": frag.get("end", 0),
 "source": meta.get("source_database", "interpro"),
 })

 df = pd.DataFrame(domains)
 if not df.empty:
 df = df.sort_values("start").reset_index(drop=True)

 print(f"Protein {uniprot_id}: {len(df)} domain annotations")
 return df
```

## 3. InterProScan prediction

```python
import time


IPRSCAN_API = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5"


def submit_interproscan(sequence, email="user@example.com",
 applications=None):
 """
 InterProScan REST API prediction。

 Parameters:
 sequence: str — amino acidsequence (FASTA or raw)
 email: str — results
 applications: list — ["Pfam", "SMART", "CDD", "ProSitePatterns"]

 ToolUniverse:
 InterProScan_scan_sequence(sequence=sequence)
 InterProScan_get_job_status(job_id=job_id)
 InterProScan_get_job_results(job_id=job_id)
 """
 if applications is None:
 applications = ["Pfam", "SMART", "CDD", "ProSitePatterns",
 "SUPERFAMILY", "Gene3D"]

 # 1. Submit job
 payload = {
 "email": email,
 "sequence": sequence,
 "appl": ",".join(applications),
 "goterms": "true",
 "pathways": "true",
 }
 resp = requests.post(f"{IPRSCAN_API}/run", data=payload)
 resp.raise_for_status
 job_id = resp.text.strip
 print(f"InterProScan job submitted: {job_id}")

 # 2. Poll for results
 max_wait = 600 # 10 min
 elapsed = 0
 while elapsed < max_wait:
 status_resp = requests.get(f"{IPRSCAN_API}/status/{job_id}")
 status = status_resp.text.strip
 if status == "FINISHED":
 break
 elif status in ("ERROR", "FAILURE", "NOT_FOUND"):
 raise RuntimeError(f"InterProScan job {job_id}: {status}")
 time.sleep(30)
 elapsed += 30
 print(f" Waiting... ({elapsed}s, status={status})")

 # 3. Get results
 result_resp = requests.get(f"{IPRSCAN_API}/result/{job_id}/json")
 result_resp.raise_for_status
 results = result_resp.json

 # Parse matches
 matches = []
 for res in results.get("results", [results]):
 for match in res.get("matches", []):
 sig = match.get("signature", {})
 for loc in match.get("locations", []):
 matches.append({
 "accession": sig.get("accession", ""),
 "name": sig.get("name", ""),
 "description": sig.get("description", ""),
 "database": sig.get("signatureLibraryRelease", {}).get("library", ""),
 "start": loc.get("start", 0),
 "end": loc.get("end", 0),
 "score": loc.get("score", None),
 "evalue": loc.get("evalue", None),
 "interpro_accession": (
 sig.get("entry", {}).get("accession", "")
 if sig.get("entry") else ""
 ),
 "interpro_name": (
 sig.get("entry", {}).get("name", "")
 if sig.get("entry") else ""
 ),
 })

 df = pd.DataFrame(matches)
 print(f"InterProScan: {len(df)} domain matches from {len(applications)} DBs")
 return df, job_id
```

## 4. visualization

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def visualize_domain_architecture(domains_df, protein_length=None,
 output="figures/domain_architecture.png"):
 """
 figuregeneration。

 Parameters:
 domains_df: DataFrame — columns: [name, start, end, source]
 protein_length: int — all (None max(end) for)
 output: str — output file
 """
 import os
 os.makedirs(os.path.dirname(output), exist_ok=True)

 if protein_length is None:
 protein_length = int(domains_df["end"].max) + 10

 # 
 colors = plt.cm.Set3.colors
 unique_sources = domains_df["source"].unique if "source" in domains_df.columns else [""]
 source_color = {s: colors[i % len(colors)] for i, s in enumerate(unique_sources)}

 fig, ax = plt.subplots(figsize=(14, 3))

 # 
 ax.plot([0, protein_length], [0.5, 0.5], "k-", linewidth=2)

 # 
 for _, row in domains_df.iterrows:
 start = row["start"]
 end = row["end"]
 source = row.get("source", "")
 color = source_color.get(source, "steelblue")

 rect = mpatches.FancyBboxPatch(
 (start, 0.2), end - start, 0.6,
 boxstyle="round,pad=0.02",
 facecolor=color, edgecolor="black", linewidth=1
 )
 ax.add_patch(rect)

 # label
 mid = (start + end) / 2
 label = row.get("name", row.get("accession", ""))
 if len(label) > 12:
 label = label[:10] + ".."
 ax.text(mid, 0.5, label, ha="center", va="center",
 fontsize=7, fontweight="bold")

 ax.set_xlim(-10, protein_length + 10)
 ax.set_ylim(-0.5, 1.5)
 ax.set_xlabel("Residue position")
 ax.set_title("Domain Architecture")
 ax.set_yticks([])

 plt.tight_layout
 plt.savefig(output, dpi=150, bbox_inches="tight")
 plt.close
 print(f"Domain architecture: {output}")
 return output
```

## 5. comparison

```python
def compare_domain_architectures(protein_list):
 """
 multipleprotein'scomparison。

 Parameters:
 protein_list: list of str — UniProt accessions
 """
 all_domains = {}
 for uniprot_id in protein_list:
 try:
 df = get_protein_domains(uniprot_id)
 all_domains[uniprot_id] = df
 except Exception as e:
 print(f" Warning: {uniprot_id} failed — {e}")
 all_domains[uniprot_id] = pd.DataFrame

 # min
 domain_sets = {}
 for prot, df in all_domains.items:
 if not df.empty:
 domain_sets[prot] = set(df["accession"].unique)
 else:
 domain_sets[prot] = set

 # allprotein
 if domain_sets:
 common = set.intersection(*domain_sets.values) if domain_sets else set
 all_unique = set.union(*domain_sets.values) if domain_sets else set
 else:
 common = set
 all_unique = set

 summary = {
 "proteins_analyzed": len(protein_list),
 "proteins_with_domains": sum(
 1 for df in all_domains.values if not df.empty
 ),
 "common_domains": sorted(common),
 "total_unique_domains": len(all_unique),
 "per_protein": {
 prot: {"count": len(s), "domains": sorted(s)}
 for prot, s in domain_sets.items
 },
 }

 print(f"Domain comparison: {len(protein_list)} proteins, "
 f"{len(common)} common domains, "
 f"{len(all_unique)} unique domains total")
 return summary, all_domains
```

## References

### Output Files

| File | Format |
|---|---|
| `results/interpro_search.csv` | CSV |
| `results/protein_domains.csv` | CSV |
| `results/interproscan_results.csv` | CSV |
| `results/domain_comparison.json` | JSON |
| `figures/domain_architecture.png` | PNG |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| InterPro | `InterPro_search_domains` | search |
| InterPro | `InterPro_get_protein_domains` | proteinretrieval |
| InterPro | `InterPro_get_domain_details` | details |
| InterProScan | `InterProScan_scan_sequence` | sequenceprediction |
| InterProScan | `InterProScan_get_job_status` | job |
| InterProScan | `InterProScan_get_job_results` | resultsretrieval |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-protein-structure-analysis` | 3D structureanalysis |
| `scientific-protein-interaction-network` | PPI network |
| `scientific-sequence-alignment` | sequence |
| `scientific-phylogenetics` | phylogenyconstruction |
| `scientific-gene-expression-transcriptomics` | expressioncorrelation |

### Dependencies

`requests`, `pandas`, `matplotlib`, `json` (stdlib), `time` (stdlib)
---

## Harness Optimization (v0.4.0)

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
