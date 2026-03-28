---
name: scientific-pathway-enrichment
description: |
 pathwayGene Ontology analysisskill。KEGG pathwaysearchmapping、
 Reactome pathwayanalysis、Gene Ontology (BP/MF/CC) annotation、
 WikiPathways pathway、Pathway Commons integrationinteraction cross-cutting
 use ORA (Over-Representation Analysis)、GSEA (Gene Set Enrichment Analysis)、
 analysispipeline。34+ ---

# Scientific Pathway & Enrichment Analysis

gene listfile
KEGG / Reactome / GO / WikiPathways / Pathway Commons 's 
5 pathway DB cross-cuttingintegrationanalysispipeline is provided。

## When to Use

- DEG (expressiongene) 's notepathway is performedand
- GSEA gene-basedpathwayactivity is evaluatedand
- KEGG / Reactome pathway's detailsmappingwhen needed
- GO (BP/MF/CC) usingclassificationwhen needed
- multiple DB 's pathwayresultsintegrationcomparisonwhen needed

---

## Quick Start

## 1. ORA (Over-Representation Analysis)

```python
import pandas as pd
import numpy as np
from scipy import stats


def over_representation_analysis(gene_list, background_genes,
 gene_sets, min_size=10, max_size=500,
 fdr_method="fdr_bh"):
 """
 testing's Over-Representation Analysis (ORA)。

 Parameters:
 gene_list: list — DEG etc.'s notegene list
 background_genes: list — backgroundgene (allexpressiongene)
 gene_sets: dict — {pathway_name: [genes]} 
 min_size / max_size: pathwayfilter
 fdr_method: testingcorrection ("fdr_bh", "bonferroni")
 """
 from statsmodels.stats.multitest import multipletests

 query = set(gene_list)
 bg = set(background_genes)
 N = len(bg) # background
 n = len(query & bg) # 's backgroundgenenumber/count

 results = []
 for pathway, members in gene_sets.items:
 pathway_bg = set(members) & bg
 K = len(pathway_bg) # pathway (background)
 k = len(query & pathway_bg) # number/count

 if K < min_size or K > max_size:
 continue

 # testing 
 pval = stats.hypergeom.sf(k - 1, N, K, n)
 fold_enrichment = (k / n) / (K / N) if (n > 0 and K > 0) else 0

 results.append({
 "pathway": pathway,
 "overlap": k,
 "pathway_size": K,
 "background_size": N,
 "query_size": n,
 "fold_enrichment": round(fold_enrichment, 2),
 "p_value": pval,
 })

 df = pd.DataFrame(results)
 if len(df) > 0:
 _, fdr, _, _ = multipletests(df["p_value"], method=fdr_method)
 df["fdr"] = fdr
 df = df.sort_values("fdr").reset_index(drop=True)

 print(f"ORA complete: {len(gene_list)} query genes, "
 f"{len(gene_sets)} pathways tested, "
 f"{(df['fdr'] < 0.05).sum} significant (FDR < 0.05)")
 return df
```

## 2. GSEA (Gene Set Enrichment Analysis)

```python
def gsea_analysis(ranked_genes, gene_sets, permutations=1000,
 min_size=15, max_size=500, seed=42):
 """
 GSEA (Subramanian et al., 2005) 's Python implementation。

 Parameters:
 ranked_genes: pd.Series — gene_symbol → fold_change or -log10(p)*sign(FC)
 gene_sets: dict — {pathway_name: [genes]}
 permutations: testingtimesnumber/count
 """
 np.random.seed(seed)
 ranked = ranked_genes.sort_values(ascending=False)
 gene_names = ranked.index.tolist
 scores = ranked.values
 N = len(gene_names)

 results = []
 for pw_name, pw_genes in gene_sets.items:
 hits = set(pw_genes) & set(gene_names)
 if len(hits) < min_size or len(hits) > max_size:
 continue

 # Running sum
 hit_mask = np.array([g in hits for g in gene_names])
 hit_scores = np.abs(scores) * hit_mask
 hit_sum = hit_scores.sum
 miss_count = N - hit_mask.sum

 if hit_sum == 0 or miss_count == 0:
 continue

 running_sum = np.cumsum(
 np.where(hit_mask, np.abs(scores) / hit_sum,
 -1.0 / miss_count)
 )

 es = running_sum[np.argmax(np.abs(running_sum))]

 # testing
 null_es = []
 for _ in range(permutations):
 perm_idx = np.random.permutation(N)
 perm_hit = hit_mask[perm_idx]
 perm_scores = np.abs(scores) * perm_hit
 ps = perm_scores.sum
 if ps == 0:
 continue
 perm_rs = np.cumsum(
 np.where(perm_hit, np.abs(scores) / ps,
 -1.0 / miss_count)
 )
 null_es.append(perm_rs[np.argmax(np.abs(perm_rs))])

 null_es = np.array(null_es)
 if es >= 0:
 pval = (null_es >= es).mean
 else:
 pval = (null_es <= es).mean

 nes = es / np.abs(null_es).mean if np.abs(null_es).mean > 0 else 0

 results.append({
 "pathway": pw_name,
 "es": round(es, 4),
 "nes": round(nes, 4),
 "p_value": pval,
 "hit_count": len(hits),
 "leading_edge": [g for g in gene_names if g in hits][:10],
 })

 df = pd.DataFrame(results).sort_values("p_value").reset_index(drop=True)

 from statsmodels.stats.multitest import multipletests
 if len(df) > 0:
 _, fdr, _, _ = multipletests(df["p_value"], method="fdr_bh")
 df["fdr"] = fdr

 print(f"GSEA complete: {len(ranked_genes)} ranked genes, "
 f"{len(results)} pathways, "
 f"{(df['fdr'] < 0.05).sum if 'fdr' in df.columns else 0} significant")
 return df
```

