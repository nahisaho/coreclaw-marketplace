---
name: scientific-biothings-idmapping
description: |
 BioThings ID mapping skill. Gene/variant/chemical/disease identifier conversion using MyGene.info, MyVariant.info, and MyChem.info APIs.
tu_tools:
 - key: biothings
 name: BioThings
 description: MyGene/MyVariant/MyChem integrationannotation API
---

# Scientific BioThings ID Mapping

BioThings API (MyGene, MyVariant, MyChem) utilizing
databasecross-cutting's ID transformationannotationretrievalpipeline is provided。

## When to Use

- gene ID 'stransformation (Entrez ↔ Ensembl ↔ Symbol ↔ UniProt) is performedand
- variant/mutation ID 's annotation (ClinVar, dbSNP, CADD ) is retrievedand
- compound ID 's transformation (DrugBank ↔ ChEMBL ↔ InChIKey ↔ PubChem) is performedand
- batchnumber/count's ID annotationwhen needed
- multipledatabase's informationintegrationwhen needed

---

## Quick Start

## 1. MyGene.info geneannotation

```python
import requests
import pandas as pd

MYGENE_API = "https://mygene.info/v3"


def mygene_query(query, fields=None, species="human", size=10):
 """
 MyGene.info genesearch。

 Parameters:
 query: str — gene symbol, Entrez ID, or keyword
 fields: str | None — comma-separated fields
 species: str — "human", "mouse", etc.

 ToolUniverse:
 MyGene_query_genes(q=query, fields=fields, species=species)
 """
 params = {
 "q": query,
 "species": species,
 "size": size,
 }
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYGENE_API}/query", params=params)
 resp.raise_for_status
 data = resp.json

 hits = data.get("hits", [])
 print(f"MyGene query '{query}': {data.get('total', 0)} total, "
 f"{len(hits)} returned")
 return hits


def mygene_get_gene(gene_id, fields=None):
 """
 MyGene.info genedetailsannotationretrieval。

 ToolUniverse:
 MyGene_get_gene_annotation(gene_id=gene_id, fields=fields)
 """
 params = {}
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYGENE_API}/gene/{gene_id}", params=params)
 resp.raise_for_status
 data = resp.json

 print(f"MyGene gene {gene_id}: {data.get('symbol', '?')} "
 f"({data.get('name', '')})")
 return data


def mygene_batch_query(gene_ids, fields=None, species="human"):
 """
 MyGene.info batchgeneannotation。

 ToolUniverse:
 MyGene_batch_query(ids=gene_ids, fields=fields, species=species)
 """
 payload = {
 "ids": ",".join(str(g) for g in gene_ids),
 "species": species,
 }
 if fields:
 payload["fields"] = fields

 resp = requests.post(f"{MYGENE_API}/gene", json=payload)
 resp.raise_for_status
 data = resp.json

 print(f"MyGene batch: {len(gene_ids)} queried → {len(data)} results")
 return data
```

## 2. MyVariant.info variant annotation

```python
MYVARIANT_API = "https://myvariant.info/v1"


def myvariant_get(variant_id, fields=None):
 """
 MyVariant.info variant annotationretrieval。

 Parameters:
 variant_id: str — HGVS notation (e.g., "chr17:g.7674220C>T")

 ToolUniverse:
 MyVariant_get_variant_annotation(variant_id=variant_id, fields=fields)
 """
 params = {}
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYVARIANT_API}/variant/{variant_id}", params=params)
 resp.raise_for_status
 data = resp.json

 clinvar = data.get("clinvar", {})
 cadd = data.get("cadd", {})
 print(f"MyVariant {variant_id}: "
 f"ClinVar={clinvar.get('clinical_significance', 'N/A')}, "
 f"CADD={cadd.get('phred', 'N/A')}")
 return data


def myvariant_query(query, fields=None, size=10):
 """
 MyVariant.info variant/mutationsearch。

 ToolUniverse:
 MyVariant_query_variants(q=query, fields=fields, size=size)
 """
 params = {"q": query, "size": size}
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYVARIANT_API}/query", params=params)
 resp.raise_for_status
 data = resp.json

 hits = data.get("hits", [])
 print(f"MyVariant query '{query}': {data.get('total', 0)} total")
 return hits
```

