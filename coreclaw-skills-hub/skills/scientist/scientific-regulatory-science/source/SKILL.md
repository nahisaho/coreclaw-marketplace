---
name: scientific-regulatory-science
description: |
 Regulatory science skill. FDA/EMA regulatory guidance, clinical trial regulation, drug approval pathway analysis, and regulatory document preparation.
---

# Scientific Regulatory Science

FDAEMAPMDA 's databasecross-cutting、
's informationalldataquality controlitemsinformation
systematic retrievespipeline is provided。

## When to Use

- FDA 'sinvestigationwhen needed
- 's 510(k) classification is verifiedand
- all (FDA, ) data is retrievedand
- ISO 13485 quality control's designCAPA designwhen needed
- 'sinvestigationwhen needed

---

## Quick Start

## 1. FDA Orange Book 

```python
import pandas as pd
import json


def query_fda_orange_book(drug_name=None, nda_number=None,
 active_ingredient=None):
 """
 FDA Orange Book (Approved Drug Products with Therapeutic Equivalence Evaluations)。

 retrievalitem:
 - (NDA/ANDA,, )
 - treatment (TE) (AB, BX, etc.)
 - information (, number, Use Code)
 - information (NCE, Orphan, Pediatric)
 - 
 """
 print(f" Querying FDA Orange Book:")
 if drug_name:
 print(f" Drug: {drug_name}")
 if active_ingredient:
 print(f" Active ingredient: {active_ingredient}")

 return {"drug_name": drug_name, "nda_number": nda_number}


def analyze_patent_landscape(drug_name):
 """
 analysis。

 - Orange Book 's
 - graph IV 's
 - 180 's
 - prediction
 """
 print(f" Patent landscape for: {drug_name}")
 print(" Analysis: Patent expiry timeline + exclusivity + generic entry")

 return {"drug_name": drug_name}
```

## 2. FDA data

```python
import pandas as pd


def query_fda_device_classification(device_name=None, product_code=None,
 regulation_number=None):
 """
 FDA classification。

 classification:
 - Class I: (General Controls)
 - Class II: (Special Controls) — 510(k) necessary
 - Class III: (PMA) necessary
 """
 print(f" FDA Device Classification:")
 if device_name:
 print(f" Device: {device_name}")
 print(" Regulatory pathways: 510(k), De Novo, PMA, HDE")

 return {"device_name": device_name, "product_code": product_code}


def query_510k_clearance(device_name=None, applicant=None,
 decision_date_from=None):
 """
 FDA 510(k) data。

 510(k) = Premarket Notification
 - Predicate device and 's (SE) 's
 - 90 (Traditional) / 30 (Special/Abbreviated)
 """
 print(f" 510(k) Clearance search:")
 if device_name:
 print(f" Device: {device_name}")

 return {"device_name": device_name}
```

## 3. ISO 13485 quality control

