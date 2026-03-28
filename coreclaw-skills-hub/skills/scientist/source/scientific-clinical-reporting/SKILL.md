---
name: scientific-clinical-reporting
description: |
 reportautomatedgenerationskill。resultssummary (SOAP )、biomarker
 filereport、report、clinical trialstructuretemplate
 (PDF/LaTeX/HTML) output。HL7 FHIR DiagnosticReport shapeformula alsosupport。
---

# Scientific Clinical Reporting

datafromstructurereportautomatedgeneratespipeline is provided。

## When to Use

- results SOAP shapeformula and and
- biomarkerfilereport is createdand
- pharmacogenomicsreport (CPIC ) when needed
- clinical trial's CSR (Clinical Study Report) summary is generatedand
- HL7 FHIR DiagnosticReport shapeformulaoutputwhen needed

---

## Quick Start

## 1. SOAP generation

```python
import json
from datetime import datetime


def generate_soap_note(patient_data, findings, assessment, plan):
 """
 SOAP shapeformula's reportgeneration。

 Parameters:
 patient_data: dict — {"id": "...", "age": 45, "sex": "M",...}
 findings: dict — {"subjective": [...], "objective": [...]}
 assessment: list — evaluationdiagnosis
 plan: list — treatmentdesign
 """
 soap = {
 "report_type": "SOAP_Note",
 "generated_at": datetime.now.isoformat,
 "patient": {
 "id": patient_data.get("id", "ANON"),
 "age": patient_data.get("age"),
 "sex": patient_data.get("sex"),
 },
 "S": { # Subjective
 "chief_complaint": findings.get("chief_complaint", ""),
 "history": findings.get("subjective", []),
 },
 "O": { # Objective
 "vitals": findings.get("vitals", {}),
 "lab_results": findings.get("lab_results", []),
 "imaging": findings.get("imaging", []),
 "physical_exam": findings.get("objective", []),
 },
 "A": { # Assessment
 "diagnoses": assessment,
 "differential": findings.get("differential", []),
 },
 "P": { # Plan
 "treatment": plan,
 "follow_up": findings.get("follow_up", ""),
 "referrals": findings.get("referrals", []),
 },
 }

 print(f"SOAP note: patient={soap['patient']['id']}, "
 f"diagnoses={len(assessment)}, plans={len(plan)}")
 return soap
```

## 2. biomarkerfilereport

```python
import pandas as pd


def biomarker_profile_report(biomarkers_df, reference_ranges=None):
 """
 biomarkerfilereportgeneration。

 Parameters:
 biomarkers_df: DataFrame — columns: [marker, value, unit, specimen]
 reference_ranges: dict — {"marker": {"low": x, "high": y, "unit": "..."}}
 """
 if reference_ranges is None:
 reference_ranges = {
 "CEA": {"low": 0, "high": 5.0, "unit": "ng/mL"},
 "AFP": {"low": 0, "high": 10.0, "unit": "ng/mL"},
 "CA19-9": {"low": 0, "high": 37.0, "unit": "U/mL"},
 "CA125": {"low": 0, "high": 35.0, "unit": "U/mL"},
 "PSA": {"low": 0, "high": 4.0, "unit": "ng/mL"},
 "HER2": {"low": 0, "high": 1, "unit": "IHC score"},
 "Ki-67": {"low": 0, "high": 14, "unit": "%"},
 "PD-L1 TPS": {"low": 0, "high": 1, "unit": "%"},
 }

 results = []
 for _, row in biomarkers_df.iterrows:
 marker = row["marker"]
 value = float(row["value"])
 ref = reference_ranges.get(marker, {})

 status = "normal"
 if ref:
 if value > ref.get("high", float("inf")):
 status = "HIGH"
 elif value < ref.get("low", float("-inf")):
 status = "LOW"

 results.append({
 "marker": marker,
 "value": value,
 "unit": row.get("unit", ref.get("unit", "")),
 "reference": f"{ref.get('low', '?')}-{ref.get('high', '?')}",
 "status": status,
 })

 report_df = pd.DataFrame(results)
 abnormal = report_df[report_df["status"] != "normal"]

 report = {
 "report_type": "Biomarker_Profile",
 "total_markers": len(report_df),
 "abnormal_count": len(abnormal),
 "results": report_df.to_dict("records"),
 "summary": (
 f"{len(abnormal)} of {len(report_df)} markers outside reference range"
 if len(abnormal) > 0
 else "All markers within reference range"
 ),
 }

 print(f"Biomarker profile: {len(report_df)} markers, "
 f"{len(abnormal)} abnormal")
 return report
```

## 3. pharmacogenomicsreport

