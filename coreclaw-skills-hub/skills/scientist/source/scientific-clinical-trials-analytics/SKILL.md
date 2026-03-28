---
name: scientific-clinical-trials-analytics
description: |
 clinical trialregistryanalysisskill。ClinicalTrials.gov API v2 's
 criteriasearch (disease×××phase×)、trial detail retrieval
 (criteria)、analysis、
 AI support (ClinicalTrialDesignAgent)、bulkData RetrievalCSV export
 integrationresearchsupportpipeline。
---

# Scientific Clinical Trials Analytics

ClinicalTrials.gov registry's data and
minpipeline is provided。40 + 'sfrom
diseasephase filter and
structuredataextraction。

## When to Use

- disease'sclinical trialinvestigationwhen needed
- 'swhen needed
- 's criteriaendpointinformation is retrievedand
- novel's design protocol's referencewhen needed
- data phylogenyextractionwhen needed

---

## Quick Start

## 1. clinical trial searchfilter

```python
import pandas as pd
import json
from datetime import datetime


def search_clinical_trials(condition=None, intervention=None,
 phase=None, status=None,
 location_country=None, sponsor=None,
 start_date_from=None, max_results=100):
 """
 ClinicalTrials.gov criteriasearch。

 Parameters:
 condition: disease (e.g., "non-small cell lung cancer")
 intervention: (e.g., "pembrolizumab")
 phase: phase ("Phase 1", "Phase 2", "Phase 3", "Phase 4")
 status: ("RECRUITING", "COMPLETED", "ACTIVE_NOT_RECRUITING")
 location_country: (e.g., "Japan")
 sponsor: 
 """
 import requests

 base_url = "https://clinicaltrials.gov/api/v2/studies"
 params = {"format": "json", "pageSize": min(max_results, 100)}

 # construction
 query_parts = []
 if condition:
 query_parts.append(f"CONDITION[{condition}]")
 if intervention:
 query_parts.append(f"INTERVENTION[{intervention}]")
 if query_parts:
 params["query.cond"] = condition
 params["query.intr"] = intervention

 if phase:
 params["filter.phase"] = phase
 if status:
 params["filter.overallStatus"] = status
 if location_country:
 params["query.locn"] = location_country

 resp = requests.get(base_url, params=params)
 data = resp.json

 studies = data.get("studies", [])
 total = data.get("totalCount", 0)

 print(f" Search results: {total} trials found")
 print(f" Filters: condition={condition}, intervention={intervention}")
 print(f" Phase: {phase}, Status: {status}")

 results = []
 for study in studies:
 protocol = study.get("protocolSection", {})
 id_module = protocol.get("identificationModule", {})
 status_module = protocol.get("statusModule", {})
 design_module = protocol.get("designModule", {})

 results.append({
 "nct_id": id_module.get("nctId"),
 "title": id_module.get("briefTitle"),
 "status": status_module.get("overallStatus"),
 "phase": design_module.get("phases", [None]),
 "enrollment": design_module.get("enrollmentInfo", {}).get("count"),
 "start_date": status_module.get("startDateStruct", {}).get("date"),
 })

 return pd.DataFrame(results), total
```

## 2. trial detail retrieval

```python
import pandas as pd
import json


def get_trial_details(nct_id):
 """
 NCT ID by/viaclinical trial'salldetailsretrieval。

 retrievalitem:
 - protocol (,,, )
 - criteria (,, /criteria)
 - (key/endpoint)
 - information
 -, research
 - (paper)
 """
 import requests

 url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"
 resp = requests.get(url, params={"format": "json"})
 data = resp.json

 protocol = data.get("protocolSection", {})

 # basicinformation
 id_mod = protocol.get("identificationModule", {})
 design_mod = protocol.get("designModule", {})
 eligibility = protocol.get("eligibilityModule", {})
 outcomes_mod = protocol.get("outcomesModule", {})
 contacts_mod = protocol.get("contactsLocationsModule", {})

 detail = {
 "nct_id": nct_id,
 "title": id_mod.get("officialTitle"),
 "brief_title": id_mod.get("briefTitle"),
 "study_type": design_mod.get("studyType"),
 "phases": design_mod.get("phases"),
 "allocation": design_mod.get("designInfo", {}).get("allocation"),
 "masking": design_mod.get("designInfo", {}).get("maskingInfo", {}).get("masking"),
 }

 # criteria
 detail["eligibility"] = {
 "min_age": eligibility.get("minimumAge"),
 "max_age": eligibility.get("maximumAge"),
 "sex": eligibility.get("sex"),
 "criteria": eligibility.get("eligibilityCriteria"),
 }

 # 
 primary_outcomes = outcomes_mod.get("primaryOutcomes", [])
 secondary_outcomes = outcomes_mod.get("secondaryOutcomes", [])
 detail["primary_outcomes"] = [
 {"measure": o.get("measure"), "timeframe": o.get("timeFrame")}
 for o in primary_outcomes
 ]

 # 
 locations = contacts_mod.get("locations", [])
 detail["n_locations"] = len(locations)
 detail["countries"] = list(set(
 loc.get("country") for loc in locations if loc.get("country")
 ))

 print(f" Trial: {nct_id}")
 print(f" Title: {detail['brief_title']}")
 print(f" Type: {detail['study_type']}, Phase: {detail['phases']}")
 print(f" Primary outcomes: {len(primary_outcomes)}")
 print(f" Locations: {detail['n_locations']} sites in {len(detail['countries'])} countries")

 return detail
```

