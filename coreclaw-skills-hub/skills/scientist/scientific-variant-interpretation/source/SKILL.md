---
name: scientific-variant-interpretation
description: |
 Variant interpretation skill. ACMG/AMP variant classification, pathogenicity evidence aggregation, clinical significance assessment, and variant report generation.
tu_tools:
 - key: clinvar
 name: ClinVar
 description: database
---

# Scientific Variant Interpretation

gene'sskill。ACMG/AMP 
classification、by/viadrugprediction、cellvariant/mutation's 
/integrationexecutes。

## When to Use

- SNV/Indel 's ACMG criteriaclassificationwhen needed
- (PGx) by/viadrugprediction is performedand
- cancercellvariant/mutation's is performedand
- disease's is supportedand
- -tabletypecorrelation's is evaluatedand

## Quick Start

### pipeline

```
Input: Variant (HGVS notation / rsID / genomic coordinates)
 ↓
Step 1: Annotation
 - ClinVar significance
 - gnomAD frequency
 - InterVar ACMG automatedclassification
 ↓
Step 2: Population Frequency
 - gnomAD allele frequency
 - frequency
 - (AF < 0.01 or 0.001)
 ↓
Step 3: Functional Impact
 - CADD / REVEL / AlphaMissense 
 - savedegree (PhyloP, GERP++)
 - prediction (SpliceAI)
 ↓
Step 4: Clinical Evidence
 - ClinVar submissions
 - COSMIC (cellvariant/mutation)
 - Literature evidence (PubMed)
 ↓
Step 5: ACMG Classification
 - 28 criteria's phylogenyfor
 - 5 classification (P, LP, VUS, LB, B)
 ↓
Output: Variant Interpretation Report
```

---

## Phase 1: ACMG/AMP classification

### 28 criteria's phylogenyevaluation

```python
ACMG_CRITERIA = {
 # Pathogenic - Very Strong
 "PVS1": "Null variant (nonsense, frameshift, canonical splice) in LOF-intolerant gene",
 # Pathogenic - Strong
 "PS1": "Same amino acid change as established pathogenic variant",
 "PS2": "De novo (confirmed parentage) in patient with disease",
 "PS3": "Functional study shows damaging effect",
 "PS4": "Prevalence in affected >> controls (OR > 5)",
 # Pathogenic - Moderate
 "PM1": "In mutational hot spot or critical functional domain",
 "PM2": "Absent from controls (or extremely rare in gnomAD)",
 "PM3": "Detected in trans with pathogenic variant (recessive)",
 "PM4": "Protein length change (in-frame del/ins in non-repeat region)",
 "PM5": "Novel missense at same position as established pathogenic",
 "PM6": "Assumed de novo (parentage not confirmed)",
 # Pathogenic - Supporting
 "PP1": "Co-segregation with disease in multiple family members",
 "PP2": "Missense in gene with low rate of benign missense",
 "PP3": "Computational evidence supports deleterious effect",
 "PP4": "Patient phenotype highly specific for gene",
 "PP5": "Reputable source reports as pathogenic",
 # Benign - Stand-alone
 "BA1": "Allele frequency > 5% in any population",
 # Benign - Strong
 "BS1": "Allele frequency greater than expected for disorder",
 "BS2": "Observed in healthy adult (for early-onset/penetrant disorder)",
 "BS3": "Functional study shows no damaging effect",
 "BS4": "Lack of segregation in affected family members",
 # Benign - Supporting
 "BP1": "Missense in gene where only truncating cause disease",
 "BP2": "Observed in trans with pathogenic variant (dominant)",
 "BP3": "In-frame del/ins in repetitive region",
 "BP4": "Computational evidence suggests no impact",
 "BP5": "Variant found in case with alternate molecular basis",
 "BP6": "Reputable source reports as benign",
 "BP7": "Synonymous with no splicing impact predicted",
}

def classify_acmg(criteria_met):
 """
 for ACMG criteriafromclassification。
 Richards et al., Genetics in Medicine 2015
 """
 pathogenic_criteria = [c for c in criteria_met if c.startswith(("PVS", "PS", "PM", "PP"))]
 benign_criteria = [c for c in criteria_met if c.startswith(("BA", "BS", "BP"))]

 pvs = [c for c in pathogenic_criteria if c.startswith("PVS")]
 ps = [c for c in pathogenic_criteria if c.startswith("PS")]
 pm = [c for c in pathogenic_criteria if c.startswith("PM")]
 pp = [c for c in pathogenic_criteria if c.startswith("PP")]

 ba = [c for c in benign_criteria if c.startswith("BA")]
 bs = [c for c in benign_criteria if c.startswith("BS")]
 bp = [c for c in benign_criteria if c.startswith("BP")]

 # Pathogenic Rules
 if (len(pvs) >= 1 and (len(ps) >= 1 or len(pm) >= 2 or
 (len(pm) == 1 and len(pp) == 1) or len(pp) >= 2)):
 return "Pathogenic"
 if len(ps) >= 2:
 return "Pathogenic"

 # Likely Pathogenic
 if len(pvs) >= 1 and len(pm) == 1:
 return "Likely Pathogenic"
 if len(ps) >= 1 and (len(pm) >= 1 or len(pm) >= 2):
 return "Likely Pathogenic"

 # Benign
 if len(ba) >= 1:
 return "Benign"
 if len(bs) >= 2:
 return "Benign"

 # Likely Benign
 if len(bs) >= 1 and len(bp) >= 1:
 return "Likely Benign"
 if len(bp) >= 2:
 return "Likely Benign"

 return "Variant of Uncertain Significance (VUS)"
```