```python
import json
from datetime import datetime


def iso13485_design_control_checklist(product_name, risk_class="II"):
 """
 ISO 13485 design。

 designprocess (ISO 13485:2016 §7.3):
 - 7.3.2 designdesign
 - 7.3.3 designinput
 - 7.3.4 designoutput
 - 7.3.5 design
 - 7.3.6 designverification
 - 7.3.7 design
 - 7.3.8 design
 - 7.3.9 designchange
 """
 checklist = {
 "product": product_name,
 "risk_class": risk_class,
 "design_phases": [
 {"phase": "Design Planning", "ref": "§7.3.2",
 "deliverables": ["DHF designfile", "design", "design"]},
 {"phase": "Design Input", "ref": "§7.3.3",
 "deliverables": ["", "design (DRS)", ""]},
 {"phase": "Design Output", "ref": "§7.3.4",
 "deliverables": ["design", "figuresurface", "DMR (Device Master Record)"]},
 {"phase": "Design Review", "ref": "§7.3.5",
 "deliverables": ["design", ""]},
 {"phase": "Design Verification", "ref": "§7.3.6",
 "deliverables": ["verificationprotocol/report", ""]},
 {"phase": "Design Validation", "ref": "§7.3.7",
 "deliverables": ["protocol/report", "evaluation (necessary)"]},
 {"phase": "Design Transfer", "ref": "§7.3.8",
 "deliverables": ["", ""]},
 {"phase": "Design Changes", "ref": "§7.3.9",
 "deliverables": ["change (ECO)", "min"]},
 ],
 }

 print(f" ISO 13485 Design Control for: {product_name} (Class {risk_class})")
 for phase in checklist["design_phases"]:
 print(f" {phase['ref']} {phase['phase']}: {len(phase['deliverables'])} deliverables")

 return checklist


def capa_process(nonconformity_description, severity="Major"):
 """
 CAPA (Corrective and Preventive Action) process。

 ISO 13485 §8.5.2  / §8.5.3 
 """
 capa_record = {
 "id": f"CAPA-{datetime.now.strftime('%Y%m%d-%H%M')}",
 "nonconformity": nonconformity_description,
 "severity": severity,
 "steps": [
 "1. problem's and",
 "2. (Containment)",
 "3. papersmin (5-Why / Fishbone)",
 "4. 's design and",
 "5. effectiveverification",
 "6. 's",
 "7. CAPA ",
 ],
 }

 print(f" CAPA initiated: {capa_record['id']}")
 print(f" Severity: {severity}")

 return capa_record
```

## 4. USPTO search

```python
import pandas as pd


def search_patents(query, start_date=None, end_date=None,
 assignee=None, max_results=50):
 """
 USPTO search (PatentsView API)。

 searchfield:
 - title
 - /
 - /
 - CPC (Cooperative Patent Classification) 
 """
 print(f" USPTO Patent search: '{query}'")
 if assignee:
 print(f" Assignee: {assignee}")
 if start_date:
 print(f" Date range: {start_date} → {end_date or 'present'}")

 return {"query": query, "max_results": max_results}
```

## References

### Output Files

| File | Format |
|---|---|
| `results/fda_orange_book.json` | JSON |
| `results/device_classification.csv` | CSV |
| `results/510k_clearances.csv` | CSV |
| `results/iso13485_checklist.json` | JSON |
| `results/capa_record.json` | JSON |
| `results/patent_search.csv` | CSV |
| `figures/patent_timeline.png` | PNG |

### Available Tools

> External tools available via [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) SMCP.

| Category | Key Tools | Usage |
|---|---|---|
| FDA Orange Book | `FDA_OrangeBook_search_drug` | search |
| FDA Orange Book | `FDA_OrangeBook_get_approval_history` | retrieval |
| FDA Orange Book | `FDA_OrangeBook_get_patent_info` | informationretrieval |
| FDA Orange Book | `FDA_OrangeBook_get_exclusivity` | information |
| FDA Orange Book | `FDA_OrangeBook_check_generic_availability` | |
| FDA Orange Book | `FDA_OrangeBook_get_te_code` | treatment |
| FAERS | `FAERS_search_adverse_event_reports` | reportsearch |
| FAERS | `FAERS_calculate_disproportionality` | min (ROR/PRR/IC) |

### Related Skills

| Skill | Relationship |
|---|---|
| `scientific-pharmacovigilance` | all |
| `scientific-pharmacogenomics` | FDA PGx biomarker |
| `scientific-clinical-trials-analytics` | clinical trialregistry |
| `scientific-admet-pharmacokinetics` | ADMET |
| `scientific-grant-writing` | |

### Dependencies

`pandas`, `numpy`, `requests`, `json`
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Clinical/Health)

Before execution, define:
- [ ] **Study design**: cohort / case-control / RCT / cross-sectional
- [ ] **Population**: inclusion/exclusion criteria, sample size justification
- [ ] **Primary endpoint**: clearly defined with measurement method
- [ ] **Ethical compliance**: IRB/consent/data anonymization confirmed

#### Pass Criteria
- CONSORT/STROBE/PRISMA guidelines followed as applicable
- Confidence intervals reported for all estimates
- Subgroup analyses pre-specified (not data-dredging)
- Adverse events / safety data reported
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
