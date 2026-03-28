---
name: scientific-critical-review
description: |
 Critical review skill. Systematic assessment of research quality, experimental rigor evaluation, statistical claim verification, and comprehensive peer review analysis.
---

# Scientific Critical Review & Revision

paper's、fix is performedskill。
peer review's pointfrompaper's point、discussion's 's 's is supported。

## When to Use

- 、's cell is performedand
- Discussion / Conclusion 's discussion and and
- dataand 'sverificationwhen needed
- 's and basiswhen needed
- peer reviewfrom's predictionwhen needed

## Quick Start

## 1. workflow

```

 ├─ Pass 1: structure（）
 │ ├─ configuration's
 │ ├─ storyline's
 │ └─ each's
 ├─ Pass 2: discussion（）
 │ ├─ and 'ssupport
 │ ├─ discussion's
 │ ├─ 's
 │ └─ limitations's
 ├─ Pass 3: data
 │ ├─ 's
 │ ├─ effect sizeconfidence interval's
 │ └─ figures/tablesand 's
 ├─ Pass 4: table（）
 │ ├─ table's
 │ ├─ table's
 │ └─ 's
 └─ Pass 5: fix's
 ├─ fix
 ├─ fix'sgeneration
 └─ fix's mintable
```

## 2. Pass 1: structure（）

```markdown
## structure

### configuration
- [ ] Abstract papers's keyresults
- [ ] Introduction CARS （Territory → Niche → Occupying）
- [ ] Methods by/viamindetailsincluding
- [ ] Results 's（）
- [ ] Discussion Results 's 、discussion providing
- [ ] Conclusion noveldiscussion 、key's

### storyline
- [ ] research's motivation（Why）→ method（How）→ （What）→ significance（So what）'s clear
- [ ] Introduction researchchallenge Discussion times
- [ ] each's 's from's

### 
- [ ] Introduction （all's 15-20% ）
- [ ] Methods degreedetails or 
- [ ] Results and Discussion 's
- [ ] figures/tables's number/count（'s）
```

## 3. Pass 2: discussion（ — important）

's discussion's.'s Discussion below/following's 7verification.

```markdown
## discussion'sverificationframework（7 Layer Deep Analysis）

### Layer 1: results's（table）
****: key 2-3 ？
****: items？
**problem**: Results 's.
**fix**: number/countvalue's 、's 。

### Layer 2: research and 's positioning
****: papersresearch's results existing's and comparison？
****: research and？？？
**problem**: "Our results are consistent with [ref].".
**fix**: /'s discussion.condition's 、
method's 、'setc.、's min.

### Layer 3: 's discussion
****: observation's？
****: 's results 's？'s 's？
**problem**: correlationas.'s tablesurface。
**fix**: 「A B」 「A and B's、C and
possible 」's 、's explicit.

### Layer 4: 's
****: min's 's possible？
****: 's results 's hypothesis？confounding factors's？
**problem**: 's good's（）。
**fix**: and also 1 items's 、 also
basis 。possible.

### Layer 5: for
****: 's min 's？
****: So what? 's？？
**problem**: 's or evaluation。
**fix**: （existing's fix/）and for
（application/application）min.

### Layer 6: limitations's
****: research's limitations？
****: 's research and？'s range？
**problem**: limitations and 's 。
**fix**: eachlimitationsabout (1) limitations、(2) results to 's degree、
(3) 's research、's 3 point 。

### Layer 7: 's researchdirection
****: research？
****: 's research's 's step？
**problem**: "Further research is needed." 's and 。
**fix**: experiment、sample size、methodincluding
possible 。
```

### discussion's