## 3. KEGG pathway mapping

```python
def kegg_pathway_analysis(gene_list, organism="hsa"):
 """
 KEGG REST API by/viapathway mapping。

 Parameters:
 gene_list: list — gene symbolor KEGG gene ID 
 organism: str — KEGG organism/species (hsa, mmu, etc.)
 """
 import requests

 base_url = "https://rest.kegg.jp"

 # 1. gene → pathway mapping
 gene_pathway_map = {}
 for gene in gene_list:
 url = f"{base_url}/link/pathway/{organism}:{gene}"
 resp = requests.get(url)
 if resp.status_code == 200 and resp.text.strip:
 for line in resp.text.strip.split("\n"):
 parts = line.strip.split("\t")
 if len(parts) == 2:
 pw = parts[1].replace("path:", "")
 gene_pathway_map.setdefault(pw, []).append(gene)

 # 2. pathway informationretrieval
 results = []
 for pw_id, genes in gene_pathway_map.items:
 info_url = f"{base_url}/get/{pw_id}"
 resp = requests.get(info_url)
 name = pw_id
 if resp.status_code == 200:
 for line in resp.text.split("\n"):
 if line.startswith("NAME"):
 name = line.replace("NAME", "").strip
 break

 results.append({
 "pathway_id": pw_id,
 "pathway_name": name,
 "gene_count": len(genes),
 "genes": genes,
 })

 df = pd.DataFrame(results).sort_values("gene_count", ascending=False)
 print(f"KEGG mapping: {len(gene_list)} genes → {len(df)} pathways")
 return df
```

## 4. Reactome pathwayanalysis

```python
def reactome_enrichment(gene_list, species="Homo sapiens",
 p_cutoff=0.05, include_interactors=False):
 """
 Reactome REST API by/viaanalysis。

 Parameters:
 gene_list: list — UniProt ID orgene symbol
 species: species name
 p_cutoff: significance level
 """
 import requests

 url = "https://reactome.org/AnalysisService/identifiers/"
 payload = "\n".join(gene_list)
 headers = {"Content-Type": "text/plain"}
 params = {
 "interactors": str(include_interactors).lower,
 "species": species,
 "sortBy": "ENTITIES_PVALUE",
 "order": "ASC",
 "resource": "TOTAL",
 }

 resp = requests.post(url, data=payload, headers=headers, params=params)
 data = resp.json

 pathways = data.get("pathways", [])
 results = []
 for pw in pathways:
 entities = pw.get("entities", {})
 results.append({
 "pathway_id": pw.get("stId", ""),
 "pathway_name": pw.get("name", ""),
 "found": entities.get("found", 0),
 "total": entities.get("total", 0),
 "ratio": round(entities.get("ratio", 0), 4),
 "p_value": entities.get("pValue", 1.0),
 "fdr": entities.get("fdr", 1.0),
 "species": pw.get("species", {}).get("name", ""),
 })

 df = pd.DataFrame(results)
 sig = df[df["fdr"] < p_cutoff] if len(df) > 0 else df
 print(f"Reactome enrichment: {len(gene_list)} genes → "
 f"{len(sig)} significant pathways (FDR < {p_cutoff})")
 return df
```

