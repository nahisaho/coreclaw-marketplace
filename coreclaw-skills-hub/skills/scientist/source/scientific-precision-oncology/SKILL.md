---
name: scientific-precision-oncology
description: |
 tumorskill。CIViCOncoKBcBioPortalCOSMICGDC/TCGA integration、
 tumorgenomemoleculebiomarkerevaluationtreatmentrecommendedsupport。
 「cancergenomeanalysis」「tumor」「OncoKB search」 。
---

# Scientific Precision Oncology

tumor（Precision Oncology）forintegrated analysisskill。
tumorgenomedatabase（CIViC, OncoKB, cBioPortal, COSMIC, GDC/TCGA） 
cross-cuttingutilizing、molecule-basedtreatment's is supported。

## When to Use

- tumorcellvariant/mutation'sevaluation
- CIViC / OncoKB search
- cBioPortal / TCGA variant/mutationfrequencyanalysis
- biomarker'streatmentrecommended
- moleculetreatment'sintegration
- cancertypecross-cuttingvariant/mutationmin

## Quick Start

### tumorpipeline

```
Phase 1: Tumor Profiling
 - cellvariant/mutationCNVgene's
 - TMB (Tumor Mutational Burden) 
 - MSI (Microsatellite Instability) 
 ↓
Phase 2: Variant Annotation
 - CIViC GraphQL API 
 - OncoKB Annotation API
 - COSMIC / cBioPortal variant/mutationfrequency
 ↓
Phase 3: Actionability Assessment
 - OncoKB Evidence Level (1-4, R1-R2)
 - CIViC Evidence Rating (A-E)
 - AMP/ASCO/CAP Tiering (I-IV)
 ↓
Phase 4: Treatment Selection
 - molecule
 - formethod's
 - 'sevaluation
 ↓
Phase 5: Clinical Trial Matching
 - ClinicalTrials.gov API search
 - criteria's automated
 - biomarker's
 ↓
Phase 6: Molecular Tumor Board Report
 - integrationgenomereportgeneration
 - treatmentrecommendedsummary
 - table
```

## Workflow

### 1. CIViC (Clinical Interpretation of Variants in Cancer)

```python
import requests
import pandas as pd

# === CIViC GraphQL API ===
CIVIC_URL = "https://civicdb.org/api/graphql"

def query_civic_variant(gene, variant_name):
 """CIViC gene'ssearch"""
 query = """
 query($gene: String!) {
 genes(name: $gene) {
 nodes {
 name
 description
 variants {
 nodes {
 name
 variantTypes { name }
 evidenceItems {
 nodes {
 status
 evidenceType
 evidenceLevel
 evidenceDirection
 significance
 disease { name }
 therapies { name }
 source { citation }
 }
 }
 }
 }
 }
 }
 }
 """
 resp = requests.post(CIVIC_URL, json={"query": query, "variables": {"gene": gene}})
 data = resp.json["data"]["genes"]["nodes"]

 results = []
 for g in data:
 for v in g["variants"]["nodes"]:
 if variant_name.upper in v["name"].upper:
 for ev in v["evidenceItems"]["nodes"]:
 if ev["status"] == "accepted":
 results.append({
 "gene": g["name"],
 "variant": v["name"],
 "type": ev["evidenceType"],
 "level": ev["evidenceLevel"],
 "direction": ev["evidenceDirection"],
 "significance": ev["significance"],
 "disease": ev["disease"]["name"] if ev["disease"] else "",
 "therapies": ", ".join(t["name"] for t in ev["therapies"]),
 "citation": ev["source"]["citation"] if ev["source"] else "",
 })
 return pd.DataFrame(results)

civic_results = query_civic_variant("BRAF", "V600E")
print(f"CIViC evidence items: {len(civic_results)}")
print(civic_results[["gene", "variant", "level", "significance", "therapies"]].head(10))
```

### 2. OncoKB Annotation

