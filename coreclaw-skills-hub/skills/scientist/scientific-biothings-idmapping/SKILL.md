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

## Verification Loop (v0.3.0)

```
PLAN → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY → check outputs against quality gates
REPORT → save all artifacts, generate report.md
```

### Quality Gates

- [ ] Figures saved to `figures/` (not plt.show)
- [ ] Figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Numeric results saved as JSON/CSV in `results/`
- [ ] Report includes methods, results, and discussion
- [ ] All figure text is English-only
