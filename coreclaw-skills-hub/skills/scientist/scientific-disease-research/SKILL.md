---
name: scientific-disease-research
description: |
 Disease research skill. Disease ontology queries, phenotype-genotype associations, clinical feature extraction, and disease mechanism pathway analysis.
tu_tools:
 - key: disgenet
 name: DisGeNET
 description: disease-gene (GDA) database
---

# Scientific Disease Research

diseaseresearchforintegrated analysisskill。genomeanalysis（GWAS）、
diseasedatabase、tabletypecross-cuttingutilizing、
disease's anddiagnosissupport is performed。

## When to Use

- GWAS results's andgene-disease's
- disease's tabletypediagnosis
- (PRS) 's
- diseasenetworkanalysis
- HPO (Human Phenotype Ontology) 's tabletypeanalysis
- DisGeNET 'sgene-disease

## Quick Start

### diseaseresearchpipeline

```
Phase 1: Phenotype Characterization
 - HPO 's tabletype
 - OMIM / Orphanet disease
 - tabletypeclustering
 ↓
Phase 2: Genetic Association
 - GWAS Catalog search (EBI)
 - Significant loci (p < 5e-8)
 - LD  blockanalysis
 ↓
Phase 3: Gene-Disease Mapping
 - DisGeNET GDA 
 - OMIM Morbid Map reference
 - eQTL / sQTL annotation
 ↓
Phase 4: Rare Disease Diagnosis
 - Orphanet diseaselogreference
 - HPO-based differential diagnosis
 - ACMG variant classification
 ↓
Phase 5: Network & Pathway Analysis
 - diseasemodule (PPI network)
 - pathwayanalysis
 - diseaseanalysis
 ↓
Phase 6: Report Generation
 - diseaseresearchreport (JSON + Markdown)
 - gene-diseasetable
 - diagnosis
```

## Workflow

### 1. GWAS Catalog API

```python
import requests
import pandas as pd
import numpy as np

GWAS_API = "https://www.ebi.ac.uk/gwas/rest/api"

def search_gwas_associations(trait_keyword, p_threshold=5e-8):
 """GWAS Catalog shape's SNP search"""
 resp = requests.get(
 f"{GWAS_API}/efoTraits/search/findBySearchQuery",
 params={"searchString": trait_keyword}
 )
 traits = resp.json.get("_embedded", {}).get("efoTraits", [])

 all_assocs = []
 for trait in traits[:5]: # top 5 shape
 trait_uri = trait["_links"]["self"]["href"]
 assoc_resp = requests.get(
 f"{trait_uri}/associations",
 params={"size": 500}
 )
 for a in assoc_resp.json.get("_embedded", {}).get("associations", []):
 p_value = float(a.get("pvalue", 1))
 if p_value < p_threshold:
 for locus in a.get("loci", []):
 for gene in locus.get("authorReportedGenes", []):
 all_assocs.append({
 "trait": trait.get("trait", ""),
 "gene": gene.get("geneName", ""),
 "rsid": a.get("snpInteraction", False),
 "p_value": p_value,
 "or_beta": a.get("orPerCopyNum", ""),
 "risk_allele": "",
 "study": a.get("study", {}).get("publicationInfo", {}).get("title", ""),
 })

 df = pd.DataFrame(all_assocs).sort_values("p_value")
 print(f"GWAS associations for '{trait_keyword}': {len(df)}")
 return df

gwas_results = search_gwas_associations("type 2 diabetes")
```

### 2. DisGeNET gene-disease

```python
DISGENET_API = "https://www.disgenet.org/api"
DISGENET_KEY = "YOUR_API_KEY"

def query_disgenet_gda(gene_symbol, source="ALL"):
 """DisGeNET Gene-Disease Associations (GDA) retrieval"""
 headers = {"Authorization": f"Bearer {DISGENET_KEY}"}
 resp = requests.get(
 f"{DISGENET_API}/gda/gene/{gene_symbol}",
 headers=headers,
 params={"source": source, "format": "json"}
 )
 data = resp.json

 results = []
 for item in data:
 results.append({
 "gene": item.get("gene_symbol", ""),
 "disease": item.get("disease_name", ""),
 "disease_id": item.get("diseaseid", ""),
 "score": item.get("score", 0),
 "ei": item.get("ei", 0), # Evidence Index
 "el": item.get("el", ""), # Evidence Level
 "n_pmids": item.get("pmid_count", 0),
 "source": item.get("source", ""),
 })

 df = pd.DataFrame(results).sort_values("score", ascending=False)
 return df

# GDA Score :
# 0.0-0.3: Weak association
# 0.3-0.6: Moderate association
# 0.6-0.8: Strong association
# 0.8-1.0: Very strong / curated association
```

