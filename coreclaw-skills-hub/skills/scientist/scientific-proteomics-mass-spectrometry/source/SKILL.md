---
name: scientific-proteomics-mass-spectrometry
description: |
 Proteomics and mass spectrometry skill. MS data processing, peptide identification, protein quantification (LFQ/TMT/iTRAQ), and proteomics statistical analysis.
---

# Scientific Proteomics & Mass Spectrometry

LC-MS/MS 's proteomicsmass spectrometrydata、
spectrumpreprocessing→peptide/compound→amount→analysis's
Standard Pipeline is provided。

## When to Use

- LC-MS/MS proteomicsdata's peptideamountwhen needed
- TMT/SILAC/LFQ by/viaexpressionanalysis is performedand
- (phosphorylation, ubiquitination, ) mappingwhen needed
- spectrumlibrarysearchmolecule is performedand
- compound (HMDB/MassBank/GNPS) when needed

---

## Quick Start

## 1. MS datapreprocessing (pyOpenMS)

```python
import numpy as np
import pandas as pd


def ms_data_preprocessing(mzml_file, noise_threshold=1000,
 peak_picking_method="centroid"):
 """
 LC-MS/MS datapreprocessingpipeline (pyOpenMS )。

 1. Raw → mzML transformation ( msconvert)
 2. peak 
 3. correction
 4. 
 5. RT 
 """
 from pyopenms import MSExperiment, MzMLFile, PeakPickerHiRes

 # mzML load
 exp = MSExperiment
 MzMLFile.load(mzml_file, exp)

 print(f" Loaded {exp.getNrSpectra} spectra from {mzml_file}")
 print(f" MS1 scans: {sum(1 for s in exp if s.getMSLevel == 1)}")
 print(f" MS2 scans: {sum(1 for s in exp if s.getMSLevel == 2)}")

 # peak
 if peak_picking_method == "centroid":
 picker = PeakPickerHiRes
 exp_picked = MSExperiment
 picker.pickExperiment(exp, exp_picked)
 print(f" After peak picking: {exp_picked.getNrSpectra} spectra")
 return exp_picked

 return exp


def feature_detection(exp, mass_error_ppm=10, noise_threshold=1000):
 """
 LC-MS — m/z × RT × intensity's 3D peak。
 """
 from pyopenms import FeatureFinder, FeatureMap

 ff = FeatureFinder
 features = FeatureMap

 ff_params = ff.getParameters
 ff_params.setValue("mass_trace:mz_tolerance", float(mass_error_ppm))
 ff_params.setValue("noise_threshold_int", float(noise_threshold))
 ff.setParameters(ff_params)

 ff.run("centroided", exp, features, FeatureMap)

 print(f" Detected {features.size} features")

 results = []
 for f in features:
 results.append({
 "mz": f.getMZ,
 "rt": f.getRT,
 "intensity": f.getIntensity,
 "charge": f.getCharge,
 "quality": f.getOverallQuality,
 })

 return pd.DataFrame(results)
```

## 2. peptide (databasesearch)

```python
import numpy as np
import pandas as pd


def peptide_identification(mzml_file, fasta_db, enzyme="Trypsin",
 missed_cleavages=2, precursor_mass_tol=10,
 fragment_mass_tol=0.02, fdr_cutoff=0.01):
 """
 MS/MS spectrumfrom's peptidepipeline。

 1. databasesearch (X!Tandem / Comet / MSGF+)
 2. PSM (Peptide-Spectrum Match) 
 3. Target-Decoy FDR 
 4. Protein inference (Occam's Razor)
 """
 from pyopenms import (
 IdXMLFile, ProteinIdentification,
 PeptideIdentification
 )

 # searchparameters
 search_params = {
 "database": fasta_db,
 "enzyme": enzyme,
 "missed_cleavages": missed_cleavages,
 "precursor_mass_tolerance": f"{precursor_mass_tol} ppm",
 "fragment_mass_tolerance": f"{fragment_mass_tol} Da",
 "fixed_modifications": ["Carbamidomethyl (C)"],
 "variable_modifications": ["Oxidation (M)", "Acetyl (Protein N-term)"],
 }

 print(f" Database search parameters:")
 for k, v in search_params.items:
 print(f" {k}: {v}")

 # FDR 
 # Target-Decoy approach: concatenate reversed sequences
 print(f" FDR cutoff: {fdr_cutoff} (1% at PSM level)")
 print(f" Method: Target-Decoy competition (TDC)")

 return search_params


def protein_quantification(psm_results, method="LFQ",
 min_peptides=2, min_ratio_count=2):
 """
 amount。

 Methods:
 - LFQ (Label-Free Quantification): MS1 intensity
 - iBAQ (intensity-Based Absolute Quantification)
 - TMT (Tandem Mass Tag): Reporter ion intensity
 - SILAC: Heavy/Light rate
 """
 print(f" Quantification method: {method}")
 print(f" Minimum peptides per protein: {min_peptides}")

 if method == "LFQ":
 # MaxLFQ : peptiderate'smediannormalization
 print(" Normalization: MaxLFQ (median of peptide ratios)")
 print(" Missing value imputation: MinDet (minimum deterministic)")

 elif method == "TMT":
 print(" TMT channels: 126-134N (TMTpro 18-plex)")
 print(" Reporter ion extraction: ±10 ppm")
 print(" Normalization: Median centering → IRS (Internal Reference Scaling)")

 elif method == "SILAC":
 print(" Labels: Light (K0R0) vs Heavy (K8R10)")
 print(" Ratio calculation: median of peptide ratios")

 elif method == "iBAQ":
 print(" iBAQ = Σ(peptide intensities) / n_observable_peptides")

 return {"method": method, "min_peptides": min_peptides}
```

