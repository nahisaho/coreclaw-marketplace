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
