---
name: scientific-public-health-data
description: |
 dataskill。NHANES investigationdata、MedlinePlus 
 information、RxNorm standard、ODPHP target、
 Health Disparities dataintegrationpipeline。
 ---

# Scientific Public Health Data

NHANES / MedlinePlus / RxNorm / ODPHP / Health Disparities /
Guidelines integrationdatapipeline is provided。

## When to Use

- NHANES investigationdata (value) is retrievedand
- MedlinePlus information is searchedand
- RxNorm 's standardizationmapping is performedand
- ODPHP Healthy People target andreferencewhen needed
- (Health Disparities) dataminwhen needed
- (USPSTF/WHO) is searchedand

---

## Quick Start

## 1. NHANES investigationData Retrieval

```python
import requests
import pandas as pd
import io

NHANES_BASE = "https://wwwn.cdc.gov/nchs/nhanes"


def get_nhanes_dataset(cycle, dataset_name):
 """
 NHANES dataset (XPT/SAS shapeformula) retrieval。

 Parameters:
 cycle: str — investigationcycle (e.g., "2017-2018", "2019-2020")
 dataset_name: str — dataset name (e.g., "DEMO_J", "BIOPRO_J")

 """
 cycle_code = cycle.replace("-", "_")
 url = f"{NHANES_BASE}/search/DataPage.aspx"

 # XPT file's
 xpt_url = f"https://wwwn.cdc.gov/Nchs/Nhanes/{cycle}/{dataset_name}.XPT"
 resp = requests.get(xpt_url)
 resp.raise_for_status

 df = pd.read_sas(io.BytesIO(resp.content), format="xport")
 print(f"NHANES {cycle} {dataset_name}: {df.shape[0]} rows × {df.shape[1]} columns")
 return df


def search_nhanes_variables(keyword):
 """
 NHANES number/countsearch。

 Parameters:
 keyword: str — number/count/'ssearch term

 """
 url = f"{NHANES_BASE}/search/variablelist.aspx"
 params = {"SearchTarget": keyword}
 resp = requests.get(url, params=params)
 resp.raise_for_status

 print(f"NHANES variable search '{keyword}': response received")
 return resp.text
```

## 2. MedlinePlus informationsearch

```python
MEDLINEPLUS_API = "https://connect.medlineplus.gov/service"
MEDLINEPLUS_WS = "https://wsearch.nlm.nih.gov/ws/query"


def search_medlineplus_health_topics(query, language="English"):
 """
 MedlinePlus search。

 """
 params = {
 "db": "healthTopics",
 "term": query,
 }
 resp = requests.get(MEDLINEPLUS_WS, params=params)
 resp.raise_for_status

 # XML response parsing
 import xml.etree.ElementTree as ET
 root = ET.fromstring(resp.text)

 results = []
 for doc in root.findall(".//document"):
 results.append({
 "title": doc.find(".//content[@name='title']").text
 if doc.find(".//content[@name='title']") is not None else "",
 "url": doc.get("url", ""),
 "summary": doc.find(".//content[@name='FullSummary']").text[:300]
 if doc.find(".//content[@name='FullSummary']") is not None else "",
 "rank": doc.get("rank", ""),
 })

 df = pd.DataFrame(results)
 print(f"MedlinePlus search '{query}': {len(df)} health topics")
 return df
```

## 3. RxNorm standard

```python
RXNORM_API = "https://rxnav.nlm.nih.gov/REST"


def rxnorm_lookup(drug_name):
 """
 RxNorm normalizationmapping。

 Parameters:
 drug_name: str — ( or )

 """
 resp = requests.get(
 f"{RXNORM_API}/rxcui.json",
 params={"name": drug_name}
 )
 resp.raise_for_status
 data = resp.json

 rxcui = data.get("idGroup", {}).get("rxnormId", [None])[0]
 if not rxcui:
 print(f"RxNorm: '{drug_name}' not found")
 return None

 # Get properties
 props_resp = requests.get(f"{RXNORM_API}/rxcui/{rxcui}/properties.json")
 props_resp.raise_for_status
 props = props_resp.json.get("properties", {})

 # Get related concepts
 related_resp = requests.get(
 f"{RXNORM_API}/rxcui/{rxcui}/related.json",
 params={"tty": "IN+BN+SBD+SCD"}
 )
 related_resp.raise_for_status
 related = related_resp.json

 result = {
 "rxcui": rxcui,
 "name": props.get("name", ""),
 "tty": props.get("tty", ""),
 "synonym": props.get("synonym", ""),
 "related_concepts": [
 {
 "rxcui": c.get("rxcui"),
 "name": c.get("name"),
 "tty": c.get("tty"),
 }
 for group in related.get("relatedGroup", {}).get("conceptGroup", [])
 for c in group.get("conceptProperties", [])
 ],
 }
 print(f"RxNorm '{drug_name}': RXCUI={rxcui}, TTY={result['tty']}")
 return result
```

