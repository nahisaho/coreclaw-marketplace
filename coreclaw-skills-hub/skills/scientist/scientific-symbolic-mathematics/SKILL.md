---
name: scientific-symbolic-mathematics
description: |
 Symbolic mathematics skill. SymPy-based symbolic computation, equation solving, calculus, linear algebra, and mathematical proof assistance.
---

# Scientific Symbolic Mathematics

SymPy and number/count (Computer Algebra System)
pipeline.

## When to Use

- minformula analysis and
- number/countformula's minmin is performedand
- 's value and
- 's parametersregardingdegreeanalysis and
- number/countformula LaTeX shapeformulatransformationwhen needed
- and number/countvaluecomparisonverificationwhen needed

---

## Quick Start

## 1. minformula's analysis

```python
import sympy as sp
from sympy import (
 symbols, Function, Eq, dsolve, classify_ode,
 exp, sin, cos, sqrt, pi, oo, integrate, diff,
 Matrix, latex, simplify, factor, expand, solve,
 Rational, Sum, Product, series,
)
import numpy as np


def solve_ode(ode_expr, dependent_var, independent_var, ics=None):
 """
 minformula's analysis。

 Parameters:
 ode_expr: sympy.Eq — ODE (e.g., Eq(f(x).diff(x, 2) + f(x), 0))
 dependent_var: sympy.Function — number/count
 independent_var: sympy.Symbol — number/count
 ics: dict — initialcondition {f(0): 1, f'(0): 0}

 K-Dense: sympy — Symbolic mathematics
 """
 # Classify ODE
 classification = classify_ode(ode_expr, dependent_var(independent_var))
 print(f"ODE classification: {classification[:3]}")

 # Solve
 solution = dsolve(ode_expr, dependent_var(independent_var), ics=ics)

 print(f"Solution: {solution}")
 print(f"LaTeX: {latex(solution)}")
 return solution


# Example: damped harmonic oscillator
x, t, omega, gamma = symbols("x t omega gamma", positive=True)
f = Function("f")

# f''(t) + 2γf'(t) + ω²f(t) = 0
damped_ode = Eq(f(t).diff(t, 2) + 2*gamma*f(t).diff(t) + omega**2*f(t), 0)
```

## 2. min

```python
def symbolic_calculus(expr, var, operations=None):
 """
 min。

 Parameters:
 expr: sympy expression — number/countformula
 var: sympy.Symbol — number/count
 operations: list — ["diff", "integrate", "series", "limit"]
 """
 if operations is None:
 operations = ["diff", "integrate"]

 results = {}

 if "diff" in operations:
 deriv = diff(expr, var)
 results["derivative"] = {"expr": deriv, "latex": latex(deriv)}
 print(f"d/d{var}({expr}) = {deriv}")

 if "integrate" in operations:
 integral = integrate(expr, var)
 results["integral"] = {"expr": integral, "latex": latex(integral)}
 print(f"∫{expr} d{var} = {integral}")

 if "series" in operations:
 ser = series(expr, var, 0, n=6)
 results["series"] = {"expr": ser, "latex": latex(ser)}
 print(f"Taylor series: {ser}")

 if "limit" in operations:
 from sympy import limit as sp_limit
 lim = sp_limit(expr, var, oo)
 results["limit"] = {"expr": lim, "latex": latex(lim)}
 print(f"lim({var}→∞) {expr} = {lim}")

 return results
```

## 3. lineshapenumber/count 

```python
def symbolic_linear_algebra(matrix_data):
 """
 lineshapenumber/count — valuedegradation。

 Parameters:
 matrix_data: list of lists — element (includes)
 """
 M = Matrix(matrix_data)
 print(f"Matrix ({M.rows}×{M.cols}):")
 sp.pprint(M)

 results = {}

 # Determinant
 det = M.det
 results["determinant"] = {"expr": det, "latex": latex(det)}
 print(f"\nDeterminant: {det}")

 # Eigenvalues & eigenvectors
 eigenvals = M.eigenvals
 results["eigenvalues"] = {str(k): v for k, v in eigenvals.items}
 print(f"Eigenvalues: {eigenvals}")

 eigenvects = M.eigenvects
 results["eigenvectors"] = [
 {"eigenvalue": str(ev[0]), "multiplicity": ev[1],
 "vectors": [str(v) for v in ev[2]]}
 for ev in eigenvects
 ]

 # Characteristic polynomial
 lam = symbols("lambda")
 char_poly = M.charpoly(lam)
 results["characteristic_polynomial"] = {
 "expr": str(char_poly.as_expr),
 "latex": latex(char_poly.as_expr),
 }
 print(f"Characteristic polynomial: {char_poly.as_expr}")

 # Inverse (if nonsingular)
 if det != 0:
 inv = M.inv
 results["inverse"] = {"latex": latex(inv)}
 print(f"Inverse exists: {M.rows}×{M.cols}")

 return results
```

