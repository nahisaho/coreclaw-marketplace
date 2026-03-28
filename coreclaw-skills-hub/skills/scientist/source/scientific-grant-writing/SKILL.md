---
name: scientific-grant-writing
description: |
 research（）writingskill。NIH R01/R21、NSF、JSPS 、
 ERC 'ssupport。Specific Aims、Research Strategy、design、
 Biosketch 's structuresupport。
 「 」「 」「Specific Aims 」 。
---

# Scientific Grant Writing

research'swritingsupportskill。key
（NIH、NSF、JSPS、ERC）'s 's
structure is supported。

## When to Use

- research's is createdand
- Specific Aims configurationwhen needed
- Research Strategy structurewhen needed
- design（Budget Justification） is createdand
- 's and

## Quick Start

### writingpipeline

```
Step 1: Funder Selection & Format
 - 'sselection
 - （NIH R01, R21, JSPS A, etc.）
 - /'sverification
 ↓
Step 2: Specific Aims
 - Opening paragraph ('s)
 - Aims (2-3 aims, measurementpossible)
 - Impact statement
 ↓
Step 3: Research Strategy
 - Significance
 - Innovation
 - Approach (per aim)
 ↓
Step 4: Supporting Documents
 - Budget & Justification
 - Biosketch / research
 - Facilities & Equipment
 - Letters of Support
 ↓
Output: Complete Grant Application
```

---

## Phase 1: Specific Aims 

### NIH Specific Aims template

```markdown
## Specific Aims (1 page)

### Opening Paragraph
[problem's important → 's → 's → 's important]

**typetemplate:**
"[Disease/Problem] affects [X million] people annually, resulting in [consequence].
Current approaches [limitation]. Our preliminary data show [finding],
suggesting that [hypothesis]. However, [gap]. This gap is critical because [reason]."

### Long-term Goal & Objective
"The long-term goal of this project is to [broad vision].
The objective of this application is to [specific, achievable goal].
Our central hypothesis is that [testable hypothesis],
based on [preliminary data / rationale]."

### Specific Aims

**Aim 1: [Action verb] + [measurable outcome]**
[2-3 sentences describing the aim, approach, and expected outcome]
Working hypothesis: [specific to this aim]

**Aim 2: [Action verb] + [measurable outcome]**
[2-3 sentences describing the aim, approach, and expected outcome]
Working hypothesis: [specific to this aim]

**Aim 3 (optional): [Action verb] + [measurable outcome]**
[2-3 sentences]

### Impact Statement
"Upon completion, this project will [expected outcome].
This contribution is significant because [reason].
The proposed research is innovative because [novel aspect]."
```

---

## Phase 2: Research Strategy

### Significance / Innovation / Approach

```markdown
## Research Strategy (12 pages for NIH R01)

### A. Significance (2-3 pages)
#### A.1 Importance of the Problem
#### A.2 Scientific Premise
 - Rigor of prior research (strengths & weaknesses)
 - How this proposal addresses gaps
#### A.3 Impact if Successful

### B. Innovation (1-2 pages)
#### B.1 Conceptual Innovation
 - New paradigm / model / theory
#### B.2 Technical Innovation
 - New methods / tools / approaches
#### B.3 Application Innovation
 - New applications / fields

### C. Approach (7-8 pages)
#### C.1 Overview & Rationale
#### C.2 Preliminary Data
 - Figures with quality data
 - Demonstrates feasibility

#### C.3 Aim 1: [Title]
 - Rationale
 - Experimental Design
 - Variables (independent, dependent, controlled)
 - Sample size justification (power analysis)
 - Controls (positive, negative)
 - Methods
 - Expected Outcomes
 - Potential Problems & Alternative Strategies
 - Timeline

#### C.4 Aim 2: [Title]
 ['sconfiguration]

#### C.5 Rigor & Reproducibility
 - Biological variables (sex, age, strain)
 - Statistical approach
 - Data management plan
 - Authentication of key resources

#### C.6 Timeline
| Activity | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|----------|--------|--------|--------|--------|--------|
| Aim 1 | ████ | ██ | | | |
| Aim 2 | | ██ | ████ | ██ | |
| Aim 3 | | | | ██ | ████ |
```

