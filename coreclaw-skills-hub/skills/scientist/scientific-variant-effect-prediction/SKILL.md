---
name: scientific-variant-effect-prediction
description: |
 Variant effect prediction skill. CADD/REVEL/AlphaMissense scoring, splice variant prediction, regulatory variant impact, and variant pathogenicity classification.
tu_tools:
 - key: spliceai
 name: SpliceAI
 description: prediction
 - key: cadd
 name: CADD
 description: integrationannotationdependency
---

# Scientific Variant Effect Prediction

AlphaMissense / CADD / SpliceAI 's 3 calculationpredictiontool integration
evaluationpipeline is provided。

## When to Use

- 'scalculationpredictionwhen needed
- CADD allgenome's degree is evaluatedand
- SpliceAI predictionwhen needed
- multiplepredictiontool's is computedand
- WGS/WES 'swhen needed

---

## Quick Start

## 1. AlphaMissense prediction

```python
import pandas as pd
import numpy as np
import requests


def alphamissense_predict(variants, uniprot_id=None):
 """
 AlphaMissense proteinstructureprediction。

 Parameters:
 variants: list[dict] — [{"protein": "P12345", "position": 42, "ref": "A", "alt": "V"}]
 uniprot_id: str — proteinall'sretrieval
 """
 results = []

 if uniprot_id:
 # proteinall'sretrieval
 # AlphaMissense calculationproviding
 print(f"Fetching AlphaMissense scores for {uniprot_id}...")
 # ToolUniverse : AlphaMissense_get_protein_scores
 # or AlphaMissense_get_residue_scores

 for var in variants:
 protein = var.get("protein", uniprot_id)
 pos = var["position"]
 ref_aa = var.get("ref", "")
 alt_aa = var.get("alt", "")

 # classificationthreshold (DeepMind recommended)
 # pathogenic: score > 0.564
 # benign: score < 0.340
 # ambiguous: 0.340 - 0.564
 score = var.get("score", np.nan)

 if not np.isnan(score):
 if score > 0.564:
 classification = "likely_pathogenic"
 elif score < 0.340:
 classification = "likely_benign"
 else:
 classification = "ambiguous"
 else:
 classification = "unknown"

 results.append({
 "protein": protein,
 "position": pos,
 "ref_aa": ref_aa,
 "alt_aa": alt_aa,
 "am_score": score,
 "am_class": classification,
 "variant": f"{ref_aa}{pos}{alt_aa}",
 })

 df = pd.DataFrame(results)
 print(f"AlphaMissense: {len(df)} variants scored")
 return df
```

## 2. CADD retrieval

```python
def cadd_score_variants(variants, genome="GRCh38", version="v1.7"):
 """
 CADD (Combined Annotation Dependent Depletion) retrieval。

 Parameters:
 variants: list[dict] — [{"chr": "1", "pos": 12345, "ref": "A", "alt": "G"}]
 genome: "GRCh37" or "GRCh38"
 version: CADD 
 """
 base_url = f"https://cadd.gs.washington.edu/api/{version}"

 results = []
 for var in variants:
 chrom = str(var["chr"]).replace("chr", "")
 pos = var["pos"]
 ref = var["ref"]
 alt = var["alt"]

 # CADD API 
 # ToolUniverse : CADD_get_variant_score
 url = f"{base_url}/{genome}/{chrom}:{pos}"
 try:
 resp = requests.get(url, timeout=30)
 if resp.status_code == 200:
 data = resp.json
 for hit in data:
 if hit.get("Ref") == ref and hit.get("Alt") == alt:
 raw = hit.get("RawScore", np.nan)
 phred = hit.get("PHRED", np.nan)
 break
 else:
 raw, phred = np.nan, np.nan
 else:
 raw, phred = np.nan, np.nan
 except Exception:
 raw, phred = np.nan, np.nan

 # CADD PHRED threshold
 # >= 20: top 1% deleterious
 # >= 30: top 0.1% deleterious
 if phred >= 30:
 cadd_class = "highly_deleterious"
 elif phred >= 20:
 cadd_class = "deleterious"
 elif phred >= 10:
 cadd_class = "moderate"
 else:
 cadd_class = "benign"

 results.append({
 "chr": chrom, "pos": pos, "ref": ref, "alt": alt,
 "cadd_raw": raw,
 "cadd_phred": phred,
 "cadd_class": cadd_class,
 "variant": f"chr{chrom}:{pos}{ref}>{alt}",
 })

 df = pd.DataFrame(results)
 print(f"CADD: {len(df)} variants scored, "
 f"{(df['cadd_phred'] >= 20).sum} deleterious (PHRED≥20)")
 return df
```

## 3. SpliceAI prediction