## 4. (drug PK example)

```python
def pk_compartment_model(n_compartments=1):
 """
 drug's method。

 Parameters:
 n_compartments: int — 1 (1-compartment) or 2 (2-compartment)
 """
 t = symbols("t", positive=True)

 if n_compartments == 1:
 # 1-compartment: dC/dt = -ke * C
 C = Function("C")
 ke, C0 = symbols("k_e C_0", positive=True)
 ode = Eq(C(t).diff(t), -ke * C(t))
 solution = dsolve(ode, C(t), ics={C(0): C0})

 # Half-life
 t_half = sp.solve(Eq(solution.rhs, C0/2), t)[0]

 # AUC (0→∞)
 auc = integrate(solution.rhs, (t, 0, oo))

 result = {
 "model": "1-compartment IV bolus",
 "ode": latex(ode),
 "solution": latex(solution),
 "half_life": latex(t_half),
 "auc_inf": latex(auc),
 }
 print(f"PK 1-compartment: C(t) = {solution.rhs}")
 print(f" t½ = {t_half}")
 print(f" AUC(0→∞) = {auc}")

 elif n_compartments == 2:
 # 2-compartment model
 C1, C2 = Function("C1"), Function("C2")
 k10, k12, k21, D, V1 = symbols("k_10 k_12 k_21 D V_1", positive=True)

 ode1 = Eq(C1(t).diff(t), -(k10 + k12)*C1(t) + k21*C2(t))
 ode2 = Eq(C2(t).diff(t), k12*C1(t) - k21*C2(t))

 system = [ode1, ode2]
 solution = sp.dsolve(system, [C1(t), C2(t)])

 result = {
 "model": "2-compartment IV bolus",
 "system": [latex(eq) for eq in system],
 "solution": [latex(sol) for sol in solution],
 }
 print(f"PK 2-compartment system defined")
 for sol in solution:
 print(f" {sol}")

 return result
```

## 5. LaTeX number/countformulaexport

```python
def export_equations_latex(equations, output_file="equations.tex"):
 """
 number/countformula LaTeX file export。

 Parameters:
 equations: dict — {name: sympy_expr}
 output_file: str — output LaTeX 
 """
 lines = [
 r"\documentclass{article}",
 r"\usepackage{amsmath,amssymb}",
 r"\begin{document}",
 "",
 ]

 for name, expr in equations.items:
 lines.append(f"% {name}")
 lines.append(r"\begin{equation}")
 lines.append(f" {latex(expr)}")
 lines.append(r"\end{equation}")
 lines.append("")

 lines.append(r"\end{document}")

 with open(output_file, "w") as f:
 f.write("\n".join(lines))

 print(f"LaTeX exported: {output_file} ({len(equations)} equations)")
 return output_file
```

---

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/symbolic_solutions.json` | (LaTeX shapeformula) | → latex-formatter, academic-writing |
| `results/ode_solutions.json` | ODE analysis | → systems-biology, admet-pharmacokinetics |
| `equations.tex` | LaTeX number/countformula | → latex-formatter |
| `figures/symbolic_plot.png` | 'svisualization | → publication-figures |

## Pipeline Integration

```
systems-biology ──→ symbolic-mathematics ──→ latex-formatter
 (SBML/ODE) (SymPy analysis) (LaTeX transformation)
 │
 ├──→ admet-pharmacokinetics (PK )
 ├──→ bayesian-statistics (likelihood)
 └──→ computational-materials 
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
3. Write `report.md` in the same language as the user's input, summarizing methods, results, and interpretation

---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Chemistry/Materials)

Before execution, define:
- [ ] **Target property**: specific value or range (e.g., band gap 1.5-2.0 eV)
- [ ] **Validity domain**: applicable chemical space, temperature/pressure range
- [ ] **Accuracy target**: prediction error threshold (MAE, RMSE)
- [ ] **Structure validation**: expected symmetry, stability criteria

#### Pass Criteria
- Crystal structures validated (symmetry, bond lengths, coordination)
- Thermodynamic stability checked (energy above hull < threshold)
- Predictions include uncertainty estimates
- Units and physical constants verified
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
