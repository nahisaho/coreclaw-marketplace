---
name: scientific-latex-formatter
description: |
 LaTeX formatter skill. LaTeX document formatting, equation typesetting, table formatting, figure placement optimization, and style file customization.
tu_tools:
 - key: crossref
 name: Crossref
 description: reference metadata/DOI resolution
---

# Scientific LaTeX Formatter

Markdown LaTeX transformation、specificationtemplate
for.tex file is generatedskill。

## When to Use

- Markdown writing LaTeX shapeformulatransformationwhen needed
- specification's LaTeX template（revtex4, elsarticle ）and
- number/countformulafigures/tablesreference's LaTeX generationwhen needed
- for's.tex +.bib + figures/ formulawhen needed
- Supplementary Information also LaTeX shapewhen needed

## Quick Start

## 1. transformationworkflow

```
Markdown (manuscript/manuscript.md)
 ├─ Phase 1: Markdown → LaTeX basictransformation
 │ ├─ (#, ##, ###) → \section, \subsection
 │ ├─ → \textbf, \textit
 │ ├─ → \begin{itemize/enumerate}
 │ └─ block → \begin{lstlisting} or verbatim
 ├─ Phase 2: element'stransformation
 │ ├─ figure's → \begin{figure}...\includegraphics
 │ ├─ table → \begin{table}...\begin{tabular}
 │ ├─ number/countformula ($...$, $$...$$) → \( \), \[ \], equation environment
 │ ├─ citation [1], [2-5] → \cite{key1}, \cite{key1,key2,...}
 │ └─ phasereference (Figure 1, Table 2) → \ref{fig:1}, \ref{tab:2}
 ├─ Phase 3: templatefor
 │ ├─ documentclass 's settings
 │ ├─ titleauthoraffiliation's structure
 │ ├─ Abstract environment's for
 │ └─ referenceliterature (bibliographystyle) 's settings
 └─ Phase 4: fileoutput
 ├─ manuscript/manuscript.tex
 ├─ manuscript/references.bib
 └─ manuscript/figures/ 
```

## 2. LaTeX template

```python
JOURNAL_TEMPLATES = {
 "nature": {
 "documentclass": r"\documentclass{nature}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 r"\usepackage{natbib}",
 ],
 "bib_style": "naturemag",
 "figure_width": r"0.8\textwidth",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": r"\affiliation{%s}",
 },
 "science": {
 "documentclass": r"\documentclass[12pt]{article}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 r"\usepackage[numbers,sort&compress]{natbib}",
 r"\usepackage{setspace}",
 r"\doublespacing",
 ],
 "bib_style": "Science",
 "figure_width": r"0.9\textwidth",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": None,
 },
 "acs": {
 "documentclass": r"\documentclass[journal=jacsat,manuscript=article]{achemso}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 ],
 "bib_style": "achemso",
 "figure_width": r"3.25in",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": r"\affiliation{%s}",
 },
 "ieee": {
 "documentclass": r"\documentclass[conference]{IEEEtran}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 r"\usepackage{cite}",
 ],
 "bib_style": "IEEEtran",
 "figure_width": r"\columnwidth",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": None,
 },
 "elsevier": {
 "documentclass": r"\documentclass[preprint,12pt]{elsarticle}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 r"\usepackage{lineno}",
 r"\modulolinenumbers[5]",
 ],
 "bib_style": "elsarticle-num",
 "figure_width": r"\textwidth",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": r"\address{%s}",
 },
 "revtex": {
 "documentclass": r"\documentclass[aps,prl,twocolumn,superscriptaddress]{revtex4-2}",
 "packages": [
 r"\usepackage{graphicx}",
 r"\usepackage{amsmath}",
 ],
 "bib_style": "apsrev4-2",
 "figure_width": r"\columnwidth",
 "abstract_env": "abstract",
 "title_cmd": r"\title{%s}",
 "author_cmd": r"\author{%s}",
 "affiliation_cmd": r"\affiliation{%s}",
 },
}
```

