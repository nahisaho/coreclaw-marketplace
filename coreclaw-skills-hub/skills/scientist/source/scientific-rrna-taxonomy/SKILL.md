---
name: scientific-rrna-taxonomy
description: |
 rRNA classificationskill。SILVA SSU/LSU rRNA database
 Greengenes2 phylogenyclassificationMGnify genomeanalysisQIIME2 classification
 scikit-bio sequenceanalysisphylogenyclassificationpipeline。
---

# Scientific rRNA Taxonomy

SILVA / Greengenes2 / MGnify utilizing rRNA and
classificationannotationpipeline is provided。16S/18S/ITS
sequence's classification andphylogenyanalysis。

## When to Use

- 16S rRNA sequence's classification is performedand
- SILVA/Greengenes2 classificationtrainingwhen needed
- MGnify fromgenomeanalysisresults is retrievedand
- 18S/ITS classification is performedand
- ASV/OTU 's classificationwhen needed
- QIIME2 customclassificationpipeline is builtand

---

## Quick Start

## 1. SILVA rRNA retrieval

```python
import requests
import pandas as pd
from pathlib import Path
from io import StringIO

SILVA_BASE = "https://www.arb-silva.de/api"


def download_silva_reference(version="138.1", subunit="SSU",
 output_dir="references"):
 """
 SILVA rRNA sequence & classificationretrieval。

 Parameters:
 version: str — SILVA 
 subunit: str — "SSU" (16S/18S) or "LSU" (23S/28S)
 output_dir: str — output directory
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # SILVA FTP from NR99 sequenceretrieval
 base_url = f"https://www.arb-silva.de/fileadmin/silva_databases/release_{version}/Exports"
 fasta_url = f"{base_url}/SILVA_{version}_{subunit}Ref_NR99_tax_silva.fasta.gz"
 tax_url = f"{base_url}/taxonomy/tax_slv_{subunit.lower}_{version}.txt.gz"

 import urllib.request
 import gzip

 # sequence
 fasta_path = output_dir / f"silva_{version}_{subunit}_NR99.fasta.gz"
 if not fasta_path.exists:
 urllib.request.urlretrieve(fasta_url, str(fasta_path))
 print(f"Downloaded: {fasta_path}")

 # classification
 tax_path = output_dir / f"silva_{version}_{subunit}_taxonomy.txt.gz"
 if not tax_path.exists:
 urllib.request.urlretrieve(tax_url, str(tax_path))
 print(f"Downloaded: {tax_path}")

 # columns
 n_seqs = 0
 with gzip.open(str(fasta_path), "rt") as f:
 for line in f:
 if line.startswith(">"):
 n_seqs += 1

 print(f"SILVA {version} {subunit}: {n_seqs} reference sequences")
 return {"fasta": str(fasta_path), "taxonomy": str(tax_path), "n_seqs": n_seqs}
```

## 2. Greengenes2 classificationretrieval

```python
def download_greengenes2(version="2024.09", output_dir="references"):
 """
 Greengenes2 classificationphylogenysequenceretrieval。

 Parameters:
 version: str — GG2 
 output_dir: str — output directory
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 gg2_base = f"https://ftp.microbio.me/greengenes_release/{version}"
 files = {
 "taxonomy": f"{gg2_base}/taxonomy.tsv.gz",
 "backbone": f"{gg2_base}/gg2-backbone.nwk.gz",
 "seqs": f"{gg2_base}/gg2-seqs.fna.gz",
 }

 import urllib.request
 paths = {}
 for name, url in files.items:
 out_path = output_dir / f"gg2_{version}_{name}{Path(url).suffix}{Path(url).suffixes[-1] if len(Path(url).suffixes) > 1 else ''}"
 out_path = output_dir / Path(url).name
 if not out_path.exists:
 try:
 urllib.request.urlretrieve(url, str(out_path))
 print(f"Downloaded: {out_path}")
 except Exception as e:
 print(f"Warning: {name} download failed: {e}")
 paths[name] = str(out_path)

 print(f"Greengenes2 {version}: {len(paths)} files downloaded")
 return paths
```

