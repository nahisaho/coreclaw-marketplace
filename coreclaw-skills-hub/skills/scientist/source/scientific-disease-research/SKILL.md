---
name: scientific-disease-research
description: |
 diseaseresearchskill。GWAS CatalogOrphanetOMIMHPODisGeNET integration、
 disease-geneanalysisdiseasediagnosissupporttabletype-typemapping
 evaluationsupport。
 「disease and gene's」「disease diagnosis」「GWAS results analysis」 。
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

| File | Format | Generation Timing |
|---|---|---|
| `results/disease_research_report.json` | diseaseresearchreport（JSON） | analysiscompletion |
| `results/disease_research_report.md` | diseaseresearchreport（Markdown） | reportgeneration |
| `results/gwas_significant_loci.json` | GWAS significant loci（JSON） | GWAS searchcompletion |

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

| Skill | Integration |
|---|---|
| `scientific-variant-interpretation` | → 's ACMG classification |
| `scientific-bioinformatics` | ← expressiondataeQTL analysis |
| `scientific-network-analysis` | ← diseasemodulePPI network |
| `scientific-meta-analysis` | ← GWAS |
| `scientific-precision-oncology` | → cancerdisease'sintegration |
| `scientific-deep-research` | ← diseaseliterature |
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
