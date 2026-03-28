---
name: scientific-structural-proteomics
description: |
 structureproteomicsintegrationskill。EMDB EM、PDBe structuredata、
 Proteins API (UniProt)、Complex Portal 、DeepGO prediction、
 EVE variant/mutationevaluation'sintegrationpipeline。
---

# Scientific Structural Proteomics

6 items's structuredatabase integration
proteinstructurepipeline is provided。

## When to Use

- PDB entry's detailsstructureinformation (resolution, experimentmethod, structure) is retrievedand
- EM information EMDB fromretrievalwhen needed
- UniProt protein'svariant/mutationgenomemapping is investigatedand
- protein's configuration Complex Portal and
- DeepGO sequence's GO prediction is performedand
- EVE missense variant/mutation's is retrievedand

---

## Quick Start

## 1. PDBe structureData Retrieval

```python
import requests
import pandas as pd

PDBE_API = "https://www.ebi.ac.uk/pdbe/api"


def get_pdbe_entry(pdb_id):
 """
 PDBe entry's summarystructureretrieval。

 Parameters:
 pdb_id: str — PDB ID (e.g., "1cbs")

 ToolUniverse:
 pdbe_get_entry_summary(pdb_id=pdb_id)
 pdbe_get_entry_quality(pdb_id=pdb_id)
 pdbe_get_entry_experiment(pdb_id=pdb_id)
 pdbe_get_entry_molecules(pdb_id=pdb_id)
 pdbe_get_entry_secondary_structure(pdb_id=pdb_id)
 pdbe_get_entry_assemblies(pdb_id=pdb_id)
 pdbe_get_entry_publications(pdb_id=pdb_id)
 """
 pdb = pdb_id.lower

 # Summary
 resp_s = requests.get(f"{PDBE_API}/pdb/entry/summary/{pdb}")
 resp_s.raise_for_status
 summary = resp_s.json.get(pdb, [{}])[0]

 # Quality
 resp_q = requests.get(f"{PDBE_API}/pdb/entry/quality/{pdb}")
 quality = (
 resp_q.json.get(pdb, [{}])[0] if resp_q.status_code == 200 else {}
 )

 # Experiment
 resp_e = requests.get(f"{PDBE_API}/pdb/entry/experiment/{pdb}")
 experiment = (
 resp_e.json.get(pdb, [{}])[0] if resp_e.status_code == 200 else {}
 )

 entry = {
 "pdb_id": pdb,
 "title": summary.get("title", ""),
 "method": experiment.get("experimental_method", ""),
 "resolution": experiment.get("resolution", ""),
 "release_date": summary.get("release_date", ""),
 "r_factor": quality.get("r_factor", ""),
 "r_free": quality.get("r_free", ""),
 }

 print(f"PDBe {pdb}: {entry['method']} @ {entry['resolution']}Å")
 return entry, summary, quality
```

## 2. EMDB EM structure

```python
EMDB_API = "https://www.ebi.ac.uk/emdb/api"


def get_emdb_structure(emdb_id):
 """
 EMDB entry's 3D EM informationretrieval。

 Parameters:
 emdb_id: str — EMDB ID (e.g., "EMD-1234")

 ToolUniverse:
 EMDB_get_structure(emdb_id=emdb_id)
 EMDB_get_map_info(emdb_id=emdb_id)
 EMDB_get_sample_info(emdb_id=emdb_id)
 EMDB_get_imaging_info(emdb_id=emdb_id)
 EMDB_get_validation(emdb_id=emdb_id)
 EMDB_get_publications(emdb_id=emdb_id)
 EMDB_search_structures(query=query)
 """
 url = f"{EMDB_API}/entry/{emdb_id}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 admin = data.get("admin", {})
 map_info = data.get("map", {})

 entry = {
 "emdb_id": emdb_id,
 "title": admin.get("title", ""),
 "resolution": map_info.get("resolution", {}).get("value", ""),
 "contour_level": map_info.get("contour_level", {}).get("value", ""),
 "deposition_date": admin.get("deposition_date", ""),
 }

 print(f"EMDB {emdb_id}: {entry['resolution']}Å resolution")
 return entry, data
```

## 3. Proteins API (UniProt) variant/mutation

```python
PROTEINS_API = "https://www.ebi.ac.uk/proteins/api"


def get_protein_features(uniprot_id):
 """
 Proteins API fromprotein'svariant/mutationinformationretrieval。

 Parameters:
 uniprot_id: str — UniProt accession (e.g., "P04637")

 ToolUniverse:
 proteins_api_get_protein(accession=uniprot_id)
 proteins_api_get_features(accession=uniprot_id)
 proteins_api_get_variants(accession=uniprot_id)
 proteins_api_get_xrefs(accession=uniprot_id)
 proteins_api_get_genome_mappings(accession=uniprot_id)
 """
 headers = {"Accept": "application/json"}

 # Protein info
 resp_p = requests.get(
 f"{PROTEINS_API}/proteins/{uniprot_id}", headers=headers
 )
 resp_p.raise_for_status
 protein = resp_p.json

 # Features
 resp_f = requests.get(
 f"{PROTEINS_API}/features/{uniprot_id}", headers=headers
 )
 features = resp_f.json if resp_f.status_code == 200 else {}

 feature_list = features.get("features", [])
 domains = [f for f in feature_list if f.get("type") == "DOMAIN"]
 variants = [f for f in feature_list if f.get("type") == "VARIANT"]

 print(f"Proteins API {uniprot_id}: "
 f"{len(domains)} domains, {len(variants)} variants")
 return protein, feature_list
```

