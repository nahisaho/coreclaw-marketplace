---
name: scientific-clinical-standards
description: |
 Clinical standards skill. CDISC SDTM/ADaM data standards, HL7 FHIR resource mapping, LOINC/SNOMED coding, and regulatory data submission format compliance.
tu_tools:
 - key: loinc
 name: LOINC
 description: forstandardsystem
 - key: icd
 name: ICD
 description: WHO classification ICD-10/ICD-11
tu_tools:
 - key: loinc
 name: LOINC
 description: standardsearch
---

# Scientific Clinical Standards

LOINC / ICD / FHIR / SNOMED CT integration
standardforsearchmappingphaseforpipeline is provided。

## When to Use

- LOINC codeitemstandardizationwhen needed
- ICD-10/ICD-11 classification is searchedand
- FHIR R4 datamappingwhen needed
- differentforsystem'stransformation is performedand
- (EHR) data's standardizationpipeline is builtand
- data's for is performedand

---

## Quick Start

## 1. LOINC codesearch

```python
import requests
import pandas as pd


LOINC_FHIR = "https://fhir.loinc.org"


def loinc_search(query, max_results=20):
 """
 LOINC — search (FHIR API)。

 Parameters:
 query: str — search query (/)
 max_results: int — maximum results
 """
 url = f"{LOINC_FHIR}/CodeSystem/$lookup"
 params = {
 "system": "http://loinc.org",
 "code": query,
 }

 # search
 try:
 resp = requests.get(url, params=params,
 timeout=30)
 if resp.status_code == 200:
 data = resp.json
 params_list = data.get("parameter", [])
 result = {}
 for p in params_list:
 result[p["name"]] = p.get(
 "valueString",
 p.get("valueCode", ""))
 return pd.DataFrame([result])
 except Exception:
 pass

 # search
 url = f"{LOINC_FHIR}/CodeSystem"
 params = {
 "_text": query,
 "_count": max_results,
 }
 resp = requests.get(url, params=params,
 timeout=30)
 resp.raise_for_status
 data = resp.json

 entries = data.get("entry", [])
 rows = []
 for entry in entries:
 resource = entry.get("resource", {})
 rows.append({
 "code": resource.get("id", ""),
 "name": resource.get("name", ""),
 "title": resource.get("title", ""),
 "status": resource.get("status", ""),
 })

 df = pd.DataFrame(rows)
 print(f"LOINC: {len(df)} results for "
 f"'{query}'")
 return df


def loinc_code_detail(loinc_code):
 """
 LOINC — detailsretrieval。

 Parameters:
 loinc_code: str — LOINC code
 (example: "2160-0" = Creatinine)
 """
 url = (f"{LOINC_FHIR}/CodeSystem/"
 f"$lookup")
 params = {
 "system": "http://loinc.org",
 "code": loinc_code,
 }
 resp = requests.get(url, params=params,
 timeout=30)
 resp.raise_for_status
 data = resp.json

 detail = {"loinc_code": loinc_code}
 for p in data.get("parameter", []):
 name = p.get("name", "")
 value = p.get(
 "valueString",
 p.get("valueCode",
 p.get("valueBoolean", "")))
 detail[name] = value

 print(f"LOINC {loinc_code}: "
 f"{detail.get('display', 'N/A')}")
 return detail
```

## 2. ICD-10/ICD-11 classificationsearch

```python
ICD_API = "https://id.who.int"


def icd11_search(query, max_results=20,
 language="en"):
 """
 ICD-11 — WHO classificationsearch。

 Parameters:
 query: str — search query 
 max_results: int — maximum results
 language: str — (en/ja)
 """
 url = (f"{ICD_API}/icd/release/11/"
 f"2024-01/mms/search")
 headers = {
 "Accept": "application/json",
 "Accept-Language": language,
 "API-Version": "v2",
 }
 params = {
 "q": query,
 "subtreesFilter": "",
 "flatResults": "true",
 }

 resp = requests.get(url, params=params,
 headers=headers,
 timeout=30)
 resp.raise_for_status
 data = resp.json

 results = []
 for item in data.get(
 "destinationEntities", [])[:max_results]:
 results.append({
 "code": item.get("theCode", ""),
 "title": item.get("title", ""),
 "chapter": item.get("chapter", ""),
 "score": item.get("score", 0),
 "id": item.get("id", ""),
 })

 df = pd.DataFrame(results)
 print(f"ICD-11: {len(df)} results for "
 f"'{query}'")
 return df


def icd10_to_icd11_mapping(icd10_code):
 """
 ICD-10 → ICD-11 mapping。

 Parameters:
 icd10_code: str — ICD-10 
 (example: "E11" = Type 2 DM)
 """
 url = (f"{ICD_API}/icd/release/11/"
 f"2024-01/mms/codeinfo/"
 f"{icd10_code}")
 headers = {
 "Accept": "application/json",
 "API-Version": "v2",
 }
 try:
 resp = requests.get(url, headers=headers,
 timeout=30)
 if resp.status_code == 200:
 data = resp.json
 print(f"ICD mapping: {icd10_code} → "
 f"{data.get('code', 'N/A')}")
 return data
 except Exception:
 pass

 # : search
 results = icd11_search(icd10_code)
 if not results.empty:
 return results.iloc[0].to_dict

 print(f"ICD mapping: {icd10_code} → not found")
 return {}
```

## 3. FHIR R4 mapping

