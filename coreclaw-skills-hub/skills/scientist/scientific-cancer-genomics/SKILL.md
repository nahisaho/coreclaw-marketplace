---
name: scientific-cancer-genomics
description: |
 Cancer genomics skill. Somatic mutation analysis, copy number variation, tumor mutational burden, microsatellite instability, driver gene identification, and oncological pathway analysis.
tu_tools:
 - key: cosmic
 name: COSMIC
 description: cancercellvariant/mutationlog
 - key: cbioportal
 name: cBioPortal
 description: cancer genomics
---

# Scientific Cancer Genomics

COSMIC / cBioPortal / DepMap 's 3 cancer genomicsintegration
cellvariant/mutationanalysispipeline is provided。

## When to Use

- cancergene'scellvariant/mutationlogsearchwhen needed
- cBioPortal cancertypecross-cutting's genevariant/mutationfrequency is investigatedand
- DepMap genedependency (essentiality) is evaluatedand
- variant/mutationanalysis (SBS/DBS/ID) is performedand
- number/count (CNA) 'sclassificationwhen needed

---

## Quick Start

## 1. COSMIC cellvariant/mutationsearch

```python
import pandas as pd
import numpy as np
import requests


def cosmic_search_mutations(gene, cancer_type=None, mutation_type=None):
 """
 COSMIC (Catalogue Of Somatic Mutations In Cancer) variant/mutationsearch。

 Parameters:
 gene: str — gene symbol (e.g., "BRAF", "TP53")
 cancer_type: str — cancertypefilter (e.g., "melanoma")
 mutation_type: str — variant/mutation ("missense", "nonsense", "frameshift")
 """
 # ToolUniverse : COSMIC_search_mutations, COSMIC_get_mutations_by_gene
 # COSMIC API necessary (Academic )

 # Cancer Gene Census (CGC) 
 cgc_genes = {
 "TP53": {"role": "TSG", "tier": 1},
 "BRAF": {"role": "oncogene", "tier": 1},
 "KRAS": {"role": "oncogene", "tier": 1},
 "EGFR": {"role": "oncogene", "tier": 1},
 "PIK3CA": {"role": "oncogene", "tier": 1},
 "BRCA1": {"role": "TSG", "tier": 1},
 "BRCA2": {"role": "TSG", "tier": 1},
 "ALK": {"role": "oncogene", "tier": 1},
 }

 gene_info = cgc_genes.get(gene.upper, {})

 result = {
 "gene": gene,
 "cgc_role": gene_info.get("role", "unknown"),
 "cgc_tier": gene_info.get("tier", None),
 "cancer_type_filter": cancer_type,
 "mutation_type_filter": mutation_type,
 }

 print(f"COSMIC query: {gene} "
 f"(CGC: {gene_info.get('role', 'N/A')}, "
 f"Tier {gene_info.get('tier', 'N/A')})")
 return result
```

## 2. cBioPortal cancer genomicsData Retrieval

```python
def cbioportal_query(genes, study_id=None, cancer_type=None,
 data_types=None):
 """
 cBioPortal REST API by/viacancer genomicsData Retrieval。

 Parameters:
 genes: list — gene symbol list
 study_id: str — cBioPortal research ID (e.g., "tcga_brca_pan_can_atlas_2018")
 cancer_type: str — cancertype (e.g., "Breast Cancer")
 data_types: list — ["mutations", "cna", "mrna", "methylation"]
 """
 base_url = "https://www.cbioportal.org/api"

 if data_types is None:
 data_types = ["mutations", "cna"]

 results = {}

 # researchlistretrieval
 if study_id is None:
 resp = requests.get(f"{base_url}/studies")
 studies = resp.json
 if cancer_type:
 studies = [s for s in studies
 if cancer_type.lower in
 s.get("cancerType", {}).get("name", "").lower]
 print(f"cBioPortal: {len(studies)} studies for '{cancer_type}'")
 results["studies"] = pd.DataFrame([{
 "study_id": s["studyId"],
 "name": s["name"],
 "cancer_type": s.get("cancerType", {}).get("name", ""),
 "sample_count": s.get("allSampleCount", 0),
 } for s in studies[:20]])
 else:
 # variant/mutationData Retrieval
 if "mutations" in data_types:
 url = f"{base_url}/molecular-profiles/{study_id}_mutations/mutations"
 params = {"projection": "DETAILED"}
 resp = requests.get(url, params=params)
 if resp.status_code == 200:
 mutations = resp.json
 mut_df = pd.DataFrame([{
 "gene": m.get("gene", {}).get("hugoGeneSymbol", ""),
 "mutation": m.get("proteinChange", ""),
 "mutation_type": m.get("mutationType", ""),
 "chromosome": m.get("chr", ""),
 "position": m.get("startPosition", ""),
 "allele_freq": m.get("tumorAltCount", 0) /
 max(m.get("tumorRefCount", 1) +
 m.get("tumorAltCount", 1), 1),
 } for m in mutations
 if m.get("gene", {}).get("hugoGeneSymbol", "") in genes])
 results["mutations"] = mut_df
 print(f" Mutations: {len(mut_df)} found in {genes}")

 return results
```

## 3. DepMap genedependencyanalysis