## 3. MyChem.info compoundannotation

```python
MYCHEM_API = "https://mychem.info/v1"


def mychem_get(chem_id, fields=None):
 """
 MyChem.info compoundannotationretrieval。

 Parameters:
 chem_id: str — InChIKey, DrugBank ID, ChEMBL ID, etc.

 ToolUniverse:
 MyChem_get_chemical_annotation(chem_id=chem_id, fields=fields)
 """
 params = {}
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYCHEM_API}/chem/{chem_id}", params=params)
 resp.raise_for_status
 data = resp.json

 drugbank = data.get("drugbank", {})
 print(f"MyChem {chem_id}: {drugbank.get('name', 'N/A')}")
 return data


def mychem_query(query, fields=None, size=10):
 """
 MyChem.info compoundsearch。

 ToolUniverse:
 MyChem_query_chemicals(q=query, fields=fields, size=size)
 """
 params = {"q": query, "size": size}
 if fields:
 params["fields"] = fields

 resp = requests.get(f"{MYCHEM_API}/query", params=params)
 resp.raise_for_status
 data = resp.json

 hits = data.get("hits", [])
 print(f"MyChem query '{query}': {data.get('total', 0)} total")
 return hits
```

## 4. database ID mapping

```python
def cross_db_id_mapping(gene_symbol):
 """
 gene symbolfrom Entrez, Ensembl, UniProt, RefSeq retrieval。

 ToolUniverse (cross-cutting):
 MyGene_query_genes(q=gene_symbol, fields="entrezgene,ensembl.gene,uniprot,refseq")
 """
 fields = "entrezgene,ensembl.gene,uniprot.Swiss-Prot,refseq.rna,symbol,name"
 hits = mygene_query(gene_symbol, fields=fields)

 results = []
 for hit in hits:
 ensembl = hit.get("ensembl", {})
 if isinstance(ensembl, list):
 ensembl = ensembl[0] if ensembl else {}
 uniprot = hit.get("uniprot", {})

 results.append({
 "symbol": hit.get("symbol", ""),
 "name": hit.get("name", ""),
 "entrez_id": hit.get("entrezgene", ""),
 "ensembl_gene": ensembl.get("gene", ""),
 "uniprot_swissprot": uniprot.get("Swiss-Prot", ""),
 "refseq_rna": hit.get("refseq", {}).get("rna", []),
 })

 df = pd.DataFrame(results)
 print(f"ID mapping '{gene_symbol}': {len(df)} entries")
 return df
```

## 5. batchintegrationannotation

```python
def batch_integrated_annotation(gene_symbols, include_variants=False):
 """
 multiplegene'sbatchintegrationannotation。

 ToolUniverse (cross-cutting):
 MyGene_batch_query(ids=entrez_ids, fields=fields)
 MyVariant_query_variants(q=gene_query) [optional]
 """
 # Step 1: Batch gene annotation
 all_hits = []
 for symbol in gene_symbols:
 hits = mygene_query(symbol, fields="entrezgene,symbol,name,summary")
 all_hits.extend(hits[:1]) # top hit per symbol

 df = pd.DataFrame(all_hits)
 print(f"Batch annotation: {len(gene_symbols)} genes → {len(df)} results")
 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/mygene_annotation.json` | JSON |
| `results/myvariant_annotation.json` | JSON |
| `results/mychem_annotation.json` | JSON |
| `results/id_mapping.csv` | CSV |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| BioThings | `MyGene_query_genes` | genesearch |
| BioThings | `MyGene_get_gene_annotation` | genedetails |
| BioThings | `MyGene_batch_query` | batchannotation |
| BioThings | `MyVariant_get_variant_annotation` | variant annotation |
| BioThings | `MyVariant_query_variants` | variant/mutationsearch |
| BioThings | `MyChem_get_chemical_annotation` | compoundannotation |
| BioThings | `MyChem_query_chemicals` | compoundsearch |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-variant-interpretation` | variant annotation |
| `scientific-gene-expression-transcriptomics` | gene expression |
| `scientific-drug-target-interaction` | DTI analysis |
| `scientific-rare-disease-genetics` | disease |
| `scientific-pathway-enrichment` | pathway analysis |

### Dependencies

`requests`, `pandas`
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
