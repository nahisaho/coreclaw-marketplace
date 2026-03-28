---
name: scientific-audit-report
description: |
 Research audit report skill. Systematic quality assessment of experimental designs, statistical analyses, reproducibility, and reporting standards compliance.
---

# Scientific Audit Report

experiment's data（）and change 、
supportreproducibilityforauditreport is generatedskill。

## When to Use

- to 's forauditwhen needed
- GLP / GMP / GCP 's is createdand
- data's transformationwhen needed
- experiment's reproducibilitywhen needed

## Quick Start

### Step 1: experimentlog's
- `messages.jsonl` 's allentry
- `conversation.md` 'sconstruction
- 's change

### Step 2: datatransformation's
- input data → data → output'sfigure
- eachtransformationstepfortool
- datashapeformula's transformation（CSV → DataFrame → results）

### Step 3: environmentinformation
- Python / R / Node.js 
- forlibrary and（pip freeze / npm list）
- OSinformation
- AI 

### Step 4: dataconsistency check
- file's（SHA-256）
- rowscolumnnumber/count'sverification
- valuevalue's
- input dataand outputdata's

### Step 5: verification
- data（unitsinformation's）
- 's
- use's

## Output Format

`audit_report.md`:

```markdown
# auditreport

## experimentoverview
- experimentID,,, period

## data（）
### input data
### transformation
### outputdata

## fortool
| tool | | for |
|--------|-----------|------|

## dataconsistency check
| file | SHA-256 | | verificationresults |
|---------|---------|--------|---------|

## 
| | | |
|------|------|---------|

## 
```

## Examples

- 「's experiment's auditreport」
- 「data」
- 「GLP's report generation」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | datareproducibilitytoolsearch |

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
