---
name: scientific-presentation-design
description: |
 presentationposterschematic diagramdesignskill。conferencepresentationslide、
 LaTeX/PPTX poster、schematic diagram（workflowfigurefigure）、
 visual abstract'ssupport。claude-scientific-skills 's 
 Scientific Communication （slides, posters, schematics） integration。
 「conferenceslide」「poster's layout design」 。
tu_tools:
 - key: biotools
 name: bio.tools
 description: presentationvisualizationtoolsearch
---

# Scientific Presentation Design

presentation's designskill。conferencepresentationslide、
poster（LaTeX/PPTX）、schematic diagram（pathway/mechanism figure）、
visual abstract's is supported。

## When to Use

- conferencepresentationfor's slide is createdand
- conferenceposter's layout is designedand
- paper's Graphical Abstract is createdand
- figureworkflowfigure and
- research'ssummary is createdand

## Quick Start

### presentationdesignpipeline

```
Input: researchcontent / conference / presentationshapeformula
 ↓
Step 1: Structure Design
 - storylineconstruction
 - configuration
 - timemin（oral case）
 ↓
Step 2: Visual Design
 - color paletteselection
 - fontsettings
 - layoutgrid
 ↓
Step 3: Content Creation
 - text block
 - figures/tables
 - schematic diagram
 ↓
Step 4: Polish
 - consistency check
 - accessibilityverification
 - export
 ↓
Output: Slides / Poster / Schematic
```

---

## Phase 1: Conference Slide Design

### Standard Composition Template

```markdown
## Oral Presentation Structure (15 min)

### Slide 1: Title (0:00 - 0:30)
- title / author / affiliation
- 1 sentence hook

### Slides 2-3: Background (0:30 - 2:30)
- research's contextresearch
- Knowledge gap 's explicit

### Slide 4: Research Question (2:30 - 3:30)
- clear RQ / hypothesis
- papersresearch's purpose

### Slides 5-7: Methods (3:30 - 6:00)
- experiment
- analysismethod
- workflowfigure

### Slides 8-11: Results (6:00 - 11:00)
- keyresults（1 slide = 1 message）
- figures/tables、
- value explicit

### Slide 12: Discussion (11:00 - 13:00)
- results's
- research and 'scomparison
- limitations

### Slide 13: Conclusions (13:00 - 14:00)
- Take-home message（3 point）
- Future directions

### Slide 14: Acknowledgments (14:00 - 14:30)
- research / Funding

### Slide 15: Q&A / Backup
```

### Slide Design Rules

```python
SLIDE_DESIGN_RULES = {
 "fonts": {
 "title": {"family": "Arial/Helvetica", "size": 28, "weight": "bold"},
 "body": {"family": "Arial/Helvetica", "size": 20, "weight": "normal"},
 "caption": {"family": "Arial/Helvetica", "size": 16, "weight": "normal"},
 },
 "colors": {
 "scientific_blue": ["#1B365D", "#2E5090", "#4A7FB5", "#8CB4D6", "#C5DAE9"],
 "nature_green": ["#1B4332", "#2D6A4F", "#40916C", "#74C69D", "#B7E4C7"],
 "warm_red": ["#6A040F", "#9D0208", "#D00000", "#DC2F02", "#E85D04"],
 },
 "layout": {
 "margin": "0.5 inch all sides",
 "max_bullets": 5,
 "max_words_per_slide": 40,
 "figure_ratio": 0.6, # figure's surface 60% above/more
 },
 "accessibility": {
 "min_contrast_ratio": 4.5,
 "colorblind_safe_palette": True,
 "alt_text_for_figures": True,
 },
}
```

---

## Phase 2: Poster Design

### LaTeX Poster Template

```latex
\\documentclass[25pt, a0paper, portrait]{tikzposter}
\\usepackage[utf8]{inputenc}

\\title{\\parbox{\\linewidth}{\\centering
 Research Title Goes Here: \\\\
 A Comprehensive Study
}}
\\author{Author A$^1$, Author B$^{1,2}$}
\\institute{$^1$Institution, $^2$Institution}

\\usetheme{Default}
\\usecolorstyle{Britain}

\\begin{document}
\\maketitle

\\begin{columns}
\\column{0.33}
\\block{Background}{
 % backgroundresearch
}
\\block{Methods}{
 % method（workflowfigurerecommended）
}

\\column{0.34}
\\block{Results}{
 % keyresultsfigures/tables
}

\\column{0.33}
\\block{Discussion}{
 % discussion
}
\\block{Conclusions}{
 % conclusion（3 bullet points）
}
\\block{References}{
 % citationliterature（）
}
\\end{columns}

\\end{document}
```

