---
name: scientific-academic-writing
description: |
 paper'swritingskill。IMRaD standard、Nature/Science system、ACS system、IEEE system、
 Elsevier system'sjournal formatsupportpaperconfigurationdesignproviding。
 「paper」「Abstract 」「Methods 」 。
 assets/ keyjournal format's Markdown template。
---

# Scientific Academic Writing

paper'swriting is supportedskill。journal formatconfigurationtemplate、
's 、citationfigures/tablesreference's is provided。

## SATORI reference

**important**: paper SATORI 's（Authors, Acknowledgements,
AI Disclosure ）、number 。
 `package.json` 's `version` field、's value for and 。

```
✅ correctexample: GitHub Copilot Agent (SATORI v0.5.1) ← package.json fromretrieval
❌ example: GitHub Copilot Agent (SATORI v0.3.0) ← 's
```

retrievalprocedure:
1. 's `package.json` 
2. `version` field's value is retrieved
3. `SATORI v{version}` 's shapeformula

## When to Use

- paper's is createdand
- Abstract / Introduction / Methods / Results / Discussion writingwhen needed
- journal formatpaperconfigurationwhen needed
- Cover Letter / Response to Reviewers is createdand
- existing's configuration and

## Quick Start

### 1. templateselection

```
journal format's selection:

Q1: ？
├── Nature / Nature Communications / Nature Materials → nature_article.md
├── Science / Science Advances → science_research_article.md
├── ACS Nano / JACS / Chem. Mater. → acs_article.md
├── IEEE Trans. / IEEE Access → ieee_transactions.md
├── Elsevier system (Acta Mater., etc.) → elsevier_article.md
├── Qiita → qiita_technical_article.md
└── 's / → imrad_standard.md (also for)
```

### 2. paperconfiguration's basicprinciples

```markdown
## paperconfiguration's CARS (Create A Research Space)

### Introduction 's 3 step:
1. **Establishing a territory** — researchmin's importantresearch's
2. **Establishing a niche** — research's 's problem
3. **Occupying the niche** — papersresearch's purposekey

### Discussion 's configuration:
1. key's（Results 's）
2. research and 's comparisonpositioning
3. 's discussion
4. research's limitations (Limitations)
5. 's outlook (Future perspectives)
6. conclusion (Conclusion) — 
```

### 3. 

#### Abstract（structure）

```markdown
## Abstract template（250 words ）

**Background/Context**: [researchmin] [challenge/problem] as [importantchallenge].

**Objective/Purpose**: papersresearch、[method/] for [researchpurpose] and
purpose and 。

**Methods**: [/data] [experimentmethod/analysismethod] for。
[keyparameters/condition] [value] and 。

**Results**: [keyquantitativeresults 2-3 ]。
[significant: p < 0.05, effect size, confidence intervaletc.including]。

**Conclusions**: 's results [/significance] 、
[application/'s outlook] for.

**Keywords**: keyword1, keyword2, keyword3, keyword4, keyword5
```

#### Introduction

```markdown
## Introduction template（800-1500 words）

### 1 : researchmin's important
[researchmin] [/significance] important [ref1, ref2]。
especially ['s] [] fromnote.

### 2 : research's
to/until [researchloop A] [method/] [ref3]、
[researchloop B] ['s method/] [ref4]。
 [researchloop C] by/via [] [significance] [ref5, ref6]。

### 3 : 's
、['s challenge 1] and ['s challenge 2] as。
especially [] about [] frommin 。

### 4 : papersresearch's purpose
papersresearch、[/method] for [purpose] and 。
、(1) [purpose 1]、(2) [purpose 2]、(3) [purpose 3] 。
```

#### Methods / Experimental

```markdown
## Methods template

### 2.1 Materials / Datasets
[] (degree XX%, [], []) for。
[dataset name] [/generationmethod] fromretrieval (n = XXX)。

### 2.2 Experimental Procedure / Data Processing
[] ([type], []) for [condition] [] 。
[parameters 1] [range/value]、[parameters 2] [range/value] and 。

### 2.3 Characterization / Analysis
[minmethod] ([type]) for [measurement] evaluation。
measurementcondition [condition'sdetails] and 。

### 2.4 Statistical Analysis
analysis [] (ver. X.X) for。
groupcomparison [testing] for、significance level p < 0.05 and 。
multiple comparison [correctionmethod] for。
```

#### Results

```markdown
## Results template

### 3.1 [experiment/analysis 1 's results]
**figures/tables's**: Figure 1a [measurement] 's [visualizationcontent] 。
**quantitative**: [parameters] [value ± SD] (n = XX) 。
**comparison**: [condition A] and comparison [condition B] [XX]% 's [/] 
observation (p = X.XXX, [testing])。
**figures/tables's reference**: 's Figure 1b 's [content] fromalso verification.

### caution: Results 's prohibitedterm
- ❌ data's（→ Discussion ）
- ❌ research and 'scomparison（→ Discussion ）
- ❌ method's（→ Methods ）
- ✅ and number/countvalue's
```

#### Discussion

