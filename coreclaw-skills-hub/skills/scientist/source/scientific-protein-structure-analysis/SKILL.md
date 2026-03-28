---
name: scientific-protein-structure-analysis
description: |
 proteinstructureanalysisskill。PDB / AlphaFold DB / PDBe utilizing 3D structureanalysis。
 structure、binding、molecular docking、structureevaluation。
 ToolUniverse 's Protein Structure Retrieval and claude-scientific-skills 's 
 PDB/AlphaFold skill integration。
 「protein's structure analysis」「PDB structure」「」 。
tu_tools:
 - key: proteinsplus
 name: ProteinsPlus
 description: proteinbindingstructureanalysistoolgroup
---

# Scientific Protein Structure Analysis

protein 3D structure'sanalysisskill。PDB、AlphaFold DB、PDBe from
structureData Retrieval、structureevaluationbindinganalysis
to/untilexecutes。

## When to Use

- protein's 3D structureretrievalevaluationwhen needed
- AlphaFold predictionstructure's degree (pLDDT) verificationwhen needed
- bindingwhen needed
- structuremultiplestructurecomparisonwhen needed
- molecular docking's receptor is performedand
- ligandbindingformulaanalysiswhen needed

## Quick Start

### 1. structureanalysispipeline

```
Input: Target protein (UniProt ID / Gene Symbol / PDB ID)
 ↓
Step 1: Structure Search
 - PDB experimentstructuresearch（X-ray, Cryo-EM, NMR）
 - AlphaFold predictionstructureretrieval
 - structure'sselection
 ↓
Step 2: Quality Assessment
 - resolution / R-factor / Rfree
 - pLDDT (AlphaFold)
 - Ramachandran min
 ↓
Step 3: Structural Features
 - 
 - binding
 - 
 ↓
Step 4: Functional Analysis
 - ligandbindinganalysis
 - proteininteractioninterface
 - 
 ↓
Output: Structure Report + Prepared Files
```

---

## Phase 1: Structure Retrieval

### PDB structureretrievalpipeline

```python
import requests

def search_pdb_structures(uniprot_id):
 """
 UniProt ID from PDB structure search。
 RCSB PDB Search API v2 for。
 """
 query = {
 "query": {
 "type": "terminal",
 "service": "text",
 "parameters": {
 "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
 "operator": "exact_match",
 "value": uniprot_id,
 }
 },
 "return_type": "entry",
 "request_options": {
 "sort": [{"sort_by": "rcsb_accession_info.deposit_date", "direction": "desc"}],
 "results_content_type": ["experimental"],
 }
 }

 response = requests.post(
 "https://search.rcsb.org/rcsbsearch/v2/query",
 json=query
 )
 return response.json.get("result_set", [])


def get_alphafold_structure(uniprot_id):
 """
 AlphaFold DB frompredictionstructure retrieval。
 """
 url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
 response = requests.get(url)
 if response.status_code == 200:
 data = response.json[0]
 return {
 "pdb_url": data["pdbUrl"],
 "cif_url": data["cifUrl"],
 "pae_url": data.get("paeImageUrl"),
 "model_version": data.get("latestVersion"),
 }
 return None
```

### structureselectioncriteria

```markdown
## Structure Selection Priority

1. **X-ray crystallography** (Resolution < 2.5 Å) — Gold standard
2. **Cryo-EM** (Resolution < 3.5 Å) — Large complexes
3. **NMR** — Solution state dynamics
4. **AlphaFold** (pLDDT > 70) — No experimental structure available

### Selection Decision Tree
- Has PDB structure?
 - Yes → Resolution < 2.5 Å? → Use X-ray
 - Yes → Large complex? → Use Cryo-EM
 - No → AlphaFold pLDDT > 70? → Use AlphaFold
 - No → Homology model needed
```

---

## Phase 2: Quality Assessment

### structuremetrics

```python
def assess_structure_quality(pdb_id):
 """
 PDB structure's metricsretrieval。
 """
 url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
 response = requests.get(url)
 data = response.json

 quality = {
 "pdb_id": pdb_id,
 "method": data.get("exptl", [{}])[0].get("method"),
 "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0],
 "r_factor": data.get("refine", [{}])[0].get("ls_R_factor_R_work"),
 "r_free": data.get("refine", [{}])[0].get("ls_R_factor_R_free"),
 "deposit_date": data.get("rcsb_accession_info", {}).get("deposit_date"),
 }

 # 
 res = quality.get("resolution")
 if res:
 if res < 2.0:
 quality["quality_tier"] = "Excellent"
 elif res < 2.5:
 quality["quality_tier"] = "Good"
 elif res < 3.0:
 quality["quality_tier"] = "Moderate"
 else:
 quality["quality_tier"] = "Low"

 return quality
```

### AlphaFold degreeevaluation

