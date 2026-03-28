---
name: scientific-genome-sequence-tools
description: |
 Genome sequence tools skill. BLAST searches, multiple sequence alignment, genome annotation, primer design, and sequence manipulation utilities.
---

# Scientific Genome Sequence Tools

genomedatabase (Ensembl, dbSNP, BLAST, NCBI, GDC) cross-cutting
sequencesearchvariant annotationcancer genomicspipeline is provided。

## When to Use

- genomesequencestructure Ensembl fromretrievalwhen needed
- rsID fromvariant/mutation's allele frequency is investigatedand
- BLAST /amino acidsequence's phasesearch is performedand
- NCBI Nucleotide fromsequencewhen needed
- GDC cancer genomicsdata (cellvariant/mutation, CNV, expression) is retrievedand

---

## Quick Start

## 1. dbSNP variant/mutationinformationretrieval

```python
import requests
import pandas as pd


def get_dbsnp_variant(rsid):
 """
 dbSNP from rsID 'svariant/mutationinformation (allele frequencyincludes) retrieval。

 Parameters:
 rsid: str — e.g. "rs7412"

 ToolUniverse:
 dbsnp_get_variant_by_rsid(rsid=rsid)
 dbsnp_get_frequencies(rsid=rsid)
 dbsnp_search_by_gene(gene_symbol=gene_symbol)
 """
 url = f"https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/{rsid.lstrip('rs')}"
 resp = requests.get(url)
 resp.raise_for_status
 data = resp.json

 # Extract primary info
 info = {
 "rsid": f"rs{data.get('refsnp_id', '')}",
 "create_date": data.get("create_date", ""),
 "update_date": data.get("update_date", ""),
 }

 # Allele frequencies
 alleles = data.get("primary_snapshot_data", {}).get(
 "allele_annotations", []
 )
 freq_data = []
 for allele in alleles:
 for freq_entry in allele.get("frequency", []):
 freq_data.append({
 "study": freq_entry.get("study_name", ""),
 "allele": freq_entry.get("allele", ""),
 "count": freq_entry.get("allele_count", 0),
 "total": freq_entry.get("total_count", 0),
 })

 df_freq = pd.DataFrame(freq_data)
 print(f"dbSNP {info['rsid']}: {len(df_freq)} frequency entries")
 return info, df_freq
```

## 2. BLAST phasesearch

```python
import time


def blast_search(sequence, program="blastn", database="nt", max_hits=10):
 """
 NCBI BLAST REST API phasesearch。

 Parameters:
 sequence: str — query sequence (nucleotide or protein)
 program: str — "blastn", "blastp", "blastx", "tblastn"
 database: str — "nt", "nr", "refseq_rna", etc.

 ToolUniverse:
 BLAST_nucleotide_search(sequence=sequence, database=database)
 BLAST_protein_search(sequence=sequence, database=database)
 """
 put_url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
 params = {
 "CMD": "Put",
 "PROGRAM": program,
 "DATABASE": database,
 "QUERY": sequence,
 "FORMAT_TYPE": "JSON2",
 "HITLIST_SIZE": max_hits,
 }
 resp = requests.post(put_url, data=params)
 resp.raise_for_status

 # Extract RID
 import re
 rid_match = re.search(r"RID = (\S+)", resp.text)
 if not rid_match:
 raise ValueError("BLAST RID not found")
 rid = rid_match.group(1)
 print(f"BLAST submitted: RID={rid}")

 # Poll for results
 for _ in range(60):
 time.sleep(10)
 check = requests.get(put_url, params={
 "CMD": "Get", "RID": rid, "FORMAT_TYPE": "JSON2"
 })
 if "Status=WAITING" not in check.text:
 break

 return check.json if check.headers.get(
 "Content-Type", ""
 ).startswith("application/json") else check.text
```

## 3. NCBI Nucleotide sequence

```python
def fetch_ncbi_sequence(accession, rettype="fasta"):
 """
 NCBI Nucleotide (E-utilities) fromsequence retrieval。

 Parameters:
 accession: str — NCBI accession (e.g., "NM_000546.6")
 rettype: str — "fasta", "gb", "gbwithparts"

 ToolUniverse:
 NCBI_search_nucleotide(query=query)
 NCBI_fetch_accessions(accessions=accessions)
 NCBI_get_sequence(accession=accession)
 """
 url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
 params = {
 "db": "nucleotide",
 "id": accession,
 "rettype": rettype,
 "retmode": "text",
 }
 resp = requests.get(url, params=params)
 resp.raise_for_status

 print(f"NCBI Nucleotide '{accession}': {len(resp.text)} chars ({rettype})")
 return resp.text
```

## 4. GDC cancer genomicsdata

