---
name: scientific-clinical-nlp
description: |
 skill。MedSpaCy / cTAKES / scispaCy
 by/viaclinical text NER、、、
 ICD-10/SNOMED-CT 、
 (De-identification) pipeline。
 TU skill ( Python library)。
---

# Scientific Clinical NLP

MedSpaCyscispaCy andclinical text
pipeline is provided。from's
extraction (NegEx)standardfor to 's
 is performed。

## When to Use

- / fromdisease is extractedand
- clinical text's (NegEx/ConText) when needed
- (/HPI/Assessment/Plan) classificationwhen needed
- ICD-10 / SNOMED-CT to 's is performedand
- PHI (De-identification) is performedand
- literature and 'sintegration

---

## Quick Start

## 1. MedSpaCy NER

```python
import medspacy
from medspacy.ner import TargetRule
from medspacy.visualization import visualize_ent


def clinical_ner(text, rules=None):
 """
 MedSpaCy — clinical text NER pipeline。

 Parameters:
 text: str — clinical text
 rules: list[dict] | None — custom
 """
 nlp = medspacy.load(
 enable=["medspacy_pyrush",
 "medspacy_target_matcher",
 "medspacy_context"])

 if rules:
 target_matcher = nlp.get_pipe(
 "medspacy_target_matcher")
 for r in rules:
 target_matcher.add(TargetRule(
 literal=r["literal"],
 category=r.get("category",
 "CONDITION")))

 doc = nlp(text)

 entities = []
 for ent in doc.ents:
 entities.append({
 "text": ent.text,
 "label": ent.label_,
 "start": ent.start_char,
 "end": ent.end_char,
 "is_negated": ent._.is_negated,
 "is_uncertain": ent._.is_uncertain,
 "is_historical": ent._.is_historical,
 "is_family": ent._.is_family,
 })

 n_neg = sum(1 for e in entities
 if e["is_negated"])
 print(f"Clinical NER: {len(entities)} entities, "
 f"{n_neg} negated")
 return entities


def clinical_ner_batch(texts, rules=None):
 """
 MedSpaCy — batch NER。

 Parameters:
 texts: list[str] — clinical text
 rules: list[dict] | None — custom
 """
 all_entities = []
 for i, text in enumerate(texts):
 ents = clinical_ner(text, rules)
 for e in ents:
 e["doc_id"] = i
 all_entities.extend(ents)

 import pandas as pd
 df = pd.DataFrame(all_entities)
 print(f"Batch NER: {len(texts)} docs, "
 f"{len(df)} total entities")
 return df
```

## 2. 

```python
def clinical_section_detect(text):
 """
 MedSpaCy — clinical text。

 Parameters:
 text: str — clinical text
 """
 import medspacy
 nlp = medspacy.load(
 enable=["medspacy_pyrush",
 "medspacy_sectionizer"])

 doc = nlp(text)

 sections = []
 for section in doc._.sections:
 sections.append({
 "category": section.category,
 "title": (section.title_span.text
 if section.title_span else ""),
 "body": (section.body_span.text[:200]
 if section.body_span else ""),
 })

 print(f"Sections detected: {len(sections)}")
 for s in sections:
 print(f" [{s['category']}] "
 f"{s['title'][:50]}")
 return sections
```

## 3. SNOMED-CT / ICD-10 

```python
def clinical_entity_linking(text,
 linker_name="umls"):
 """
 scispaCy — 's UMLS/SNOMED 。

 Parameters:
 text: str — clinical text
 linker_name: str — ("umls", "mesh",
 "snomed")
 """
 import spacy
 import scispacy
 from scispacy.linking import EntityLinker

 nlp = spacy.load("en_core_sci_md")
 nlp.add_pipe("scispacy_linker",
 config={"resolve_abbreviations": True,
 "linker_name": linker_name})

 doc = nlp(text)
 linker = nlp.get_pipe("scispacy_linker")

 linked = []
 for ent in doc.ents:
 for cui, score in ent._.kb_ents[:3]:
 concept = linker.kb.cui_to_entity.get(
 cui, {})
 linked.append({
 "text": ent.text,
 "cui": cui,
 "score": round(score, 3),
 "canonical_name": (
 concept.canonical_name
 if hasattr(concept,
 "canonical_name")
 else str(concept)),
 })

 import pandas as pd
 df = pd.DataFrame(linked)
 print(f"Entity linking: {len(doc.ents)} entities → "
 f"{len(df)} CUI mappings")
 return df
```

## 4. NLP integrationpipeline

```python
def clinical_nlp_pipeline(texts,
 output_dir="results"):
 """
 NLP integrationpipeline。

 Parameters:
 texts: list[str] — clinical text
 output_dir: str — output directory
 """
 import pandas as pd
 from pathlib import Path
 output_dir = Path(output_dir)
 output_dir.mkdir(parents=True, exist_ok=True)

 # 1) NER + 
 ner_df = clinical_ner_batch(texts)
 ner_df.to_csv(output_dir / "clinical_ner.csv",
 index=False)

 # 2) 
 all_sections = []
 for i, text in enumerate(texts):
 secs = clinical_section_detect(text)
 for s in secs:
 s["doc_id"] = i
 all_sections.extend(secs)
 section_df = pd.DataFrame(all_sections)
 section_df.to_csv(
 output_dir / "clinical_sections.csv",
 index=False)

 # 3) ('s)
 if texts:
 link_df = clinical_entity_linking(texts[0])
 link_df.to_csv(
 output_dir / "entity_linking.csv",
 index=False)

 print(f"Clinical NLP pipeline → {output_dir}")
 return {"ner": ner_df, "sections": section_df}
```

---

## Pipeline Integration

```
text-mining-nlp → clinical-nlp → clinical-reporting
 (PubMed/literature) (NER/NegEx) (structurereport)
 │ │ ↓
 biomedical-ner ───────┘ pharmacogenomics
 (scispaCy) (PGx support)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `results/clinical_ner.csv` | + | → phenotype-hpo |
| `results/clinical_sections.csv` | classification | → clinical-reporting |
| `results/entity_linking.csv` | UMLS/SNOMED | → disease-research |

## Data Acquisition

> All data retrieval is implemented in Python using `requests` and public REST APIs.
> No external ToolUniverse tools are required.

### Implementation Pattern

```python
import requests
import pandas as pd

def fetch_api_data(url, params=None):
    """Generic REST API data retrieval with error handling."""
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

### Report Generation

After data acquisition, generate a structured report:

1. Save raw results to `results/` as CSV/JSON
2. Create visualizations in `figures/`
3. Write `report.md` summarizing methods, results, and interpretation

---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
