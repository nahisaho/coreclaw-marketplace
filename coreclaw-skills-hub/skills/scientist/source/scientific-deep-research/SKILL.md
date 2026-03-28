---
name: scientific-deep-research
description: |
 literature'sskill。SHIKIGAMI 's WebResearcher 
 （Think→Report→Action cycle）research implementation。
 databasesearch、evaluation、、verification、
 integrationinvestigationproviding。
 「literatureinvestigation」「research」「systematic review 」 。
---

# Scientific Deep Research

literature's is supportedskill。SHIKIGAMI 's WebResearcher
（Think→Report→Action cycle）research、
databasesearchevaluationverificationintegration.

## MCPintegration

`deep-research` MCP usepossible、MCP 's `deep-research`
template utilizing。MCP providesstructure：

1. **Question Elaboration** — researchchallenge keyworddefinition
2. **Subquestion Generation** — 3〜5units's degradationcomprehensive
3. **Web Search** — eachaboutfrominformation
4. **Content Analysis** — 'sevaluation
5. **Report Generation** — structurereportgeneration、allcitation

MCP 's results 、papersskill's evaluationverification
evaluation。MCP use 's workflow for。

## When to Use

- research'sresearchinvestigation is performedand
- Systematic Review / Scoping Review 's literaturesearch is performedand
- 's research's latest comprehensiveinvestigationwhen needed
- comparisonmethodcomparisonforinformationwhen needed
- Grant proposal / Research proposal 's backgroundinvestigationwhen needed
- paper Introduction forliterature is performedand

## Quick Start

### 1. Deep Research workflowoverview

```
Phase 1: Research Question Definition（researchchallenge'sdefinition）
 ↓
Phase 2: Deep Research（）
 ┌──────────────────────────────────────────┐
 │ Think → Search → Evaluate → Synthesize │ ← cycle
 │ ( 15 ) │
 └──────────────────────────────────────────┘
 ↓
Phase 3: Evidence Synthesis（integration）
 ↓
Phase 4: Research Report（reportgeneration）
```

### 2. WebResearcher （research）

SHIKIGAMI's Think→Report→Action cycleresearchoptimization:

```
┌─────────────────────────────────────────────────────┐
│ Round N │
│ ┌─────────────────────────────────────────────┐ │
│ │ Workspace ('s Synthesis + literature) │ │
│ └─────────────────────────────────────────────┘ │
│ ↓ │
│ ┌───────────┐ ┌───────────┐ ┌───────────────┐ │
│ │ Think │→│ Search │→│ Evaluate │ │
│ │ ( │ │ (DB │ │ ( │ │
│ │ │ │ search) │ │ evaluation) │ │
│ │ min) │ │ │ │ │ │
│ └───────────┘ └───────────┘ └───────┬───────┘ │
│ ↓ │
│ ┌───────────────┐ │
│ │ Synthesize │ │
│ │ (evolution │ │
│ │ ) │ │
│ └───────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Phase 1: Research Question Definition

### PICO/PECO structure

structure、search's is built。

```markdown
## Research Question 's structure

### PICO (research)
- **P** (Population): research
- **I** (Intervention): method
- **C** (Comparison): comparisonexistingmethod
- **O** (Outcome): evaluation metric

### PECO (observationresearch)
- **P** (Population): 
- **E** (Exposure): 
- **C** (Comparison): comparisongroup
- **O** (Outcome): 

### SPIDER (research)
- **S** (Sample): 
- **PI** (Phenomenon of Interest): 
- **D** (Design): research
- **E** (Evaluation): evaluationmethod
- **R** (Research type): researchtype
```

### search'sdesign

```markdown
## searchtemplate

### 1. keyworddesign
| | paperskeyword | keyword | MeSH / |
|------|-----------------|---------------|-----------------|
| P | [] | [population] | [MeSH term] |
| I/E | [/] | [intervention]| [MeSH term] |
| C | [comparison] | [comparison] | [MeSH term] |
| O | [] | [outcome] | [MeSH term] |

### 2. 's
(P terms) AND (I terms) AND (O terms)

### 3. criteria
| criteria | | |
|------|------|------|
| publication | [YYYY]-present | < [YYYY] |
| | English, Japanese | Others |
| research | [RCT, Cohort, etc.] | [Case report, etc.] |
| publicationtype | Original article, Review | Editorial, Letter |
```

---

## Phase 2: Deep Research（）

### Think phase（min）

each's 's status evaluation、's.

```markdown
## Think phase's

### status'sevaluation
- [ ] 's literaturenumber/count and
- [ ] 's researchchallenge
- [ ] 
- [ ] 's

