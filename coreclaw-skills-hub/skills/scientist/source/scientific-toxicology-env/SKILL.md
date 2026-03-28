---
name: scientific-toxicology-env
description: |
 toxicityenvironmentskill。CTD (Comparative Toxicogenomics Database)
 -gene-diseaseToxCast/Tox21 looptoxicity
 IRIS evaluationT3DB /environmenttoxicityPubChem BioAssay toxicitydata。
tu_tools:
 - key: ctd
 name: CTD
 description: -disease-genedatasearch
---

# Scientific Toxicology & Environmental Health

CTD / Tox21 / ToxCast / T3DB / IRIS utilizingtoxicityenvironment
pipeline is provided。-gene-disease、loop
toxicity、evaluation。

## When to Use

- genedisease is investigatedand (CTD)
- Tox21/ToxCast data toxicityanalysiswhen needed
- IRIS evaluationdata (RfD/RfC/UR) referencewhen needed
- environmenttoxicity'sdetailsdatabase (T3DB) is searchedand
- PubChem BioAssay fromtoxicityloopdata is retrievedand
- ADMET toxicitypredictionand experimenttoxicitydata forwhen needed

---

## Quick Start

## 1. CTD -gene-diseasesearch

```python
import requests
import pandas as pd
import json

CTD_BASE = "https://ctdbase.org/tools"


def ctd_chemical_gene(chemical_name, limit=100):
 """
 CTD — -geneinteraction search。

 Parameters:
 chemical_name: str — chemical name (example: "Bisphenol A")
 limit: int — maximum retrieval count
 """
 url = f"{CTD_BASE}/batchQuery.go"
 params = {
 "inputType": "chem",
 "inputTerms": chemical_name,
 "report": "genes_curated",
 "format": "json",
 }
 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json[:limit]

 results = []
 for entry in data:
 results.append({
 "chemical": entry.get("ChemicalName", ""),
 "gene": entry.get("GeneSymbol", ""),
 "organism": entry.get("Organism", ""),
 "interaction": entry.get("Interaction", ""),
 "pubmed_ids": entry.get("PubMedIDs", ""),
 })

 df = pd.DataFrame(results)
 print(f"CTD: {chemical_name} → {len(df)} gene interactions")
 return df
```

## 2. CTD -diseasesearch

```python
def ctd_chemical_disease(chemical_name, limit=100):
 """
 CTD — -diseasesearch。

 Parameters:
 chemical_name: str — chemical name
 limit: int — maximum retrieval count
 """
 url = f"{CTD_BASE}/batchQuery.go"
 params = {
 "inputType": "chem",
 "inputTerms": chemical_name,
 "report": "diseases_curated",
 "format": "json",
 }
 resp = requests.get(url, params=params, timeout=60)
 resp.raise_for_status
 data = resp.json[:limit]

 results = []
 for entry in data:
 results.append({
 "chemical": entry.get("ChemicalName", ""),
 "disease": entry.get("DiseaseName", ""),
 "disease_id": entry.get("DiseaseID", ""),
 "direct_evidence": entry.get("DirectEvidence", ""),
 "inference_score": float(entry.get("InferenceScore", 0)),
 })

 df = pd.DataFrame(results)
 df = df.sort_values("inference_score", ascending=False)
 print(f"CTD: {chemical_name} → {len(df)} disease associations")
 return df
```

## 3. Tox21/ToxCast Data Retrieval

```python
COMPTOX_BASE = "https://comptox.epa.gov/dashboard/api"


def tox21_assay_search(chemical_identifier, assay_source="Tox21"):
 """
 CompTox Dashboard — Tox21/ToxCast resultsretrieval。

 Parameters:
 chemical_identifier: str — DTXSID or CAS
 assay_source: str — "Tox21" or "ToxCast"
 """
 # CompTox Dashboard API 'sData Retrieval
 url = f"{COMPTOX_BASE}/chemical/search"
 params = {"query": chemical_identifier}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 chem_data = resp.json

 dtxsid = chem_data.get("dtxsid", chemical_identifier)

 # endpointretrieval
 url_assay = f"{COMPTOX_BASE}/chemical/{dtxsid}/assays"
 resp_assay = requests.get(url_assay, timeout=30)
 resp_assay.raise_for_status
 assays = resp_assay.json

 results = []
 for assay in assays:
 if assay_source.lower in assay.get("assaySource", "").lower:
 results.append({
 "assay_name": assay.get("assayName", ""),
 "assay_source": assay.get("assaySource", ""),
 "endpoint": assay.get("assayEndpoint", ""),
 "activity": assay.get("activity", ""),
 "ac50_um": assay.get("ac50", None),
 "hit_call": assay.get("hitCall", ""),
 })

 df = pd.DataFrame(results)
 n_active = (df["hit_call"] == "Active").sum if len(df) > 0 else 0
 print(f"Tox21/ToxCast: {dtxsid} → {len(df)} assays, {n_active} active")
 return df
```