## 3. Markdown → LaTeX transformation

```python
import re
from pathlib import Path


def md_to_latex(md_text, journal_format="elsevier"):
 """
 Markdown LaTeX transformation.

 Args:
 md_text: str — Markdown 
 journal_format: str — journal format

 Returns:
 str: LaTeX 
 """
 tex = md_text

 # === ===
 tex = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', tex, flags=re.MULTILINE)
 tex = re.sub(r'^## (.+)$', r'\\subsection{\1}', tex, flags=re.MULTILINE)
 tex = re.sub(r'^# (.+)$', r'\\section{\1}', tex, flags=re.MULTILINE)

 # === formula ===
 tex = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', tex)
 tex = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', tex)
 tex = re.sub(r'\*(.+?)\*', r'\\textit{\1}', tex)

 # === number/countformula ===
 # number/countformula $$...$$ → \[ \] (equation environmentlabel necessarymanual)
 tex = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', tex, flags=re.DOTALL)
 # number/countformula LaTeX also 's ($...$)

 # === figure's ===
 tex = _convert_figures(tex, journal_format)

 # === table's transformation ===
 tex = _convert_tables(tex)

 # === citation's transformation ===
 # [1] → \cite{ref1}, [1, 2] → \cite{ref1,ref2}, [1-3] → \cite{ref1,ref2,ref3}
 tex = re.sub(r'\[(\d+(?:[-,\s]\d+)*)\]', _convert_citation, tex)

 # === 'stransformation ===
 tex = _convert_lists(tex)

 # === ===
 # & and % LaTeX 's
 tex = tex.replace('&amp;', r'\&')
 tex = tex.replace('%', r'\%')

 return tex


def _convert_figures(tex, journal_format):
 """Markdown 's figure LaTeX figure environment transformation."""
 tmpl = JOURNAL_TEMPLATES.get(journal_format, JOURNAL_TEMPLATES["elsevier"])
 fig_width = tmpl["figure_width"]

 def fig_replacer(m):
 alt_text = m.group(1)
 img_path = m.group(2)
 # filefromextension (LaTeX extension also)
 img_base = Path(img_path).stem
 # Figure number alt_text fromextraction
 fig_num = re.search(r'(\d+)', alt_text)
 label = f"fig:{fig_num.group(1)}" if fig_num else f"fig:{img_base}"

 return (
 f"\\begin{{figure}}[htbp]\n"
 f" \\centering\n"
 f" \\includegraphics[width={fig_width}]{{{img_path}}}\n"
 f" \\caption{{{alt_text}}}\n"
 f" \\label{{{label}}}\n"
 f"\\end{{figure}}"
 )

 tex = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fig_replacer, tex)
 return tex


def _convert_tables(tex):
 """Markdown table LaTeX tabular environment transformation."""
 lines = tex.split('\n')
 result = []
 in_table = False
 table_lines = []

 for line in lines:
 if re.match(r'^\|.*\|$', line.strip):
 if not in_table:
 in_table = True
 table_lines = []
 table_lines.append(line.strip)
 else:
 if in_table:
 result.append(_table_to_latex(table_lines))
 in_table = False
 table_lines = []
 result.append(line)

 if in_table:
 result.append(_table_to_latex(table_lines))

 return '\n'.join(result)


def _table_to_latex(table_lines):
 """Markdown table's LaTeX tabular transformation."""
 # header
 headers = [c.strip for c in table_lines[0].strip('|').split('|')]
 n_cols = len(headers)
 col_spec = '|' + '|'.join(['c'] * n_cols) + '|'

 latex = [
 r"\begin{table}[htbp]",
 r" \centering",
 f" \\begin{{tabular}}{{{col_spec}}}",
 r" \hline",
 " " + " & ".join(f"\\textbf{{{h}}}" for h in headers) + r" \\",
 r" \hline",
 ]

 # data（ |---|---| ）
 for line in table_lines[2:]:
 cells = [c.strip for c in line.strip('|').split('|')]
 latex.append(" " + " & ".join(cells) + r" \\")

 latex.extend([
 r" \hline",
 r" \end{tabular}",
 r" \caption{[table's]}",
 r" \label{tab:label}",
 r"\end{table}",
 ])

 return '\n'.join(latex)


def _convert_citation(m):
 """citationnumber \\cite{} shapeformulatransformation."""
 raw = m.group(1)
 # "1-3" → "ref1,ref2,ref3", "1, 2" → "ref1,ref2"
 nums = []
 for part in re.split(r'[,\s]+', raw):
 if '-' in part:
 start, end = part.split('-')
 nums.extend(range(int(start), int(end) + 1))
 else:
 nums.append(int(part))
 keys = ','.join(f"ref{n}" for n in sorted(set(nums)))
 return f"\\cite{{{keys}}}"


def _convert_lists(tex):
 """Markdown LaTeX environment transformation."""
 lines = tex.split('\n')
 result = []
 in_list = False
 list_type = None

 for line in lines:
 ul_match = re.match(r'^(\s*)[-*]\s+(.+)$', line)
 ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)

 if ul_match and not in_list:
 in_list = True
 list_type = "itemize"
 result.append(r"\begin{itemize}")
 result.append(f" \\item {ul_match.group(2)}")
 elif ul_match and in_list and list_type == "itemize":
 result.append(f" \\item {ul_match.group(2)}")
 elif ol_match and not in_list:
 in_list = True
 list_type = "enumerate"
 result.append(r"\begin{enumerate}")
 result.append(f" \\item {ol_match.group(2)}")
 elif ol_match and in_list and list_type == "enumerate":
 result.append(f" \\item {ol_match.group(2)}")
 else:
 if in_list:
 result.append(f"\\end{{{list_type}}}")
 in_list = False
 list_type = None
 result.append(line)

 if in_list:
 result.append(f"\\end{{{list_type}}}")

 return '\n'.join(result)
```