### 's
- SEARCH: large → additionsearch
- VISIT: paper → detailsretrieval
- VERIFY: important → verification
- COMPLETE: mininformation → integrationphase to 
```

**important**: Think phase's inference
（、SHIKIGAMI ）。

### Search phase（databasesearch）

#### searchdatabase

| database | min | searchmethod | degree |
|-------------|---------|----------|--------|
| **PubMed / MEDLINE** | | MeSH + Free text | P0  |
| **Google Scholar** | allmin | Free text | P0 (all) |
| **arXiv** | CSnumber/count | Free text | P0 (CS) |
| **Semantic Scholar** | allmin (AI analysis) | API / Free text | P1 |
| **Web of Science** | allmin (IF ) | Topic search | P1 |
| **Scopus** | allmin | Title-Abs-Key | P1 |
| **CrossRef** | DOI data | DOI lookup | P2 |
| **CiNii** | papersliterature | Free text | P1 (papers) |
| **J-STAGE** | papers | Free text | P1 (papers) |
| **ChemRxiv** | | Free text | P2  |
| **bioRxiv / medRxiv** | | Free text | P2  |

#### search（required）

```markdown
## search's rules

### search（required）
- all's papers'sexecutes
- example: ["ZnO ", "ZnO thin film sputtering properties"]

### 
- below/following'sevaluation:
.ac.jp,.edu,.gov,.go.jp,.org 
 pubmed.ncbi.nlm.nih.gov
 scholar.google.com
 arxiv.org
 doi.org

### searchformula's structure
- (AND, OR, NOT) utilizing
- (*) 
- search ("exact phrase") degree
- filter: publication、research、

### failure's
- 404/5xx error → Wayback Machine → Archive.today
- searchresults 0 items → → → topto
```

### Evaluate phase（evaluation）

eachliteratureinformation's and is evaluated。

#### （Evidence Hierarchy）

```markdown
## classification

| Level | research | degree | |
|-------|-------------|--------|------|
| 1a | Systematic Review of RCTs | ★★★★★ | [SR] |
| 1b | Individual RCT | ★★★★☆ | [RCT] |
| 2a | Systematic Review of Cohort | ★★★★☆ | [SR-C] |
| 2b | Individual Cohort Study | ★★★☆☆ | [Cohort] |
| 3a | Systematic Review of Case-Control | ★★★☆☆ | [SR-CC] |
| 3b | Individual Case-Control Study | ★★☆☆☆ | [CC] |
| 4 | Case Series / Cross-sectional | ★★☆☆☆ | [CS] |
| 5 | Expert Opinion / Narrative Review | ★☆☆☆☆ | [EO] |
| — | Preprint (not peer-reviewed) | ☆☆☆☆☆ | [PP] |
```

#### 

```markdown
## evaluation

| evaluationitem | range | |
|---------|-----------|------|
| ** IF / ** | 0-25 | ×2 |
| **author's h-index / ** | 0-25 | ×1.5 |
| **sample size n** | 0-25 | ×1.5 |
| **method's** | 0-25 | ×1 |
| **reproducibilitydata** | 0-25 | ×1 |
| **publication's** | 0-25 | ×0.5 |

### degree
- 80-100: ★★★★★ 
- 60-79: ★★★★☆ 
- 40-59: ★★★☆☆ degree
- 20-39: ★★☆☆☆ 
- 0-19: ★☆☆☆☆ caution

### degree's
- 60 → verificationrequired（verification）
- → 「⚠️ peer review」required
- 5 above/more → 「⚠️ verification」recommended
```

#### evaluation

```markdown
## literature'sevaluation (Critical Appraisal)

### RCT evaluation (Cochrane Risk of Bias )
- [ ] randomization's method
- [ ] 's
- [ ] （evaluation）
- [ ] data's
- [ ] 's selection
- [ ] 's 's

### observationresearchevaluation (Newcastle-Ottawa Scale )
- [ ] group's selection
- [ ] group's comparisonpossible
- [ ] 's measurement
- [ ] min

### systematic reviewevaluation (AMSTAR-2 )
- [ ] protocol
- [ ] literaturesearch
- [ ] evaluation
- [ ] 's method
```

### Synthesize phase（evolution）

eachinformation integration、evolutionreport is updated。

```markdown
## Evolving Research Report（evolutionreport）

### Round N 's content
| Element | Description |
|------|------|
| **Rationale（basis）** | researchchallenge 's |
| **Evidence（）** | also 's highinformation'sextraction（） |
| **Summary（）** | point 's 's integration |
| **Confidence（degree）** | 0-100% — mininformation 's |
| **Gaps（）** | 'slist |

