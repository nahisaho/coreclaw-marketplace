---
name: scientific-drug-target-profiling
description: |
 skill。ToolUniverse / Open Targets / ChEMBL / UniProt
 utilizing。druggabilityevaluation、all、
 -disease、pipelinemin integration。
 「evaluation」「druggability min」「protein」 。
tu_tools:
 - key: dgidb
 name: DGIdb
 description: drug-gene interactiondatabase
---

# Scientific Drug Target Profiling

'sskill。ToolUniverse（mims-harvard）'s 
Target Intelligence Gatherer 、9 items's
evaluates。

## When to Use

- 'sdruggability is evaluatedand
- protein'ssafety profile is verifiedand
- -disease's intensity amountwhen needed
- knownligand comprehensivewhen needed
- pipeline（'scompound） investigationwhen needed

## Quick Start

### 1. 9 

```
PATH 1: Identity Resolution
 Gene Symbol → UniProt → Ensembl → ChEMBL Target ID

PATH 2: Basic Protein Information
 UniProt Entry → Function, Localization, Domains

PATH 3: Structural Biology
 PDB Structures → AlphaFold → Binding Sites

PATH 4: Function & Pathways
 GO Terms → Reactome → KEGG → Pathway Context

PATH 5: Expression Profile
 GTEx → HPA → Tissue Specificity → Single-cell

PATH 6: Genetic Variation & Disease
 ClinVar → gnomAD → GWAS → Constraint Scores

PATH 7: Drug Interactions & Druggability
 ChEMBL Activities → DGIdb → Known Drugs → Probes

PATH 8: Literature & Research Landscape
 PubMed → OpenAlex → Publication Trends

PATH 9: Safety & Toxicology
 Essential Genes → Phenotypes → Off-target Risk
```

---

## Phase 1: Identity Resolution

### ID mapping

```python
def resolve_target_ids(query):
 """
 /Gene Symbol fromkey ID.
 """
 ids = {
 "query": query,
 "uniprot_accession": None, # e.g., P04637
 "ensembl_id": None, # e.g., ENSG00000141510
 "entrez_id": None, # e.g., 7157
 "chembl_target_id": None, # e.g., CHEMBL3927
 "hgnc_symbol": None, # e.g., TP53
 "open_targets_id": None, # = Ensembl ID
 }

 # Step 1: UniProt search（Gene Name → Accession）
 # Step 2: Ensembl ID retrieval（UniProt xref）
 # Step 3: ChEMBL Target ID（UniProt → ChEMBL mapping）
 # Step 4: Cross-validation（each DB verification）

 return ids
```

> **name's**: 's gene multipleorganism/species、
> UniProt taxonomy filter human (9606).

---

## Phase 2: Druggability Assessment

### druggability 3 axisevaluation

```
┌─────────────────────────────────────────┐
│ Druggability Matrix │
├─────────────┬───────────┬───────────────┤
│ Modality │ Metric │ Threshold │
├─────────────┼───────────┼───────────────┤
│ Small Mol │ Pocket? │ ≥1 druggable │
│ Antibody │ Surface? │ extracellular │
│ PROTAC │ E3 dist │ ≤30 Å │
│ ASO/siRNA │ mRNA expr │ detectable │
│ Gene Therapy│ LOF/GOF │ disease link │
└─────────────┴───────────┴───────────────┘
```

### Target Development Level (TDL) classification

```python
def classify_tdl(target_data):
 """
 Pharos TDL classificationclassification。
 Tclin: 
 Tchem: activation（ChEMBL）
 Tbio: 
 Tdark: information
 """
 if target_data.get("approved_drugs"):
 return "Tclin"
 elif target_data.get("chembl_activities_count", 0) > 0:
 potent = [a for a in target_data["activities"]
 if a.get("pchembl_value", 0) >= 6.0]
 if potent:
 return "Tchem"
 if target_data.get("go_annotations") or target_data.get("publications", 0) > 5:
 return "Tbio"
 return "Tdark"
```

---

## Phase 3: Safety Profiling

### allevaluation

```markdown
## Safety Assessment

### Genetic Constraint
- [ ] pLI score: ___ (>0.9 = highly constrained, LOF intolerant)
- [ ] LOEUF: ___ (<0.35 = constrained)
- [ ] Missense Z-score: ___ (>3.09 = missense-constrained)

### Essential Gene Analysis
- [ ] DepMap dependency score: ___ (<-0.5 = broadly essential)
- [ ] Mouse knockout phenotype: ___
- [ ] Lethal phenotype: ___ (YES/NO)

### Expression Breadth
- [ ] Tissue specificity index (tau): ___
- [ ] Ubiquitously expressed: ___ (risk for on-target toxicity)
- [ ] Brain/Heart/Liver expression: ___ (safety-critical organs)

### Off-target Risk
- [ ] Paralog count: ___
- [ ] Closest paralog similarity: ___ %
- [ ] Shared binding site features: ___
```

---

## Phase 4: Disease Association

### 