## 5. Gene Ontology annotation

```python
def go_enrichment(gene_list, background_genes=None,
 ontology="BP", organism="human",
 method="fisher", fdr_cutoff=0.05):
 """
 Gene Ontology analysis (goatools / gseapy )。

 Parameters:
 gene_list: list — notegene list
 ontology: "BP" (Biological Process), "MF" (Molecular Function),
 "CC" (Cellular Component)
 method: "fisher" or "chi2"
 """
 import requests

 # QuickGO API GO term retrieval
 results = []
 url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
 batch_size = 100

 for i in range(0, len(gene_list), batch_size):
 batch = gene_list[i:i + batch_size]
 params = {
 "geneProductId": ",".join(batch),
 "aspect": ontology,
 "taxonId": "9606" if organism == "human" else organism,
 "limit": 200,
 }
 resp = requests.get(url, params=params, headers={"Accept": "application/json"})
 if resp.status_code == 200:
 data = resp.json
 for result in data.get("results", []):
 results.append({
 "gene": result.get("geneProductId", ""),
 "go_id": result.get("goId", ""),
 "go_name": result.get("goName", ""),
 "evidence": result.get("goEvidence", ""),
 "aspect": result.get("goAspect", ""),
 })

 df = pd.DataFrame(results)
 if len(df) > 0:
 term_counts = df.groupby(["go_id", "go_name"]).size.reset_index(name="count")
 term_counts = term_counts.sort_values("count", ascending=False)
 print(f"GO {ontology} enrichment: {len(gene_list)} genes → "
 f"{len(term_counts)} unique GO terms")
 return term_counts

 return df
```

## 6. integrationheatmap

```python
def integrated_enrichment_heatmap(ora_results_dict, top_n=20,
 fdr_cutoff=0.05,
 output="figures/enrichment_heatmap.png"):
 """
 multiple DB 's results integrationheatmapvisualization。

 Parameters:
 ora_results_dict: dict — {"KEGG": df, "Reactome": df, "GO_BP": df}
 top_n: tablepathwaynumber/count
 fdr_cutoff: significance level
 """
 import matplotlib.pyplot as plt
 import os

 os.makedirs(os.path.dirname(output), exist_ok=True)

 fig, axes = plt.subplots(1, len(ora_results_dict),
 figsize=(6 * len(ora_results_dict), 10))
 if len(ora_results_dict) == 1:
 axes = [axes]

 for ax, (db_name, df) in zip(axes, ora_results_dict.items):
 sig = df[df["fdr"] < fdr_cutoff].head(top_n)
 if len(sig) == 0:
 ax.set_title(f"{db_name}\n(no significant)")
 continue

 neg_log_fdr = -np.log10(sig["fdr"].clip(lower=1e-50))

 ax.barh(range(len(sig)), neg_log_fdr, color="steelblue")
 ax.set_yticks(range(len(sig)))
 ax.set_yticklabels(sig["pathway"].str[:50], fontsize=8)
 ax.set_xlabel("-log10(FDR)")
 ax.set_title(f"{db_name} (top {len(sig)})")
 ax.axvline(-np.log10(fdr_cutoff), color="red", ls="--", alpha=0.5)
 ax.invert_yaxis

 plt.tight_layout
 plt.savefig(output, dpi=300, bbox_inches="tight")
 plt.close
 print(f"Saved: {output}")
 return output
```

## References

### Output Files

| File | Format |
|---|---|
| `results/ora_results.csv` | CSV |
| `results/gsea_results.csv` | CSV |
| `results/kegg_pathways.csv` | CSV |
| `results/reactome_enrichment.csv` | CSV |
| `results/go_enrichment.csv` | CSV |
| `figures/enrichment_heatmap.png` | PNG |
| `figures/gsea_running_sum.png` | PNG |

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
| `scientific-gene-expression-transcriptomics` | DEG → ORA/GSEA |
| `scientific-proteomics-mass-spectrometry` | protein → pathway |
| `scientific-metabolomics` | metabolite → pathway mapping |
| `scientific-single-cell-genomics` | scRNA-seq → GO |
| `scientific-multi-omics` | multi-omicsintegration |
| `scientific-network-analysis` | pathway → network |
| `scientific-systems-biology` | FBA/GRN → pathwayintegration |

### Dependencies

`scipy`, `statsmodels`, `pandas`, `numpy`, `matplotlib`, `requests`, `gseapy` (optional)
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
