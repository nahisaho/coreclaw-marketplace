---
name: scientific-reproducible-reporting
description: |
 possibleskill。Quarto 
 Jupyter Book configurationPapermill 
 nbconvert automatedtransformationSphinx-Gallery example。
---

# Scientific Reproducible Reporting

possiblereportgenerationpipeline providing、
 → → 's automated.

## When to Use

- Quarto possible is createdand
- Jupyter Book configuration's is builtand
- Papermill automatedwhen needed
- nbconvert eachtypeshapeformulatransformationwhen needed
- CI/CD analysisreportautomatedgenerationwhen needed
- multipleparameters analysiswhen needed

---

## Quick Start

## 1. Quarto template

```python
import os


def generate_quarto_document(title="Scientific Analysis Report",
 author="SATORI",
 format_type="html",
 output_dir="quarto_project"):
 """
 Quarto templategeneration。

 Parameters:
 title: str — title
 author: str — author
 format_type: str — "html" / "pdf" / "docx" / "revealjs"
 output_dir: str — output directory
 """
 os.makedirs(output_dir, exist_ok=True)

 # _quarto.yml
 quarto_config = f"""project:
 type: default
 output-dir: _output

format:
 {format_type}:
 toc: true
 toc-depth: 3
 number-sections: true
 code-fold: true
 code-tools: true
 theme: cosmo

execute:
 echo: true
 warning: false
 cache: true

bibliography: references.bib
csl: nature.csl
"""

 # 
 main_qmd = f"""---
title: "{title}"
author: "{author}"
date: today
format:
 {format_type}:
 code-fold: true
 code-tools: true
jupyter: python3
---

## 

's report SATORI skillusingpossibleanalysis。

```{{python}}
#| label: setup
#| echo: false

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# parameters (Papermill )
n_samples = 1000
random_seed = 42
```

## dataoverview

```{{python}}
#| label: data-summary
#| tbl-cap: "datasetoverview"

np.random.seed(random_seed)
df = pd.DataFrame({{
 "x": np.random.randn(n_samples),
 "y": np.random.randn(n_samples),
 "group": np.random.choice(["A", "B", "C"], n_samples)
}})
df.describe
```

## visualization

```{{python}}
#| label: fig-scatter
#| fig-cap: "scatter plot"

fig, ax = plt.subplots(figsize=(8, 6))
for g, sub in df.groupby("group"):
 ax.scatter(sub["x"], sub["y"], label=g, alpha=0.6, s=20)
ax.legend
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show
```

## conclusion

analysisresults's summary.

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
"""

 # references.bib (template)
 bib_template = """@article{example2024,
 title={Example Reference},
 author={Author, A.},
 journal={Journal},
 year={2024}
}
"""

 with open(os.path.join(output_dir, "_quarto.yml"), "w") as f:
 f.write(quarto_config)
 with open(os.path.join(output_dir, "report.qmd"), "w") as f:
 f.write(main_qmd)
 with open(os.path.join(output_dir, "references.bib"), "w") as f:
 f.write(bib_template)

 print(f"Quarto project → {output_dir}/")
 print(f" Build: cd {output_dir} && quarto render report.qmd")
 return output_dir
```

## 2. Papermill 

```python
def papermill_parametric_run(template_notebook, output_dir,
 parameter_sets, kernel="python3"):
 """
 Papermill — multipleparameters automated。

 Parameters:
 template_notebook: str — template
 output_dir: str — output directory
 parameter_sets: list[dict] — parameters's
 kernel: str — kernel
 """
 import papermill as pm

 os.makedirs(output_dir, exist_ok=True)
 results = []

 for i, params in enumerate(parameter_sets):
 output_path = os.path.join(output_dir, f"run_{i:03d}.ipynb")
 try:
 pm.execute_notebook(
 template_notebook,
 output_path,
 parameters=params,
 kernel_name=kernel)
 results.append({
 "run": i, "params": params,
 "output": output_path, "status": "success"})
 except Exception as e:
 results.append({
 "run": i, "params": params,
 "output": output_path, "status": f"error: {str(e)}"})

 import pandas as pd
 results_df = pd.DataFrame(results)
 n_success = (results_df["status"] == "success").sum
 print(f"Papermill: {n_success}/{len(parameter_sets)} runs succeeded")
 return results_df
```