```python
EVIDENCE_TIERS = {
 "T1": "Genetic + Clinical (GWAS + ClinVar pathogenic)",
 "T2": "Strong biological (functional studies + animal models)",
 "T3": "Associative (expression correlation + network guilt-by-association)",
 "T4": "Computational prediction only",
}

def grade_disease_association(target_id, disease_id, evidence_sources):
 """
 -disease'sevaluation。
 Open Targets overall_association_score + addition T1-T4 。
 """
 score = evidence_sources.get("open_targets_score", 0)
 has_gwas = evidence_sources.get("gwas_significance", False)
 has_clinvar = evidence_sources.get("clinvar_pathogenic", False)
 has_functional = evidence_sources.get("functional_study", False)

 if has_gwas and has_clinvar:
 return "T1", score
 elif has_functional or score > 0.7:
 return "T2", score
 elif score > 0.3:
 return "T3", score
 else:
 return "T4", score
```

---

## Phase 5: Competitive Landscape

### pipelinemapping

```markdown
## Competitive Intelligence

### Known Drugs (Approved)
| Drug | Mechanism | Indication | Approval Year |
|------|-----------|------------|---------------|

### Clinical Pipeline
| Compound | Phase | Sponsor | Indication | NCT ID |
|----------|-------|---------|------------|--------|

### Chemical Probes
| Probe | Potency | Selectivity | Source |
|-------|---------|-------------|--------|

### Patent Landscape
| Patent Family | Assignee | Filing Date | Key Claims |
|---------------|----------|-------------|------------|
```

---

## Report Template

### report

```markdown
# Target Intelligence Report: [TARGET NAME]

**Generated**: [Date] | **Analyst**: SATORI Drug Target Profiling

## 1. Executive Summary
[2-3 sentences: target name, key disease links (with evidence tier), druggability verdict]

## 2. Target Identifiers
| Database | ID | Verified |
|----------|----|----------|
| UniProt | | ✓/✗ |
| Ensembl | | ✓/✗ |
| ChEMBL | | ✓/✗ |

## 3. Protein Biology
### 3.1 Function & Localization
### 3.2 Domain Architecture
### 3.3 Pathway Context

## 4. Structural Biology
### 4.1 Experimental Structures (PDB)
### 4.2 AlphaFold Prediction
### 4.3 Binding Sites & Pockets

## 5. Expression Profile
### 5.1 Tissue Expression (GTEx/HPA)
### 5.2 Disease-specific Expression

## 6. Disease Associations
[Table with evidence tiers T1-T4]

## 7. Druggability Assessment
### 7.1 TDL Classification
### 7.2 Modality Assessment
### 7.3 Tractability Score

## 8. Known Ligands & Drugs
### 8.1 Approved Drugs
### 8.2 Clinical Candidates
### 8.3 Chemical Probes & Tool Compounds

## 9. Safety Profile
### 9.1 Genetic Constraint
### 9.2 Essential Gene Status
### 9.3 Off-target Risk

## 10. Competitive Landscape

## 11. Recommendations
### 11.1 Go/No-Go Assessment
### 11.2 Suggested Modality
### 11.3 Key Experiments Needed

## 12. Data Sources & Methodology
```

---

## Completeness Checklist

### requireditem

- [ ] ID Resolution: UniProt, Ensembl, ChEMBL, HGNC 's 4ID verification
- [ ] Druggability: TDL classification + and also 2 'sevaluation
- [ ] Safety: pLI + LOEUF + DepMap 's 3 
- [ ] Disease: top 5 disease's T1-T4 
- [ ] Literature: keypaper ≥3 itemscitation
- [ ] Competitive: and Ph3 

## Best Practices

1. **ID Cross-validate**: UniProt and Ensembl 's directionmappingverification
2. **name**: Gene Symbol 's taxonomy filter 
3. **Evidence Tier **: 's disease T1-T4 
4. **allverification**: Essential gene case Go/No-Go 
5. **structureinformation**: PDB experimentstructure > AlphaFold prediction > Homology model

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/target_profile_report.md` | filereport（Markdown） | allanalysiscompletion |
| `results/target_profile.json` | structurefiledata（JSON） | allanalysiscompletion |
| `results/druggability_matrix.json` | druggability（JSON） | Druggability evaluationcompletion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| UniProt | `UniProt_get_entry_by_accession` | protein entry retrieval |
| UniProt | `UniProt_get_function_by_accession` | proteininformation |
| ChEMBL | `ChEMBL_get_target` | informationretrieval |
| ChEMBL | `ChEMBL_get_target_activities` | activitydata |
| OpenTargets | `OpenTargets_get_associated_targets_by_disease_efoId` | disease- |
| DGIdb | `DGIdb_get_gene_druggability` | druggabilityevaluation |
| DGIdb | `DGIdb_get_drug_gene_interactions` | drug-gene interaction |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-hypothesis-pipeline` | ← hypothesisdefinitionfromto 'sinput |
| `scientific-deep-research` | ← literatureinvestigation |
| `scientific-bioinformatics` | ← genomeproteomedataproviding |
| `scientific-network-analysis` | ← PPI networkpathway information |
| `scientific-admet-pharmacokinetics` | → for/againstcompound's ADMET evaluation |
| `scientific-protein-structure-analysis` | → protein'sstructureanalysis |
| `scientific-drug-repurposing` | → 's |
| `scientific-academic-writing` | → publishing research results |