### Poster Layout Principles

```markdown
## Poster Design Principles

### Layout
- 3-column or 2-column layout
- : →、→
- 's clear
- header（title + author） 15%

### Typography
- Title: 72-96 pt
- Section headers: 48-60 pt
- Body text: 28-36 pt
- 3 and

### Figures
- degree (300+ DPI)
- （postersurface's 40-50%）
- 
- color

### Content
- Introduction: 150-200 words
- Methods: figure（）
- Results: figure
- Conclusions: 3-5 bullet points
- References: 5-10 citations max
```

---

## Phase 3: schematic diagram

### Mermaid-Based Schematics

```markdown
## schematic diagram

### 1. workflowfigure
step's pipeline

### 2. figure
molecule's figure

### 3. experimentfigure
experimentgroup's condition

### 4. Graphical Abstract
paperall 1 sheets
```

```python
# matplotlib 'sschematic diagramgeneration
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_workflow_schematic(steps, title="Workflow"):
 """
 workflowschematic diagram's automatedgeneration。
 """
 fig, ax = plt.subplots(1, 1, figsize=(12, len(steps) * 1.5 + 2))
 ax.set_xlim(0, 10)
 ax.set_ylim(0, len(steps) * 2 + 1)
 ax.axis('off')

 colors = plt.cm.Blues(np.linspace(0.3, 0.8, len(steps)))

 for i, (step_name, description) in enumerate(steps):
 y = len(steps) * 2 - i * 2
 # Box
 rect = mpatches.FancyBboxPatch(
 (1, y - 0.5), 8, 1.2,
 boxstyle="round,pad=0.1",
 facecolor=colors[i], edgecolor='#333333', linewidth=1.5
 )
 ax.add_patch(rect)
 ax.text(5, y + 0.1, step_name, ha='center', va='center',
 fontsize=14, fontweight='bold', color='white')
 ax.text(5, y - 0.25, description, ha='center', va='center',
 fontsize=10, color='white', style='italic')
 # Arrow
 if i < len(steps) - 1:
 ax.annotate('', xy=(5, y - 0.7), xytext=(5, y - 0.5),
 arrowprops=dict(arrowstyle='->', color='#333333', lw=2))

 ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
 plt.tight_layout
 return fig
```

---

## Report Template

```markdown
# Presentation Design: [Title]

**Format**: [Oral / Poster / Graphical Abstract]
**Venue**: [Conference / Journal]
**Date**: [date]

## 1. Story Arc
## 2. Design Specifications
| Element | Value |
|---------|-------|
| Format | |
| Dimensions | |
| Color palette | |
| Font family | |

## 3. Section Outline
## 4. Figures Required
## 5. Generated Files
- [ ] slides.pptx / slides.tex
- [ ] poster.pdf / poster.tex
- [ ] figures/*.svg
```

---

## Completeness Checklist

- [ ] Storyline: clear logical flow
- [ ] Design: color palette selection, font consistency
- [ ] Figures: high resolution, color-blind friendly
- [ ] Text: minimal, 1 slide = 1 message
- [ ] Accessibility: contrast ratio ≥ 4.5
- [ ] Export: PDF + source files

## Best Practices

1. **1 Slide = 1 Message**: avoid information overload
2. **figure > **: 
3. **color**: viridis/cividis systemrecommended
4. **3 **: posterfrom and
5. **10-20-30 **: 10 slides, 20 min, 30pt font (Kawasaki)

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | presentationvisualizationtoolsearch |

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `presentation/slides.md` | presentation（Markdown） | slideconfigurationcompletion |
| `presentation/poster.tex` | postertemplate（LaTeX） | Poster Designcompletion |
| `figures/workflow_schematic.png` | workflowschematic diagram（PNG） | figures/tablesgenerationcompletion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-publication-figures` | ← Figure generationcolor palette |
| `scientific-academic-writing` | ← research |
| `scientific-clinical-decision-support` | ← results's presentation |
| `scientific-latex-formatter` | ← LaTeX support |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Visualization)

Before execution, define:
- [ ] **Target audience**: journal / conference / dashboard / internal
- [ ] **Figure dimensions**: width x height, DPI requirement
- [ ] **Color scheme**: colorblind-safe palette confirmed
- [ ] **Data-ink ratio**: minimize non-data elements

#### Pass Criteria
- All figures saved to disk (never plt.show())
- Figures embedded in report.md with captions
- Text is English-only, font size >= 8pt
- Accessibility: contrast ratio >= 4.5:1
- Vector format (SVG/PDF) provided when requested
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
