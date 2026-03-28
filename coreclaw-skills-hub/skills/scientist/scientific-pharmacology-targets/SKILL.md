---
name: scientific-pharmacology-targets
description: |
 Pharmacology targets skill. Target validation, druggability assessment, target prioritization scoring, and pharmacological target-disease mapping.
tu_tools:
 - key: bindingdb
 name: BindingDB
 description: bindingdatabase
 - key: gtopdb
 name: GtoPdb
 description: Guide to PHARMACOLOGY
 - key: brenda
 name: BRENDA
 description: enzymedatabase
---

# Scientific Pharmacology Targets

multiple'sdatabase (BindingDB, GPCRdb, GtoPdb, BRENDA, Pharos) 
integrationpipeline is provided。

## When to Use

- protein's knownligandbinding is investigatedand
- GPCR 's ligandvariant/mutationstructureinformation is retrievedand
- drug-interaction'sdatabasecross-cuttingsearch is performedand
- enzymeinhibitiondata (BRENDA) is investigatedand
- (Tdark/Tbio) 's druggability is evaluatedand

---

## Quick Start

## 1. BindingDB bindingData Retrieval

```python
import requests
import pandas as pd


def get_bindingdb_ligands(uniprot_id, cutoff=None):
 """
 BindingDB from UniProt ID 's ligandbindingData Retrieval。

 Parameters:
 uniprot_id: str — UniProt accession (e.g., "P00533")
 cutoff: float | None — affinity cutoff nM

 ToolUniverse:
 BindingDB_get_ligands_by_uniprot(uniprot_id=uniprot_id)
 BindingDB_get_targets_by_compound(smiles=smiles)
 """
 url = "https://bindingdb.org/axis2/services/BDBService"
 params = {
 "uniprot": uniprot_id,
 "response": "json",
 }
 if cutoff:
 params["cutoff"] = cutoff

 resp = requests.get(f"{url}/getLigandsByUniprot", params=params)
 resp.raise_for_status
 data = resp.json

 ligands = data.get("getLigandsByUniprotResponse", {}).get("affinities", [])
 results = []
 for lig in ligands:
 results.append({
 "monomer_id": lig.get("monomerid", ""),
 "smiles": lig.get("smiles", ""),
 "affinity_type": lig.get("affinity_type", ""),
 "affinity_value_nm": lig.get("affinity", ""),
 "source": lig.get("source", ""),
 })

 df = pd.DataFrame(results)
 print(f"BindingDB '{uniprot_id}': {len(df)} ligands")
 return df
```

## 2. GPCRdb GPCR 

```python
def get_gpcrdb_profile(protein_entry):
 """
 GPCRdb from GPCR 's ligandvariant/mutationstructureinformationretrieval。

 Parameters:
 protein_entry: str — GPCRdb entry name (e.g., "adrb2_human")

 ToolUniverse:
 GPCRdb_get_protein(entry_name=protein_entry)
 GPCRdb_get_ligands(entry_name=protein_entry)
 GPCRdb_get_mutations(entry_name=protein_entry)
 GPCRdb_get_structures(entry_name=protein_entry)
 GPCRdb_list_proteins
 """
 base = "https://gpcrdb.org/services"

 # Protein info
 resp_p = requests.get(f"{base}/protein/{protein_entry}/")
 resp_p.raise_for_status
 protein = resp_p.json

 # Ligands
 resp_l = requests.get(f"{base}/ligands/{protein_entry}/")
 ligands = resp_l.json if resp_l.status_code == 200 else []

 # Mutations
 resp_m = requests.get(f"{base}/mutants/{protein_entry}/")
 mutations = resp_m.json if resp_m.status_code == 200 else []

 # Structures
 resp_s = requests.get(f"{base}/structure/protein/{protein_entry}/")
 structures = resp_s.json if resp_s.status_code == 200 else []

 profile = {
 "entry_name": protein.get("entry_name", ""),
 "name": protein.get("name", ""),
 "family": protein.get("family", ""),
 "species": protein.get("species", ""),
 "num_ligands": len(ligands),
 "num_mutations": len(mutations),
 "num_structures": len(structures),
 }

 print(f"GPCRdb '{protein_entry}': "
 f"{profile['num_ligands']} ligands, "
 f"{profile['num_mutations']} mutations, "
 f"{profile['num_structures']} structures")
 return profile, ligands, mutations, structures
```

## 3. GtoPdb data

```python
def get_gtopdb_target_pharmacology(target_id):
 """
 Guide to PHARMACOLOGY (GtoPdb) from
 's interactionData Retrieval。

 ToolUniverse:
 GtoPdb_get_target(target_id=target_id)
 GtoPdb_get_target_interactions(target_id=target_id)
 GtoPdb_get_ligand(ligand_id=ligand_id)
 GtoPdb_search_interactions(query=query)
 """
 base = "https://www.guidetopharmacology.org/services"

 # Target info
 resp_t = requests.get(f"{base}/targets/{target_id}")
 resp_t.raise_for_status
 target = resp_t.json

 # Interactions
 resp_i = requests.get(f"{base}/targets/{target_id}/interactions")
 interactions = resp_i.json if resp_i.status_code == 200 else []

 results = []
 for ix in interactions:
 results.append({
 "ligand_id": ix.get("ligandId", ""),
 "ligand_name": ix.get("ligandName", ""),
 "type": ix.get("type", ""),
 "action": ix.get("action", ""),
 "affinity_type": ix.get("affinityType", ""),
 "affinity_median": ix.get("affinityMedian", ""),
 "approved": ix.get("approvedDrug", False),
 })

 df = pd.DataFrame(results)
 print(f"GtoPdb target {target_id} ({target.get('name', '')}): "
 f"{len(df)} interactions")
 return target, df
```

