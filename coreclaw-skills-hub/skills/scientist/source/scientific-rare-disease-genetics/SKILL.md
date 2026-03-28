---
name: scientific-rare-disease-genetics
description: |
 diseaseskill。OMIM gene-diseasemapping、Orphanet disease
 classificationgene、DisGeNET disease-gene、IMPC tabletype
 reference、gene-tabletypeintegrated analysispipeline。
---

# Scientific Rare Disease Genetics

OMIM / Orphanet / DisGeNET / IMPC integration
diseasepipeline is provided。

## When to Use

- disease's genewhen needed
- OMIM gene-disease's Mendelian is investigatedand
- Orphanet diseaseclassification and rate is searchedand
- DisGeNET disease-gene (GDA) is retrievedand
- IMPC tabletype andcomparisonwhen needed

---

## Quick Start

## 1. OMIM gene-diseasemapping

```python
import requests
import pandas as pd

OMIM_API = "https://api.omim.org/api"


def search_omim(query, api_key, include="geneMap"):
 """
 OMIM databasesearch。

 Parameters:
 query: str — search term (gene name、disease)
 api_key: str — OMIM API 
 include: str — "geneMap", "clinicalSynopsis", "all"

 """
 params = {
 "search": query,
 "include": include,
 "format": "json",
 "apiKey": api_key,
 }
 resp = requests.get(f"{OMIM_API}/entry/search", params=params)
 resp.raise_for_status
 data = resp.json

 entries = data.get("omim", {}).get("searchResponse", {}).get("entryList", [])
 results = []
 for entry in entries:
 e = entry.get("entry", {})
 gene_map = e.get("geneMap", {})
 results.append({
 "mim_number": e.get("mimNumber"),
 "title": e.get("titles", {}).get("preferredTitle", ""),
 "gene_symbols": gene_map.get("geneSymbols", ""),
 "chromosome": gene_map.get("computedCytoLocation", ""),
 "phenotypes": [
 p.get("phenotype", "")
 for p in gene_map.get("phenotypeMapList", [])
 ],
 "inheritance": [
 p.get("phenotypeMappingKey", "")
 for p in gene_map.get("phenotypeMapList", [])
 ],
 })

 df = pd.DataFrame(results)
 print(f"OMIM search '{query}': {len(df)} entries")
 return df
```

## 2. Orphanet diseaseclassification

```python
ORPHANET_API = "https://api.orphadata.com"


def search_orphanet_diseases(query):
 """
 Orphanet diseasesearch。

 """
 resp = requests.get(
 f"{ORPHANET_API}/rd-cross-referencing",
 params={"query": query}
 )
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data if isinstance(data, list) else [data]:
 results.append({
 "orpha_code": item.get("ORPHAcode", ""),
 "name": item.get("Preferred term", ""),
 "prevalence_class": item.get("Prevalence", {}).get("PrevalenceClass", ""),
 "inheritance": item.get("TypeOfInheritance", []),
 "age_of_onset": item.get("AgeOfOnset", []),
 "genes": item.get("DisorderGeneAssociationList", []),
 })

 df = pd.DataFrame(results)
 print(f"Orphanet search '{query}': {len(df)} diseases")
 return df
```

## 3. DisGeNET disease-gene

```python
DISGENET_API = "https://www.disgenet.org/api"


def get_disease_gene_associations(disease_id, api_key):
 """
 DisGeNET GDA by/viadisease-generetrieval。

 Parameters:
 disease_id: str — UMLS CUI (e.g., "C0023264") or disease name
 api_key: str — DisGeNET API key

 """
 headers = {"Authorization": f"Bearer {api_key}"}
 resp = requests.get(
 f"{DISGENET_API}/gda/disease/{disease_id}",
 headers=headers
 )
 resp.raise_for_status
 data = resp.json

 results = []
 for gda in data:
 results.append({
 "gene_symbol": gda.get("gene_symbol", ""),
 "gene_id": gda.get("geneid", ""),
 "gda_score": gda.get("score", 0),
 "ei": gda.get("ei", 0), # Evidence Index
 "el": gda.get("el", ""), # Evidence Level
 "n_pmids": gda.get("pmid_count", 0),
 "source": gda.get("source", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty:
 df = df.sort_values("gda_score", ascending=False)

 print(f"DisGeNET '{disease_id}': {len(df)} gene associations, "
 f"top GDA score={df['gda_score'].max:.3f}" if len(df) > 0 else "")
 return df
```

