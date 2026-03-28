---
name: scientific-paper-quality
description: |
 Paper quality assessment skill. Manuscript quality scoring, structural completeness checking, statistical reporting assessment, and writing clarity evaluation.
---

# Scientific Paper Quality

paperquantitativemetrics evaluation、's is supportedskill。
structure.

## When to Use

- 's is performedand
- 's quantitativeevaluationwhen needed
- items（number/count、figures/tablesnumber/count）to 's is verifiedand
- 'sevaluationwhen needed
- tablewhen needed
- 'scomparisonwhen needed
- possible's pointfrom Methods verificationwhen needed

## Quick Start

## 1. workflow

```
 (manuscript/manuscript.md)
 ├─ Dimension 1: metrics
 │ ├─ Flesch-Kincaid Grade Level
 │ ├─ Gunning Fog Index
 │ ├─ mean / mean
 │ └─ 
 ├─ Dimension 2: structure
 │ ├─ （IMRAD rate）
 │ ├─ configuration's
 │ ├─ figures/tables-reference's
 │ └─ 's
 ├─ Dimension 3: table
 │ ├─ (TTR / MTLD)
 │ ├─ forrate
 │ ├─ table's
 │ ├─ / table's
 │ └─ table's
 ├─ Dimension 4: 
 │ ├─ number/count
 │ ├─ figures/tablesnumber/count
 │ ├─ referenceliteraturenumber/count
 │ └─ items
 ├─ Dimension 5: possible
 │ ├─ Methods 's detailsdegree
 │ ├─ method's all
 │ ├─ datafor
 │ └─ /
 └─ output
 └─ manuscript/quality_report.json
```

## 2. metrics

```python
import re
import json
import math
from pathlib import Path
from collections import Counter


def compute_readability(text):
 """
 's metricscalculation.

 Args:
 text: str — analysis

 Returns:
 dict: {
 "flesch_kincaid_grade": float,
 "gunning_fog": float,
 "avg_sentence_length": float,
 "avg_word_length": float,
 "sentences": int,
 "words": int,
 "syllables": int,
 "complex_words": int,
 }
 """
 # preprocessing: Markdown 
 clean = _strip_markdown(text)

 sentences = _split_sentences(clean)
 words = _tokenize_words(clean)
 n_sentences = len(sentences)
 n_words = len(words)

 if n_sentences == 0 or n_words == 0:
 return {"error": "Text is too short"}

 syllable_counts = [_count_syllables(w) for w in words]
 n_syllables = sum(syllable_counts)
 complex_words = sum(1 for s in syllable_counts if s >= 3)

 # Flesch-Kincaid Grade Level
 fk_grade = (0.39 * (n_words / n_sentences)
 + 11.8 * (n_syllables / n_words)
 - 15.59)

 # Gunning Fog Index
 fog = 0.4 * ((n_words / n_sentences) + 100 * (complex_words / n_words))

 return {
 "flesch_kincaid_grade": round(fk_grade, 1),
 "gunning_fog": round(fog, 1),
 "avg_sentence_length": round(n_words / n_sentences, 1),
 "avg_word_length": round(sum(len(w) for w in words) / n_words, 1),
 "sentences": n_sentences,
 "words": n_words,
 "syllables": n_syllables,
 "complex_words": complex_words,
 }


def _strip_markdown(text):
 """Markdown."""
 text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
 text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
 text = re.sub(r'\*(.+?)\*', r'\1', text)
 text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
 text = re.sub(r'\[(.+?)\]\(.*?\)', r'\1', text)
 text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
 text = re.sub(r'`(.+?)`', r'\1', text)
 text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
 text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
 return text


def _split_sentences(text):
 """min."""
 sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
 return [s.strip for s in sentences if s.strip and len(s.strip) > 5]


def _tokenize_words(text):
 """min."""
 return re.findall(r'\b[a-zA-Z]+\b', text)


def _count_syllables(word):
 """'s number/count is estimated。"""
 word = word.lower
 if len(word) <= 3:
 return 1
 vowels = "aeiou"
 count = 0
 prev_vowel = False
 for char in word:
 is_vowel = char in vowels
 if is_vowel and not prev_vowel:
 count += 1
 prev_vowel = is_vowel
 if word.endswith('e') and count > 1:
 count -= 1
 return max(1, count)
```