---

## Phase 3: JSPS template

### researchpurposeresearchdesignresearch

```markdown
## JSPS formula

### 1. researchpurpose、researchmethodetc.（overview）
[400: research's all]

### 2. papersresearch's background
- 「」
- 's research and papersresearch's positioning
- to/until's research

### 3. research's purpose and method
[researchpurpose → method → ]

### 4. research's
- 's method selection
- research and 's
- novel

### 5. papersresearchto/untiland 's
[target]

### 6. researchdesign
| degree | researchcontent | （）|
|------|----------|-----------|

### 7. research
[ORCID / Google Scholar fromautomatedretrievalpossible]
```

---

## Phase 4: Budget Planning

### designtemplate

```python
def create_budget_plan(total_budget, duration_years, personnel_pct=0.60):
 """
 research's designtemplategeneration。
 NIH support。
 """
 budget = {
 "total": total_budget,
 "duration": duration_years,
 "annual": total_budget / duration_years,
 "categories": {
 "personnel": total_budget * personnel_pct,
 "equipment": total_budget * 0.10,
 "supplies": total_budget * 0.15,
 "travel": total_budget * 0.05,
 "other": total_budget * 0.05,
 "indirect": total_budget * 0.05,
 }
 }
 return budget

BUDGET_JUSTIFICATION_TEMPLATE = """
## Budget Justification

### A. Senior/Key Personnel
- PI ([Name]): X calendar months effort @ [salary]
 Justification: [role in project]

### B. Other Personnel
- Postdoctoral researcher: 12 calendar months @ [salary]
 Justification: [specific tasks]

### C. Equipment (>$5,000)
- [Equipment name]: $[cost]
 Justification: [why needed, no alternative]

### D. Travel
- Domestic conference: $[cost] x [#]
 Justification: [dissemination]
- International collaboration: $[cost]

### E. Supplies
- Reagents: $[cost]
- Computing: $[cost]

### F. Other Direct Costs
"""
```

---

## Report Template

```markdown
# Grant Application: [Title]

**Funder**: [NIH / NSF / JSPS / ERC]
**Category**: [R01 / B / etc.]
**PI**: [Name]
**Date**: [date]

## Document Checklist
- [ ] Specific Aims (1 page)
- [ ] Research Strategy (12 pages)
- [ ] Budget & Justification
- [ ] Biosketch
- [ ] Facilities & Equipment
- [ ] Data Management Plan
- [ ] Letters of Support
```

---

## Completeness Checklist

- [ ] Specific Aims: → hypothesis → Aims → 
- [ ] Research Strategy: Significance + Innovation + Approach
- [ ] Preliminary Data: ≥2 figures showing feasibility
- [ ] Power Analysis: sample size's basis
- [ ] Alternative Strategy: each Aim Plan B 
- [ ] Budget: 's min
- [ ] Timeline: all Aim 's Gantt chart

## Best Practices

1. **Reviewer 's point**: 's also
2. **Specific Aims **: 1 Aim 's failure alldesign
3. **Preliminary Data **: Feasibility 's rate
4. **'s 95% **: 's also point
5. **Broader Impacts **: 's（NSF）

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `grants/specific_aims.md` | Specific Aims （Markdown） | Aims completion |
| `grants/research_strategy.md` | Research Strategy（Markdown） | allcompletion |
| `grants/budget.json` | design（JSON） | completion |

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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-research-methodology` | ← researchmethod'sproviding |
| `scientific-hypothesis-pipeline` | ← hypothesisdefinitionchallengesettings |
| `scientific-deep-research` | ← literatureresearchinvestigation |
| `scientific-academic-writing` | ← skill |
| `scientific-scientific-schematics` | ← researchdesignfigurefiguregeneration |
| `scientific-regulatory-science` | ← |
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
  |-- Generate report.md with all sections in the user's input language
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
| G5 | All figure/table text is English-only; report.md body matches the user's input language | MUST |
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