## 3. (PTM) analysis

```python
import pandas as pd
import numpy as np


def ptm_site_localization(psm_results, ptm_types=None,
 localization_prob_cutoff=0.75):
 """
 'sanalysis。

 key PTM :
 - Phosphorylation (S/T/Y): phosphorylation
 - Ubiquitination (K): ubiquitination (diGly remnant)
 - Acetylation (K): 
 - Methylation (K/R): methylation
 - Glycosylation (N/S/T): glycan
 - SUMOylation (K): SUMO 
 """
 ptm_types = ptm_types or ["Phospho (S)", "Phospho (T)", "Phospho (Y)"]

 print(f" PTM types analyzed: {ptm_types}")
 print(f" Localization probability cutoff: {localization_prob_cutoff}")
 print(" Methods: phosphoRS / Ascore / ptmRS")

 # PTM analysis (Motif-X / pLogo)
 print(" Motif enrichment: Motif-X algorithm")
 print(" Window: ±7 residues around modification site")
 print(" Significance: p < 1e-6 (binomial test)")

 return {"ptm_types": ptm_types, "cutoff": localization_prob_cutoff}


def phosphoproteomics_kinase_activity(phosphosites_df,
 kinase_substrate_db="PhosphoSitePlus"):
 """
 proteomicsfrom's activity (KSEA)。

 Kinase-Substrate Enrichment Analysis:
 - PhosphoSitePlus / NetworKIN 's-for
 - each's group'smean log2FC 
 - z-test significantevaluation
 """
 print(f" Kinase-substrate database: {kinase_substrate_db}")
 print(" Algorithm: KSEA (Kinase-Substrate Enrichment Analysis)")
 print(" Score: mean(log2FC of substrates) × sqrt(n_substrates)")

 return {"database": kinase_substrate_db, "method": "KSEA"}
```

## 4. spectrummolecule

```python
import numpy as np
import pandas as pd


def spectral_similarity_scoring(query_spectrum, library_spectrum,
 method="modified_cosine",
 mz_tolerance=0.02):
 """
 MS/MS spectrum's degree。

 Methods:
 - cosine: standarddegree
 - modified_cosine: amount
 - spec2vec: Word2Vec 's spectrum
 """
 from matchms import Spectrum, calculate_scores
 from matchms.similarity import ModifiedCosine, CosineGreedy

 if method == "modified_cosine":
 similarity_func = ModifiedCosine(tolerance=mz_tolerance)
 else:
 similarity_func = CosineGreedy(tolerance=mz_tolerance)

 score = similarity_func.pair(query_spectrum, library_spectrum)

 print(f" Similarity method: {method}")
 print(f" Score: {score['score']:.4f}")
 print(f" Matched peaks: {score['matches']}")

 return score


def molecular_networking(spectra_list, min_cosine=0.7,
 min_matched_peaks=6, max_neighbors=10):
 """
 GNPS molecule。

 spectrum's fixdegree networkconstruction。
 structure itemscompound shape → unknowncompound'sutilizing。
 """
 from matchms import calculate_scores
 from matchms.similarity import ModifiedCosine
 import networkx as nx

 sim_func = ModifiedCosine(tolerance=0.02)

 G = nx.Graph
 n = len(spectra_list)
 edge_count = 0

 for i in range(n):
 G.add_node(i)
 for j in range(i + 1, n):
 score = sim_func.pair(spectra_list[i], spectra_list[j])
 if (score["score"] >= min_cosine and
 score["matches"] >= min_matched_peaks):
 G.add_edge(i, j, weight=score["score"],
 matches=score["matches"])
 edge_count += 1

 print(f" Molecular network: {n} nodes, {edge_count} edges")
 print(f" Connected components: {nx.number_connected_components(G)}")
 print(f" Parameters: min_cosine={min_cosine}, min_matched={min_matched_peaks}")

 return G
```

