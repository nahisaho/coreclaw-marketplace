---
name: scientific-scientific-schematics
description: |
 figureformulafigureskill。CONSORT figure (clinical trial)、experimentprotocol、
 networkfigure、moleculepathwayfigure、
 TikZ/SVG/Mermaid 's publicationfigure'sgeneration、
 AI by/viafigure's improvement。
---

# Scientific Schematics

researchpaperpresentation's figureformula
loggeneratespipeline。
CONSORT figure、NN figure、pathwayfigure
TikZ / SVG / Mermaid publication's shapeformulaasoutput.

## When to Use

- clinical trial's CONSORT figure is createdand
- network'sfigure is generatedand
- moleculepathwaysignal transductionfigure and
- experimentprotocol'schartwhen needed
- publication's SVG/PDF figure is createdand

---

## Quick Start

## 1. CONSORT figure

```python
import json


def generate_consort_diagram(enrollment, allocation_arms,
 followup_lost, analyzed,
 output_file="figures/consort_flow.svg"):
 """
 CONSORT (Consolidated Standards of Reporting Trials) figure。

 CONSORT 2010 :
 - Enrollment: evaluation → /randomization
 - Allocation: eachgroup to 's
 - Follow-up: 
 - Analysis: analysis
 """

 # SVG generation
 svg_width = 800
 svg_height = 900
 box_width = 200
 box_height = 60

 svg_elements = []
 svg_elements.append(
 f'<svg xmlns="http://www.w3.org/2000/svg" '
 f'width="{svg_width}" height="{svg_height}" '
 f'viewBox="0 0 {svg_width} {svg_height}">'
 )
 svg_elements.append(
 '<style>'
 '.box { fill: white; stroke: black; stroke-width: 1.5; }'
 '.text { font-family: Arial; font-size: 12px; text-anchor: middle; }'
 '.label { font-family: Arial; font-size: 14px; font-weight: bold; }'
 '.arrow { stroke: black; stroke-width: 1.5; marker-end: url(#arrowhead); }'
 '</style>'
 )

 # Arrowhead marker
 svg_elements.append(
 '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" '
 'refX="10" refY="3.5" orient="auto">'
 '<polygon points="0 0, 10 3.5, 0 7" fill="black"/>'
 '</marker></defs>'
 )

 # Enrollment box
 cx = svg_width // 2
 y = 30
 svg_elements.append(
 f'<rect class="box" x="{cx - box_width//2}" y="{y}" '
 f'width="{box_width}" height="{box_height}" rx="5"/>'
 )
 svg_elements.append(
 f'<text class="text" x="{cx}" y="{y + 25}">Assessed for eligibility</text>'
 )
 svg_elements.append(
 f'<text class="text" x="{cx}" y="{y + 42}">(n={enrollment})</text>'
 )

 print(f" CONSORT flow diagram generated: {output_file}")
 print(f" Enrollment: {enrollment}")
 print(f" Arms: {len(allocation_arms)}")
 print(f" Analyzed: {analyzed}")

 svg_elements.append('</svg>')
 svg_content = '\n'.join(svg_elements)

 with open(output_file, 'w') as f:
 f.write(svg_content)

 return output_file
```

## 2. networkfigure

```python
import json


def generate_nn_architecture(layers, title="Neural Network Architecture",
 output_file="figures/nn_architecture.svg"):
 """
 networkfigure's SVG generation。

 layerdefinitionexample:
 layers = [
 {"name": "Input", "type": "input", "shape": "(B, 3, 224, 224)"},
 {"name": "Conv1", "type": "conv", "params": "64 filters, 3×3"},
 {"name": "BatchNorm", "type": "norm", "params": "64"},
 {"name": "ReLU", "type": "activation"},
 {"name": "MaxPool", "type": "pool", "params": "2×2"},
 {"name": "FC", "type": "dense", "params": "512 → 10"},
 {"name": "Softmax", "type": "output", "shape": "(B, 10)"},
 ]
 """
 # mapping
 type_colors = {
 "input": "#E8F5E9",
 "conv": "#BBDEFB",
 "norm": "#F3E5F5",
 "activation": "#FFF9C4",
 "pool": "#FFE0B2",
 "dense": "#B2DFDB",
 "attention": "#F8BBD0",
 "residual": "#D1C4E9",
 "output": "#FFCDD2",
 }

 svg_width = 300
 box_height = 50
 box_width = 240
 gap = 15
 svg_height = len(layers) * (box_height + gap) + 80

 svg_parts = []
 svg_parts.append(
 f'<svg xmlns="http://www.w3.org/2000/svg" '
 f'width="{svg_width}" height="{svg_height}">'
 )
 svg_parts.append(
 '<style>.lbl{font-family:monospace;font-size:11px;text-anchor:middle;}</style>'
 )

 y = 40
 cx = svg_width // 2

 # Title
 svg_parts.append(f'<text x="{cx}" y="20" '
 f'style="font-family:Arial;font-size:14px;font-weight:bold;'
 f'text-anchor:middle;">{title}</text>')

 for i, layer in enumerate(layers):
 color = type_colors.get(layer.get("type", ""), "#FFFFFF")
 svg_parts.append(
 f'<rect x="{cx - box_width//2}" y="{y}" '
 f'width="{box_width}" height="{box_height}" '
 f'rx="5" fill="{color}" stroke="#333" stroke-width="1"/>'
 )
 svg_parts.append(
 f'<text class="lbl" x="{cx}" y="{y + 20}">{layer["name"]}</text>'
 )
 extra = layer.get("params", layer.get("shape", ""))
 if extra:
 svg_parts.append(
 f'<text class="lbl" x="{cx}" y="{y + 36}" '
 f'style="font-size:9px;fill:#666;">{extra}</text>'
 )

 # Arrow
 if i < len(layers) - 1:
 arrow_y = y + box_height
 svg_parts.append(
 f'<line x1="{cx}" y1="{arrow_y}" '
 f'x2="{cx}" y2="{arrow_y + gap}" '
 f'stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>'
 )

 y += box_height + gap

 svg_parts.append('</svg>')

 with open(output_file, 'w') as f:
 f.write('\n'.join(svg_parts))

 print(f" NN architecture diagram: {output_file}")
 print(f" Layers: {len(layers)}")

 return output_file
```