## 3. structuremin

```python
IMRAD_BALANCE = {
 "ideal_ratios": {
 "Introduction": (0.15, 0.25),
 "Methods": (0.15, 0.30),
 "Results": (0.20, 0.35),
 "Discussion": (0.20, 0.35),
 },
 "abstract_max_words": {
 "nature": 150,
 "science": 125,
 "acs": 250,
 "ieee": 250,
 "elsevier": 300,
 "default": 250,
 },
}


def analyze_structure(text):
 """
 paperstructure's min.

 Returns:
 dict: {
 "section_word_counts": {"Introduction": 450,...},
 "section_ratios": {"Introduction": 0.18,...},
 "balance_score": float (0-1),
 "balance_issues": [...],
 "figure_text_coverage": {...},
 "paragraph_stats": {...},
 }
 """
 sections = _split_into_sections(text)
 total_body_words = 0
 section_words = {}

 # IMRAD 's number/count
 for name, content in sections.items:
 clean = _strip_markdown(content)
 wc = len(_tokenize_words(clean))
 section_words[name] = wc
 if any(k.lower in name.lower for k in
 ["introduction", "method", "result", "discussion"]):
 total_body_words += wc

 # rate
 section_ratios = {}
 if total_body_words > 0:
 for name, wc in section_words.items:
 section_ratios[name] = round(wc / total_body_words, 3)

 # evaluation
 balance_issues = []
 balance_scores = []

 for section, (low, high) in IMRAD_BALANCE["ideal_ratios"].items:
 matched_key = None
 for key in section_ratios:
 if section.lower in key.lower:
 matched_key = key
 break

 if matched_key:
 ratio = section_ratios[matched_key]
 if ratio < low:
 balance_issues.append(
 f"{section} ({ratio:.0%} < {low:.0%})"
 )
 balance_scores.append(ratio / low)
 elif ratio > high:
 balance_issues.append(
 f"{section} ({ratio:.0%} > {high:.0%})"
 )
 balance_scores.append(high / ratio)
 else:
 balance_scores.append(1.0)

 balance_score = sum(balance_scores) / len(balance_scores) if balance_scores else 0.5

 # figures/tablesreference
 figure_refs = set(re.findall(r'(?:Fig(?:ure)?\.?\s*|fig\.?\s*)(\d+)', text, re.IGNORECASE))
 figure_embeds = set(re.findall(r'!\[.*?(?:Fig(?:ure)?\.?\s*|fig\.?\s*)(\d+)', text, re.IGNORECASE))
 table_refs = set(re.findall(r'Table\s+(\d+)', text, re.IGNORECASE))

 # 
 paragraphs = [p for p in text.split('\n\n') if p.strip and not p.strip.startswith('#')]
 para_lengths = [len(_tokenize_words(p)) for p in paragraphs]

 return {
 "section_word_counts": section_words,
 "section_ratios": section_ratios,
 "balance_score": round(balance_score, 2),
 "balance_issues": balance_issues,
 "figure_text_coverage": {
 "figures_referenced": sorted(figure_refs),
 "figures_embedded": sorted(figure_embeds),
 "tables_referenced": sorted(table_refs),
 },
 "paragraph_stats": {
 "count": len(paragraphs),
 "avg_length": round(sum(para_lengths) / max(1, len(para_lengths)), 1),
 "min_length": min(para_lengths) if para_lengths else 0,
 "max_length": max(para_lengths) if para_lengths else 0,
 },
 }
```

## 4. table