## 3. MGnify genomeanalysisresultsretrieval

```python
MGNIFY_BASE = "https://www.ebi.ac.uk/metagenomics/api/v1"


def mgnify_study_search(query, biome=None, limit=25):
 """
 MGnify — genomeresearchsearch。

 Parameters:
 query: str — search query
 biome: str — (example: "root:Environmental:Aquatic")
 limit: int — maximum retrieval count

 TU: mgnify
 """
 params = {"search": query, "page_size": limit}
 if biome:
 params["lineage"] = biome

 resp = requests.get(f"{MGNIFY_BASE}/studies", params=params, timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for study in data.get("data", []):
 attrs = study.get("attributes", {})
 results.append({
 "study_id": study["id"],
 "name": attrs.get("study-name", ""),
 "abstract": attrs.get("study-abstract", "")[:200],
 "biome": attrs.get("biome-name", ""),
 "samples_count": attrs.get("samples-count", 0),
 })

 df = pd.DataFrame(results)
 print(f"MGnify: '{query}' → {len(df)} studies")
 return df


def mgnify_taxonomy(analysis_id):
 """
 MGnify — classificationannotationresultsretrieval。

 Parameters:
 analysis_id: str — MGnify analysis ID

 TU: mgnify
 """
 url = f"{MGNIFY_BASE}/analyses/{analysis_id}/taxonomy/ssu"
 resp = requests.get(url, params={"page_size": 100}, timeout=30)
 resp.raise_for_status
 data = resp.json

 taxa = []
 for entry in data.get("data", []):
 attrs = entry.get("attributes", {})
 taxa.append({
 "lineage": attrs.get("lineage", ""),
 "count": attrs.get("count", 0),
 "rank": attrs.get("hierarchy", {}).get("rank", ""),
 })

 df = pd.DataFrame(taxa)
 df = df.sort_values("count", ascending=False)
 print(f"MGnify taxonomy ({analysis_id}): {len(df)} taxa")
 return df
```

## 4. QIIME2 classificationpipeline

```python
def qiime2_classify_sklearn(sequences_path, reference_seqs, reference_tax,
 classifier_output="classifier.qza"):
 """
 QIIME2 scikit-learn classificationtraining & classification。

 Parameters:
 sequences_path: str — inputsequence (FASTA or QZA)
 reference_seqs: str — sequence
 reference_tax: str — classification
 classifier_output: str — classificationoutput path
 """
 import subprocess

 # 1) import
 subprocess.run([
 "qiime", "tools", "import",
 "--type", "FeatureData[Sequence]",
 "--input-path", reference_seqs,
 "--output-path", "ref-seqs.qza",
 ], check=True)

 subprocess.run([
 "qiime", "tools", "import",
 "--type", "FeatureData[Taxonomy]",
 "--input-format", "HeaderlessTSVTaxonomyFormat",
 "--input-path", reference_tax,
 "--output-path", "ref-taxonomy.qza",
 ], check=True)

 # 2) classificationtraining
 subprocess.run([
 "qiime", "feature-classifier", "fit-classifier-naive-bayes",
 "--i-reference-reads", "ref-seqs.qza",
 "--i-reference-taxonomy", "ref-taxonomy.qza",
 "--o-classifier", classifier_output,
 ], check=True)

 # 3) classification
 subprocess.run([
 "qiime", "feature-classifier", "classify-sklearn",
 "--i-classifier", classifier_output,
 "--i-reads", sequences_path,
 "--o-classification", "taxonomy.qza",
 ], check=True)

 print(f"QIIME2 classification complete: {classifier_output}")
 return "taxonomy.qza"
```

## 5. classificationanalysis