## 4. Complex Portal 

```python
def get_complex_portal(complex_id):
 """
 Complex Portal fromprotein's detailsretrieval。

 Parameters:
 complex_id: str — Complex Portal ID (e.g., "CPX-1")

 ToolUniverse:
 ComplexPortal_get_complex(complex_id=complex_id)
 ComplexPortal_search_complexes(query=query)
 """
 url = (
 f"https://www.ebi.ac.uk/intact/complex-ws/complex/{complex_id}"
 )
 resp = requests.get(url, headers={"Accept": "application/json"})
 resp.raise_for_status
 data = resp.json

 participants = data.get("participants", [])
 subunits = []
 for p in participants:
 interactor = p.get("interactor", {})
 subunits.append({
 "identifier": interactor.get("identifier", ""),
 "name": interactor.get("name", ""),
 "stoichiometry": p.get("stoichiometry", ""),
 })

 print(f"Complex Portal {complex_id}: "
 f"{data.get('name', '?')}, {len(subunits)} subunits")
 return data, subunits
```

## 5. DeepGO prediction & EVE variant/mutationevaluation

```python
def predict_deepgo_function(sequence):
 """
 DeepGO proteinsequencefrom GO prediction。

 ToolUniverse:
 DeepGO_predict_function(sequence=sequence)
 """
 url = "https://deepgo.cbrc.kaust.edu.sa/deepgo/api/create"
 resp = requests.post(url, json={"data_format": "fasta", "data": sequence})
 resp.raise_for_status
 data = resp.json

 predictions = data.get("predictions", [])
 print(f"DeepGO: {len(predictions)} GO term predictions")
 return predictions


def get_eve_variant_score(gene_name, variant=None):
 """
 EVE (Evolutionary model of Variant Effect) by/via
 missense variant/mutation'sretrieval。

 ToolUniverse:
 EVE_get_gene_info(gene_name=gene_name)
 EVE_get_variant_score(gene_name=gene_name, variant=variant)
 """
 url = f"https://evemodel.org/api/proteins/{gene_name}"

 if variant:
 url += f"/variants/{variant}"

 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 if variant:
 score = data.get("eve_score", None)
 classification = data.get("eve_class", "")
 print(f"EVE {gene_name} {variant}: score={score}, class={classification}")
 else:
 print(f"EVE {gene_name}: found")

 return data
```

## References

### Output Files

| File | Format |
|---|---|
| `results/pdbe_entry.json` | JSON |
| `results/emdb_structure.json` | JSON |
| `results/protein_features.json` | JSON |
| `results/complex_portal.json` | JSON |
| `results/deepgo_predictions.json` | JSON |
| `results/eve_scores.json` | JSON |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| PDBe | `pdbe_get_entry_summary` | entrysummary |
| PDBe | `pdbe_get_entry_quality` | structure |
| PDBe | `pdbe_get_entry_experiment` | experimentmethod |
| PDBe | `pdbe_get_entry_molecules` | moleculeinformation |
| PDBe | `pdbe_get_entry_secondary_structure` | structure |
| PDBe | `pdbe_get_entry_assemblies` | |
| PDBe | `pdbe_get_entry_publications` | literature |
| PDBe | `pdbe_get_entry_related_publications` | literature |
| PDBe | `pdbe_get_entry_observed_residues_ratio` | observation |
| PDBe | `pdbe_get_entry_status` | |
| EMDB | `EMDB_get_structure` | EM structure |
| EMDB | `EMDB_get_map_info` | information |
| EMDB | `EMDB_get_sample_info` | information |
| EMDB | `EMDB_get_imaging_info` | |
| EMDB | `EMDB_get_validation` | |
| EMDB | `EMDB_get_publications` | literature |
| EMDB | `EMDB_search_structures` | EM structuresearch |
| Proteins API | `proteins_api_get_protein` | proteininformation |
| Proteins API | `proteins_api_get_features` | |
| Proteins API | `proteins_api_get_variants` | variant/mutation |
| Proteins API | `proteins_api_get_xrefs` | reference |
| Proteins API | `proteins_api_get_genome_mappings` | genomemapping |
| Proteins API | `proteins_api_get_epitopes` | |
| Proteins API | `proteins_api_get_proteomics` | proteomics |
| Proteins API | `proteins_api_get_publications` | literature |
| Proteins API | `proteins_api_get_comments` | |
| Proteins API | `proteins_api_search` | search |
| Complex Portal | `ComplexPortal_get_complex` | details |
| Complex Portal | `ComplexPortal_search_complexes` | search |
| DeepGO | `DeepGO_predict_function` | GO prediction |
| EVE | `EVE_get_gene_info` | geneinformation |
| EVE | `EVE_get_variant_score` | variant/mutation |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-protein-structure-analysis` | proteinstructure |
| `scientific-proteomics-mass-spectrometry` | proteomics |
| `scientific-protein-interaction-network` | PPI |
| `scientific-molecular-docking` | |
| `scientific-variant-interpretation` | variant/mutation |

### Dependencies

`requests`, `pandas`