```markdown
## Discussion template

### 1 : key's
papersresearch's keybelow/following's 3 point:
(1) [ 1 — also importantresults]、
(2) [ 2]、(3) [ 3]。

### 2 : research and 'scomparison
[ 1] [research's results] and [refX]、
[/] results.
、[ 2] about [research Y] 's ([refY]) and 
differentresults 。's [] 
and.

### 3 : 's discussion
[observation] 'sas、
[hypothesis/] (Figure X)。
[basis 1] and [basis 2] 's.

### 4 : limitations and outlook
papersresearch items's limitations.
 [limitations 1]、 [limitations 2].
 ['s researchdirection] and 、
[] and 。

### 5 : conclusion
above/more's resultsfrom、[keyconclusion] 。
papersresearch [min] in [/significance] is providedalso 's.
```

### 4. figures/tables's reference

```markdown
## figures/tablesreference's formula

| | figure's reference | table's reference | figure |
|---|---|---|---|
| Nature system | Fig. 1a | Table 1 | Extended Data Fig. 1 |
| Science system | Fig. 1A | Table 1 | fig. S1 |
| ACS system | Figure 1a | Table 1 | Figure S1 |
| IEEE system | Fig. 1(a) | TABLE I | — |
| Elsevier system | Fig. 1(a) | Table 1 | Fig. S1 |
| IMRaD standard | Figure 1 | Table 1 | Supplementary Figure S1 |

## figures/tables's
**Figure **: figureall's（）。
and 's (a)..., (b)..., (c)...

**Table **: table's 。content 。
table's noteas。
```

### 5. citationreferenceliterature's formula

```markdown
## citationlist

### Nature system（number）
papers: "... has been reported¹."
literature: 1. Author, A. B., Author, C. D. & Author, E. F.
 Title of article. *Journal* **vol**, pages (year).

### Science system（number）
papers: "... has been reported (1)."
literature: 1. A. B. Author, C. D. Author, E. F. Author,
 Title of article. *Journal* **vol**, pages (year).

### ACS system（number、）
papers: "... has been reported.¹"
literature: (1) Author, A. B.; Author, C. D.; Author, E. F.
 Title of Article. *Journal* **year**, *vol*, pages.

### IEEE system（number）
papers: "... has been reported [1]."
literature: [1] A. B. Author, C. D. Author, and E. F. Author,
 "Title of article," *Journal*, vol. X, no. Y, pp. XX-YY, year.

### Elsevier system（author-）
papers: "... has been reported (Author et al., 2024)."
literature: Author, A.B., Author, C.D., Author, E.F., 2024.
 Title of article. Journal Vol, pages.
```

### 6. Cover Letter template

```markdown
Dear Editor,

We are pleased to submit our manuscript entitled "[title]" for
consideration for publication in [].

[1-2 researchbackground and motivation]

In this study, we [research's key].
Our key findings include:
(1) [key 1],
(2) [key 2], and
(3) [key 3].

These results [research's significance], which we believe will be of
significant interest to the readership of [].

This manuscript has not been published or submitted elsewhere.
All authors have approved the manuscript and agree with its submission
to []. We declare no competing interests.

We suggest the following reviewers:
1. Prof. [Name], [Affiliation] ([email])
2. Prof. [Name], [Affiliation] ([email])
3. Prof. [Name], [Affiliation] ([email])

Thank you for your consideration.

Sincerely,
[Corresponding Author Name]
[Affiliation]
[Email]
```

### 7. Response to Reviewers template

```markdown
# Response to Reviewers

We thank the reviewers for their constructive comments, which have
significantly improved our manuscript. Below we address each comment
point by point. Reviewer comments are shown in **bold**, and our
responses follow each comment. Changes in the revised manuscript
are highlighted in blue.

---

## Reviewer 1

**Comment 1**: ['s 'scitation]

**Response**: We thank the reviewer for this insightful comment.
[times's content]
We have revised the manuscript accordingly (page X, lines YY-ZZ).

> **Revised text**: "[fix'scitation]"

---

**Comment 2**: []

**Response**: [times]

---

## Reviewer 2

**Comment 1**: []

**Response**: [times]
```

### 8. figure'sworkflow

paper、analysis generationfigure。`figures/` directory 
savefile automated、Markdown 's papersinsertion.

```markdown
## figure's

### basicprocedure
1. `figures/` directory、generation'sfilelist is retrieved
2. eachfigure Results 's `![Figure N](figures/filename.png)` 
3. Figure Captions / Figure Legends also same
4. Supplementary 's figure `![Figure SN](figures/filename.png)` 

### 

#### papers（Results ）
- results's and figure
- figure's

![Figure 1](figures/fig1_overview.png)
**Figure 1.** [figure's]

#### figure
- composite figure 1 items's as
- 's (a), (b), (c) 

![Figure 2](figures/fig2_composite.png)
**Figure 2.** [figureall's 。]
(a) [ a]。(b) [ b]。(c) [ c]。

### 'sfigurereference + 

| | example |
|---|---|
| Nature system | `![Fig. 1](figures/fig1.png)` + `**Fig. 1 \| [title].**` |
| Science system | `![Fig. 1](figures/fig1.png)` + `**Fig. 1. [title].**` |
| ACS system | `![Figure 1](figures/figure1.png)` + `**Figure 1.** []` |
| IEEE system | `![Fig. 1](figures/fig1.png)` + `**Fig. 1.** []` |
| Elsevier system | `![Fig. 1](figures/fig1.png)` + `**Fig. 1.** []` |
| Qiita | `![](./figures/Fig1_description.png)` |

### figures/ directory's

paperwriting、below/following's procedure figure:
1. 's `figures/` directory search
2. `.png`, `.svg`, `.pdf` file listretrieval
3. filefromfigurenumbercontent（example: `violin_hardness.png` → 's Violin Plot）
4. Results 's Figure number
5. papers's 、generation
```

