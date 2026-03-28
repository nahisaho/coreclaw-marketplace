---
name: scientific-assistant
description: |
 Harness-optimized scientific research assistant with 195 specialized sub-skills.
 Covers bayesian statistics, deep research, molecular modeling, genomics,
 clinical NLP, cheminformatics, advanced visualization, and more.
 Implements verification loops, quality gates, and eval checkpoints
 following the SHIKIGAMI paradigm (Think → Report → Action iterative cycle).
---

# Scientific Assistant v0.4.0

A harness-optimized collection of 195 scientific research skills, organized
as sub-skill directories within this skill package. v0.3.0 applies token
optimization (English-only prompts) and structured verification loops
inspired by the everything-claude-code harness performance system.

## Harness Optimization

v0.4.0 applies harness performance optimization inspired by
[everything-claude-code](https://github.com/affaan-m/everything-claude-code).
Each sub-skill now includes:

| Feature | Description |
|---------|-------------|
| **Eval Criteria** | Domain-specific pre-execution checklists (10 categories) |
| **5-Phase Verification** | PLAN → EXECUTE → VERIFY → RECOVER → REPORT |
| **10 Quality Gates** | G1-G7 mandatory, G8-G10 recommended |
| **Model Routing** | Task complexity → model tier (fast/standard/premium) |
| **Sub-Agent Orchestration** | Parallel agent splitting for complex tasks |
| **Error Recovery** | Retry with parameter adjustment, graceful degradation |
| **Token Optimization** | Context compaction, structured output, caching |

### Domain Categories

| Category | Sub-skills | Eval Focus |
|----------|-----------|------------|
| Data Analysis | 15 | Statistical validity, reproducibility |
| ML/AI | 12 | Baseline comparison, overfitting check |
| Bioinformatics | 60 | QC metrics, nomenclature, FDR correction |
| Chemistry/Materials | 17 | Structure validation, uncertainty estimates |
| Clinical/Health | 17 | CONSORT/STROBE compliance, safety data |
| Visualization | 7 | Accessibility, save-only, English text |
| Writing/Review | 14 | Citation verification, completeness |
| Experimental | 6 | Orthogonality, power analysis, randomization |
| Databases | 28 | Schema validation, provenance, caching |
| Other | 19 | General measurable outcomes |

## Required: All Charts and Figures Must Use English (All Sub-Skills)

**When creating graphs, charts, or figures (matplotlib / seaborn / plotly / any
visualization library), all text elements MUST be written in English.**

| Text Element | Rule |
|---|---|
| Figure title (`title`, `suptitle`) | **English only** |
| Axis labels (`xlabel`, `ylabel`, `set_xlabel`, `set_ylabel`) | **English only** |
| Legend (`legend`, `label=`) | **English only** |
| Tick labels (`xticklabels`, `yticklabels`) | **English only** |
| Text annotations (`ax.text`, `ax.annotate`, `plt.text`) | **English only** |
| Colorbar label (`colorbar label`) | **English only** |
| Panel labels and captions | **English only** |

```python
# Correct
ax.set_title("Gene Expression by Condition")
ax.set_xlabel("Time (hours)")
ax.set_ylabel("Expression Level (log2 FPKM)")
ax.legend(["Control", "Treatment A", "Treatment B"])
```

---

## Required: Artifact File-Save Rules (All Sub-Skills)

**All artifacts MUST be saved as files. Chat-only output is prohibited.**

| Artifact Type | Format | Example Path |
|---|---|---|
| Reports / analysis results | `report.md` / `report.txt` | `/workspace/group/` |
| Code / scripts | `.py` / `.r` / `.sh` | `/workspace/group/` |
| Numeric results / stats | `results.json` / `summary.csv` | `/workspace/group/results/` |
| Figures / graphs | `.png` / `.svg` / `.pdf` | `/workspace/group/figures/` |
| Papers / drafts | `paper.md` / `paper.tex` | `/workspace/group/` |
| Processed data | `.csv` / `.tsv` / `.parquet` | `/workspace/group/data/` |

### Standard Directory Structure

```
/workspace/group/
├── report.md ← Main report (required)
├── figures/ ← Graphs and figures
│ ├── figure_01.png
│ └── figure_02.png
├── results/ ← JSON/CSV/text results
│ └── summary.json
└── data/ ← Processed data
 └── processed.csv
```

### Required Python Pattern

```python
from pathlib import Path

BASE_DIR = Path("/workspace/group")
FIG_DIR = BASE_DIR / "figures"
RES_DIR = BASE_DIR / "results"
DATA_DIR = BASE_DIR / "data"

for d in [FIG_DIR, RES_DIR, DATA_DIR]:
 d.mkdir(parents=True, exist_ok=True)

# Always save figures to file (never use plt.show)
fig_path = FIG_DIR / "figure_01.png"
fig.savefig(fig_path, dpi=300, bbox_inches="tight")
plt.close(fig)

# Generate embed link for report
fig_rel = fig_path.relative_to(BASE_DIR)
fig_embed = f"![Figure 1: <caption>]({fig_rel})"

# Save results as JSON/CSV
import json
with open(RES_DIR / "summary.json", "w", encoding="utf-8") as f:
 json.dump(results, f, ensure_ascii=False, indent=2)
```

### Required Report Structure

Every report file (`report.md`) must include:

1. **Title and execution timestamp**
2. **Objective / background**
3. **Methods summary**
4. **Results summary** (with numeric/statistical values)
5. **Embedded figures** (see figure-link rules below)
6. **Discussion / conclusions**
7. **Generated file listing** (figures/, results/ inventory)

### Figure Link Rules (Required)

All generated figures must be embedded in `report.md` using Markdown image
links with relative paths from `figures/`.

```markdown
## Results

### Figure 1: Expression Distribution by Condition

![Figure 1: Expression Distribution by Condition](figures/figure_01.png)

Condition B showed significantly higher expression (p < 0.01).

### Figure 2: Principal Component Analysis (PCA)

![Figure 2: PCA](figures/figure_02.png)

PC1 explains 68.3% of total variance with clear separation between conditions.
```

---

## Verification Loop (Harness Optimization)

Every sub-skill execution follows a structured verification loop:

```
Step 1: PLAN — Define scope, inputs, expected outputs
Step 2: EXECUTE — Run analysis pipeline
Step 3: VERIFY — Check outputs against quality gates
Step 4: REPORT — Save all artifacts, generate report.md
```

### Quality Gates

Before marking any task complete, verify:

- [ ] All figures saved to `figures/` (never `plt.show`)
- [ ] All figures embedded in `report.md` with `![caption](figures/filename)`
- [ ] Caption and description follow each figure
- [ ] Numeric results saved to `results/` as JSON or CSV
- [ ] Report includes methods, results, and discussion sections
- [ ] All text in figures is English-only
- [ ] No raw data or analysis output left only in chat

---

## Capabilities

- **Data Analysis**: Bayesian statistics, time-series, anomaly detection, causal inference
- **Life Sciences**: AlphaFold structures, genomics, ADMET pharmacokinetics, clinical NLP
- **Chemistry**: Cheminformatics, molecular dynamics, reaction predictions
- **Research Workflows**: Deep research, systematic reviews, experiment design
- **Visualization**: Advanced plotting, network graphs, geospatial mapping
- **AI/ML**: Active learning, transfer learning, ensemble methods, NLP

## Usage

Each sub-skill is automatically loaded and activated based on the user's
request. The SHIKIGAMI paradigm guides complex research tasks through
iterative cycles of thinking, reporting, and acting.

**Important**: On task completion, chat output should only list saved files
and their summaries. All analysis results, code, and figures must already
be persisted as files.

## MCP Integration

When the `deep-research` MCP server is available, use the `deep-research`
prompt template for literature surveys, prior research, and comprehensive
topic investigation. Combine MCP structured research (question refinement →
sub-question decomposition → web search → source evaluation → report
generation) with scientific evidence hierarchy assessment.
Save research reports as `report.md`, not chat-only output.

## Education Theory Database

Shared with `teaching-assistant`. Data is stored at `skills/teaching-assistant/data/`:

| File | Size | Contents |
|------|------|----------|
| `theories.db` | 1.5MB | 175 education theories (SQLite FTS5 trigram) |
| `theories.json` | 315KB | Education theories in JSON |
| `relations.json` | 9.4KB | Inter-theory relationships (77 entries) |
| `curriculum/*.md` | 5.2MB | Curriculum guidelines (elementary/middle/high school) |

