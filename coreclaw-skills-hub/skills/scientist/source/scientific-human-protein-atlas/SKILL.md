---
name: scientific-human-protein-atlas
description: |
 Human Protein Atlas (HPA) integrationskill。tissue/cellproteinexpression、
 cancerprognosisbiomarker、RNA expressionfile、cell、
 proteininteraction's searchanalysispipeline。
tu_tools:
 - key: hpa
 name: Human Protein Atlas
 description: tissue/cellproteinexpressionRNA expressioncancerprognosis
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

 ToolUniverse:
 HPA_get_gene_basic_info_by_ensembl_id(ensembl_id=ensembl_id)
 HPA_get_comprehensive_gene_details_by_ensembl_id(ensembl_id=ensembl_id)
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

 ToolUniverse:
 HPA_get_rna_expression_by_source(gene=gene_name, source="HPA")
 HPA_get_rna_expression_in_specific_tissues(gene=gene_name, tissues=tissues)
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

 ToolUniverse:
 HPA_get_cancer_prognostics_by_gene(gene=gene_name)
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

 ToolUniverse:
 HPA_get_subcellular_location(gene=gene_name)
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

 ToolUniverse:
 HPA_get_protein_interactions_by_gene(gene=gene_name)
 HPA_get_biological_processes_by_gene(gene=gene_name)
 HPA_get_contextual_biological_process_analysis(gene=gene_name)
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

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| HPA | `HPA_generic_search` | forsearch |
| HPA | `HPA_get_gene_basic_info_by_ensembl_id` | genebasicinformation |
| HPA | `HPA_get_comprehensive_gene_details_by_ensembl_id` | details |
| HPA | `HPA_get_rna_expression_by_source` | RNA expression |
| HPA | `HPA_get_rna_expression_in_specific_tissues` | tissueexpression |
| HPA | `HPA_get_cancer_prognostics_by_gene` | cancerprognosis |
| HPA | `HPA_get_subcellular_location` | cell |
| HPA | `HPA_get_protein_interactions_by_gene` | PPI |
| HPA | `HPA_get_biological_processes_by_gene` | process |
| HPA | `HPA_get_contextual_biological_process_analysis` | processanalysis |
| HPA | `HPA_get_disease_expression_by_gene_tissue_disease` | diseaseexpression |
| HPA | `HPA_get_comparative_expression_by_gene_and_cellline` | cellcomparison |
| HPA | `HPA_get_gene_tsv_data_by_ensembl_id` | TSV data |
| HPA | `HPA_search_genes_by_query` | genesearch |

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
