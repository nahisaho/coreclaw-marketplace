---
name: scientific-latex-export
description: |
 LaTeX export skill. Markdown-to-LaTeX conversion, journal-specific LaTeX template generation, bibliography management, and publication-ready PDF compilation.
---

# Scientific LaTeX Export

experimentresults papershapeformula（IMRaD: Introduction, Materials & Methods,
Results, Discussion）structure、LaTeX is generatedskill。

## When to Use

- experimentresults papershapeformula and and
- conferencepresentationfor's is createdand
- research and publicationforwhen needed
- arXiv / bioRxiv to 'swhen needed

## Quick Start

### Step 1: experimentdata's
- experiment's
- generation（CSV,, report）
- forskilltool's

### Step 2: IMRaD structureto 'stransformation
1. **Title & Abstract** — research's（250）
2. **Introduction** — backgroundpurposehypothesis
3. **Materials & Methods** — experimentconditionmethodanalysismethod
4. **Results** — datafigures/tables's
5. **Discussion** — results's research and 's comparisonlimitations
6. **References** — citationliterature（BibTeXshapeformula）

### Step 3: figures/tables's shape
- matplotlib / R 's figure publication-quality 
- table LaTeX tabular shapeformulatransformation
- 's

### Step 4: LaTeX generation

## Output Format

```markdown
paper.tex # LaTeX file
paper.bib # BibTeX referenceliterature
figures/ # figurefile
```

### LaTeX templatestructure:
```latex
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx, amsmath, booktabs, hyperref}
\usepackage[japanese]{babel} % paperssupport

\title{...}
\author{...}
\date{\today}

\begin{document}
\maketitle
\begin{abstract}... \end{abstract}

\section{Introduction}
\section{Materials and Methods}
\section{Results}
\section{Discussion}
\section*{Acknowledgments}

\bibliographystyle{unsrt}
\bibliography{paper}
\end{document}
```

## Examples

- 「's experimentresults paper」
- 「IMRaDshapeformula LaTeXoutput」
- 「bioRxivfor's」

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | reference metadata/DOI resolution |

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