## 4. Health Disparities Data Retrieval

```python
HD_API = "https://data.cdc.gov/resource"


def get_health_disparities(indicator, dataset_id="pqnx-3xr5"):
 """
 CDC Data Retrieval。

 Parameters:
 indicator: str — 
 dataset_id: str — CDC Socrata dataset ID

 """
 params = {
 "$where": f"indicator LIKE '%{indicator}%'",
 "$limit": 1000,
 }
 resp = requests.get(f"{HD_API}/{dataset_id}.json", params=params)
 resp.raise_for_status
 data = resp.json

 df = pd.DataFrame(data)
 print(f"Health Disparities '{indicator}': {len(df)} records")
 return df
```

## 5. ODPHP 

```python
ODPHP_API = "https://health.gov/myhealthfinder/api/v3"


def search_health_guidelines(keyword, category=None):
 """
 ODPHP MyHealthfinder guideline search。

 """
 params = {"keyword": keyword}
 if category:
 params["categoryId"] = category
 resp = requests.get(f"{ODPHP_API}/topicsearch.json", params=params)
 resp.raise_for_status
 data = resp.json

 results = []
 for topic in data.get("Result", {}).get("Resources", {}).get("Resource", []):
 results.append({
 "title": topic.get("Title", ""),
 "categories": topic.get("Categories", ""),
 "url": topic.get("AccessibleVersion", ""),
 "sections": [
 s.get("Title", "") for s in topic.get("Sections", {}).get("section", [])
 ],
 })

 df = pd.DataFrame(results)
 print(f"ODPHP search '{keyword}': {len(df)} guidelines")
 return df
```

## 6. guideline search (USPSTF)

```python
def search_clinical_guidelines(query, source="uspstf"):
 """
 USPSTF/WHO guideline search。

 """
 sources = {
 "uspstf": "https://www.uspreventiveservicestaskforce.org/uspstf/api",
 "who": "https://app.magicapp.org/api",
 }
 base_url = sources.get(source, sources["uspstf"])

 resp = requests.get(f"{base_url}/search", params={"q": query})
 if resp.status_code == 200:
 data = resp.json
 results = []
 for item in data.get("results", []):
 results.append({
 "title": item.get("title", ""),
 "grade": item.get("grade", ""),
 "population": item.get("population", ""),
 "date": item.get("date", ""),
 "recommendation": item.get("recommendation", ""),
 })
 df = pd.DataFrame(results)
 else:
 df = pd.DataFrame

 print(f"Guidelines ({source}) search '{query}': {len(df)} recommendations")
 return df
```

---

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

## Pipeline Output

| Output File | Description | Related Skill |
|---|---|---|
| `results/nhanes_data.csv` | NHANES data | → epidemiology-public-health, survival-clinical |
| `results/drug_mapping.json` | RxNorm mapping | → pharmacovigilance, pharmacogenomics |
| `results/health_guidelines.json` | | → clinical-decision-support |
| `results/health_disparities.csv` | | → epidemiology-public-health, causal-inference |

## Pipeline Integration

```
epidemiology-public-health ──→ public-health-data ──→ clinical-decision-support
 (RR/OR/DAG) (NHANES/CDC/ODPHP) (GRADE )
 │
 ├──→ pharmacovigilance (RxNorm + all)
 ├──→ pharmacogenomics (RxNorm + PGx)
 └──→ survival-clinical (NHANES )
```
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