```python
def depmap_gene_dependency(genes, cell_lineage=None):
 """
 DepMap (Cancer Dependency Map) genedependencyanalysis。

 Parameters:
 genes: list — gene symbol list
 cell_lineage: str — cellphylogenyfilter (e.g., "Lung", "Breast")
 """
 # ToolUniverse :
 # DepMap_search_genes, DepMap_get_gene_dependencies
 # DepMap_get_cell_line, DepMap_get_cell_lines, DepMap_search_cell_lines

 # DepMap CRISPR (Chronos) dependency score:
 # negative = essential (dependency), ~0 = non-essential
 # Common Essential: mean < -0.5 across 90% of lines
 # Selective Dependency: mean < -0.5 in specific lineages

 results = []
 for gene in genes:
 result = {
 "gene": gene,
 "cell_lineage": cell_lineage,
 "query_type": "CRISPR_dependency",
 # 's ToolUniverse retrieval
 "interpretation": (
 "Chronos score < 0: gene essentiality increases. "
 "score < -0.5: likely essential in this lineage. "
 "score ~ 0: non-essential."
 ),
 }
 results.append(result)

 df = pd.DataFrame(results)
 print(f"DepMap: queried {len(genes)} genes "
 f"(lineage: {cell_lineage or 'pan-cancer'})")
 return df
```

## 4. variant/mutationanalysis

```python
def mutational_signature_analysis(mutations_df, genome="GRCh38",
 n_signatures=None):
 """
 cellvariant/mutationanalysis (COSMIC SBS signatures)。

 Parameters:
 mutations_df: DataFrame — columns: [chr, pos, ref, alt, sample]
 genome: str — referencegenome
 n_signatures: int — extractionnumber/count (None=automated)
 """
 from itertools import product

 # 96 
 bases = ["C", "T"]
 contexts = []
 for ref in bases:
 for alt in ["A", "C", "G", "T"]:
 if ref == alt:
 continue
 for five in "ACGT":
 for three in "ACGT":
 contexts.append(f"{five}[{ref}>{alt}]{three}")

 # and 'slogconstruction
 samples = mutations_df["sample"].unique
 catalog = pd.DataFrame(0, index=contexts, columns=samples)

 for _, row in mutations_df.iterrows:
 ref = row["ref"]
 alt = row["alt"]
 sample = row["sample"]
 context = row.get("trinucleotide_context", "N[N>N]N")
 if context in catalog.index:
 catalog.loc[context, sample] += 1

 print(f"Mutation catalog: {len(contexts)} contexts, "
 f"{len(samples)} samples, "
 f"{catalog.sum.sum:.0f} total mutations")

 # NMF degradation (SigProfilerExtractor )
 from sklearn.decomposition import NMF

 X = catalog.values.T # samples × contexts
 if n_signatures is None:
 n_signatures = min(5, len(samples))

 model = NMF(n_components=n_signatures, random_state=42, max_iter=1000)
 W = model.fit_transform(X) # exposure matrix
 H = model.components_ # signature profiles

 signatures = pd.DataFrame(H.T, index=contexts,
 columns=[f"SBS_{i+1}" for i in range(n_signatures)])
 exposures = pd.DataFrame(W, index=samples,
 columns=[f"SBS_{i+1}" for i in range(n_signatures)])

 print(f"Extracted {n_signatures} mutational signatures")
 return signatures, exposures
```

## References

### Output Files

| File | Format |
|---|---|
| `results/cosmic_mutations.csv` | CSV |
| `results/cbioportal_mutations.csv` | CSV |
| `results/depmap_dependencies.csv` | CSV |
| `results/mutation_signatures.csv` | CSV |
| `results/signature_exposures.csv` | CSV |
| `figures/mutation_spectrum.png` | PNG |
| `figures/signature_profiles.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| COSMIC | `COSMIC_search_mutations` | cellvariant/mutationsearch |
| COSMIC | `COSMIC_get_mutations_by_gene` | genevariant/mutationretrieval |
| cBioPortal | `cBioPortal_get_cancer_studies` | cancerresearchlist |
| cBioPortal | `cBioPortal_get_mutations` | variant/mutationData Retrieval |
| cBioPortal | `cBioPortal_get_molecular_profiles` | moleculefile |
| cBioPortal | `cBioPortal_get_patients` | patientData Retrieval |
| cBioPortal | `cBioPortal_get_sample_lists` | |
| cBioPortal | `cBioPortal_get_samples` | details |
| DepMap | `DepMap_get_gene_dependencies` | genedependency |
| DepMap | `DepMap_get_cell_line` | cellinformation |
| DepMap | `DepMap_get_cell_lines` | celllist |
| DepMap | `DepMap_search_cell_lines` | cellsearch |
| DepMap | `DepMap_search_genes` | genesearch |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-precision-oncology` | tumorfile → treatmentselection |
| `scientific-variant-interpretation` | |
| `scientific-variant-effect-prediction` | calculationprediction |
| `scientific-disease-research` | GWAS → cancer |
| `scientific-drug-target-profiling` | → dependency |

### Dependencies

`pandas`, `numpy`, `requests`, `scikit-learn`, `matplotlib`
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