```python
def assess_alphafold_confidence(pdb_file_path):
 """
 AlphaFold pLDDT 'sanalysis。
 B-factor pLDDT.
 """
 from Bio.PDB import PDBParser
 import numpy as np

 parser = PDBParser(QUIET=True)
 structure = parser.get_structure("af", pdb_file_path)

 plddt_scores = []
 for atom in structure.get_atoms:
 if atom.name == "CA":
 plddt_scores.append(atom.bfactor)

 plddt_array = np.array(plddt_scores)

 return {
 "mean_plddt": np.mean(plddt_array),
 "median_plddt": np.median(plddt_array),
 "pct_very_high": np.sum(plddt_array > 90) / len(plddt_array) * 100, # >90: very high
 "pct_confident": np.sum(plddt_array > 70) / len(plddt_array) * 100, # >70: confident
 "pct_low": np.sum(plddt_array < 50) / len(plddt_array) * 100, # <50: low/disordered
 "interpretation": {
 ">90": "Very high confidence (well modeled)",
 "70-90": "Confident (backbone reliable)",
 "50-70": "Low confidence (caution)",
 "<50": "Very low (likely disordered / use with care)",
 }
 }
```

---

## Phase 3: Binding Site Analysis

### 

```python
def detect_binding_sites(pdb_id):
 """
 PDBe Arpeggio / fpocket usingbinding。
 """
 # fpocket 's
 # fpocket Voronoi possible
 pocket_info = {
 "method": "fpocket / DoGSiteScorer",
 "pockets": [],
 }

 # PDBe Binding Sites API
 url = f"https://www.ebi.ac.uk/pdbe/api/pdb/entry/binding_sites/{pdb_id}"
 response = requests.get(url)
 if response.status_code == 200:
 data = response.json.get(pdb_id.lower, [])
 for site in data:
 pocket_info["pockets"].append({
 "site_id": site.get("site_id"),
 "details": site.get("details"),
 "residues": site.get("site_residues", []),
 })

 return pocket_info
```

---

## Report Template

```markdown
# Protein Structure Report: [PROTEIN NAME]

**UniProt**: [accession] | **Date**: [date]

## 1. Structure Summary
| Feature | Value |
|---------|-------|
| Best PDB | |
| Resolution | |
| Method | |
| AlphaFold available | |
| Mean pLDDT | |

## 2. Available Structures
| PDB ID | Method | Resolution | Ligands | Chains |
|--------|--------|------------|---------|--------|

## 3. Quality Assessment
### 3.1 Selected Structure
### 3.2 Ramachandran Statistics
### 3.3 AlphaFold Confidence Map

## 4. Domain Architecture
| Domain | Start | End | Pfam | Description |
|--------|-------|-----|------|-------------|

## 5. Binding Sites
| Site | Key Residues | Known Ligands | Druggability |
|------|-------------|---------------|-------------|

## 6. Structural Insights
### 6.1 Active Site
### 6.2 Allosteric Sites
### 6.3 PPI Interface

## 7. Files Generated
- [ ] Cleaned PDB (waters removed, single chain)
- [ ] AlphaFold structure
- [ ] Pocket analysis results
```

---

## Completeness Checklist

- [ ] PDB search: UniProt ID allexperimentstructureretrieval
- [ ] AlphaFold structure: predictionstructure's retrieval and pLDDT evaluation
- [ ] evaluation: Resolution / R-factor / pLDDT
- [ ] : InterPro / Pfam mapping
- [ ] binding: and also 1 'sdetailsanalysis
- [ ] ligand: crystalligand'slist

## Best Practices

1. **experimentstructure**: AlphaFold experimentstructure 's
2. **resolution < 2.5 Å selection**: for resolutionrequired
3. **pLDDT < 50 for**: 's possible
4. **multiplestructure'scomparison**: different
5. **ligandinformationutilizing**: crystalligandfrom pharmacophore 

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `results/structure_report.md` | structureanalysisreport（Markdown） | allanalysiscompletion |
| `results/structure_analysis.json` | structuredata（JSON） | evaluationcompletion |
| `results/binding_sites.json` | bindingdata（JSON） | analysiscompletion |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| UniProt | `UniProt_get_entry_by_accession` | protein entry retrieval |
| InterPro | `InterPro_get_protein_domains` | domain annotation |
| InterPro | `InterProScan_scan_sequence` | sequence domain scan |
| BindingDB | `BindingDB_get_ligands_by_uniprot` | ligandbindingdata |
| Proteins API | `proteins_api_get_features` | protein feature information |
| AlphaMissense | `AlphaMissense_get_protein_scores` | prediction |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-drug-target-profiling` | ← protein's structureanalysis |
| `scientific-bioinformatics` | ← sequenceinformation |
| `scientific-sequence-analysis` | ← amino acidsequenceanalysisresults |
| `scientific-protein-design` | → structure-based de novo proteindesign |
| `scientific-cheminformatics` | → bindinginformationmolecular docking use |
| `scientific-academic-writing` | → publishing research results |