```python
def score_discussion_depth(discussion_text):
 """
 Discussion 's discussion's 7 evaluates。

 Returns:
 dict: each's（0-3）andevaluation
 """
 layers = {
 "L1_summary": {
 "name": "results's",
 "indicators": [
 "key's clear",
 "number/countvalue's 's",
 ],
 },
 "L2_prior_work": {
 "name": "research and 's positioning",
 "indicators": [
 "3 itemsabove/more's research and 's comparison",
 "/'s",
 "conditionmethod'sby/viamin",
 ],
 },
 "L3_mechanism": {
 "name": "'s discussion",
 "indicators": [
 "and correlation",
 "//",
 "'s",
 ],
 },
 "L4_alternatives": {
 "name": "'s",
 "indicators": [
 "and also 1 items's hypothesis",
 "confounding factors's possible",
 "also",
 ],
 },
 "L5_implications": {
 "name": "",
 "indicators": [
 "clear",
 "forapplication's possible",
 "",
 ],
 },
 "L6_limitations": {
 "name": "limitations's",
 "indicators": [
 "2 itemsabove/more's limitations",
 "eachlimitations's results to 's degree",
 "",
 ],
 },
 "L7_future": {
 "name": "'s researchdirection",
 "indicators": [
 "'s step",
 "possibleexperiment",
 ],
 },
 }

 # each 0-3 
 # 0 =, 1 = tablesurface, 2 =, 3 = 
 scores = {}
 for layer_id, layer in layers.items:
 # manualevaluation。
 # AI each indicator 's degree.
 scores[layer_id] = {
 "name": layer["name"],
 "score": 0, # 0-3 evaluation
 "indicators": layer["indicators"],
 "comments": [],
 }

 total = sum(s["score"] for s in scores.values)
 max_total = len(scores) * 3

 return {
 "layers": scores,
 "total_score": total,
 "max_score": max_total,
 "percentage": round(total / max_total * 100, 1) if max_total > 0 else 0,
 "grade": (
 "A (Excellent)" if total >= 18 else
 "B (Good)" if total >= 14 else
 "C (Adequate)" if total >= 10 else
 "D (Needs improvement)" if total >= 6 else
 "F (Major revision required)"
 ),
 }
```

## 4. Pass 3: data

```markdown
## 's verification

### number/countvalue's
- [ ] papers's number/countvaluefigures/tables's value and
- [ ] meanvalue ± SD/SEM 's table
- [ ] sample size (n) all's testing

### inference
- [ ] fortesting（、variance'sverification）
- [ ] p-valueeffect size（Cohen's d, η² ）
- [ ] 95% confidence interval
- [ ] multiple comparison's correction for
- [ ] power（power）（especiallyresultscase）

### 's
| 's table | problem | fix |
|---|---|---|
| "A causes B" | correlationand | "A is associated with B" / "A may contribute to B" |
| "significantly increased" | p-value's | "statistically significantly increased (d = 0.8, large effect)" |
| "proves that..." | | "provides strong evidence that..." / "supports the hypothesis that..." |
| "for the first time" | verification | "to our knowledge, this is the first report of..." |
| "novel" | for | novel |
| "no difference" | power's possible | "no statistically significant difference was detected (power = 0.XX)" |

### figures/tablesand 'sconsistency check

1. Results all'sfigures/tables
2. all'sfigures/tablespapers reference（figures/tables）
3. figure's and papers's
4. table's number/countvalue and papers's number/countvalue
```

## 5. Pass 4: table（）

```markdown
## 'sverification

### table's

degree table's min:

| degree | papers | |
|---|---|---|
| (90%+) | 〜 / | demonstrate / show / reveal |
| (70-90%) | 〜 / 〜 and | suggest / indicate / appear to |
| (50-70%) | 〜's possible | may / might / could / possible |
| (30-50%) | 〜's possible | cannot rule out / possible but unlikely |
| | 〜 and | speculate / hypothesize |

### 's and fix

:
- 「〜 」→「〜 results 」
- 「 」「」「」→ deletionorbasis addition
- 「all's〜 」→ range clear
- 「」→ "to our knowledge" addition

### 'sverification

| | forexample | |
|---|---|---|
| | Therefore, Thus, Hence | →conclusion's |
| | However, In contrast, Conversely | |
| addition | Furthermore, Moreover, In addition | papers additioninformation、 |
| | Although, Despite, Nevertheless | 's |

### table's

| | |
|---|---|
| "It is well known that..." | deletion |
| "In order to..." | "To..." |
| "Due to the fact that..." | "Because..." |
| "A total of 50 samples" | "50 samples" |
| "It should be noted that..." | deletion |
| "As can be seen in Figure 1..." | "Figure 1 shows..." |
```

