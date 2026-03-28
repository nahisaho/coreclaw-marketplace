---
name: scientific-lab-automation
description: |
 Lab automation skill. Laboratory workflow automation, instrument control scripting, sample tracking, experimental protocol automation, and LIMS integration.
tu_tools:
 - key: biotools
 name: bio.tools
 description: experimentautomatedTool Registry Search
---

# Scientific Lab Automation

experimentautomated and protocol'sskill。's 、
protocol's structure、experiment（ELN）integration、
reproducibility's experimentworkflow'sconstruction is supported。

## When to Use

- protocol automatedwhen needed
- experimentprotocolstandardizationwhen needed
- ELN（experiment） and LIMS and 's integrationsettingswhen needed
- reproducibility'sexperimentworkflow is designedand
- loop (HTS) designwhen needed

## Quick Start

### experimentautomatedpipeline

```
Step 1: Protocol Design
 - procedure's structure（input/output/parameters）
 - SOP template
 - parameters's definition
 ↓
Step 2: Automation Script
 - PyLabRobot / Opentrons Python API
 - layoutdefinition
 - 
 ↓
Step 3: Validation
 - （simulation）
 - verification
 - edgetesting
 ↓
Step 4: Execution & Logging
 - automated
 - dataautomated
 - alert
 ↓
Step 5: Documentation
 - ELN entryautomatedgeneration
 - Protocols.io 
 - data（LIMS integration）
```

---

## Phase 1: automated

### PyLabRobot protocol

```python
# PyLabRobot: Universal Python interface for liquid handling robots
# Supports: Hamilton STAR/Vantage, Opentrons OT-2/Flex, Tecan, etc.

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources import Plate, Tip

async def serial_dilution_protocol(lh: LiquidHandler, source_well, dest_plate,
 dilution_factor=2, n_dilutions=8, volume_ul=100):
 """
 systemprotocol。
 PyLabRobot 's API dependency's。
 """
 # all minnote
 buffer_volume = volume_ul * (1 - 1/dilution_factor)
 for i in range(n_dilutions):
 await lh.aspirate(
 resource=lh.deck.get_resource("buffer_trough"),
 volume=buffer_volume,
 )
 await lh.dispense(
 resource=dest_plate[0][i],
 volume=buffer_volume,
 )

 # fromsystem
 transfer_volume = volume_ul / dilution_factor
 await lh.aspirate(resource=source_well, volume=transfer_volume)
 await lh.dispense(resource=dest_plate[0][0], volume=transfer_volume)

 for i in range(n_dilutions - 1):
 await lh.aspirate(resource=dest_plate[0][i], volume=transfer_volume)
 await lh.dispense(resource=dest_plate[0][i+1], volume=transfer_volume)

 return {"status": "complete", "n_dilutions": n_dilutions}
```

### Opentrons OT-2 protocol

```python
from opentrons import protocol_api

metadata = {
 'protocolName': 'Serial Dilution',
 'author': 'SATORI',
 'apiLevel': '2.16',
}

def run(protocol: protocol_api.ProtocolContext):
 # 'sdefinition
 tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
 plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
 reservoir = protocol.load_labware('nest_12_reservoir_15ml', 3)
 pipette = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

 # minnote
 pipette.distribute(
 100,
 reservoir['A1'],
 plate.columns[1:12],
 )

 # system
 pipette.transfer(
 100,
 plate.columns[:11],
 plate.columns[1:12],
 mix_after=(3, 50),
 )
```

---

## Phase 2: protocolstructure

### SOP template

```markdown
## Standard Operating Procedure

### Protocol: [Protocol Name]
**Version**: [X.Y] | **Date**: [YYYY-MM-DD] | **Author**: [name]

### 1. Purpose & Scope

### 2. Materials & Equipment
| Item | Catalog # | Vendor | Quantity |
|------|-----------|--------|----------|

### 3. Reagent Preparation
| Reagent | Final Conc | Stock Conc | Volume | Solvent |
|---------|------------|------------|--------|---------|

### 4. Procedure
| Step | Action | Parameters | Duration | Notes |
|------|--------|------------|----------|-------|
| 1 | | | | |
| 2 | | | | |

### 5. Quality Control
| QC Check | Acceptance Criteria | Method |
|----------|---------------------|--------|

### 6. Data Recording
- [ ] Raw data location: ___
- [ ] Analysis script: ___
- [ ] ELN entry: ___

### 7. Safety
| Hazard | PPE Required | SDS Reference |
|--------|-------------|---------------|

### 8. Revision History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
```

---

## Phase 3: ELN / LIMS integration

### Protocols.io integration

```python
def create_protocol_io_entry(protocol_data):
 """
 Protocols.io API protocol。
 """
 import requests

 headers = {
 "Authorization": f"Bearer {PROTOCOLS_IO_TOKEN}",
 "Content-Type": "application/json",
 }

 payload = {
 "title": protocol_data["title"],
 "description": protocol_data["description"],
 "steps": [
 {"description": step, "duration": dur}
 for step, dur in zip(protocol_data["steps"], protocol_data["durations"])
 ],
 "materials": protocol_data.get("materials", []),
 }

 response = requests.post(
 "https://www.protocols.io/api/v4/protocols",
 headers=headers,
 json=payload,
 )
 return response.json
```

---

## Report Template

```markdown
# Lab Automation Report: [Protocol Name]

**Robot**: [Hamilton STAR / Opentrons OT-2 / etc.]
**Date**: [date]

## 1. Protocol Overview
## 2. Deck Layout
## 3. Execution Log
| Step | Time | Action | Volume | Well | Status |
|------|------|--------|--------|------|--------|

## 4. QC Results
## 5. Data Files Generated
## 6. ELN Entry Reference
```

---

## Completeness Checklist

- [ ] protocolstructure: allstepcleardefinition
- [ ] parametersdefinition: 、temperature、time specification
- [ ] : /simulation
- [ ] QC criteria: criteriadefinition
- [ ] data: automated'ssettings
- [ ] : SOP + ELN entry

## Best Practices

1. **dependencydesign**: PyLabRobot 's API typedependency
2. ****: simulationverification
3. **Dead volume calculation**: 's dead volume amount
4. **degreeverification**: /amountmethod valueverification
5. ****: protocol's change Git 

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `biotools` | bio.tools | experimentautomatedTool Registry Search |

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `protocols/protocol.py` | automatedprotocol（Python） | protocoldesigncompletion |
| `protocols/sop.md` | SOP template（Markdown） | SOP completion |
| `results/qc_report.json` | QC report（JSON） | completion |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-protein-design` | ← designprotein's expressionprotocol |
| `scientific-doe` | ← Experimental Design-basedautomatedprotocoldesign |
| `scientific-process-optimization` | ← optimizationparameters's implementation |
| `scientific-data-preprocessing` | → automatedretrievaldata's preprocessing |
| `scientific-academic-writing` | → automatedmethod's Methods |
---

## Harness Optimization (v0.4.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Database/API Access)

Before execution, define:
- [ ] **Data source**: API endpoint, version, access method
- [ ] **Query scope**: search terms, filters, expected result count
- [ ] **Output format**: JSON/CSV/TSV with expected schema
- [ ] **Rate limiting**: respect API limits, implement retry logic

#### Pass Criteria
- API responses validated against expected schema
- Missing/null values handled and documented
- Data provenance recorded (query, timestamp, version)
- Results cached to avoid redundant API calls
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
