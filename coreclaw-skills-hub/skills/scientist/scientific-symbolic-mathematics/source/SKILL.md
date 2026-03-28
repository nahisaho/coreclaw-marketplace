---
name: scientific-symbolic-mathematics
description: |
 Symbolic mathematics skill. SymPy-based symbolic computation, equation solving, calculus, linear algebra, and mathematical proof assistance.
tu_tools:
 - key: biotools
 name: bio.tools
 description: number/countformulaanalysistoolsearch
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

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | number/countformulaanalysistoolsearch |

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