## 6. Pass 5: fix's

```markdown
## fixprotocol

### Step 1: problem's

| degree | | example |
|---|---|---|
| **Critical** | errordata | results and conclusion's 、method's error |
| **Major** | discussion's 's basis | Layer 3-4 's 、 |
| **Minor** | table's improvementformula's | 、table、citationshapeformula |
| **Suggestion** | addition point | additiondata、figures/tables |

### Step 2: reportgeneration

eachproblemaboutbelow/following's structure:

**[degree] — problem's**

- **problem**: [problem's]
- ****: [ / / ]
- **basis**: [problem's]
- **fix**: [fix]

### Step 3: fix's for

fixbelow/following's for:
1. Critical problem allfix
2. Major problem fix（discussion'sincluding）
3. Minor fix for
4. all'sverification
```

## 7. discussiontemplate

's Discussion for。

```markdown
## discussion

### A: 「→→」（research and 's）

**Before (shallow):**
> Our results are consistent with Smith et al. (2023).

**After (deep):**
> Our finding that [] is consistent with the observations
> by Smith et al. (2023), who reported [research's results] using
> [research's method]. This agreement across [differentcondition/method] strengthens
> the evidence that ['s/]. Moreover, our results extend
> their findings by demonstrating that [papersresearch's addition], which was
> not previously examined due to [].

### B: 「→min→integration」（'s）

**Before (shallow):**
> However, our results differ from those of Jones et al. (2022).

**After (deep):**
> Interestingly, our observation of [papersresearch's results] contrasts with
> Jones et al. (2022), who found [research's results]. This discrepancy
> likely stems from differences in [condition 1: e.g.temperaturerange/sample size/
> measurementmethod]. Specifically, our use of [papersresearch's condition] compared to their
> [research's condition] may have ['s]. A unified interpretation
> of both findings could be that [integration], where [condition] acts as
> a moderating factor.

### C: 「→basis→verificationmethod」

**Before (shallow):**
> The increase in hardness may be due to grain refinement.

**After (deep):**
> The observed increase in hardness (from XX to YY HV) with
> increasing [condition] can be attributed to [ 1: e.g.
> grain boundary strengthening following the Hall-Petch relationship].
> This interpretation is supported by our XRD analysis showing a
> decrease in crystallite size from XX to YY nm (Fig. X), which
> corresponds to [prediction]. An alternative explanation involving
> [ 2: e.g. solid solution strengthening] is less likely
> because ['s basis]. To definitively distinguish between these
> mechanisms, [additionexperiment: TEM observation of grain boundaries]
> would be required.

### D: 「quantitativecomparison→→prediction」

**Before (shallow):**
> The effect size was large (d = 0.9).

**After (deep):**
> The large effect size (Cohen's d = 0.9, 95% CI [0.5, 1.3])
> indicates a practically meaningful difference between [group A] and
> [group B]. To contextualize this magnitude, [: e.g.
> typical effect sizes in this field range from 0.3 to 0.6 (meta-analysis
> by Lee et al., 2021)], suggesting that [condition] has a notably strong
> influence on []. Extrapolating from our dose-response data,
> we predict that [condition's value] would be required to achieve [targetvalue],
> which warrants validation in ['sexperiment].

### E: 「limitations→evaluation→」

**Before (shallow):**
> A limitation of this study is the small sample size.

**After (deep):**
> A limitation of this study is the relatively small sample size
> (n = XX per group). Post-hoc power analysis indicates that our study
> had 0.XX power to detect a medium effect size (d = 0.5), which
> raises the possibility that some true effects may have been missed
> (Type II error). However, the primary findings showed large effect
> sizes (d > 0.8) with statistical significance, suggesting they are
> robust to sample size concerns. The non-significant secondary outcomes
> should be interpreted with caution and verified in a larger cohort.
> Based on our preliminary effect sizes, a minimum of [calculationvalue]
> participants per group would be needed to achieve 0.80 power for
> the secondary analyses.
```

## 8. 

each's 。