---

## Phase 2: (PGx)

### PharmGKB / CPIC 

```python
PGX_GENES = {
 "CYP2D6": {
 "drugs": ["codeine", "tramadol", "tamoxifen", "atomoxetine"],
 "phenotypes": ["Poor Metabolizer", "Intermediate", "Normal", "Ultrarapid"],
 },
 "CYP2C19": {
 "drugs": ["clopidogrel", "voriconazole", "escitalopram", "omeprazole"],
 "phenotypes": ["Poor Metabolizer", "Intermediate", "Normal", "Rapid", "Ultrarapid"],
 },
 "CYP2C9": {
 "drugs": ["warfarin", "phenytoin", "celecoxib"],
 "phenotypes": ["Poor Metabolizer", "Intermediate", "Normal"],
 },
 "DPYD": {
 "drugs": ["fluorouracil", "capecitabine"],
 "phenotypes": ["Poor Metabolizer", "Intermediate", "Normal"],
 },
 "TPMT": {
 "drugs": ["azathioprine", "mercaptopurine", "thioguanine"],
 "phenotypes": ["Poor Metabolizer", "Intermediate", "Normal"],
 },
 "HLA-B": {
 "variants": {"*57:01": "abacavir hypersensitivity", "*58:01": "allopurinol SJS/TEN"},
 },
}

def pgx_recommendation(gene, phenotype, drug):
 """
 CPIC -baseddrugforamountrecommended。
 """
 recommendations = {
 "avoid": "'s forrecommended",
 "reduce_dose": "standardforamount's 25-50% amount",
 "standard_dose": "standardforamount start",
 "increase_dose": "standardforamount min's possible、amount",
 }
 # 's recommended CPIC tablefromretrieval
 return recommendations
```

---

## Phase 3: cellvariant/mutation

### OncoKB / COSMIC 

```markdown
## Somatic Variant Interpretation

### Oncogenicity Classification
| Level | Description |
|-------|-------------|
| Oncogenic | Functionally validated driver |
| Likely Oncogenic | Strong computational/indirect evidence |
| VUS | Insufficient evidence |
| Likely Benign | Evidence against oncogenicity |
| Benign | Confirmed passenger |

### Therapeutic Actionability (OncoKB Levels)
| Level | Description |
|-------|-------------|
| 1 | FDA-approved, same tumor type |
| 2 | Standard care, different tumor type |
| 3A | Clinical evidence in same tumor type |
| 3B | Clinical evidence in different tumor type |
| 4 | Preclinical evidence |
| R1 | Resistance to approved therapy |
| R2 | Resistance to investigational therapy |
```

---

## Report Template

```markdown
# Variant Interpretation Report

**Variant**: [HGVS notation]
**Gene**: [gene symbol]
**Date**: [date]

## 1. Variant Summary
| Feature | Value |
|---------|-------|
| Genomic location | |
| Transcript | |
| Protein change | |
| Variant type | |

## 2. Population Frequency
| Database | Frequency | Population |
|----------|-----------|------------|

## 3. In Silico Predictions
| Tool | Score | Prediction |
|------|-------|------------|
| CADD | | |
| REVEL | | |
| AlphaMissense | | |
| SpliceAI | | |

## 4. Clinical Evidence
### 4.1 ClinVar
### 4.2 Literature
### 4.3 Functional Studies

## 5. ACMG Classification
| Criterion | Applied | Evidence |
|-----------|---------|----------|
**Final Classification**: [P/LP/VUS/LB/B]

## 6. Pharmacogenomic Implications
（）

## 7. Treatment Implications
（cancercellvariant/mutationcase）

## 8. Recommendations
```

---

## Completeness Checklist

- [ ] note: HGVS、rsID、genomecoordinates'snormalization
- [ ] frequency: gnomAD all + 
- [ ] In silico prediction: CADD + REVEL + and also 1 additiontool
- [ ] ClinVar: all'sverification
- [ ] ACMG classification: 28 criteria's phylogenyevaluation
- [ ] PGx: genecase CPIC reference

## Best Practices

1. **ACMG phylogeny**: all 28 criteria 1 itemsitemsevaluation、basis
2. **frequencyverification**: 's frequency
3. **research**: calculationpredictionthan also experiment
4. **ClinVar evaluationverification**: 3-4 's entry also high
5. **PGx CPIC verification**: Level A/B 's implementation

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `results/variant_report.md` | report（Markdown） | allanalysiscompletion |
| `results/variant_classification.json` | ACMG/AMP classificationdata（JSON） | classificationcompletion |
| `results/pgx_report.json` | report（JSON） | PGx evaluationcompletion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| ClinVar | `clinvar_search_variants` | 'sclassificationsearch |
| gnomAD | `gnomad_get_gene_constraints` | genemetrics（pLI / LOEUF） |
| ClinGen | `ClinGen_get_gene_validity` | gene-disease'sevaluation |
| AlphaMissense | `AlphaMissense_get_variant_score` | prediction |
| PharmGKB | `PharmGKB_search_variants` | search |
| CADD | `CADD_get_variant_score` | |
| MyVariant | `MyVariant_get_variant_annotation` | integrationannotation |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-bioinformatics` | ← genomedata |
| `scientific-sequence-analysis` | ← sequencesavedegreeinformation |
| `scientific-data-preprocessing` | ← data's preprocessingnormalization |
| `scientific-clinical-decision-support` | → results'sclinical decision support |
| `scientific-academic-writing` | → publishing research results |
| `scientific-pharmacogenomics` | ← Star metabolismtype |

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