```python
WEAK_VERBS = [
 "is", "are", "was", "were", "been", "being",
 "have", "has", "had", "do", "does", "did",
 "make", "makes", "made", "get", "gets", "got",
 "seem", "seems", "seemed", "appear", "appears",
]

REDUNDANT_PHRASES = {
 "in order to": "to",
 "due to the fact that": "because",
 "it is important to note that": "[omit]",
 "it should be noted that": "[omit]",
 "a large number of": "many",
 "a small number of": "few",
 "in the case of": "for",
 "on the other hand": "conversely",
 "at the present time": "now / currently",
 "in the event that": "if",
 "in close proximity to": "near",
 "has the ability to": "can",
 "is able to": "can",
 "as a matter of fact": "[omit]",
 "it is well known that": "[omit or cite]",
 "it has been shown that": "[cite]",
 "take into account": "consider",
 "a number of": "several",
 "the majority of": "most",
 "prior to": "before",
 "subsequent to": "after",
 "in spite of": "despite",
 "for the purpose of": "to / for",
}

HEDGE_WORDS = [
 "might", "could", "may", "possibly", "perhaps",
 "somewhat", "relatively", "apparently", "presumably",
 "likely", "unlikely", "tend to", "seems to",
]

OVERCLAIM_PHRASES = [
 "clearly demonstrates", "undoubtedly", "proves that",
 "unequivocally", "definitely", "without doubt",
 "conclusively proves", "perfect", "always",
 "never", "all cases", "completely",
 "the first to", "novel", "unprecedented",
 "for the first time",
]


def analyze_vocabulary(text):
 """
 table's min.

 Returns:
 dict: {
 "vocabulary_diversity": float (TTR),
 "academic_word_ratio": float,
 "weak_verb_count": int,
 "weak_verb_examples": [...],
 "redundant_phrases": [...],
 "hedge_count": int,
 "overclaim_count": int,
 "overclaim_examples": [...],
 }
 """
 clean = _strip_markdown(text)
 words = _tokenize_words(clean)
 words_lower = [w.lower for w in words]

 if not words:
 return {"error": "Text is too short"}

 # Type-Token Ratio (TTR)
 unique_words = set(words_lower)
 ttr = len(unique_words) / len(words_lower)

 # 
 weak_verb_positions = []
 for i, w in enumerate(words_lower):
 if w in WEAK_VERBS:
 context_start = max(0, i - 3)
 context_end = min(len(words), i + 4)
 weak_verb_positions.append({
 "verb": w,
 "context": " ".join(words[context_start:context_end]),
 })

 # table
 redundant_found = []
 text_lower = clean.lower
 for phrase, suggestion in REDUNDANT_PHRASES.items:
 count = text_lower.count(phrase)
 if count > 0:
 redundant_found.append({
 "phrase": phrase,
 "suggestion": suggestion,
 "count": count,
 })

 # table
 hedge_count = sum(text_lower.count(h) for h in HEDGE_WORDS)

 # 
 overclaim_found = []
 for phrase in OVERCLAIM_PHRASES:
 if phrase.lower in text_lower:
 overclaim_found.append(phrase)

 return {
 "vocabulary_diversity_ttr": round(ttr, 3),
 "total_words": len(words),
 "unique_words": len(unique_words),
 "weak_verb_count": len(weak_verb_positions),
 "weak_verb_examples": weak_verb_positions[:10],
 "redundant_phrases": redundant_found,
 "hedge_count": hedge_count,
 "overclaim_count": len(overclaim_found),
 "overclaim_examples": overclaim_found,
 }
```

## 5. 