## 5. expression + 

```python
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


def differential_protein_expression(intensity_matrix, groups,
 log2fc_cutoff=1.0, fdr_cutoff=0.05,
 imputation="MinDet"):
 """
 expressionanalysis。

 Parameters:
 intensity_matrix: proteins × samples (log2 LFQ intensity)
 groups: loop (e.g., ["Treatment", "Control",...])
 imputation: valuemethod (MinDet / MinProb / KNN / QRILC)
 """
 group_names = sorted(set(groups))
 g1, g2 = group_names[0], group_names[1]
 g1_idx = [i for i, g in enumerate(groups) if g == g1]
 g2_idx = [i for i, g in enumerate(groups) if g == g2]

 results = []
 for protein in intensity_matrix.index:
 vals1 = intensity_matrix.loc[protein, intensity_matrix.columns[g1_idx]].dropna
 vals2 = intensity_matrix.loc[protein, intensity_matrix.columns[g2_idx]].dropna

 if len(vals1) < 2 or len(vals2) < 2:
 continue

 log2fc = vals2.mean - vals1.mean
 stat, pval = ttest_ind(vals1, vals2, equal_var=False)

 results.append({
 "protein": protein,
 "log2FC": log2fc,
 "pvalue": pval,
 "mean_g1": vals1.mean,
 "mean_g2": vals2.mean,
 "n_g1": len(vals1),
 "n_g2": len(vals2),
 })

 df = pd.DataFrame(results)
 df["padj"] = multipletests(df["pvalue"], method="fdr_bh")[1]

 sig_up = df[(df["padj"] < fdr_cutoff) & (df["log2FC"] > log2fc_cutoff)]
 sig_down = df[(df["padj"] < fdr_cutoff) & (df["log2FC"] < -log2fc_cutoff)]

 print(f" {g2} vs {g1}:")
 print(f" Total proteins tested: {len(df)}")
 print(f" Significant UP: {len(sig_up)} (log2FC > {log2fc_cutoff}, FDR < {fdr_cutoff})")
 print(f" Significant DOWN: {len(sig_down)} (log2FC < -{log2fc_cutoff}, FDR < {fdr_cutoff})")

 return df
```

## References

### Output Files

| File | Format |
|---|---|
| `results/features_detected.csv` | CSV |
| `results/psm_results.csv` | CSV |
| `results/protein_quant.csv` | CSV |
| `results/ptm_sites.csv` | CSV |
| `results/differential_proteins.csv` | CSV |
| `results/molecular_network.graphml` | GraphML |
| `figures/volcano_proteomics.png` | PNG |
| `figures/molecular_network.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| PRIDE | `PRIDE_search_proteomics` | proteomicssearch |
| PRIDE | `PRIDE_get_project` | detailsretrieval |
| PRIDE | `PRIDE_get_project_files` | proteomicsdatafileretrieval |
| UniProt | `search_uniprot_by_name` | search |
| UniProt | `get_uniprot_entry` | entrydetails |
| KEGG | `kegg_get_pathway_info` | pathway information |
| Reactome | `reactome_pathway_analysis` | pathwayanalysis |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-metabolomics` | metabolite MS analysis |
| `scientific-spectral-signal` | spectrumanalysis |
| `scientific-bioinformatics` | sequencedatabase |
| `scientific-network-analysis` | moleculenetworkvisualization |
| `scientific-multi-omics` | multi-omics integration |

### Dependencies

`pyopenms`, `matchms`, `pandas`, `numpy`, `scipy`, `scikit-learn`, `networkx`, `statsmodels`
---

## Harness Optimization (v0.4.0)

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