```python
def create_fhir_observation(
 loinc_code, value, unit,
 patient_id, effective_date):
 """
 FHIR R4 Observation 。

 Parameters:
 loinc_code: str — LOINC code
 value: float — measurementvalue
 unit: str — 
 patient_id: str — patient ID
 effective_date: str — measurementdatetime (ISO 8601)
 """
 observation = {
 "resourceType": "Observation",
 "status": "final",
 "code": {
 "coding": [{
 "system": "http://loinc.org",
 "code": loinc_code,
 }]
 },
 "subject": {
 "reference": f"Patient/{patient_id}"
 },
 "effectiveDateTime": effective_date,
 "valueQuantity": {
 "value": value,
 "unit": unit,
 "system": (
 "http://unitsofmeasure.org"),
 },
 }

 print(f"FHIR Observation: "
 f"LOINC {loinc_code} = {value} {unit}")
 return observation


def create_fhir_condition(
 icd_code, icd_system,
 patient_id, onset_date,
 clinical_status="active"):
 """
 FHIR R4 Condition 。

 Parameters:
 icd_code: str — ICD 
 icd_system: str — "icd10" or "icd11"
 patient_id: str — patient ID
 onset_date: str — (ISO 8601)
 clinical_status: str — status
 """
 system_uri = (
 "http://hl7.org/fhir/sid/icd-10"
 if icd_system == "icd10"
 else "http://id.who.int/icd/release/11/mms"
 )

 condition = {
 "resourceType": "Condition",
 "clinicalStatus": {
 "coding": [{
 "system": ("http://terminology."
 "hl7.org/CodeSystem/"
 "condition-clinical"),
 "code": clinical_status,
 }]
 },
 "code": {
 "coding": [{
 "system": system_uri,
 "code": icd_code,
 }]
 },
 "subject": {
 "reference": f"Patient/{patient_id}"
 },
 "onsetDateTime": onset_date,
 }

 print(f"FHIR Condition: {icd_system.upper} "
 f"{icd_code} ({clinical_status})")
 return condition
```

## 4. forsystemphasetransformation

```python
def cross_reference_codes(code, source_system,
 target_systems=None):
 """
 forsystemphasereference。

 Parameters:
 code: str — 
 source_system: str — system
 ("loinc"/"icd10"/"icd11"/"snomed")
 target_systems: list[str] | None —
 system
 """
 if target_systems is None:
 target_systems = [
 "loinc", "icd10", "icd11", "snomed"]
 target_systems = [
 s for s in target_systems
 if s != source_system]

 mappings = {"source": code,
 "source_system": source_system}

 if source_system == "loinc":
 detail = loinc_code_detail(code)
 mappings["display"] = detail.get(
 "display", "")

 if source_system == "icd10":
 m = icd10_to_icd11_mapping(code)
 if m:
 mappings["icd11"] = m.get("code", "")
 mappings["icd11_title"] = m.get(
 "title", "")

 print(f"Cross-ref: {source_system}:{code} → "
 f"{len(mappings) - 2} mappings")
 return mappings
```

## 5. standardintegrationpipeline

```python
def clinical_standards_pipeline(
 lab_data, diagnosis_data,
 output_dir="results"):
 """
 standardforintegrationpipeline。

 Parameters:
 lab_data: pd.DataFrame — data
 columns: [test_name, value, unit, date]
 diagnosis_data: pd.DataFrame — diagnosisdata
 columns: [diagnosis, icd_code, date]
 output_dir: str — output directory
 """
 from pathlib import Path
 out = Path(output_dir)
 out.mkdir(parents=True, exist_ok=True)

 # 1) LOINC mapping
 loinc_maps = []
 for _, row in lab_data.iterrows:
 result = loinc_search(row["test_name"], 1)
 if not result.empty:
 loinc_maps.append({
 "test_name": row["test_name"],
 "loinc_code": result.iloc[0].get(
 "code", ""),
 "value": row["value"],
 "unit": row["unit"],
 })
 if loinc_maps:
 loinc_df = pd.DataFrame(loinc_maps)
 loinc_df.to_csv(
 out / "loinc_mappings.csv",
 index=False)

 # 2) diagnosis ICD mapping
 icd_maps = []
 for _, row in diagnosis_data.iterrows:
 result = icd11_search(row["diagnosis"], 1)
 if not result.empty:
 icd_maps.append({
 "diagnosis": row["diagnosis"],
 "icd11_code": result.iloc[0].get(
 "code", ""),
 "icd11_title": result.iloc[0].get(
 "title", ""),
 })
 if icd_maps:
 icd_df = pd.DataFrame(icd_maps)
 icd_df.to_csv(
 out / "icd_mappings.csv",
 index=False)

 # 3) FHIR Bundle generation
 fhir_resources = []
 for item in loinc_maps:
 obs = create_fhir_observation(
 item["loinc_code"],
 item["value"], item["unit"],
 "patient-001", "2024-01-01")
 fhir_resources.append(obs)

 print(f"Clinical standards pipeline → {out}")
 return {
 "loinc_mappings": loinc_maps,
 "icd_mappings": icd_maps,
 "fhir_resources": fhir_resources,
 }
```

---

## Pipeline Integration

```
clinical-reporting → clinical-standards → clinical-decision-support
 (report) (forstandardization) (clinical decision supportsupport)
 │ │ ↓
 public-health-data ───────┘ pharmacogenomics
 (data) (genome)
```

## Pipeline Output

| File | Description | Next Skill |
|---------|------|---------|
| `loinc_mappings.csv` | LOINC codemapping | → clinical-decision |
| `icd_mappings.csv` | ICD mapping | → epidemiology |
| `fhir_bundle.json` | FHIR R4 | → EHR integration |

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `loinc` | LOINC | standardsearch |
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