## 4. all.tex filegeneration

```python
def generate_tex_file(manuscript_path, journal_format="elsevier",
 title="", authors="", affiliations="",
 abstract_text="", keywords=None, filepath=None):
 """
 Markdown fromall.tex file is generated。

 Args:
 manuscript_path: Path — input Markdown file
 journal_format: str — journal format
 title, authors, affiliations: str — data
 abstract_text: str — 
 keywords: list[str] — keyword
 filepath: Path — output destination（: manuscript/manuscript.tex）
 """
 from pathlib import Path

 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "manuscript.tex"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 tmpl = JOURNAL_TEMPLATES.get(journal_format, JOURNAL_TEMPLATES["elsevier"])

 # Markdown papers loadtransformation
 with open(manuscript_path, "r", encoding="utf-8") as f:
 md_text = f.read

 body_tex = md_to_latex(md_text, journal_format)

 # construction
 preamble = [tmpl["documentclass"]]
 preamble.extend(tmpl["packages"])
 preamble.append("")

 # titleauthor
 doc_begin = [r"\begin{document}", ""]
 if title:
 doc_begin.append(tmpl["title_cmd"] % title)
 if authors:
 doc_begin.append(tmpl["author_cmd"] % authors)
 if affiliations and tmpl.get("affiliation_cmd"):
 doc_begin.append(tmpl["affiliation_cmd"] % affiliations)
 doc_begin.append(r"\maketitle")

 # 
 if abstract_text:
 doc_begin.extend([
 "",
 f"\\begin{{{tmpl['abstract_env']}}}",
 abstract_text,
 f"\\end{{{tmpl['abstract_env']}}}",
 ])

 # keyword
 if keywords:
 doc_begin.extend([
 "",
 r"\begin{keyword}",
 " \\sep ".join(keywords),
 r"\end{keyword}",
 ])

 # 
 doc_end = [
 "",
 f"\\bibliographystyle{{{tmpl['bib_style']}}}",
 r"\bibliography{references}",
 "",
 r"\end{document}",
 ]

 # binding
 full_tex = '\n'.join(preamble) + '\n' + '\n'.join(doc_begin) + '\n\n'
 full_tex += body_tex + '\n'
 full_tex += '\n'.join(doc_end) + '\n'

 with open(filepath, "w", encoding="utf-8") as f:
 f.write(full_tex)

 print(f" → LaTeX file save: {filepath}")
 return filepath
```