```python
ONCOKB_URL = "https://www.oncokb.org/api/v1"
ONCOKB_TOKEN = "YOUR_ONCOKB_TOKEN" # oncokb.org retrieval

def annotate_oncokb(gene, variant, tumor_type=None):
 """OncoKB annotation"""
 headers = {"Authorization": f"Bearer {ONCOKB_TOKEN}"}

 # Variant annotation
 params = {"hugoSymbol": gene, "alteration": variant}
 if tumor_type:
 params["tumorType"] = tumor_type

 resp = requests.get(f"{ONCOKB_URL}/annotate/mutations/byHGVSg",
 headers=headers, params=params)
 data = resp.json

 return {
 "gene": gene,
 "variant": variant,
 "oncogenic": data.get("oncogenic", ""),
 "mutation_effect": data.get("mutationEffect", {}).get("knownEffect", ""),
 "highest_sensitive_level": data.get("highestSensitiveLevel", ""),
 "highest_resistance_level": data.get("highestResistanceLevel", ""),
 "treatments": [
 {
 "drugs": ", ".join(d["drugName"] for d in t.get("drugs", [])),
 "level": t.get("level", ""),
 "indication": t.get("levelAssociatedCancerType", {}).get("name", ""),
 }
 for t in data.get("treatments", [])
 ],
 }

# OncoKB Evidence Levels
ONCOKB_LEVELS = {
 "LEVEL_1": "FDA-recognized biomarker (same indication)",
 "LEVEL_2": "Standard care biomarker (same indication)",
 "LEVEL_3A": "Compelling clinical evidence (same indication)",
 "LEVEL_3B": "Standard care or compelling evidence (different indication)",
 "LEVEL_4": "Compelling biological evidence",
 "LEVEL_R1": "Standard care resistance biomarker",
 "LEVEL_R2": "Compelling clinical resistance evidence",
}
```

### 3. cBioPortal analysis

```python
CBIOPORTAL_URL = "https://www.cbioportal.org/api"

def query_cbioportal_mutations(gene, study_ids=None):
 """cBioPortal variant/mutationfrequencyretrieval"""
 if study_ids is None:
 # TCGA PanCancer Atlas studies
 resp = requests.get(f"{CBIOPORTAL_URL}/studies",
 params={"keyword": "tcga_pan_can_atlas"})
 study_ids = [s["studyId"] for s in resp.json]

 all_mutations = []
 for study_id in study_ids:
 # Get molecular profile
 profiles = requests.get(
 f"{CBIOPORTAL_URL}/molecular-profiles",
 params={"studyId": study_id}
 ).json

 mut_profiles = [p for p in profiles if p["molecularAlterationType"] == "MUTATION_EXTENDED"]
 if not mut_profiles:
 continue

 profile_id = mut_profiles[0]["molecularProfileId"]

 # Get mutations
 mutations = requests.get(
 f"{CBIOPORTAL_URL}/molecular-profiles/{profile_id}/mutations",
 params={"entrezGeneId": gene_to_entrez(gene)}
 ).json

 for m in mutations:
 all_mutations.append({
 "study": study_id,
 "sample_id": m.get("sampleId", ""),
 "protein_change": m.get("proteinChange", ""),
 "mutation_type": m.get("mutationType", ""),
 "variant_type": m.get("variantType", ""),
 })

 df = pd.DataFrame(all_mutations)

 # variant/mutationfrequency
 if not df.empty:
 freq = df["protein_change"].value_counts.head(20)
 print(f"Top mutations for {gene}:")
 print(freq)

 return df

def gene_to_entrez(gene_symbol):
 """Hugo symbol → Entrez ID transformation"""
 mapping = {"BRAF": 673, "EGFR": 1956, "KRAS": 3845, "TP53": 7157, "PIK3CA": 5290}
 return mapping.get(gene_symbol, 0)
```

### 4. TMB / MSI 

```python
def calculate_tmb(mutations_df, exome_size_mb=38.0):
 """
 Tumor Mutational Burden (TMB) 
 TMB = nonsynonymous mutations / exome size (Mb)
 """
 # Nonsynonymous 's
 nonsynonymous = mutations_df[
 mutations_df["mutation_type"].isin([
 "Missense_Mutation", "Nonsense_Mutation",
 "Frame_Shift_Del", "Frame_Shift_Ins",
 "In_Frame_Del", "In_Frame_Ins",
 "Splice_Site", "Translation_Start_Site",
 ])
 ]

 tmb = len(nonsynonymous) / exome_size_mb

 # TMB (FDA: ≥10 mut/Mb = TMB-High → Pembrolizumab)
 if tmb >= 20:
 category = "TMB-Very High"
 elif tmb >= 10:
 category = "TMB-High"
 elif tmb >= 5:
 category = "TMB-Intermediate"
 else:
 category = "TMB-Low"

 return {"tmb": round(tmb, 2), "category": category,
 "nonsynonymous_count": len(nonsynonymous)}


def assess_msi(microsatellite_loci_results):
 """
 MSI (Microsatellite Instability) 
 Bethesda Panel: BAT25, BAT26, D2S123, D5S346, D17S250
 """
 unstable_count = sum(1 for r in microsatellite_loci_results if r["status"] == "unstable")
 total = len(microsatellite_loci_results)

 if unstable_count >= 2:
 status = "MSI-H" # High
 elif unstable_count == 1:
 status = "MSI-L" # Low
 else:
 status = "MSS" # Stable

 return {"status": status, "unstable_loci": unstable_count, "total_loci": total}
```

### 5. moleculetumorreportgeneration