## 4. Pharos/TCRD search

```python
def search_pharos_targets(query, tdl=None):
 """
 Pharos / TCRD frominformationretrieval。
 Target Development Level (TDL) filterpossible。

 Parameters:
 query: str — gene symbol or target name
 tdl: str | None — "Tclin", "Tchem", "Tbio", "Tdark"

 ToolUniverse:
 Pharos_search_targets(q=query)
 Pharos_get_target(q=query)
 Pharos_get_tdl_summary
 Pharos_get_disease_targets(disease_name=disease_name)
 """
 url = "https://pharos-api.ncats.io/graphql"
 gql = """
 query TargetSearch($term: String!, $top: Int) {
 targets(filter: { term: $term }, top: $top) {
 targets {
 name
 sym
 uniprot { accession }
 tdl
 fam
 novelty
 jensenScore
 diseaseCount
 ligandCount
 }
 count
 }
 }
 """
 variables = {"term": query, "top": 20}
 resp = requests.post(url, json={"query": gql, "variables": variables})
 resp.raise_for_status
 data = resp.json["data"]["targets"]

 results = []
 for t in data["targets"]:
 results.append({
 "symbol": t.get("sym", ""),
 "name": t.get("name", ""),
 "uniprot": t.get("uniprot", {}).get("accession", ""),
 "tdl": t.get("tdl", ""),
 "family": t.get("fam", ""),
 "novelty": t.get("novelty", 0),
 "disease_count": t.get("diseaseCount", 0),
 "ligand_count": t.get("ligandCount", 0),
 })

 df = pd.DataFrame(results)
 if tdl:
 df = df[df["tdl"] == tdl]

 print(f"Pharos '{query}': {len(df)} targets"
 f"{f' (TDL={tdl})' if tdl else ''}")
 return df
```

## 5. integration

```python
def integrated_target_profile(uniprot_id, gene_symbol):
 """
 multipledatabase integrationfile。

 ToolUniverse (cross-cutting):
 BindingDB_get_ligands_by_uniprot(uniprot_id)
 Pharos_get_target(q=gene_symbol)
 GtoPdb_get_targets → GtoPdb_get_target_interactions
 """
 profile = {
 "uniprot_id": uniprot_id,
 "gene_symbol": gene_symbol,
 }

 # BindingDB ligands
 try:
 bdb_df = get_bindingdb_ligands(uniprot_id)
 profile["bindingdb_ligand_count"] = len(bdb_df)
 except Exception:
 profile["bindingdb_ligand_count"] = 0

 # Pharos TDL
 try:
 pharos_df = search_pharos_targets(gene_symbol)
 if not pharos_df.empty:
 row = pharos_df.iloc[0]
 profile["tdl"] = row.get("tdl", "")
 profile["novelty"] = row.get("novelty", 0)
 except Exception:
 profile["tdl"] = "Unknown"

 print(f"Integrated profile {gene_symbol}: TDL={profile.get('tdl', '?')}, "
 f"BindingDB={profile['bindingdb_ligand_count']} ligands")
 return profile
```

## References

### Output Files

| File | Format |
|---|---|
| `results/bindingdb_ligands.csv` | CSV |
| `results/gpcrdb_profile.json` | JSON |
| `results/gtopdb_interactions.csv` | CSV |
| `results/pharos_targets.csv` | CSV |
| `results/integrated_target_profile.json` | JSON |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| BindingDB | `BindingDB_get_ligands_by_uniprot` | UniProt→ligand |
| BindingDB | `BindingDB_get_ligands_by_uniprots` | batch |
| BindingDB | `BindingDB_get_ligands_by_pdb` | PDB→ligand |
| BindingDB | `BindingDB_get_targets_by_compound` | compound→ |
| GPCRdb | `GPCRdb_get_protein` | GPCR details |
| GPCRdb | `GPCRdb_get_ligands` | GPCR ligand |
| GPCRdb | `GPCRdb_get_mutations` | GPCR variant/mutation |
| GPCRdb | `GPCRdb_get_structures` | GPCR structure |
| GPCRdb | `GPCRdb_list_proteins` | GPCR list |
| GtoPdb | `GtoPdb_get_target` | information |
| GtoPdb | `GtoPdb_get_target_interactions` | interaction |
| GtoPdb | `GtoPdb_get_ligand` | ligandinformation |
| GtoPdb | `GtoPdb_get_targets` | list |
| GtoPdb | `GtoPdb_list_ligands` | ligandlist |
| GtoPdb | `GtoPdb_get_disease` | disease |
| GtoPdb | `GtoPdb_list_diseases` | diseaselist |
| GtoPdb | `GtoPdb_search_interactions` | interactionsearch |
| BRENDA | `BRENDA_get_inhibitors` | enzymeinhibition |
| Pharos | `Pharos_search_targets` | search |
| Pharos | `Pharos_get_target` | details |
| Pharos | `Pharos_get_tdl_summary` | TDL summary |
| Pharos | `Pharos_get_disease_targets` | disease→ |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-drug-target-interaction` | DTI prediction |
| `scientific-compound-similarity` | compound similarity |
| `scientific-compound-screening` | compound |
| `scientific-molecular-docking` | molecular docking |
| `scientific-protein-interaction-network` | PPI network |

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