```python
JOURNAL_REQUIREMENTS = {
 "nature": {
 "max_words": 3000,
 "max_figures": 8,
 "max_references": 50,
 "max_abstract_words": 150,
 "requires_data_availability": True,
 "requires_author_contributions": True,
 "requires_competing_interests": True,
 },
 "science": {
 "max_words": 2500,
 "max_figures": 4,
 "max_references": 40,
 "max_abstract_words": 125,
 "requires_data_availability": True,
 "requires_author_contributions": True,
 "requires_competing_interests": True,
 },
 "acs": {
 "max_words": 7000,
 "max_figures": 10,
 "max_references": 60,
 "max_abstract_words": 250,
 "requires_data_availability": False,
 "requires_author_contributions": True,
 "requires_competing_interests": True,
 },
 "ieee": {
 "max_words": 8000,
 "max_figures": 12,
 "max_references": 50,
 "max_abstract_words": 250,
 "requires_data_availability": False,
 "requires_author_contributions": False,
 "requires_competing_interests": False,
 },
 "elsevier": {
 "max_words": 8000,
 "max_figures": 15,
 "max_references": 80,
 "max_abstract_words": 300,
 "requires_data_availability": True,
 "requires_author_contributions": True,
 "requires_competing_interests": True,
 },
}


def check_journal_compliance(text, journal_format="elsevier"):
 """
 items to 's.

 Returns:
 dict: {
 "passed": bool,
 "violations": [...],
 "warnings": [...],
 "word_count": int,
 "figure_count": int,
 "reference_count": int,
 }
 """
 reqs = JOURNAL_REQUIREMENTS.get(journal_format, JOURNAL_REQUIREMENTS["elsevier"])
 clean = _strip_markdown(text)
 words = _tokenize_words(clean)
 word_count = len(words)

 # figure's number/count
 figures = set(re.findall(r'!\[.*?\]\(.*?\)', text))
 figure_count = len(figures)

 # referenceliterature's number/count
 ref_section = re.search(r'#{1,2}\s*References(.*)', text, re.DOTALL | re.IGNORECASE)
 ref_count = 0
 if ref_section:
 ref_count = len(re.findall(r'^\s*\d+[.\)]', ref_section.group(1), re.MULTILINE))

 # Abstract number/count
 abstract_match = re.search(r'#{1,2}\s*Abstract\s*\n(.*?)(?=\n#{1,2}\s|\Z)',
 text, re.DOTALL | re.IGNORECASE)
 abstract_words = len(_tokenize_words(abstract_match.group(1))) if abstract_match else 0

 violations = []
 warnings = []

 # number/count
 if word_count > reqs["max_words"]:
 violations.append(
 f"number/count: {word_count} / {reqs['max_words']} "
 f"( {word_count - reqs['max_words']} )"
 )
 elif word_count > reqs["max_words"] * 0.9:
 warnings.append(
 f"number/count: {word_count} / {reqs['max_words']}"
 )

 # figures/tablesnumber/count
 if figure_count > reqs["max_figures"]:
 violations.append(
 f"figures/tablesnumber/count: {figure_count} / {reqs['max_figures']}"
 )

 # referenceliteraturenumber/count
 if ref_count > reqs["max_references"]:
 warnings.append(
 f"referenceliteraturenumber/count: {ref_count} / {reqs['max_references']}"
 )

 # Abstract number/count
 if abstract_words > reqs["max_abstract_words"]:
 violations.append(
 f"Abstract number/count: {abstract_words} / {reqs['max_abstract_words']}"
 )

 # required
 text_lower = text.lower
 if reqs.get("requires_data_availability"):
 if "data availability" not in text_lower and "data access" not in text_lower:
 violations.append("Data Availability Statement items")

 if reqs.get("requires_author_contributions"):
 if "author contribution" not in text_lower and "contributions" not in text_lower:
 warnings.append("Author Contributions items")

 if reqs.get("requires_competing_interests"):
 if "competing interest" not in text_lower and "conflict of interest" not in text_lower:
 warnings.append("Competing Interests items")

 return {
 "journal": journal_format,
 "passed": len(violations) == 0,
 "violations": violations,
 "warnings": warnings,
 "word_count": word_count,
 "abstract_words": abstract_words,
 "figure_count": figure_count,
 "reference_count": ref_count,
 }
```

## 6. possible