```python
import json

def generate_mtb_report(patient_id, variants, civic_data, oncokb_data,
 tmb_result, msi_result, output_dir="results"):
 """Molecular Tumor Board (MTB) reportgeneration"""
 report = {
 "patient_id": patient_id,
 "report_date": pd.Timestamp.now.isoformat,
 "genomic_profile": {
 "tmb": tmb_result,
 "msi": msi_result,
 "variants": variants,
 },
 "actionable_findings": [],
 "clinical_trials": [],
 }

 # Actionability integration
 for v in variants:
 finding = {
 "gene": v["gene"],
 "variant": v["variant"],
 "oncokb_level": oncokb_data.get(f"{v['gene']}_{v['variant']}", {}).get("highest_sensitive_level", ""),
 "civic_evidence": [],
 "therapies": [],
 }

 # CIViC integration
 civic_match = civic_data[
 (civic_data["gene"] == v["gene"]) &
 (civic_data["variant"].str.contains(v["variant"], case=False))
 ]
 for _, ev in civic_match.iterrows:
 finding["civic_evidence"].append({
 "level": ev["level"],
 "therapies": ev["therapies"],
 "significance": ev["significance"],
 })

 report["actionable_findings"].append(finding)

 # AMP/ASCO/CAP Tier classification
 for finding in report["actionable_findings"]:
 level = finding["oncokb_level"]
 if level in ["LEVEL_1", "LEVEL_2"]:
 finding["amp_tier"] = "Tier I (Strong clinical significance)"
 elif level in ["LEVEL_3A", "LEVEL_3B"]:
 finding["amp_tier"] = "Tier II (Potential clinical significance)"
 elif level == "LEVEL_4":
 finding["amp_tier"] = "Tier III (Unknown significance)"
 else:
 finding["amp_tier"] = "Tier IV (Benign/likely benign)"

 # JSON output
 with open(f"{output_dir}/mtb_report.json", "w") as f:
 json.dump(report, f, indent=2, default=str)

 # Markdown report
 md = f"# Molecular Tumor Board Report\n\n"
 md += f"**Patient**: {patient_id} | **Date**: {report['report_date']}\n\n"
 md += f"## Genomic Profile\n\n"
 md += f"| Metric | Result |\n|---|---|\n"
 md += f"| TMB | {tmb_result['tmb']} mut/Mb ({tmb_result['category']}) |\n"
 md += f"| MSI | {msi_result['status']} |\n\n"
 md += f"## Actionable Findings\n\n"
 md += "| Gene | Variant | OncoKB Level | AMP Tier | Therapies |\n|---|---|---|---|---|\n"
 for f_ in report["actionable_findings"]:
 therapies = "; ".join(set(
 e["therapies"] for e in f_["civic_evidence"] if e["therapies"]
 ))
 md += f"| {f_['gene']} | {f_['variant']} | {f_['oncokb_level']} | {f_['amp_tier']} | {therapies} |\n"

 with open(f"{output_dir}/mtb_report.md", "w") as f_out:
 f_out.write(md)

 return report
```

---

## Best Practices

1. **database**: CIViC + OncoKB + COSMIC 's
2. **cancertype**: samevariant/mutationalso cancertype than significance different
3. **'s**: Level 1 > 2 > 3A > 3B > 4 's
4. **variant/mutation**: 'sevaluation
5. **TMB/MSI immunemethod's**: TMB-High (≥10) → Pembrolizumab 
6. **VUS (Variant of Unknown Significance) 's**: predictiontool for

## Completeness Checklist

- [ ] cellvariant/mutation（SNV/Indel/CNV/Fusion）
- [ ] CIViC retrieval
- [ ] OncoKB annotationcompletion
- [ ] cBioPortal variant/mutationfrequencyverification
- [ ] TMB / MSI 
- [ ] AMP/ASCO/CAP Tier classification
- [ ] treatmentrecommendedsummary（molecule + immunemethod）
- [ ] clinical trial
- [ ] MTB report（JSON + Markdown）generation

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/mtb_report.json` | moleculetumorreport（JSON） | completion |
| `results/mtb_report.md` | MTB report（Markdown） | reportgeneration |
| `results/variant_actionability.json` | significance（JSON） | annotationcompletion |

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

| Skill | Integration |
|---|---|
| `scientific-variant-interpretation` | ← cellsystemvariant/mutation's ACMG classification |
| `scientific-clinical-decision-support` | → treatmentrecommended's clinical decision support |
| `scientific-bioinformatics` | ← RNA-seq expressiondataanalysis |
| `scientific-network-analysis` | ← analysisprediction |
| `scientific-drug-target-profiling` | ← druggabilityevaluation |
| `scientific-disease-research` | ← cancertype's background |
| `scientific-deep-research` | ← tumorlatestliterature |
| `scientific-pharmacogenomics` | ← PGx metabolismtypeamount |
---

## Harness Optimization (v0.5.0)

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
