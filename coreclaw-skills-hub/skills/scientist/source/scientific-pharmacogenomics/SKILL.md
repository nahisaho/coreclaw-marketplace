---
name: scientific-pharmacogenomics
description: |
 pharmacogenomics (genome) analysisskill。PharmGKB/ClinPGx by/via
 gene-druginteraction、CPIC retrieval、Star classification、
 metabolismenzymetabletype (PM/IM/NM/RM/UM)、FDA genomebiomarker、
 amount、PGx reportgenerationintegration
 unitsdrugmethodsupportpipeline。
---

# Scientific Pharmacogenomics

genetype-baseddrugselectionforamount is supported
pharmacogenomicspipeline。CPIC/DPWG PharmGKB
FDA PGx biomarker's database andintegration。

## When to Use

- genetype-baseddrugselectionamountwhen needed
- CPIC/DPWG 's phylogenywhen needed
- Star classificationmetabolismenzymetabletype (PM/IM/NM/RM/UM) when needed
- FDA pharmacogenomicsbiomarker is verifiedand
- unitsdrugmethodreport is generatedand

---

## Quick Start

## 1. gene-druginteraction

```python
import pandas as pd
import json


def query_gene_drug_interactions(gene_symbol, data_source="PharmGKB"):
 """
 gene-druginteraction's 。

 key PGx gene:
 - CYP2D6:,, 
 - CYP2C19:,, 
 - CYP2C9:, 
 - CYP3A5: 
 - DPYD:, 
 - TPMT/NUDT15:, 6-MP
 - UGT1A1: 
 - SLCO1B1: 
 - HLA-B: (*57:01), (*15:02)
 - VKORC1: 
 """
 print(f" Querying {data_source} for gene: {gene_symbol}")

 # PharmGKB 's keyfield
 query_fields = {
 "gene": gene_symbol,
 "clinical_annotations": "Tier 1A-3",
 "drug_labels": "FDA/EMA/PMDA/HCSC",
 "guideline_annotations": "CPIC/DPWG/CPNDS",
 "variant_annotations": "Clinical significance",
 "pathway_annotations": "PK/PD pathways",
 }

 return query_fields


def get_cpic_guidelines(gene_symbol=None, drug_name=None):
 """
 CPIC 'sretrieval。

 CPIC Level:
 - Level A: change
 - Level A/B: change recommended
 - Level B: 
 - Level C: informationproviding
 - Level D: fordata
 """
 print(f" Querying CPIC guidelines:")
 if gene_symbol:
 print(f" Gene: {gene_symbol}")
 if drug_name:
 print(f" Drug: {drug_name}")

 return {"gene": gene_symbol, "drug": drug_name, "level": "pending"}
```

## 2. Star classificationtabletype

```python
import pandas as pd
import numpy as np


def star_allele_annotation(gene, genotype_variants):
 """
 Star classificationpipeline。

 PharmCAT (Pharmacogenomics Clinical Annotation Tool) 's
 Star → tabletypetransformation。

 Parameters:
 gene: gene (e.g., "CYP2D6")
 genotype_variants: {rsID: genotype} 
 """
 # CYP2D6 Star example
 cyp2d6_alleles = {
 "*1": {"function": "Normal", "activity_score": 1.0},
 "*2": {"function": "Normal", "activity_score": 1.0},
 "*3": {"function": "No function", "activity_score": 0.0},
 "*4": {"function": "No function", "activity_score": 0.0},
 "*5": {"function": "No function (gene deletion)", "activity_score": 0.0},
 "*6": {"function": "No function", "activity_score": 0.0},
 "*9": {"function": "Decreased", "activity_score": 0.5},
 "*10": {"function": "Decreased", "activity_score": 0.25},
 "*17": {"function": "Decreased", "activity_score": 0.5},
 "*41": {"function": "Decreased", "activity_score": 0.5},
 }

 print(f" Gene: {gene}")
 print(f" Variants provided: {len(genotype_variants)}")
 print(f" Reference: PharmCAT + PharmVar")

 return cyp2d6_alleles


def determine_metabolizer_phenotype(gene, diplotype, activity_scores):
 """
 Activity Score 's metabolismenzymetabletype。

 tabletypeclassification:
 - PM (Poor Metabolizer): AS = 0
 - IM (Intermediate Metabolizer): 0 < AS < 1.25
 - NM (Normal Metabolizer): 1.25 ≤ AS ≤ 2.25
 - RM (Rapid Metabolizer): 2.25 < AS ≤ 3.0 (CYP2C19 's)
 - UM (Ultra-rapid Metabolizer): AS > 3.0 or gene duplication
 """
 as1, as2 = activity_scores
 total_as = as1 + as2

 if total_as == 0:
 phenotype = "PM (Poor Metabolizer)"
 elif total_as < 1.25:
 phenotype = "IM (Intermediate Metabolizer)"
 elif total_as <= 2.25:
 phenotype = "NM (Normal Metabolizer)"
 elif total_as <= 3.0:
 phenotype = "RM (Rapid Metabolizer)"
 else:
 phenotype = "UM (Ultra-rapid Metabolizer)"

 print(f" Gene: {gene}")
 print(f" Diplotype: {diplotype}")
 print(f" Activity Score: {as1} + {as2} = {total_as}")
 print(f" Phenotype: {phenotype}")

 # CPIC amount
 if gene == "CYP2D6" and "PM" in phenotype:
 print(" ⚠ CPIC: (to 's transformation)")
 print(" ⚠ CPIC: → recommended")

 return {"gene": gene, "diplotype": diplotype,
 "activity_score": total_as, "phenotype": phenotype}
```