```python
REPRODUCIBILITY_CHECKS = {
 "statistical_methods": {
 "patterns": [
 r't-test|ANOVA|chi-square|Mann-Whitney|Kruskal-Wallis|Wilcoxon',
 r'p\s*[<>=]\s*0\.\d+|α\s*=\s*0\.\d+|significance level',
 r'n\s*=\s*\d+|sample size|number of (?:samples|subjects|participants)',
 r'confidence interval|CI|standard (?:deviation|error)',
 r'effect size|Cohen[\'s]?\s*d|η²|R²',
 ],
 "required": ["test_type", "significance_level", "sample_size"],
 },
 "software_versions": {
 "patterns": [
 r'Python\s+\d+\.\d+|R\s+\d+\.\d+|MATLAB\s+R\d{4}',
 r'(?:version|v\.?)\s*\d+\.\d+',
 r'scikit-learn|scipy|numpy|pandas|statsmodels|ggplot',
 ],
 },
 "data_availability": {
 "patterns": [
 r'data\s+(?:are|is)\s+(?:available|deposited|accessible)',
 r'(?:GitHub|Zenodo|Figshare|Dryad)',
 r'accession\s+(?:number|code)',
 r'(?:doi|DOI):\s*10\.\d+',
 ],
 },
}


def check_reproducibility(text):
 """
 Methods 's possible is evaluated。

 Returns:
 dict: {
 "score": float (0-1),
 "checks": {
 "statistical_methods": {"present": [...], "missing": [...]},
 "software_versions": {"present": [...], "missing": [...]},
 "data_availability": {"present": [...], "missing": [...]},
 },
 "recommendations": [...],
 }
 """
 # Methods extraction
 methods_match = re.search(
 r'#{1,2}\s*(?:Methods?|Materials?\s+and\s+Methods?|Experimental)\s*\n(.*?)(?=\n#{1,2}\s|\Z)',
 text, re.DOTALL | re.IGNORECASE
 )
 methods_text = methods_match.group(1) if methods_match else text

 checks = {}
 total_found = 0
 total_checks = 0

 for category, config in REPRODUCIBILITY_CHECKS.items:
 present = []
 for pattern in config["patterns"]:
 matches = re.findall(pattern, methods_text, re.IGNORECASE)
 if matches:
 present.extend(set(matches))

 checks[category] = {
 "present": present,
 "found": len(present) > 0,
 }
 total_checks += 1
 if present:
 total_found += 1

 score = total_found / total_checks if total_checks > 0 else 0

 recommendations = []
 if not checks["statistical_methods"]["found"]:
 recommendations.append(
 "method'sdetails（testing、significance level、sample size）"
 )
 if not checks["software_versions"]["found"]:
 recommendations.append(
 "for/libraryand 's"
 )
 if not checks["data_availability"]["found"]:
 recommendations.append(
 "data's forregarding（ URL ）addition"
 )

 return {
 "score": round(score, 2),
 "checks": checks,
 "recommendations": recommendations,
 }
```

## 7. pipeline