```python
def spliceai_predict(variants, genome="GRCh38",
 delta_threshold=0.2):
 """
 SpliceAI prediction。

 Parameters:
 variants: list[dict] — [{"chr": "1", "pos": 12345, "ref": "A", "alt": "G"}]
 delta_threshold: float — Δthreshold
 0.2: high recall, 0.5: recommended, 0.8: high precision
 """
 results = []

 for var in variants:
 chrom = str(var["chr"]).replace("chr", "")
 pos = var["pos"]
 ref = var["ref"]
 alt = var["alt"]

 # ToolUniverse : SpliceAI_predict_splice
 # SpliceAI 4 items's Δoutput:
 # DS_AG: acceptor gain, DS_AL: acceptor loss
 # DS_DG: donor gain, DS_DL: donor loss
 ds_ag = var.get("ds_ag", 0)
 ds_al = var.get("ds_al", 0)
 ds_dg = var.get("ds_dg", 0)
 ds_dl = var.get("ds_dl", 0)

 max_delta = max(ds_ag, ds_al, ds_dg, ds_dl)

 if max_delta >= 0.8:
 splice_class = "high_impact"
 elif max_delta >= 0.5:
 splice_class = "moderate_impact"
 elif max_delta >= 0.2:
 splice_class = "low_impact"
 else:
 splice_class = "no_impact"

 results.append({
 "chr": chrom, "pos": pos, "ref": ref, "alt": alt,
 "ds_acceptor_gain": ds_ag,
 "ds_acceptor_loss": ds_al,
 "ds_donor_gain": ds_dg,
 "ds_donor_loss": ds_dl,
 "max_delta": max_delta,
 "splice_class": splice_class,
 "variant": f"chr{chrom}:{pos}{ref}>{alt}",
 })

 df = pd.DataFrame(results)
 impacted = (df["max_delta"] >= delta_threshold).sum
 print(f"SpliceAI: {len(df)} variants, "
 f"{impacted} with splice impact (Δ≥{delta_threshold})")
 return df
```

## 4. evaluation

```python
def consensus_pathogenicity(am_df, cadd_df, spliceai_df,
 am_threshold=0.564, cadd_threshold=20,
 splice_threshold=0.5):
 """
 AlphaMissense + CADD + SpliceAI 'sevaluation。

 Parameters:
 am_df: AlphaMissense results DataFrame
 cadd_df: CADD results DataFrame
 spliceai_df: SpliceAI results DataFrame
 """
 # ID binding
 merged = cadd_df.copy

 if len(am_df) > 0:
 merged = merged.merge(
 am_df[["variant", "am_score", "am_class"]],
 on="variant", how="left"
 )
 if len(spliceai_df) > 0:
 merged = merged.merge(
 spliceai_df[["variant", "max_delta", "splice_class"]],
 on="variant", how="left"
 )

 # 
 def compute_consensus(row):
 votes = 0
 total = 0

 if "cadd_phred" in row and not pd.isna(row.get("cadd_phred")):
 total += 1
 if row["cadd_phred"] >= cadd_threshold:
 votes += 1

 if "am_score" in row and not pd.isna(row.get("am_score")):
 total += 1
 if row["am_score"] >= am_threshold:
 votes += 1

 if "max_delta" in row and not pd.isna(row.get("max_delta")):
 total += 1
 if row["max_delta"] >= splice_threshold:
 votes += 1

 if total == 0:
 return "insufficient_data"
 ratio = votes / total
 if ratio >= 0.67:
 return "pathogenic"
 elif ratio >= 0.33:
 return "uncertain"
 else:
 return "benign"

 merged["consensus"] = merged.apply(compute_consensus, axis=1)
 merged["evidence_count"] = merged.apply(
 lambda r: sum(1 for c in ["cadd_phred", "am_score", "max_delta"]
 if c in r and not pd.isna(r.get(c))), axis=1)

 print(f"Consensus: {len(merged)} variants — "
 f"{(merged['consensus'] == 'pathogenic').sum} pathogenic, "
 f"{(merged['consensus'] == 'uncertain').sum} uncertain, "
 f"{(merged['consensus'] == 'benign').sum} benign")
 return merged
```

## References

### Output Files

| File | Format |
|---|---|
| `results/alphamissense_scores.csv` | CSV |
| `results/cadd_scores.csv` | CSV |
| `results/spliceai_scores.csv` | CSV |
| `results/consensus_pathogenicity.csv` | CSV |
| `figures/variant_score_distribution.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| AlphaMissense | `AlphaMissense_get_protein_scores` | proteinall |
| AlphaMissense | `AlphaMissense_get_variant_score` | units |
| AlphaMissense | `AlphaMissense_get_residue_scores` | |
| CADD | `CADD_get_variant_score` | units PHRED |
| CADD | `CADD_get_position_scores` | all |
| CADD | `CADD_get_range_scores` | range |
| SpliceAI | `SpliceAI_predict_splice` | Δprediction |
| SpliceAI | `SpliceAI_predict_pangolin` | Pangolin prediction |
| SpliceAI | `SpliceAI_get_max_delta` | Δretrieval |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-variant-interpretation` | ACMG/AMP |
| `scientific-population-genetics` | gnomAD frequencyreference |
| `scientific-disease-research` | disease- |
| `scientific-pharmacogenomics` | PGx |
| `scientific-protein-structure-analysis` | structure→evaluation |

### Dependencies

`pandas`, `numpy`, `requests`
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