```markdown
### Abstract to 's
1. papers also research's all？
2. quantitativeresults（number/countvalue）？
3. ？
4. number/count？

### Introduction to 's
1. 's research necessary's？
2. research's？（'s goodliterature's citation）
3. 's？
4. researchpurpose clear？

### Methods to 's
1. 's research 's method sameresults？
2. experiment/group？
3. sample size's basis？
4. 's method？

### Results to 's
1. results's？
2. results also？（）
3. all'sfigures/tablespapers reference？
4. error SD SEM ？

### Discussion to 's
1. discussion's 7 （Layer 1-7）all？
2. ？
3. limitationsfor/againstevaluation and？
4. conclusion 's range？
```

## 9. results's outputshapeformula

results filesave.than 、fix's 、
peer reviewsupport'sreference、hypothesis and 's verification possible。

### 9.1 report'ssave

```python
def save_review_report(review_data, filepath=None):
 """
 results Markdown fileassave.
 
 Args:
 review_data: dict — results
 {"scores": {...}, "issues": [...], "revisions": [...]}
 filepath: Path — save（: manuscript/review_report.md）
 """
 import datetime
 from pathlib import Path
 
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "review_report.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 scores = review_data.get("scores", {})
 issues = review_data.get("issues", [])
 
 content = f"""# Critical Review Report

> datetime: {datetime.datetime.now.strftime('%Y-%m-%d %H:%M')}

## 1. evaluation

| evaluationitem | (0-3) | |
|---|---|---|
| structure's clear | {scores.get('structure', 0)} | {scores.get('structure_comment', '')} |
| 's | {scores.get('logic', 0)} | {scores.get('logic_comment', '')} |
| discussion's | {scores.get('discussion', 0)} | {scores.get('discussion_comment', '')} |
| | {scores.get('statistics', 0)} | {scores.get('statistics_comment', '')} |
| 's | {scores.get('writing', 0)} | {scores.get('writing_comment', '')} |
| **** | **{sum(scores.get(k, 0) for k in ['structure','logic','discussion','statistics','writing'])}/15** | |

## 2. fixtermlist

"""
 # degree loop
 for priority in ["Critical", "Major", "Minor", "Suggestion"]:
 group = [i for i in issues if i.get("priority") == priority]
 if group:
 content += f"### {priority}\n\n"
 for issue in group:
 content += f"- [ ] **{issue['section']}**: {issue['summary']}\n"
 content += f" - problem: {issue['problem']}\n"
 content += f" - fix: {issue['fix']}\n\n"
 
 # fix's min
 revisions = review_data.get("revisions", [])
 if revisions:
 content += "## 3. 's fix\n\n"
 for rev in revisions:
 content += f"### {rev['section']}\n\n"
 content += f"**fix:**\n> {rev['before']}\n\n"
 content += f"**fix:**\n> {rev['after']}\n\n"
 content += f"**fix:** {rev['reason']}\n\n"
 
 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)
 
 print(f" → reportsave: {filepath}")
 return filepath
```

### 9.2 results's JSON save

```python
def save_review_json(review_data, filepath=None):
 """
 results JSON assave.
 hypothesisand 'sverification、's comparison for。
 """
 import datetime, json
 from pathlib import Path
 
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "review_report.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 # hypothesisfilereference
 hypothesis_ref = None
 hypothesis_path = BASE_DIR / "docs" / "hypothesis.json"
 if hypothesis_path.exists:
 with open(hypothesis_path, "r", encoding="utf-8") as f:
 hypothesis_ref = json.load(f).get("hypothesis")
 
 data = {
 "version": "1.0",
 "created_at": datetime.datetime.now.isoformat,
 "hypothesis_ref": hypothesis_ref,
 "scores": review_data.get("scores", {}),
 "issues": review_data.get("issues", []),
 "discussion_depth": review_data.get("discussion_depth", {}),
 "revision_count": len(review_data.get("revisions", [])),
 }
 
 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(data, f, indent=2, ensure_ascii=False, default=str)
 
 print(f" → JSON save: {filepath}")
 return filepath
```

### 9.3 fix'ssave