### completioncriteria
- [ ] keyresearchchallenge times
- [ ] 5 items'speer reviewliterature
- [ ] search
- [ ] all's data URL/DOI 
- [ ] degree 60% above/more's 3 itemsabove/more
- [ ] 、verification completion
```

---

## Phase 3: Evidence Synthesis（integration）

### PRISMA （Systematic Review for）

```markdown
## PRISMA 2020 template

### Identification（）
- databasesearch: n = ___
 - PubMed: n = ___
 - Google Scholar: n = ___
 - arXiv: n = ___
 - 's: n = ___
- 's 's information: n = ___
 - citationliterature: n = ___
 - citationliterature: n = ___
 - manualsearch: n = ___

### Screening（）
- : n = ___
- title/: n = ___
 - : n = ___ (: ___)
- all: n = ___
 - : n = ___ (: ___)

### Included（）
- integrationresearch: n = ___
- amountintegration（）research: n = ___
```

### integrationmintemplate

```markdown
## integrationtable

| # | author  | research | n | keyresults | degree | DOI |
|---|----------|-------------|---|---------|--------|-----|
| 1 | Author (2024) | [RCT] | 100 | [key finding] | ★★★★☆ | 10.xxxx |
| 2 | Author (2023) | [Cohort] | 500 | [key finding] | ★★★☆☆ | 10.xxxx |
|... | | | | | | |