```python
import numpy as np


def taxonomy_consensus(classifications, confidence_threshold=0.8):
 """
 multipleclassification'sclassification。

 Parameters:
 classifications: dict — {method: DataFrame(feature_id, taxon, confidence)}
 confidence_threshold: float — degreethreshold
 """
 all_features = set
 for method_df in classifications.values:
 all_features.update(method_df["feature_id"].tolist)

 consensus = []
 for feat_id in all_features:
 taxa = {}
 for method, df in classifications.items:
 row = df[df["feature_id"] == feat_id]
 if len(row) > 0:
 taxa[method] = {
 "taxon": row.iloc[0]["taxon"],
 "confidence": row.iloc[0].get("confidence", 1.0),
 }

 # and 's
 if taxa:
 lineages = [t["taxon"] for t in taxa.values]
 confidences = [t["confidence"] for t in taxa.values]

 # mincomparison
 split_lineages = [l.split(";") for l in lineages]
 max_depth = max(len(sl) for sl in split_lineages)
 consensus_lineage = []

 for rank_idx in range(max_depth):
 rank_taxa = [sl[rank_idx] for sl in split_lineages
 if rank_idx < len(sl)]
 most_common = max(set(rank_taxa), key=rank_taxa.count)
 agreement = rank_taxa.count(most_common) / len(rank_taxa)

 if agreement >= confidence_threshold:
 consensus_lineage.append(most_common)
 else:
 break

 consensus.append({
 "feature_id": feat_id,
 "consensus_taxon": ";".join(consensus_lineage),
 "depth": len(consensus_lineage),
 "methods_agree": len(taxa),
 "mean_confidence": np.mean(confidences),
 })

 df = pd.DataFrame(consensus)
 print(f"Consensus: {len(df)} features, "
 f"mean depth={df['depth'].mean:.1f}")
 return df
```

## 6. rRNA classificationintegrationpipeline

```python
def rrna_taxonomy_pipeline(input_fasta, output_dir="results",
 silva_version="138.1", use_greengenes=True):
 """
 SILVA + Greengenes2 integration rRNA classificationpipeline。

 Parameters:
 input_fasta: str — input 16S rRNA sequence
 output_dir: str — output directory
 silva_version: str — SILVA 
 use_greengenes: bool — GG2 also for
 """
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) 
 silva_ref = download_silva_reference(
 version=silva_version, output_dir=str(output_dir / "refs")
 )

 refs = {"silva": silva_ref}
 if use_greengenes:
 gg2_ref = download_greengenes2(
 output_dir=str(output_dir / "refs")
 )
 refs["greengenes2"] = gg2_ref

 # 2) QIIME2 classification (SILVA)
 silva_taxonomy = qiime2_classify_sklearn(
 input_fasta,
 silva_ref["fasta"],
 silva_ref["taxonomy"],
 classifier_output=str(output_dir / "silva_classifier.qza"),
 )

 # 3) MGnify comparisonreference
 # (analysisdata MGnify retrieval)

 print(f"Pipeline complete: {len(refs)} references used")
 return refs
```

---

## Pipeline Integration

```
microbiome-metagenomics → rrna-taxonomy → phylogenetics
 (DADA2 ASV pipeline) (SILVA/GG2 classification) (ETE3 phylogeny)
 │ │ ↓
environmental-ecology ─────────┘ population-genetics
 (α/β ) │ (Fst/ADMIXTURE)
 ↓
 pathway-enrichment
 
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/taxonomy.csv` | classificationresults | → microbiome-metagenomics |
| `results/consensus.csv` | classification | → phylogenetics |
| `results/refs/` | SILVA/GG2 | — |
| `results/mgnify_taxonomy.csv` | MGnify classificationresults | → environmental-ecology |

### usepossibletool (ToolUniverse SMCP)

| Config Key | toolnumber/count | key |
|-----------|---------|---------|
| `mgnify` | 3+ | genomeresearchsearchclassificationfileannotation |
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