```python
def save_revised_manuscript(original_path, revisions, output_path=None):
 """
 fixsave.
 's 's 、fixfileassave。
 
 Args:
 original_path: Path — 'sfile
 revisions: list[dict] — fix
 [{"before": "...", "after": "...", "section": "..."}]
 output_path: Path — output destination（: manuscript/manuscript_revised.md）
 """
 from pathlib import Path
 
 if output_path is None:
 output_path = BASE_DIR / "manuscript" / "manuscript_revised.md"
 output_path.parent.mkdir(parents=True, exist_ok=True)
 
 # 'sload
 with open(original_path, "r", encoding="utf-8") as f:
 content = f.read
 
 # fix for
 applied = 0
 for rev in revisions:
 if rev["before"] in content:
 content = content.replace(rev["before"], rev["after"], 1)
 applied += 1
 
 with open(output_path, "w", encoding="utf-8") as f:
 f.write(content)
 
 print(f" → fixsave: {output_path} ({applied}/{len(revisions)} itemsfor)")
 return output_path
```

### 9.4 fixmin'ssave

```python
def save_revision_diff(revisions, filepath=None):
 """
 fix's min Markdown fileassave.
 peer reviewsupport (Response to Reviewers) reference。
 """
 import datetime
 from pathlib import Path
 
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "revision_diff.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)
 
 content = f"""# fixminreport

> fixdatetime: {datetime.datetime.now.strftime('%Y-%m-%d %H:%M')}
> fixnumber/count: {len(revisions)}

"""
 for i, rev in enumerate(revisions, 1):
 content += f"""## fix {i}: {rev.get('section', 'N/A')}

**degree**: {rev.get('priority', 'N/A')}

**fix:**
> {rev['before']}

**fix:**
> {rev['after']}

**fix:** {rev.get('reason', '')}

---

"""
 
 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)
 
 print(f" → fixminreportsave: {filepath}")
 return filepath
```

### 9.5 workflowintegration

```python
def run_review_pipeline(manuscript_path):
 """
 pipeline、all's results filesave.
 
 output file:
 manuscript/review_report.md — report
 manuscript/review_report.json — results (JSON)
 manuscript/manuscript_revised.md — fix
 manuscript/revision_diff.md — fixmin
 """
 print("=" * 60)
 print("Critical Review Pipeline")
 print("=" * 60)
 
 # Pass 1-4: 
 review_data = {
 "scores": {}, # Pass 1-4 
 "issues": [], # problem
 "revisions": [], # fix
 "discussion_depth": {}, # 7degreeminresults
 }
 
 # Pass 5: filesave
 save_review_report(review_data)
 save_review_json(review_data)
 
 if review_data["revisions"]:
 save_revised_manuscript(manuscript_path, review_data["revisions"])
 save_revision_diff(review_data["revisions"])
 
 print("\n" + "=" * 60)
 print("Done!")
 print("=" * 60)
```

### reporttemplate

```markdown
# Critical Review Report

## 1. evaluation

| evaluationitem | (0-3) | |
|---|---|---|
| structure's clear | X | [] |
| 's | X | [] |
| discussion's | X | [] |
| | X | [] |
| 's | X | [] |
| **** | **X/15** | **[]** |

## 2. fixtermlist

### Critical
- [ ] [fixterm 1]
- [ ] [fixterm 2]

### Major
- [ ] [fixterm 3]
- [ ] [fixterm 4]

### Minor
- [ ] [fixterm 5]

## 3. 's fix

### Discussion 's fix

**fix:**
> ['s]

**fix:**
> [improvement]

**fix:** ['s]
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

| File | Format | Generated When |
|---|---|---|
| `manuscript/review_report.md` | report（Markdown） | Pass 1-4 completion |
| `manuscript/review_report.json` | results（JSON） | Pass 1-4 completion |
| `manuscript/manuscript_revised.md` | fix | Pass 5 completion |
| `manuscript/revision_diff.md` | fix's min | Pass 5 completion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | → papersskill → fix |
| `scientific-statistical-testing` | 's verification for |
| `scientific-publication-figures` | figures/tables'sconsistency checkfor |
| `scientific-hypothesis-pipeline` | hypothesisand conclusion's verification for |

```
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