## 'sintegration
### 
- [multiple's research]

### 
- [literature A] [ X] 、[literature B] [ Y] 
 - : [method's / 's /...]

### 
- [minresearch]
```

---

## Phase 4: Research Report（reportgeneration）

### reporttemplate

```markdown
# Deep Research Report: [research]

**generation**: YYYY-MM-DD
**number of rounds**: N times
**literaturenumber/count**: M items
**keydatabase**: [PubMed, Google Scholar,...]

---

## Executive Summary

[3-5 key]

## 1. Research Question

### 1.1 structureresearchchallenge
[PICO/PECO shapeformula]

### 1.2 search
[searchformulafilter's]

## 2. Findings

### 2.1 [ 1]
[Findings + citations]

### 2.2 [ 2]
[Findings + citations]

### 2.3 [ 3]
[Findings + citations]

## 3. Evidence Summary

### 3.1 table
[integrationmintable]

### 3.2 's
[GRADE by/viaevaluation]

## 4. Knowledge Gaps & Future Directions

[and 's researchdirection]

## 5. References

[allcitationliterature — DOI/URL required]
```

---

## 

### （required）

```markdown
## alldatainformation

### requireditem
| item | | example |
|------|------|---|
| **author** | author et al. | Smith et al. |
| **** | publication | 2024 |
| **** | | Nature |
| **DOI** | Digital Object Identifier | 10.1038/s41586-... |
| **URL** | for URL | https://doi.org/10.1038/... |
| **** | informationretrieval | 2026-02-12 |
| **** | research | [RCT] |
| **degree** | evaluationresults | ★★★★☆ (78/100) |
```

### 

```markdown
## information's degree（required）

| | | forcondition |
|---------|------|---------|
| ✅ | verification（2+ verification） | multiple'sverification |
| 📎 | single | 1 items's from's information |
| ⚠️ | peer reviewverification | 、literature |
| ❓ | AI by/via | 、including |
| 🔄 | data（5 above/more） | latestinformationverification |
| ⚡ (?) | information's | multiple information |

### forexample
- ✅ ZnO 'sband gap 3.37 eV [Smith 2024, Tanaka 2023]
- 📎 novelcatalyst's transformationrate 95% and [Lee 2024]
- ⚠️ amountby/viaoptimization 10x high-speed（）[arXiv:2024.xxxxx]
- ❓ 's method 's also forpossible and
- ⚡ (?) $50B [Report A] vs $35B [Report B]
```

---

## verification（Cross-Validation）

```markdown
## verification's

### requiredcondition
- importantnumber/countvaluedata → 2 verification
- key → researchverification
- → 3 'sverification

### number/countvaluedata's
| rate | degree | |
|--------|--------|----------|
| < 5% | | rangeas (e.g., 3.35-3.37 eV) |
| 5-20% | | ⚡ (?) 、measurementcondition's note |
| > 20% | | ⚡ (?) 、additioninvestigation、condition's min |

### content's
1. 's
2. each's explicit
3. 's min
 - research's
 - 's
 - measurementmethod's
 - publication's possible
```

---

## （Quality Gates）

```markdown
## Deep Research completion

### Phase 1→2 （researchchallengedefinition→start）
- [ ] PICO/PECO structure
- [ ] searchkeyworddefinition
- [ ] criteria clear

### Phase 2→3 （→integration）
- [ ] 5 items'speer reviewliterature
- [ ] all's data DOI/URL 
- [ ] search
- [ ] degree 60% above/more's 3 itemsabove/more
- [ ] keyfor/againstverification completion

### Phase 3→4 （integration→report）
- [ ] table
- [ ] 
- [ ] 

### Phase 4 completion（report）
- [ ] allcitation DOI/URL 
- [ ] 
- [ ] PRISMA （）
- [ ] Executive Summary papers and
```

---

## searchtemplate（min）

### 

```markdown
## PubMed search

### MeSH + Free text 's
("Drug Delivery Systems"[MeSH] OR "drug delivery"[tiab])
AND
("Nanoparticles"[MeSH] OR nanoparticle*[tiab])
AND
("Neoplasms"[MeSH] OR cancer[tiab] OR tumor[tiab])

### filter
- Publication date: 2020/01/01 - present
- Article type: Clinical Trial, Randomized Controlled Trial, Review
- Language: English, Japanese
```

### 

```markdown
## Google Scholar / Scopus search

### keyword
("ZnO thin film" OR "zinc oxide film")
AND
(sputtering OR "physical vapor deposition" OR PVD)
AND
(optical OR electrical OR "band gap")

### filter: 2020-present
### citationnumber/count: citationnumber/counttop 50 itemsverification
```

### AI

```markdown
## arXiv / Semantic Scholar search

### keyword
("large language model" OR LLM)
AND
("retrieval augmented generation" OR RAG)
AND
(evaluation OR benchmark)

### filter: cs.CL, cs.AI, cs.IR
### : latest + citationnumber/count
```

---

## skill and 'sintegration

### Position in the Pipeline

```
deep-research → hypothesis-pipeline → pipeline-scaffold → academic-writing
 (literatureinvestigation) (hypothesisdefinition) (analysis) 
```

### integrationskill

| Skill | Integration |
|--------|---------|
| `scientific-hypothesis-pipeline` | Deep Research 's resultsfromhypothesis formula |
| `scientific-academic-writing` | literature Introduction / Discussion |
| `scientific-citation-checker` | citation'sverification |
| `scientific-critical-review` | report's |
| `scientific-meta-analysis` | literaturedata |
| `scientific-statistical-testing` | number/countvaluedata'sverification |

---

## Output Files

| file | shapeformula | content |
|---------|------|------|
| `research/research_report.md` | Markdown | Deep Research report |
| `research/evidence_table.json` | JSON | integrationtable |
| `research/search_log.md` | Markdown | searchlog（searchformularesultsnumber/countdatetime） |
| `research/source_registry.json` | JSON | registry |
| `research/prisma_flow.md` | Markdown | PRISMA （） |

### research_report.md 's

```markdown
---
title: "[research]"
date: "YYYY-MM-DD"
rounds: N
sources_count: M
databases: ["PubMed", "Google Scholar",...]
confidence_score: XX%
---

# Deep Research Report: [research]
...
```

### evidence_table.json 's schema

```json
{
 "research_question": "...",
 "search_strategy": {
 "databases": ["PubMed", "Google Scholar"],
 "date_range": "2020-2026",
 "keywords": {
 "ja": ["keyword1", "keyword2"],
 "en": ["keyword1", "keyword2"]
 }
 },
 "sources": [
 {
 "id": "S001",
 "authors": "Smith et al.",
 "year": 2024,
 "title": "...",
 "journal": "Nature",
 "doi": "10.1038/...",
 "url": "https://doi.org/...",
 "evidence_level": "1b",
 "study_design": "RCT",
 "sample_size": 100,
 "key_findings": ["..."],
 "credibility_score": 85,
 "accessed_date": "2026-02-12"
 }
 ],
 "synthesis": {
 "consistent_findings": ["..."],
 "conflicting_findings": ["..."],
 "evidence_gaps": ["..."]
 }
}
```

### source_registry.json 's schema

```json
{
 "registry_version": "1.0",
 "created_at": "2026-02-12T00:00:00+09:00",
 "sources": [
 {
 "id": "S001",
 "url": "https://doi.org/...",
 "doi": "10.1038/...",
 "accessed_at": "2026-02-12T10:30:00+09:00",
 "retrieval_method": "search",
 "query_used": "ZnO thin film sputtering",
 "database": "Google Scholar",
 "status": "active",
 "credibility_score": 85,
 "evidence_level": "2b",
 "cross_validated": true,
 "cross_validation_sources": ["S003", "S007"]
 }
 ]
}
```

## References

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| PubMed | `PubMed_search_articles` | literaturesearch |
| PubMed | `PubMed_get_cited_by` | citation structure analysis |
| EuropePMC | `EuropePMC_search_articles` | European literature search |
| Crossref | `Crossref_search_works` | publication information search |
| OpenAlex | `OpenAlex_Guidelines_Search` | literature |
| ArXiv | `ArXiv_search_papers` | search |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
