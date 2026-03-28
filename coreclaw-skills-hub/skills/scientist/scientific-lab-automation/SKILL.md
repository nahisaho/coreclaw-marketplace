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