```python
def pharmacogenomics_report(genotypes, medications):
 """
 CPIC 'spharmacogenomicsreport。

 Parameters:
 genotypes: dict — {"CYP2D6": "*1/*4", "CYP2C19": "*1/*2",...}
 medications: list — ["codeine", "clopidogrel",...]
 """
 # CPIC phenotype mapping 
 cpic_phenotypes = {
 "CYP2D6": {
 "*1/*1": "Normal Metabolizer",
 "*1/*4": "Intermediate Metabolizer",
 "*4/*4": "Poor Metabolizer",
 "*1/*2xN": "Ultrarapid Metabolizer",
 },
 "CYP2C19": {
 "*1/*1": "Normal Metabolizer",
 "*1/*2": "Intermediate Metabolizer",
 "*2/*2": "Poor Metabolizer",
 "*1/*17": "Rapid Metabolizer",
 "*17/*17": "Ultrarapid Metabolizer",
 },
 }

 # recommended 
 drug_gene_map = {
 "codeine": {"gene": "CYP2D6", "action": {
 "Poor Metabolizer": "AVOID — use alternative analgesic",
 "Ultrarapid Metabolizer": "AVOID — toxicity risk",
 "Intermediate Metabolizer": "Use with caution, consider alternative",
 }},
 "clopidogrel": {"gene": "CYP2C19", "action": {
 "Poor Metabolizer": "Use alternative antiplatelet (e.g., prasugrel)",
 "Intermediate Metabolizer": "Consider alternative antiplatelet",
 }},
 }

 recommendations = []
 for drug in medications:
 entry = drug_gene_map.get(drug, {})
 gene = entry.get("gene", "Unknown")
 genotype = genotypes.get(gene, "Unknown")
 phenotype_map = cpic_phenotypes.get(gene, {})
 phenotype = phenotype_map.get(genotype, "Indeterminate")

 action = entry.get("action", {}).get(phenotype, "Standard dosing")
 recommendations.append({
 "drug": drug,
 "gene": gene,
 "genotype": genotype,
 "phenotype": phenotype,
 "recommendation": action,
 "cpic_level": "A" if drug in drug_gene_map else "N/A",
 })

 report = {
 "report_type": "Pharmacogenomics",
 "genotypes_tested": genotypes,
 "medications_queried": medications,
 "recommendations": recommendations,
 }

 print(f"PGx report: {len(genotypes)} genes, {len(medications)} drugs, "
 f"{len(recommendations)} recommendations")
 return report
```

## 4. structurereportoutput (LaTeX/HTML)

```python
def export_clinical_report(report, output_format="html",
 output_path="reports/clinical_report"):
 """
 report LaTeX/HTML/FHIR JSON shapeformulaoutput。

 Parameters:
 report: dict — SOAP, Biomarker, PGx report
 output_format: "html", "latex", "fhir_json"
 output_path: str — output destination (extension)
 """
 import os
 os.makedirs(os.path.dirname(output_path), exist_ok=True)
 report_type = report.get("report_type", "Clinical")

 if output_format == "html":
 filepath = f"{output_path}.html"
 html_parts = [
 "<!DOCTYPE html><html><head>",
 f"<title>{report_type} Report</title>",
 "<style>body{font-family:Arial;margin:2em;}"
 "table{border-collapse:collapse;width:100%;}"
 "td,th{border:1px solid #ddd;padding:8px;}</style>",
 "</head><body>",
 f"<h1>{report_type} Report</h1>",
 ]

 if report_type == "SOAP_Note":
 for section in ["S", "O", "A", "P"]:
 html_parts.append(f"<h2>{section}</h2>")
 html_parts.append(f"<pre>{json.dumps(report.get(section, {}), indent=2, ensure_ascii=False)}</pre>")

 elif report_type == "Biomarker_Profile":
 html_parts.append("<table><tr><th>Marker</th><th>Value</th>"
 "<th>Reference</th><th>Status</th></tr>")
 for r in report.get("results", []):
 status_color = "red" if r["status"] != "normal" else "green"
 html_parts.append(
 f"<tr><td>{r['marker']}</td><td>{r['value']} {r['unit']}</td>"
 f"<td>{r['reference']}</td>"
 f"<td style='color:{status_color}'>{r['status']}</td></tr>"
 )
 html_parts.append("</table>")

 html_parts.append("</body></html>")
 with open(filepath, "w") as f:
 f.write("\n".join(html_parts))

 elif output_format == "fhir_json":
 filepath = f"{output_path}.fhir.json"
 fhir = {
 "resourceType": "DiagnosticReport",
 "status": "final",
 "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074",
 "code": "LAB"}]}],
 "code": {"text": report_type},
 "issued": report.get("generated_at", datetime.now.isoformat),
 "result": [],
 }
 with open(filepath, "w") as f:
 json.dump(fhir, f, indent=2)

 elif output_format == "latex":
 filepath = f"{output_path}.tex"
 with open(filepath, "w") as f:
 f.write(f"\\documentclass{{article}}\n")
 f.write(f"\\title{{{report_type} Report}}\n")
 f.write("\\begin{document}\n\\maketitle\n")
 f.write(f"Report type: {report_type}\n")
 f.write("\\end{document}\n")

 print(f"Report exported: {filepath}")
 return filepath
```

## References

### Output Files

| File | Format |
|---|---|
| `reports/soap_note.json` | JSON |
| `reports/biomarker_profile.json` | JSON |
| `reports/pgx_report.json` | JSON |
| `reports/clinical_report.html` | HTML |
| `reports/clinical_report.tex` | LaTeX |
| `reports/clinical_report.fhir.json` | FHIR JSON |

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
| `scientific-variant-interpretation` | report |
| `scientific-variant-effect-prediction` | |
| `scientific-pharmacogenomics` | PGx |
| `scientific-precision-oncology` | tumorreport |
| `scientific-disease-research` | diseaseinformationintegration |

### Dependencies

`pandas`, `json` (stdlib), `datetime` (stdlib)
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
