---
name: scientific-clinical-nlp
description: |
 Clinical NLP skill. MedSpaCy/cTAKES/scispaCy-based clinical text NER, section detection, negation detection, ICD-10/SNOMED-CT entity linking, and de-identification pipelines.
tu_tools:
 - key: umls
 name: UMLS
 description: forsearch
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `umls` | UMLS | forsearch |

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
