---
name: scientific-latex-export
description: |
 experimentresults papershapeformula（LaTeX / IMRaD）exportskill。
 IntroductionMaterials & MethodsResultsDiscussion 's structure
 publicationfor'sautomatedgenerates。
 「paper」「LaTeXoutput」「publication」 。
---

# Scientific LaTeX Export

experimentresults papershapeformula（IMRaD: Introduction, Materials & Methods,
Results, Discussion）structure、LaTeX is generatedskill。

## When to Use

- experimentresults papershapeformula and and
- conferencepresentationfor's is createdand
- research and publicationforwhen needed
- arXiv / bioRxiv to 'swhen needed

## Quick Start

### Step 1: experimentdata's
- experiment's
- generation（CSV,, report）
- forskilltool's

### Step 2: IMRaD structureto 'stransformation
1. **Title & Abstract** — research's（250）
2. **Introduction** — backgroundpurposehypothesis
3. **Materials & Methods** — experimentconditionmethodanalysismethod
4. **Results** — datafigures/tables's
5. **Discussion** — results's research and 's comparisonlimitations
6. **References** — citationliterature（BibTeXshapeformula）

### Step 3: figures/tables's shape
- matplotlib / R 's figure publication-quality 
- table LaTeX tabular shapeformulatransformation
- 's

### Step 4: LaTeX generation

## Output Format

```markdown
paper.tex # LaTeX file
paper.bib # BibTeX referenceliterature
figures/ # figurefile
```

### LaTeX templatestructure:
```latex
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx, amsmath, booktabs, hyperref}
\usepackage[japanese]{babel} % paperssupport

\title{...}
\author{...}
\date{\today}

\begin{document}
\maketitle
\begin{abstract}... \end{abstract}

\section{Introduction}
\section{Materials and Methods}
\section{Results}
\section{Discussion}
\section*{Acknowledgments}

\bibliographystyle{unsrt}
\bibliography{paper}
\end{document}
```

## Examples

- 「's experimentresults paper」
- 「IMRaDshapeformula LaTeXoutput」
- 「bioRxivfor's」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | reference metadata/DOI resolution |
---

## Harness Optimization (v0.4.0)

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