## 3. FDA PGx biomarker

```python
import pandas as pd


def query_fda_pgx_biomarkers(drug_name=None, gene_name=None,
 biomarker_type=None):
 """
 FDA pharmacogenomicsbiomarker's。

 FDA PGx Labeling Categories:
 - Required: testingrequired (e.g., HLA-B*57:01 for abacavir)
 - Recommended: testingrecommended
 - Actionable: PGx information
 - Informative: referenceinformation

 300+ 's gene-drug FDA label。
 """
 print(" Querying FDA Pharmacogenomic Biomarkers:")
 if drug_name:
 print(f" Drug: {drug_name}")
 if gene_name:
 print(f" Gene: {gene_name}")
 if biomarker_type:
 print(f" Type: {biomarker_type}")

 # FDA keybiomarkerexample
 key_biomarkers = [
 {"gene": "HLA-B*57:01", "drug": "Abacavir", "action": "Required",
 "recommendation": "HLA-B*57:01 → (reaction)"},
 {"gene": "CYP2C19", "drug": "Clopidogrel", "action": "Actionable",
 "recommendation": "PM → (ticagrelor/prasugrel)"},
 {"gene": "DPYD", "drug": "5-FU/Capecitabine", "action": "Recommended",
 "recommendation": "PM → foramount 50% amount or "},
 {"gene": "UGT1A1*28", "drug": "Irinotecan", "action": "Recommended",
 "recommendation": "TA7/TA7 → timesamountamount"},
 {"gene": "TPMT/NUDT15", "drug": "Azathioprine", "action": "Recommended",
 "recommendation": "PM → 10%foramount or "},
 ]

 return pd.DataFrame(key_biomarkers)


def pgx_dosing_recommendation(gene, phenotype, drug):
 """
 tabletype-based CPIC amountgeneration。
 """
 # CPIC amounttableexample (CYP2C19 × Clopidogrel)
 cpic_table = {
 ("CYP2C19", "UM", "Clopidogrel"): "standardforamount 75 mg/day",
 ("CYP2C19", "RM", "Clopidogrel"): "standardforamount 75 mg/day",
 ("CYP2C19", "NM", "Clopidogrel"): "standardforamount 75 mg/day",
 ("CYP2C19", "IM", "Clopidogrel"): "recommended (ticagrelor/prasugrel)",
 ("CYP2C19", "PM", "Clopidogrel"): "recommended (ticagrelor/prasugrel)",
 }

 key = (gene, phenotype.split(" ")[0], drug)
 recommendation = cpic_table.get(key, "information")

 result = {
 "gene": gene,
 "phenotype": phenotype,
 "drug": drug,
 "recommendation": recommendation,
 "source": "CPIC",
 "evidence_level": "Level A",
 }

 print(f" PGx Dosing Recommendation:")
 print(f" Gene: {gene} | Phenotype: {phenotype}")
 print(f" Drug: {drug}")
 print(f" Recommendation: {recommendation}")

 return result
```

## 4. PGx reportgeneration

```python
import json
import pandas as pd
from datetime import datetime


def generate_pgx_report(patient_results, output_file="results/pgx_report.json"):
 """
 PGx reportgeneration。

 information:
 - patientgenetype
 - Star → tabletypemapping
 - eachdrug's CPIC/DPWG 
 - FDA biomarker
 - 
 """
 import os
 os.makedirs(os.path.dirname(output_file), exist_ok=True)

 report = {
 "report_type": "Pharmacogenomics Report",
 "generated_at": datetime.now.isoformat,
 "patient_id": patient_results.get("patient_id", "anonymous"),
 "genes_tested": [],
 "actionable_findings": [],
 "drug_recommendations": [],
 }

 for gene_result in patient_results.get("gene_results", []):
 gene_entry = {
 "gene": gene_result["gene"],
 "diplotype": gene_result["diplotype"],
 "phenotype": gene_result["phenotype"],
 "activity_score": gene_result.get("activity_score"),
 }
 report["genes_tested"].append(gene_entry)

 # 'sextraction
 if "PM" in gene_result["phenotype"] or "UM" in gene_result["phenotype"]:
 report["actionable_findings"].append({
 "gene": gene_result["gene"],
 "phenotype": gene_result["phenotype"],
 "clinical_significance": "Actionable — amount/recommended",
 })

 with open(output_file, "w") as f:
 json.dump(report, f, ensure_ascii=False, indent=2)

 print(f" PGx Report generated: {output_file}")
 print(f" Genes tested: {len(report['genes_tested'])}")
 print(f" Actionable findings: {len(report['actionable_findings'])}")

 return report
```

## References

### Output Files

| File | Format |
|---|---|
| `results/pgx_report.json` | JSON |
| `results/gene_drug_interactions.csv` | CSV |
| `results/star_allele_calls.csv` | CSV |
| `results/dosing_recommendations.csv` | CSV |
| `figures/pgx_phenotype_summary.png` | PNG |

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
| `scientific-variant-interpretation` | ACMG/AMP |
| `scientific-pharmacovigilance` | all |
| `scientific-clinical-decision-support` | clinical decision support |
| `scientific-precision-oncology` | tumor PGx (OncoKB) |
| `scientific-population-genetics` | allele frequency |

### Dependencies

`pandas`, `numpy`, `json`
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