### 3. HPO (Human Phenotype Ontology) tabletypeanalysis

```python
HPO_API = "https://hpo.jax.org/api"

def phenotype_matching(hpo_terms):
 """HPO fromdisease"""

 # HPO term → disease mapping
 disease_scores = {}

 for hpo_id in hpo_terms:
 resp = requests.get(f"{HPO_API}/hpo/term/{hpo_id}/diseases")
 diseases = resp.json.get("diseases", [])

 for d in diseases:
 disease_name = d.get("diseaseName", "")
 disease_id = d.get("diseaseId", "")
 if disease_id not in disease_scores:
 disease_scores[disease_id] = {
 "name": disease_name,
 "matched_hpo": [],
 "total_hpo": d.get("numberOfAnnotations", 0),
 }
 disease_scores[disease_id]["matched_hpo"].append(hpo_id)

 # Jaccard-like 
 results = []
 for did, info in disease_scores.items:
 matched = len(info["matched_hpo"])
 total_query = len(hpo_terms)
 total_disease = info["total_hpo"]
 # Harmonic mean of precision and recall
 precision = matched / total_query if total_query > 0 else 0
 recall = matched / total_disease if total_disease > 0 else 0
 f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

 results.append({
 "disease_id": did,
 "disease_name": info["name"],
 "matched_hpo_count": matched,
 "total_disease_hpo": total_disease,
 "precision": round(precision, 3),
 "recall": round(recall, 3),
 "f1_score": round(f1, 3),
 })

 return pd.DataFrame(results).sort_values("f1_score", ascending=False)

# example: tabletype'sdiagnosis
patient_hpo = ["HP:0001250", "HP:0001249", "HP:0000252"] # seizures, ID, microcephaly
candidates = phenotype_matching(patient_hpo)
print("Top diagnostic candidates:")
print(candidates.head(10))
```

### 4. Orphanet diseasesearch

```python
ORPHANET_API = "https://api.orphacode.org"

def search_orphanet(query):
 """Orphanet diseasesearch"""
 resp = requests.get(
 f"{ORPHANET_API}/EN/ClinicalEntity/ApproximateName/{query}",
 headers={"apiKey": "YOUR_ORPHANET_KEY"}
 )
 data = resp.json

 results = []
 for item in data:
 results.append({
 "orpha_code": item.get("ORPHAcode", ""),
 "name": item.get("Preferred term", ""),
 "type": item.get("typology", ""),
 "prevalence": item.get("prevalence", ""),
 "inheritance": item.get("inheritance", ""),
 "age_of_onset": item.get("age_of_onset", ""),
 })

 return pd.DataFrame(results)


def get_disease_genes(orpha_code):
 """Orphanet diseasegeneretrieval"""
 resp = requests.get(
 f"{ORPHANET_API}/EN/ClinicalEntity/orphacode/{orpha_code}/Gene",
 headers={"apiKey": "YOUR_ORPHANET_KEY"}
 )
 data = resp.json
 genes = []
 for g in data.get("DisorderGeneAssociationList", []):
 gene_info = g.get("Gene", {})
 genes.append({
 "gene_symbol": gene_info.get("Symbol", ""),
 "gene_name": gene_info.get("Name", ""),
 "association_type": g.get("DisorderGeneAssociationType", {}).get("Name", ""),
 "status": g.get("DisorderGeneAssociationStatus", {}).get("Name", ""),
 })
 return pd.DataFrame(genes)
```

### 5. Polygenic Risk Score (PRS) 

```python
def calculate_prs(gwas_summary_stats, individual_genotypes):
 """
 Polygenic Risk Score (PRS) by C+T (Clumping + Thresholding)

 PRS = Σ (beta_i × genotype_i) for i in selected SNPs
 """
 # LD Clumping 
 clumped = gwas_summary_stats[gwas_summary_stats["p_value"] < 5e-8].copy

 # effect size's direction
 clumped["beta"] = np.where(
 clumped["effect_allele"] == clumped["risk_allele"],
 clumped["beta"],
 -clumped["beta"]
 )

 # PRS 
 prs_scores = []
 for sample_id, geno in individual_genotypes.groupby("sample_id"):
 merged = clumped.merge(geno, on="rsid", how="inner")
 prs = (merged["beta"] * merged["dosage"]).sum
 prs_scores.append({
 "sample_id": sample_id,
 "prs_raw": prs,
 "n_snps_used": len(merged),
 })

 prs_df = pd.DataFrame(prs_scores)

 # Z-score standardization
 prs_df["prs_zscore"] = (prs_df["prs_raw"] - prs_df["prs_raw"].mean) / prs_df["prs_raw"].std

 # 
 prs_df["percentile"] = prs_df["prs_zscore"].rank(pct=True) * 100

 return prs_df
```