## 5. BibTeX filegeneration

```python
def generate_bib_file(references, filepath=None):
 """
 citationfrom BibTeX file is generated。

 Args:
 references: list[dict] — eachreference'sdata
 [{"key": "ref1", "type": "article", "author": "...",
 "title": "...", "journal": "...", "year": "...",...}]
 filepath: Path — output destination（: manuscript/references.bib）
 """
 from pathlib import Path

 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "references.bib"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 content = ""
 for ref in references:
 ref_type = ref.get("type", "article")
 key = ref.get("key", "unknown")
 fields = []

 for field_name in ["author", "title", "journal", "year", "volume",
 "number", "pages", "doi", "publisher", "booktitle",
 "url", "note"]:
 if field_name in ref and ref[field_name]:
 fields.append(f" {field_name} = {{{ref[field_name]}}}")

 content += f"@{ref_type}{{{key},\n"
 content += ",\n".join(fields)
 content += "\n}\n\n"

 with open(filepath, "w", encoding="utf-8") as f:
 f.write(content)

 print(f" → BibTeX file save: {filepath} ({len(references)} items)")
 return filepath
```

## 6. LaTeX transformationPipeline Integration

```python
def run_latex_pipeline(manuscript_path, journal_format="elsevier",
 title="", authors="", affiliations="",
 abstract_text="", keywords=None, references=None):
 """
 Markdown → LaTeX transformationpipeline is executed。

 output file:
 manuscript/manuscript.tex — LaTeX file
 manuscript/references.bib — BibTeX referencedatabase
 """
 print("=" * 60)
 print("LaTeX Formatter Pipeline")
 print("=" * 60)

 # Phase 1-3: Markdown → LaTeX transformation + templatefor
 print("\n[Phase 1-3] Markdown → LaTeX transformation...")
 tex_path = generate_tex_file(
 manuscript_path, journal_format=journal_format,
 title=title, authors=authors, affiliations=affiliations,
 abstract_text=abstract_text, keywords=keywords,
 )

 # Phase 4: BibTeX generation
 if references:
 print("\n[Phase 4] BibTeX filegeneration...")
 generate_bib_file(references)

 print("\n" + "=" * 60)
 print("LaTeX transformationDone!")
 print(f" : pdflatex manuscript.tex && bibtex manuscript && pdflatex manuscript.tex × 2")
 print("=" * 60)

 return tex_path
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | reference metadata/DOI resolution |

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `manuscript/manuscript.tex` | LaTeX file | transformationcompletion |
| `manuscript/references.bib` | BibTeX referencedatabase | transformationcompletion |

### supporttemplate

| template | documentclass | bib_style |
|---|---|---|
| Nature system | `nature` | `naturemag` |
| Science system | `article` (12pt) | `Science` |
| ACS system | `achemso` | `achemso` |
| IEEE system | `IEEEtran` | `IEEEtran` |
| Elsevier system | `elsarticle` | `elsarticle-num` |
| APS/PRL system | `revtex4-2` | `apsrev4-2` |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | input: `manuscript/manuscript.md` (Markdown ) |
| `scientific-supplementary-generator` | SI 's LaTeX transformationalsosupport |
| `scientific-citation-checker` | citation's verification BibTeX generation |
| `scientific-publication-figures` | `figures/` 's figure `\includegraphics` transformation |

```

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