```python
def run_quality_check(manuscript_path, journal_format="elsevier",
 comparison_path=None, filepath=None):
 """
 paperpipeline is executed。

 Args:
 manuscript_path: Path — manuscript file path
 journal_format: str — journal format
 comparison_path: Path — comparisonfor（etc.、mintablefor）
 filepath: Path — report output path

 output file:
 manuscript/quality_report.json — 
 """
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "quality_report.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 print("=" * 60)
 print("Paper Quality Check Pipeline")
 print("=" * 60)

 with open(manuscript_path, "r", encoding="utf-8") as f:
 text = f.read

 # Dimension 1: 
 print("\n[Dim 1] metrics calculation...")
 readability = compute_readability(text)
 print(f" → Flesch-Kincaid Grade: {readability.get('flesch_kincaid_grade', 'N/A')}")
 print(f" → Gunning Fog Index: {readability.get('gunning_fog', 'N/A')}")
 print(f" → mean: {readability.get('avg_sentence_length', 'N/A')} ")

 # Dimension 2: structure
 print("\n[Dim 2] structuremin...")
 structure = analyze_structure(text)
 print(f" → : {structure['balance_score']}")
 for issue in structure["balance_issues"]:
 print(f" ⚠️ {issue}")

 # Dimension 3: table
 print("\n[Dim 3] table min...")
 vocabulary = analyze_vocabulary(text)
 print(f" → (TTR): {vocabulary.get('vocabulary_diversity_ttr', 'N/A')}")
 print(f" → table: {len(vocabulary.get('redundant_phrases', []))} type")
 print(f" → : {vocabulary.get('overclaim_count', 0)} ")

 # Dimension 4: 
 print(f"\n[Dim 4] verification ({journal_format})...")
 compliance = check_journal_compliance(text, journal_format)
 status = "✅ PASS" if compliance["passed"] else "❌ FAIL"
 print(f" → {status}")
 for v in compliance["violations"]:
 print(f" ❌ {v}")
 for w in compliance["warnings"]:
 print(f" ⚠️ {w}")

 # Dimension 5: possible
 print("\n[Dim 5] possible verification...")
 reproducibility = check_reproducibility(text)
 print(f" → possible: {reproducibility['score']}")
 for rec in reproducibility["recommendations"]:
 print(f" 💡 {rec}")

 # (0-100)
 scores = {
 "readability": _readability_score(readability),
 "structure": structure["balance_score"],
 "vocabulary": _vocabulary_score(vocabulary),
 "compliance": 1.0 if compliance["passed"] else 0.5,
 "reproducibility": reproducibility["score"],
 }
 weights = {
 "readability": 0.20,
 "structure": 0.20,
 "vocabulary": 0.20,
 "compliance": 0.25,
 "reproducibility": 0.15,
 }
 overall = sum(scores[k] * weights[k] for k in scores) * 100

 print(f"\n{'=' * 60}")
 print(f": {overall:.0f} / 100")
 print(f"{'=' * 60}")

 # comparison（）
 comparison = None
 if comparison_path:
 print("\n[comparison] 's calculation...")
 with open(comparison_path, "r", encoding="utf-8") as f:
 old_text = f.read
 old_readability = compute_readability(old_text)
 old_scores = {
 "readability": _readability_score(old_readability),
 "structure": analyze_structure(old_text)["balance_score"],
 "vocabulary": _vocabulary_score(analyze_vocabulary(old_text)),
 }
 old_overall = sum(old_scores.get(k, 0) * weights[k] for k in old_scores) * 100
 comparison = {
 "score_change": round(overall - old_overall, 1),
 "improved": overall > old_overall,
 }
 print(f" → : {comparison['score_change']:+.1f}")

 # reportsave
 report = {
 "manuscript": str(manuscript_path),
 "journal": journal_format,
 "overall_score": round(overall, 1),
 "dimension_scores": {k: round(v * 100, 1) for k, v in scores.items},
 "readability": readability,
 "structure": structure,
 "vocabulary": vocabulary,
 "compliance": compliance,
 "reproducibility": reproducibility,
 "comparison": comparison,
 }

 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(report, f, indent=2, ensure_ascii=False)

 print(f"\n → reportsave: {filepath}")
 return report


def _readability_score(readability):
 """ 0-1 transformation.paper's range FK Grade 12-16。"""
 fk = readability.get("flesch_kincaid_grade", 14)
 if 12 <= fk <= 16:
 return 1.0
 elif 10 <= fk < 12 or 16 < fk <= 18:
 return 0.7
 else:
 return 0.4


def _vocabulary_score(vocabulary):
 """ 0-1 transformation."""
 ttr = vocabulary.get("vocabulary_diversity_ttr", 0.5)
 redundant = len(vocabulary.get("redundant_phrases", []))
 overclaim = vocabulary.get("overclaim_count", 0)

 score = min(1.0, ttr * 2) # TTR 0.5 point
 score -= redundant * 0.02 # table 1 items items -0.02
 score -= overclaim * 0.05 # 1 items items -0.05
 return max(0.0, round(score, 2))
```

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

## References

### Output Files

| File | Format | Generated When |
|---|---|---|
| `manuscript/quality_report.json` | | completion |

### metricslist

| Dimension | metrics | range（paper） |
|---|---|---|
| | Flesch-Kincaid Grade | 12-16 |
| | Gunning Fog Index | 12-18 |
| | mean | 15-25 |
| structure | IMRAD | each 15-35% |
| | TTR  | > 0.4 |
| | table | < 5 type |
| | number/count | dependency |
| reproducibility | method | required |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | `manuscript/manuscript.md` 'sevaluation |
| `scientific-critical-review` | cellresults and 's |
| `scientific-peer-review-response` | 's improvement quantitativeverification |
| `scientific-revision-tracker` | 'scomparison |
| `scientific-latex-formatter` | 'sQuality Gates |
---

## Harness Optimization (v0.5.0)

> Optimized following [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
> harness performance patterns: eval-first, multi-phase verification, model routing,
> sub-agent orchestration, and systematic error recovery.

### Eval Criteria (Writing/Review)

Before execution, define:
- [ ] **Target venue**: journal name, word/page limit, citation style
- [ ] **Document structure**: required sections (IMRaD / custom)
- [ ] **Quality standard**: PRISMA / CONSORT / ARRIVE as applicable
- [ ] **Completeness check**: all required sections present

#### Pass Criteria
- All citations verifiable (DOI or PMID present)
- No placeholder text remaining ([TODO], [CITE], etc.)
- Figure/table references match actual figures/tables
- Word count within target range
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