```python
def get_gdc_mutations(gene_symbol, project_id=None):
 """
 NCI GDC (Genomic Data Commons) fromcellvariant/mutationdata retrieval。

 Parameters:
 gene_symbol: str — e.g. "TP53"
 project_id: str | None — e.g. "TCGA-BRCA"

 ToolUniverse:
 GDC_get_ssm_by_gene(gene_symbol=gene_symbol)
 GDC_get_mutation_frequency(project_id=project_id)
 GDC_get_gene_expression(gene_id=gene_id, project_id=project_id)
 GDC_get_cnv_data(gene_id=gene_id)
 GDC_list_projects
 GDC_search_cases(filters=filters)
 GDC_list_files(filters=filters)
 """
 url = "https://api.gdc.cancer.gov/ssms"
 filters = {
 "op": "and",
 "content": [
 {"op": "in", "content": {
 "field": "consequence.transcript.gene.symbol",
 "value": [gene_symbol],
 }},
 ],
 }
 if project_id:
 filters["content"].append({
 "op": "in",
 "content": {
 "field": "cases.project.project_id",
 "value": [project_id],
 },
 })

 import json
 params = {
 "filters": json.dumps(filters),
 "fields": ("ssm_id,consequence.transcript.gene.symbol,"
 "consequence.transcript.aa_change,"
 "consequence.transcript.consequence_type,"
 "genomic_dna_change"),
 "size": 100,
 "format": "json",
 }
 resp = requests.get(url, params=params)
 resp.raise_for_status
 hits = resp.json.get("data", {}).get("hits", [])

 results = []
 for hit in hits:
 for csq in hit.get("consequence", []):
 tx = csq.get("transcript", {})
 results.append({
 "ssm_id": hit.get("ssm_id", ""),
 "gene": tx.get("gene", {}).get("symbol", ""),
 "aa_change": tx.get("aa_change", ""),
 "consequence_type": tx.get("consequence_type", ""),
 "genomic_dna_change": hit.get("genomic_dna_change", ""),
 })

 df = pd.DataFrame(results)
 print(f"GDC SSMs '{gene_symbol}'"
 f"{f' ({project_id})' if project_id else ''}: {len(df)} mutations")
 return df
```

## 5. integrationgenomevariant/mutationpipeline

```python
def integrated_variant_pipeline(rsid, gene_symbol=None):
 """
 dbSNP + GDC integrationgenomevariant/mutationanalysispipeline。

 ToolUniverse (cross-cutting):
 dbsnp_get_variant_by_rsid(rsid) → GDC_get_ssm_by_gene(gene_symbol)
 """
 pipeline_result = {"rsid": rsid}

 # Step 1: dbSNP
 info, freq_df = get_dbsnp_variant(rsid)
 pipeline_result["dbsnp"] = info

 # Step 2: GDC somatic mutations (if gene provided)
 if gene_symbol:
 gdc_df = get_gdc_mutations(gene_symbol)
 pipeline_result["gdc_mutation_count"] = len(gdc_df)
 pipeline_result["gdc_top_consequences"] = (
 gdc_df["consequence_type"].value_counts.head(5).to_dict
 if not gdc_df.empty else {}
 )

 print(f"Integrated variant: {rsid}"
 f" | GDC={pipeline_result.get('gdc_mutation_count', 'N/A')}")
 return pipeline_result
```

## References

### Output Files

| File | Format |
|---|---|
| `results/dbsnp_variant.json` | JSON |
| `results/dbsnp_frequencies.csv` | CSV |
| `results/blast_results.json` | JSON |
| `results/ncbi_sequence.fasta` | FASTA |
| `results/gdc_mutations.csv` | CSV |

### Available Tools

| Category | Key Tools | Usage |
|---|---|---|
| dbSNP | `dbsnp_get_variant_by_rsid` | rsID variant/mutationinformation |
| dbSNP | `dbsnp_get_frequencies` | allele frequency |
| dbSNP | `dbsnp_search_by_gene` | gene→variant/mutation |
| BLAST | `BLAST_nucleotide_search` | nucleotide homology search |
| BLAST | `BLAST_protein_search` | protein homology search |
| NCBI | `NCBI_search_nucleotide` | sequencesearch |
| NCBI | `NCBI_fetch_accessions` | accessionretrieval |
| NCBI | `NCBI_get_sequence` | sequence |
| GDC | `GDC_get_ssm_by_gene` | cellvariant/mutation |
| GDC | `GDC_get_mutation_frequency` | variant/mutationfrequency |
| GDC | `GDC_get_gene_expression` | expressiondata |
| GDC | `GDC_get_cnv_data` | CNV data |
| GDC | `GDC_list_projects` | list |
| GDC | `GDC_search_cases` | casesearch |
| GDC | `GDC_list_files` | filelist |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-variant-interpretation` | variant annotation |
| `scientific-population-genetics` | population genetics |
| `scientific-cancer-genomics` | cancer genomics |
| `scientific-rare-disease-genetics` | disease |
| `scientific-biothings-idmapping` | ID mapping |

### Dependencies

`requests`, `pandas`
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