## 4. IMPC tabletypereference

```python
IMPC_API = "https://www.ebi.ac.uk/mi/impc/solr"


def get_impc_mouse_phenotypes(gene_symbol):
 """
 IMPC tabletypeData Retrieval。

 """
 params = {
 "q": f"marker_symbol:{gene_symbol}",
 "rows": 100,
 "wt": "json",
 }
 resp = requests.get(f"{IMPC_API}/genotype-phenotype/select", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for doc in data.get("response", {}).get("docs", []):
 results.append({
 "gene_symbol": doc.get("marker_symbol", ""),
 "mp_term_id": doc.get("mp_term_id", ""),
 "mp_term_name": doc.get("mp_term_name", ""),
 "top_level_mp": doc.get("top_level_mp_term_name", []),
 "p_value": doc.get("p_value", None),
 "effect_size": doc.get("effect_size", None),
 "zygosity": doc.get("zygosity", ""),
 "procedure_name": doc.get("procedure_name", ""),
 })

 df = pd.DataFrame(results)
 if not df.empty and "p_value" in df.columns:
 df = df.sort_values("p_value")

 print(f"IMPC '{gene_symbol}': {len(df)} phenotype associations")
 return df
```

## 5. gene-tabletypeintegrated analysis

```python
def rare_disease_gene_analysis(gene_symbol, omim_api_key=None,
 disgenet_api_key=None):
 """
 all DB integration's diseasegene。
 """
 profile = {"gene": gene_symbol, "sources": {}}

 # 1. OMIM
 if omim_api_key:
 try:
 omim_df = search_omim(gene_symbol, omim_api_key)
 profile["sources"]["omim"] = {
 "entries": len(omim_df),
 "phenotypes": omim_df["phenotypes"].explode.dropna.unique.tolist
 if not omim_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["omim"] = {"error": str(e)}

 # 2. Orphanet
 try:
 orpha_df = search_orphanet_diseases(gene_symbol)
 profile["sources"]["orphanet"] = {
 "diseases": len(orpha_df),
 "names": orpha_df["name"].tolist if not orpha_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["orphanet"] = {"error": str(e)}

 # 3. DisGeNET
 if disgenet_api_key:
 try:
 dgn_df = get_disease_gene_associations(gene_symbol, disgenet_api_key)
 profile["sources"]["disgenet"] = {
 "associations": len(dgn_df),
 "max_gda_score": float(dgn_df["gda_score"].max)
 if not dgn_df.empty else 0,
 }
 except Exception as e:
 profile["sources"]["disgenet"] = {"error": str(e)}

 # 4. IMPC
 try:
 impc_df = get_impc_mouse_phenotypes(gene_symbol)
 profile["sources"]["impc"] = {
 "phenotypes": len(impc_df),
 "top_phenotypes": impc_df["mp_term_name"].head(5).tolist
 if not impc_df.empty else [],
 }
 except Exception as e:
 profile["sources"]["impc"] = {"error": str(e)}

 n_sources = sum(1 for v in profile["sources"].values if "error" not in v)
 print(f"Rare disease profile '{gene_symbol}': {n_sources}/4 sources OK")
 return profile
```

## References

### Output Files

| File | Format |
|---|---|
| `results/omim_search.csv` | CSV |
| `results/orphanet_diseases.csv` | CSV |
| `results/disgenet_gda.csv` | CSV |
| `results/impc_phenotypes.csv` | CSV |
| `results/rare_disease_profile.json` | JSON |

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
| `scientific-disease-research` | GWAS/Orphanet diseaseresearch |
| `scientific-variant-interpretation` | ACMG |
| `scientific-variant-effect-prediction` | prediction |
| `scientific-population-genetics` | population genetics |
| `scientific-human-protein-atlas` | proteinexpression |

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