### 6. diseaseresearchreportgeneration

```python
import json

def generate_disease_report(disease_name, gwas_df, gda_df, hpo_df,
 output_dir="results"):
 """diseaseresearchintegrationreport"""
 report = {
 "disease": disease_name,
 "analysis_date": pd.Timestamp.now.isoformat,
 "gwas_summary": {
 "total_associations": len(gwas_df),
 "genome_wide_significant": len(gwas_df[gwas_df["p_value"] < 5e-8]),
 "top_loci": gwas_df.nsmallest(10, "p_value").to_dict("records"),
 },
 "gene_disease_associations": {
 "total_genes": gda_df["gene"].nunique,
 "strong_associations": len(gda_df[gda_df["score"] >= 0.6]),
 "top_genes": gda_df.nlargest(10, "score").to_dict("records"),
 },
 "phenotype_network": {
 "hpo_terms_used": len(hpo_df) if hpo_df is not None else 0,
 },
 }

 with open(f"{output_dir}/disease_research_report.json", "w") as f:
 json.dump(report, f, indent=2, default=str)

 md = f"# Disease Research Report: {disease_name}\n\n"
 md += f"## GWAS Summary\n\n"
 md += f"- Genome-wide significant loci: {report['gwas_summary']['genome_wide_significant']}\n\n"
 md += "| Gene | p-value | OR/Beta | Study |\n|---|---|---|---|\n"
 for locus in report["gwas_summary"]["top_loci"]:
 md += f"| {locus.get('gene', '')} | {locus.get('p_value', '')} | {locus.get('or_beta', '')} | {locus.get('study', '')[:50]} |\n"
 md += f"\n## Gene-Disease Associations (DisGeNET)\n\n"
 md += f"- Strong associations (score≥0.6): {report['gene_disease_associations']['strong_associations']}\n\n"
 md += "| Gene | Disease | GDA Score | Evidence |\n|---|---|---|---|\n"
 for g in report["gene_disease_associations"]["top_genes"]:
 md += f"| {g.get('gene', '')} | {g.get('disease', '')} | {g.get('score', '')} | {g.get('n_pmids', '')} PMIDs |\n"

 with open(f"{output_dir}/disease_research_report.md", "w") as f:
 f.write(md)

 return report
```

---

## Best Practices

1. **GWAS significance level**: genomesignificance level p < 5×10⁻⁸ for
2. **LD **: SNP 's
3. **DisGeNET **: GDA score 0.6 above/more「」 and
4. **HPO 's degree**: HPO （example: HP:0000001）
5. **PRS 's limitations**: PRS 's prediction units's diagnosis limitations
6. **disease gene**: GWAS than WES/WGS + ACMG classificationeffective
7. **'s**: (Population Stratification) correction

## Completeness Checklist

- [ ] disease/shape's definition and HPO mapping
- [ ] GWAS Catalog searchsignificant loci 
- [ ] DisGeNET GDA retrieval
- [ ] Orphanet diseaseinformationreference
- [ ] HPO 's tabletype
- [ ] pathwaynetworkanalysis
- [ ] diseaseresearchreport（JSON + Markdown）generation

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/disease_research_report.json` | diseaseresearchreport（JSON） | analysiscompletion |
| `results/disease_research_report.md` | diseaseresearchreport（Markdown） | reportgeneration |
| `results/gwas_significant_loci.json` | GWAS significant loci（JSON） | GWAS searchcompletion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| OpenTargets | `OpenTargets_get_disease_id_description_by_name` | disease IDretrieval |
| OpenTargets | `OpenTargets_get_associated_targets_by_disease_efoId` | disease |
| EFO/OLS | `OSL_get_efo_id_by_disease_name` | EFO ID |
| HPO | `get_HPO_ID_by_phenotype` | tabletype→HPO mapping |
| Monarch | `Monarch_get_gene_diseases` | gene-disease |
| ClinVar | `clinvar_search_variants` | search |
| ClinicalTrials | `search_clinical_trials` | diseaseclinical trial |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-variant-interpretation` | → 's ACMG classification |
| `scientific-bioinformatics` | ← expressiondataeQTL analysis |
| `scientific-network-analysis` | ← diseasemodulePPI network |
| `scientific-meta-analysis` | ← GWAS |
| `scientific-precision-oncology` | → cancerdisease'sintegration |
| `scientific-deep-research` | ← diseaseliterature |

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
