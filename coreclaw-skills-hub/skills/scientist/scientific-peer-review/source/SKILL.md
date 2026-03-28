---
name: scientific-peer-review
description: |
 Peer review skill. Structured peer review generation following journal guidelines, constructive critique formulation, statistical audit, and review scoring.
---

# Scientific Peer Review

experimentresults systematic evaluation、reproducibilitymethod's
allabout is providedskill。

## When to Use

- experimentresults's is evaluatedand
- paper's cell is performedand
- 's experimentresultswhen needed
- analysis's is verifiedand

## Quick Start

### Step 1: datareport's
- experimentdatafile's verification（CSV, JSON, ）
- experimentreport / conversation.md 's
- formethodparameters's

### Step 2: method'sevaluation
- experiment's（group's 、）
- sample size's min
- measurementmethod's
- 's possible

### Step 3: analysis'sverification
- formethod's
- multiple comparisoncorrection's
- effect size's
- confidence interval's
- p-value's 's

### Step 4: reproducibility's evaluation
- procedure's detailsdegree（possible）
- data's
- environmentcondition's

### Step 5: reportgeneration

## Output Format

`peer_review.md` below/following's structuregeneration:

```markdown
# peer reviewreport

## evaluation
[A: / B: / C: fix / D: fix]

## 1. method'sevaluation
## 2. analysis's
## 3. reproducibility's evaluation
## 4. data's
## 5. conclusion's
## 6. improvement
## 7. recommendedterm
```

## Scoring Criteria

| item | evaluationcriteria |
|------|---------|
| method | experiment's 、group、 |
| | method's 、multiple comparison、effect size |
| reproducibility | procedure's detailsdegree、data |
| conclusion | dataconclusion |

## Examples

**Prompt Examples:**
- 「's experimentresults」
- 「analysis'speer review」
- 「reproducibility's pointfromevaluation」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | literature evidence for review comments |

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