## 3. analysis

```python
import pandas as pd
import numpy as np


def competitive_landscape_analysis(condition, intervention_class=None,
 status_filter=None):
 """
 disease'sanalysis。

 minitem:
 - phasedistribution (Phase 1/2/3/4)
 - distribution (Recruiting/Completed/Terminated)
 - number/count
 - (start)
 - distribution
 """
 print(f" Competitive landscape for: {condition}")
 if intervention_class:
 print(f" Intervention class: {intervention_class}")

 # phasedistributionanalysis
 phase_mapping = {
 "PHASE1": "Phase 1",
 "PHASE2": "Phase 2",
 "PHASE3": "Phase 3",
 "PHASE4": "Phase 4",
 "EARLY_PHASE1": "Early Phase 1",
 }

 return {"condition": condition, "intervention_class": intervention_class}


def extract_trial_adverse_events(nct_id):
 """
 'sadverse event dataextraction。

 FDA criteria:
 - Serious AE (SAE):,,, 
 - Other AE: Grade 1-4 
 - CTCAE v5.0 grading
 """
 print(f" Extracting adverse events for: {nct_id}")
 print(" Categories: Serious AE, Other AE")
 print(" Grading: CTCAE v5.0")

 return {"nct_id": nct_id}


def extract_trial_outcomes(nct_id):
 """
 results (Results section) from'sdataextraction。

 - Primary outcome measures + results
 - Secondary outcome measures
 - (Screened → Enrolled → Completed → Analyzed)
 """
 print(f" Extracting outcomes for: {nct_id}")

 return {"nct_id": nct_id}
```

## 4. bulkData Retrievalexport

```python
import pandas as pd
import json


def bulk_trial_export(condition, max_trials=1000,
 output_file="results/clinical_trials_export.csv"):
 """
 large-scaleclinical trialdata's bulkretrievalCSV export。

 support (1000 items = 10 × 100 items/)。
 """
 import os
 os.makedirs(os.path.dirname(output_file), exist_ok=True)

 all_results = []
 page_token = None

 print(f" Bulk export for: {condition}")
 print(f" Max trials: {max_trials}")

 # — API 
 # while len(all_results) < max_trials:
 # resp = requests.get(url, params={..., "pageToken": page_token})
 # studies = resp.json["studies"]
 # all_results.extend(studies)
 # page_token = resp.json.get("nextPageToken")

 print(f" Exported to: {output_file}")

 return output_file


def trial_design_summary(trials_df):
 """
 clinical trial's 。

 - Study type distribution (Interventional/Observational)
 - Allocation (Randomized/Non-randomized)
 - Masking (Open/Single/Double/Triple/Quadruple)
 - Primary purpose (Treatment/Prevention/Diagnostic)
 """
 print(" Trial Design Summary:")

 if "study_type" in trials_df.columns:
 type_dist = trials_df["study_type"].value_counts
 for st, count in type_dist.items:
 print(f" {st}: {count}")

 return trials_df.describe
```

## References

### Output Files

| File | Format |
|---|---|
| `results/clinical_trials_search.csv` | CSV |
| `results/trial_details.json` | JSON |
| `results/competitive_landscape.json` | JSON |
| `results/clinical_trials_export.csv` | CSV |
| `results/trial_adverse_events.csv` | CSV |
| `figures/trial_phase_distribution.png` | PNG |
| `figures/trial_timeline.png` | PNG |

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
| `scientific-survival-clinical` | analysis (KM/Cox) |
| `scientific-meta-analysis` | integration |
| `scientific-epidemiology-public-health` | |
| `scientific-clinical-decision-support` | clinical decision support |
| `scientific-pharmacovigilance` | all |

### Dependencies

`pandas`, `numpy`, `requests`, `json`
---

## Harness Optimization (v0.5.0)

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