## 3. Jupyter Book configuration

```python
def generate_jupyter_book(title="Scientific Analysis Book",
 chapters=None,
 output_dir="jupyter_book"):
 """
 Jupyter Book templategeneration。

 Parameters:
 title: str — title
 chapters: list[dict] | None — information [{"title":..., "file":...}]
 output_dir: str — output directory
 """
 os.makedirs(output_dir, exist_ok=True)

 if chapters is None:
 chapters = [
 {"title": "Introduction", "file": "intro"},
 {"title": "Data Loading", "file": "ch01_data"},
 {"title": "Exploratory Analysis", "file": "ch02_eda"},
 {"title": "Modeling", "file": "ch03_model"},
 {"title": "Results", "file": "ch04_results"},
 ]

 # _config.yml
 config = f"""title: "{title}"
author: SATORI
execute:
 execute_notebooks: auto
 timeout: 600
repository:
 url: ""
launch_buttons:
 binderhub_url: ""
sphinx:
 extra_extensions:
 - sphinx_proof
"""

 # _toc.yml
 toc_entries = "\n".join(
 [f" - file: {ch['file']}" for ch in chapters])
 toc = f"""format: jb-book
root: intro
chapters:
{toc_entries}
"""

 with open(os.path.join(output_dir, "_config.yml"), "w") as f:
 f.write(config)
 with open(os.path.join(output_dir, "_toc.yml"), "w") as f:
 f.write(toc)

 # eachtemplate
 for ch in chapters:
 filepath = os.path.join(output_dir, f"{ch['file']}.md")
 if not os.path.exists(filepath):
 content = f"# {ch['title']}\n\nThis chapter covers {ch['title'].lower}.\n"
 with open(filepath, "w") as f:
 f.write(content)

 print(f"Jupyter Book → {output_dir}/")
 print(f" Build: jupyter-book build {output_dir}")
 return output_dir
```

## 4. nbconvert automatedtransformation

```python
def batch_convert_notebooks(notebook_dir, output_format="html",
 output_dir=None, execute=True):
 """
 transformation。

 Parameters:
 notebook_dir: str — directory
 output_format: str — "html" / "pdf" / "markdown" / "script"
 output_dir: str | None — output destination (None=directory)
 execute: bool — transformation
 """
 import subprocess
 import glob

 notebooks = sorted(glob.glob(os.path.join(notebook_dir, "*.ipynb")))
 if output_dir:
 os.makedirs(output_dir, exist_ok=True)

 results = []
 for nb_path in notebooks:
 cmd = ["jupyter", "nbconvert", f"--to={output_format}"]
 if execute:
 cmd.append("--execute")
 if output_dir:
 cmd.extend(["--output-dir", output_dir])
 cmd.append(nb_path)

 try:
 subprocess.run(cmd, check=True, capture_output=True, text=True)
 results.append({"notebook": nb_path, "status": "success"})
 except subprocess.CalledProcessError as e:
 results.append({"notebook": nb_path, "status": f"error: {e.stderr[:100]}"})

 import pandas as pd
 results_df = pd.DataFrame(results)
 n_ok = (results_df["status"] == "success").sum
 print(f"nbconvert ({output_format}): {n_ok}/{len(notebooks)} converted")
 return results_df
```

---

## Pipeline Integration

```
[analysiscompletion] → reproducible-reporting → presentation-design
 (reportautomatedgeneration) 
 │ ↓
 interactive-dashboard academic-writing
 (dashboard) (paperwriting)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `quarto_project/` | Quarto | → quarto render |
| `papermill_runs/` | results | → |
| `jupyter_book/` | Jupyter Book | → jb build |
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