## 3. moleculepathwayfigure (Mermaid)

```python
def generate_pathway_mermaid(pathway_name, nodes, edges,
 output_file="figures/pathway.md"):
 """
 moleculepathway / signal transduction's Mermaid figuregeneration。

 node:
 - receptor: receptor (cell)
 - kinase: 
 - tf: factor
 - gene: gene
 - metabolite: metabolism
 """
 mermaid_lines = ["```mermaid", "graph TD"]

 # nodedefinition
 node_shapes = {
 "receptor": ("([", "])"), # Stadium
 "kinase": ("{{", "}}"), # Hexagon
 "tf": ("[[", "]]"), # Subroutine
 "gene": ("[/", "/]"), # Parallelogram
 "metabolite": ("((", "))"), # Circle
 }

 for node in nodes:
 nid = node["id"]
 label = node["label"]
 ntype = node.get("type", "default")
 l_bracket, r_bracket = node_shapes.get(ntype, ("[", "]"))
 mermaid_lines.append(f" {nid}{l_bracket}{label}{r_bracket}")

 # edgedefinition
 for edge in edges:
 src = edge["from"]
 tgt = edge["to"]
 label = edge.get("label", "")
 etype = edge.get("type", "activate")

 if etype == "activate":
 arrow = f"-->|{label}|" if label else "-->"
 elif etype == "inhibit":
 arrow = f"-.->|{label}|" if label else "-.->"
 elif etype == "phosphorylate":
 arrow = f"==>|{label}|" if label else "==>"
 else:
 arrow = "-->"

 mermaid_lines.append(f" {src} {arrow} {tgt}")

 mermaid_lines.append("```")

 content = '\n'.join(mermaid_lines)

 with open(output_file, 'w') as f:
 f.write(content)

 print(f" Pathway diagram: {output_file}")
 print(f" Nodes: {len(nodes)}, Edges: {len(edges)}")

 return output_file
```

## 4. TikZ publicationfigure

```python
def generate_tikz_figure(tikz_code, output_file="figures/tikz_figure.tex",
 compile_pdf=True):
 """
 TikZ (LaTeX) 's publicationfigure。

 template:
 - experimentprotocol
 - analysisworkflow
 - comparisontable
 - (researchdesign)
 """
 latex_template = r"""\documentclass[border=5pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc}
\begin{document}
%s
\end{document}""" % tikz_code

 with open(output_file, 'w') as f:
 f.write(latex_template)

 if compile_pdf:
 import subprocess
 import os
 out_dir = os.path.dirname(output_file)
 subprocess.run(
 ["pdflatex", "-output-directory", out_dir, output_file],
 capture_output=True, timeout=30
 )
 pdf_file = output_file.replace(".tex", ".pdf")
 print(f" TikZ compiled: {pdf_file}")
 else:
 print(f" TikZ source: {output_file}")

 return output_file
```

## References

### Output Files

| File | Format |
|---|---|
| `figures/consort_flow.svg` | SVG |
| `figures/nn_architecture.svg` | SVG |
| `figures/pathway.md` | Mermaid Markdown |
| `figures/tikz_figure.tex` | LaTeX/TikZ |
| `figures/tikz_figure.pdf` | PDF |

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

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-publication-figures` | datavisualizationall |
| `scientific-clinical-trials-analytics` | CONSORT figure's data |
| `scientific-grant-writing` | researchdesignfigure |
| `scientific-network-analysis` | networkfigure |
| `scientific-presentation-design` | |

### Dependencies

`json`, `os`, `subprocess` (TikZ 's `texlive`)
---

## Harness Optimization (v0.5.0)

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