## 4. T3DB toxicitysearch

```python
T3DB_BASE = "https://t3db.ca/api"


def t3db_search(query, search_type="name"):
 """
 T3DB — /environmenttoxicitydatabasesearch。

 Parameters:
 query: str — search term
 search_type: str — "name", "cas", "category"
 """
 url = f"{T3DB_BASE}/toxins/search"
 params = {"query": query, "search_type": search_type}
 resp = requests.get(url, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for toxin in data.get("toxins", []):
 results.append({
 "name": toxin.get("name", ""),
 "t3db_id": toxin.get("t3db_id", ""),
 "cas_number": toxin.get("cas_number", ""),
 "category": toxin.get("category", ""),
 "toxicity_class": toxin.get("toxicity_class", ""),
 "ld50_oral": toxin.get("ld50_oral", ""),
 "target_organs": toxin.get("target_organs", []),
 })

 df = pd.DataFrame(results)
 print(f"T3DB: '{query}' → {len(df)} toxins")
 return df
```

## 5. EPA IRIS evaluation

```python
def iris_risk_assessment(chemical_name):
 """
 EPA IRIS — evaluationData Retrieval。

 Parameters:
 chemical_name: str — chemical name
 """
 url = "https://iris.epa.gov/AtoZ"
 resp = requests.get(url, timeout=30)

 # IRIS structure API — ordata
 # : CompTox Dashboard API 
 url_comptox = f"{COMPTOX_BASE}/chemical/search"
 params = {"query": chemical_name}
 resp = requests.get(url_comptox, params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 risk_data = {
 "chemical": chemical_name,
 "dtxsid": data.get("dtxsid", ""),
 "rfd_oral_mg_kg_day": data.get("rfdOral", None),
 "rfc_inhalation_mg_m3": data.get("rfcInhalation", None),
 "cancer_classification": data.get("cancerClassification", ""),
 "oral_slope_factor": data.get("oralSlopeFactor", None),
 "inhalation_unit_risk": data.get("inhalationUnitRisk", None),
 }

 print(f"IRIS: {chemical_name}")
 for k, v in risk_data.items:
 if v and k != "chemical":
 print(f" {k}: {v}")
 return risk_data
```

## 6. toxicitypathway analysis

```python
def toxicity_pathway_analysis(chemical_name, species="Homo sapiens"):
 """
 CTD + pathwayintegrationtoxicityanalysis。

 Parameters:
 chemical_name: str — chemical name
 species: str — organism/species
 """
 # 1) CTD generetrieval
 gene_df = ctd_chemical_gene(chemical_name, limit=500)
 if species:
 gene_df = gene_df[gene_df["organism"] == species]

 gene_list = gene_df["gene"].unique.tolist

 # 2) CTD diseaseretrieval
 disease_df = ctd_chemical_disease(chemical_name, limit=100)

 # 3) pathway (KEGG enrichment via Enrichr)
 enrichr_url = "https://maayanlab.cloud/Enrichr"
 add_resp = requests.post(
 f"{enrichr_url}/addList",
 files={"list": (None, "\n".join(gene_list))}
 )
 user_list_id = add_resp.json["userListId"]

 enrich_resp = requests.get(
 f"{enrichr_url}/enrich",
 params={"userListId": user_list_id, "backgroundType": "KEGG_2021_Human"}
 )
 pathways = enrich_resp.json.get("KEGG_2021_Human", [])

 pathway_results = []
 for pw in pathways[:20]:
 pathway_results.append({
 "pathway": pw[1],
 "p_value": pw[2],
 "adj_p_value": pw[6],
 "genes": pw[5],
 })

 print(f"Toxicity pathway: {chemical_name}")
 print(f" Target genes: {len(gene_list)}")
 print(f" Diseases: {len(disease_df)}")
 print(f" Pathways: {len(pathway_results)}")
 return {
 "genes": gene_df,
 "diseases": disease_df,
 "pathways": pd.DataFrame(pathway_results),
 }
```

---

## Pipeline Integration

```
admet-pharmacokinetics → toxicology-env → pharmacovigilance
 (ADMET toxicityprediction) (CTD/Tox21/IRIS) (all)
 │ │ ↓
cheminformatics ───────────────┘ disease-research
 (RDKit structurealert) │ (disease-gene)
 ↓
 public-health-data
 (CDC/WHO )
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/ctd_gene_interactions.csv` | CTD -gene | → pathway-enrichment |
| `results/ctd_disease_associations.csv` | CTD -disease | → disease-research |
| `results/tox21_assays.csv` | Tox21/ToxCast results | → admet-pharmacokinetics |
| `results/toxicity_pathways.json` | toxicitypathway analysisresults | → pharmacovigilance |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `ctd` | CTD | -disease-genedatasearch |
---

## Harness Optimization (v0.4.0)

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