### 9. AI for (AI Usage Disclosure)

'sgeneration AI 's for.
AI 's items 、**authoras**。

```markdown
## AI for's（）

| | | |
|---|---|---|
| Nature system | Methods | required (2023〜) |
| Science system | Acknowledgements | required |
| ACS system | Methods or Acknowledgements | recommended |
| IEEE system | Acknowledgements | recommended |
| Elsevier system | for AI Disclosure | required (2024〜) |
```

#### AI fortemplate

**caution**: number package.json fromretrieves and。

```markdown
## Methods （Nature system）

**Use of AI tools**: This study used GitHub Copilot Agent with SATORI
skills (v{package.json 's version}) for [for: data analysis /
figure generation / manuscript drafting / literature review].
All AI-generated content was reviewed and verified by the authors,
who take full responsibility for the content of this publication.

## Acknowledgements（Science / ACS / IEEE system）

The authors acknowledge the use of GitHub Copilot Agent with SATORI
skills (v{package.json 's version}) for [for].
All outputs were critically reviewed and validated by the authors.

## AI Disclosure （Elsevier system）

During the preparation of this work, the authors used GitHub Copilot
Agent with SATORI skills (v{package.json 's version}) for [for].
After using this tool, the authors reviewed and edited the content as
needed and take full responsibility for the content of the publication.
```

#### Authors 's

```markdown
## AI 's caution

❌ prohibited: AI toolas
 (ICMJE : necessary)

❌ error:
 Author A¹, GitHub Copilot Agent (SATORI v0.3.0)¹, Author B²

✅ correct:
 Author A¹*, Author B²
 （AI for Methods / Acknowledgements / AI Disclosure ）
```

### 10. Supplementary Information configuration

```markdown
## Supplementary Information template

# Supplementary Information for:
# [papertitle]

[author]

## Supplementary Figures

**Figure S1.** []

**Figure S2.** []

## Supplementary Tables

**Table S1.** []

## Supplementary Methods

### S1. [additionexperimentmethod'sdetails]

### S2. [additionanalysismethod'sdetails]

## Supplementary References

[SI 's citationliterature]
```

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

## References

### Output Files

| File | Format |
|---|---|
| `manuscript/manuscript.md` | Markdown |
| `manuscript/figures/` | figures/tablesdirectory |
| `manuscript/supplementary.md` | information |
| `manuscript/cover_letter.md` | |
| `manuscript/response_to_reviewers.md` | times |

### templatefile (assets/)

| file | support |
|---|---|
| `assets/imrad_standard.md` | IMRaD standardshapeformula |
| `assets/nature_article.md` | Nature / Nature Communications |
| `assets/science_research_article.md` | Science / Science Advances |
| `assets/acs_article.md` | ACS Nano / JACS / Chem. Mater. |
| `assets/ieee_transactions.md` | IEEE Transactions |
| `assets/elsevier_article.md` | Elsevier system |
| `assets/qiita_technical_article.md` | Qiita （AI for Science ） |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-hypothesis-pipeline` | `docs/hypothesis.md` load、Introduction 's researchhypothesisMethods 's analysisdesign automated |
| `scientific-critical-review` | 's cell。recommended |
| `scientific-publication-figures` | `figures/` 's figures/tables |
| `scientific-pipeline-scaffold` | `results/analysis_summary.json` fromnumber/countvalueresultsreference |
| `scientific-statistical-testing` | 's for |

### Position in the Pipeline

```
hypothesis-pipeline → pipeline-scaffold → academic-writing → critical-review
 (hypothesisdefinition) (analysis)  (fix)
```

paperwritingbelow/following's file reference:
- `docs/hypothesis.md` — hypothesisdefinition（Introduction / Methods ）
- `docs/workflow_design.md` — analysisworkflow（Methods ）
- `results/analysis_summary.json` — analysisresultssummary（Results ）
- `figures/*.png` — figures/tables（papers `![Figure N](figures/...)` ）
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Writing/Review)

Before execution, define:
- [ ] **Target venue**: journal name, word/page limit, citation style
- [ ] **Document structure**: required sections (IMRaD / custom)
- [ ] **Quality standard**: PRISMA / CONSORT / ARRIVE as applicable
- [ ] **Completeness check**: all required sections present

#### Pass Criteria
- All citations verifiable (DOI or PMID present)
- No placeholder text remaining ([TODO], [CITE], etc.)
- Figure/table references match actual figures/tables
- Word count within target range
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
