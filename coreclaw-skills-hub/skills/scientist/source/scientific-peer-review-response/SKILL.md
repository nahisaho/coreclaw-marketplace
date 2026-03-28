---
name: scientific-peer-review-response
description: |
 peer reviewto 's systematicsupport andgenerationskill。
 peer review's structureanalysis（Major/Minor/Editorial classification）、
 timesgeneration、mapping、
 multiplesupport is performed。
 「peer reviewtimes」「reviewer response 」「 」 。
tu_tools:
 - key: crossref
 name: Crossref
 description: literature evidence for review comments
---

# Scientific Peer Review Response

peer reviewstructure、's times is generatedskill。
and 's support explicit、peer reviewto 's is supported。

## When to Use

- frompeer reviewresults（Decision Letter）and
- eachpeer reviewfor/againsttimes is createdand
- inchange andpeer review'smapping is performedand
- 2nd / 3rd 'speer reviewcorrespondingand
- to 's（） is createdand

## Quick Start

## 1. peer reviewsupportworkflow

```
Decision Letter 
 ├─ Phase 1: structure
 │ ├─ peer reviewand min
 │ ├─ each Major / Minor / Editorial classification
 │ ├─ 's
 │ └─ supportdegree's
 ├─ Phase 2: support
 │ ├─ (Accept): 's fix
 │ ├─ partial (Partially Accept): fix + 
 │ ├─ (Rebut): -based
 │ └─ additionexperiment/analysis's
 ├─ Phase 3: timesgeneration
 │ ├─ times
 │ ├─ citation + times + 's 3point
 │ └─ additiondata/figures/tables's insertion
 ├─ Phase 4: mapping
 │ ├─ → 'ssupporttable
 │ ├─ change's
 │ └─ /numberreference
 └─ Phase 5: fileoutput
 ├─ manuscript/response_to_reviewers.md
 ├─ manuscript/response_mapping.json
 └─ manuscript/cover_letter_revised.md
```

## 2. structure

```python
import re
import json
from pathlib import Path

COMMENT_SEVERITY = {
 "major": {
 "keywords": [
 "fundamental", "significant", "serious", "critical",
 "major concern", "major issue", "major revision",
 "additional experiment", "new analysis", "must address",
 "strongly recommend", "", "papers",
 ],
 "weight": 3,
 },
 "minor": {
 "keywords": [
 "minor", "small", "slight", "consider",
 "suggest", "would benefit", "could improve",
 "clarify", "explain", "", "",
 ],
 "weight": 1,
 },
 "editorial": {
 "keywords": [
 "typo", "grammar", "spelling", "formatting",
 "reference", "citation", "figure label", "table format",
 "", "",
 ],
 "weight": 0,
 },
}


def parse_decision_letter(decision_text):
 """
 Decision Letter analysis、peer reviewand 's structure.

 Args:
 decision_text: str — /peer reviewfrom's all

 Returns:
 dict: {
 "editor_decision": "major_revision" | "minor_revision" | "reject",
 "editor_comments": str,
 "reviewers": [
 {
 "id": "Reviewer 1",
 "comments": [
 {
 "number": 1,
 "text": "...",
 "severity": "major" | "minor" | "editorial",
 "requires_new_data": bool,
 "related_section": str,
 }
 ]
 }
 ]
 }
 """
 result = {
 "editor_decision": _detect_decision(decision_text),
 "editor_comments": "",
 "reviewers": [],
 }

 # 'sextraction
 editor_match = re.search(
 r'(?:Editor|Associate Editor|AE)[\'s]*\s*(?:Comments?|Decision)[\s:]*\n(.*?)(?=Reviewer\s+\d|$)',
 decision_text, re.DOTALL | re.IGNORECASE
 )
 if editor_match:
 result["editor_comments"] = editor_match.group(1).strip

 # peer reviewand 's min
 reviewer_sections = re.split(
 r'(Reviewer\s+\d+|Referee\s+\d+)',
 decision_text, flags=re.IGNORECASE
 )

 i = 1
 while i < len(reviewer_sections) - 1:
 reviewer_id = reviewer_sections[i].strip
 reviewer_text = reviewer_sections[i + 1].strip
 comments = _extract_comments(reviewer_text, reviewer_id)
 result["reviewers"].append({
 "id": reviewer_id,
 "comments": comments,
 })
 i += 2

 return result


def _detect_decision(text):
 """'s."""
 text_lower = text.lower
 if "reject" in text_lower and "resubmi" not in text_lower:
 return "reject"
 if "major revision" in text_lower or "major revisions" in text_lower:
 return "major_revision"
 if "minor revision" in text_lower or "minor revisions" in text_lower:
 return "minor_revision"
 if "accept" in text_lower:
 return "accept"
 return "unknown"


def _extract_comments(text, reviewer_id):
 """fromunits extractionclassification."""
 comments = []

 # number'sextraction: "1.", "1)", "(1)", "Comment 1:" 
 numbered = re.split(
 r'(?:^|\n)\s*(?:(\d+)[.\):]|\((\d+)\)|Comment\s+(\d+)\s*:)',
 text
 )

 if len(numbered) > 1:
 # number items
 idx = 0
 for i in range(1, len(numbered), 2):
 num_str = numbered[i] or numbered[i + 1] if i + 1 < len(numbered) else None
 body = numbered[i + 1] if i + 1 < len(numbered) else ""
 if body and body.strip:
 idx += 1
 comments.append(_classify_comment(body.strip, idx))
 else:
 # min
 paragraphs = [p.strip for p in text.split('\n\n') if p.strip]
 for idx, para in enumerate(paragraphs, 1):
 if len(para) > 20: # also 's
 comments.append(_classify_comment(para, idx))

 return comments


def _classify_comment(text, number):
 """'s importantdegreeautomatedclassification."""
 text_lower = text.lower
 severity = "minor" # 

 for sev, config in COMMENT_SEVERITY.items:
 for kw in config["keywords"]:
 if kw.lower in text_lower:
 severity = sev
 break

 # additionexperiment/analysisnecessary's
 requires_new_data = bool(re.search(
 r'additional\s+(?:experiment|data|analysis|result)|'
 r'new\s+(?:experiment|data|analysis)|'
 r'perform\s+(?:additional|further)|'
 r'addition(?:experiment|analysis|data)',
 text_lower
 ))

 # 's
 related_section = _infer_section(text)

 return {
 "number": number,
 "text": text,
 "severity": severity,
 "requires_new_data": requires_new_data,
 "related_section": related_section,
 }


def _infer_section(text):
 """paper is estimated。"""
 text_lower = text.lower
 section_keywords = {
 "Abstract": ["abstract", "summary"],
 "Introduction": ["introduction", "background", "motivation"],
 "Methods": ["method", "experimental", "procedure", "protocol"],
 "Results": ["result", "figure", "table", "data"],
 "Discussion": ["discussion", "interpretation", "mechanism", "implication"],
 "Conclusion": ["conclusion", "concluding"],
 "References": ["reference", "citation", "bibliography"],
 "SI": ["supplementary", "supporting information", "SI"],
 }
 for section, keywords in section_keywords.items:
 if any(kw in text_lower for kw in keywords):
 return section
 return "General"
```

## 3. timesgeneration

```python
RESPONSE_TEMPLATES = {
 "accept": {
 "prefix": "We thank the reviewer for this insightful comment.",
 "action": "As suggested, we have revised the manuscript as follows:",
 "location": "Please see the revised text in {section}, {page_info}.",
 },
 "partially_accept": {
 "prefix": "We appreciate this constructive suggestion.",
 "action": "We have partially addressed this point as follows:",
 "location": "The relevant changes can be found in {section}, {page_info}.",
 },
 "rebut": {
 "prefix": "We respectfully appreciate the reviewer raising this point.",
 "action": "After careful consideration, we believe that:",
 "location": "We have added a clarification in {section}, {page_info}.",
 },
 "new_data": {
 "prefix": "We thank the reviewer for suggesting this additional analysis.",
 "action": "We have performed the requested analysis, and the results show:",
 "location": "The new data are presented in {section} ({figure_info}).",
 },
}


def generate_response_letter(parsed_comments, responses, round_number=1):
 """
 's times is generated。

 Args:
 parsed_comments: dict — parse_decision_letter 's results
 responses: list[dict] — eachto 's support
 [{"reviewer": "Reviewer 1", "comment_num": 1,
 "strategy": "accept" | "partially_accept" | "rebut" | "new_data",
 "response_text": "...",
 "revised_location": {"section": "...", "page": "...", "lines": "..."},
 "new_figure": None | "Figure S3"
 }]
 round_number: int — peer review（1st, 2nd,...）

 Returns:
 str: timesall（Markdown）
 """
 round_label = _ordinal(round_number)

 letter = [
 f"# Response to Reviewers ({round_label} Revision)",
 "",
 "We sincerely thank the editor and reviewers for their constructive "
 "comments and suggestions. We have carefully addressed all the points "
 "raised in the review. Below, we provide our point-by-point responses.",
 "",
 "**Notation:**",
 "- Reviewer comments are shown in **bold italic**.",
 "- Our responses are in regular text.",
 "- Revised text in the manuscript is shown in blue.",
 "",
 "---",
 "",
 ]

 # 
 if parsed_comments.get("editor_comments"):
 letter.extend([
 "## Editor Comments",
 "",
 f"***{parsed_comments['editor_comments']}***",
 "",
 "**Response:** We thank the editor for handling our manuscript and "
 "providing these comments. We have addressed all reviewer concerns "
 "as detailed below.",
 "",
 "---",
 "",
 ])

 # peer reviewand 's times
 for reviewer in parsed_comments["reviewers"]:
 letter.extend([
 f"## {reviewer['id']}",
 "",
 ])

 reviewer_responses = [
 r for r in responses
 if r["reviewer"] == reviewer["id"]
 ]

 for comment in reviewer["comments"]:
 matching = [
 r for r in reviewer_responses
 if r["comment_num"] == comment["number"]
 ]

 letter.extend([
 f"### Comment {comment['number']} [{comment['severity'].upper}]",
 "",
 f"***{comment['text']}***",
 "",
 ])

 if matching:
 resp = matching[0]
 tmpl = RESPONSE_TEMPLATES.get(resp["strategy"], RESPONSE_TEMPLATES["accept"])

 letter.append(f"**Response:** {tmpl['prefix']}")
 letter.append("")
 letter.append(resp["response_text"])
 letter.append("")

 loc = resp.get("revised_location", {})
 if loc:
 location_text = tmpl["location"].format(
 section=loc.get("section", "[Section]"),
 page_info=f"page {loc.get('page', 'X')}, lines {loc.get('lines', 'X-Y')}",
 figure_info=resp.get("new_figure", ""),
 )
 letter.append(location_text)
 letter.append("")
 else:
 letter.extend([
 "**Response:** [times]",
 "",
 ])

 letter.extend(["---", ""])

 return "\n".join(letter)


def _ordinal(n):
 """number/countvalue number/counttabletransformation."""
 suffixes = {1: "1st", 2: "2nd", 3: "3rd"}
 return suffixes.get(n, f"{n}th")
```

## 4. mapping

```python
def generate_response_mapping(parsed_comments, responses, filepath=None):
 """
 peer reviewand 'ssupporttable（） is generated。

 Args:
 parsed_comments: dict
 responses: list[dict]
 filepath: Path

 Returns:
 dict: mappingdata
 """
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "response_mapping.json"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 mapping = {
 "decision": parsed_comments["editor_decision"],
 "total_comments": sum(
 len(r["comments"]) for r in parsed_comments["reviewers"]
 ),
 "summary": {
 "major": 0, "minor": 0, "editorial": 0,
 "accepted": 0, "partially_accepted": 0,
 "rebutted": 0, "new_data_added": 0,
 },
 "reviewers": [],
 }

 for reviewer in parsed_comments["reviewers"]:
 reviewer_map = {
 "id": reviewer["id"],
 "comments": [],
 }

 for comment in reviewer["comments"]:
 mapping["summary"][comment["severity"]] += 1

 matched = [
 r for r in responses
 if r["reviewer"] == reviewer["id"]
 and r["comment_num"] == comment["number"]
 ]

 strategy = matched[0]["strategy"] if matched else "pending"
 location = matched[0].get("revised_location", {}) if matched else {}

 if strategy == "accept":
 mapping["summary"]["accepted"] += 1
 elif strategy == "partially_accept":
 mapping["summary"]["partially_accepted"] += 1
 elif strategy == "rebut":
 mapping["summary"]["rebutted"] += 1
 elif strategy == "new_data":
 mapping["summary"]["new_data_added"] += 1

 reviewer_map["comments"].append({
 "number": comment["number"],
 "severity": comment["severity"],
 "strategy": strategy,
 "section": comment["related_section"],
 "revised_location": location,
 "requires_new_data": comment["requires_new_data"],
 })

 mapping["reviewers"].append(reviewer_map)

 with open(filepath, "w", encoding="utf-8") as f:
 json.dump(mapping, f, indent=2, ensure_ascii=False)

 print(f" → mappingfile save: {filepath}")
 return mapping
```

## 5. 

```python
def generate_revised_cover_letter(parsed_comments, mapping,
 journal_name="", manuscript_id="",
 filepath=None):
 """
 's is generated。

 Args:
 parsed_comments: dict
 mapping: dict — generate_response_mapping 's results
 journal_name: str
 manuscript_id: str
 """
 if filepath is None:
 filepath = BASE_DIR / "manuscript" / "cover_letter_revised.md"
 filepath.parent.mkdir(parents=True, exist_ok=True)

 s = mapping["summary"]
 total = s["major"] + s["minor"] + s["editorial"]

 letter = f"""# Cover Letter (Revised Manuscript)

**Date:** []
**Manuscript ID:** {manuscript_id or "[ID]"}
**Journal:** {journal_name or "[]"}

Dear Editor,

Thank you for the opportunity to revise our manuscript entitled "[title]"
(Manuscript ID: {manuscript_id or "[ID]"}).

We are grateful to the reviewers for their constructive comments, which have
significantly improved the quality of our manuscript. We have carefully
addressed all {total} comments raised by the reviewers.

**Summary of revisions:**

- **Major comments:** {s["major"]} (all addressed)
- **Minor comments:** {s["minor"]} (all addressed)
- **Editorial comments:** {s["editorial"]} (all corrected)

**Key changes in the revised manuscript:**

1. [keychangepoint 1 — number to 'sreference]
2. [keychangepoint 2]
3. [keychangepoint 3]

All changes in the revised manuscript are highlighted in blue for easy
identification. A detailed point-by-point response to each reviewer comment
is provided in the accompanying "Response to Reviewers" document.

We believe that the revised manuscript addresses all concerns raised by the
reviewers and is now suitable for publication in {journal_name or "[]"}.

Sincerely,

[author]
"""

 with open(filepath, "w", encoding="utf-8") as f:
 f.write(letter)

 print(f" → （） save: {filepath}")
 return filepath
```

## 6. Pipeline Integration

```python
def run_review_response_pipeline(decision_letter_path, responses=None,
 round_number=1, journal_name="",
 manuscript_id=""):
 """
 peer reviewsupportpipeline is executed。

 Args:
 decision_letter_path: Path — Decision Letter 's file path
 responses: list[dict] — eachto 'ssupport（None case templateoutput）
 round_number: int — peer review
 journal_name: str
 manuscript_id: str

 output file:
 manuscript/response_to_reviewers.md — times
 manuscript/response_mapping.json — -mapping
 manuscript/cover_letter_revised.md — 
 """
 print("=" * 60)
 print(f"Peer Review Response Pipeline (Round {round_number})")
 print("=" * 60)

 # Phase 1: structure
 print("\n[Phase 1] Decision Letter analysis...")
 with open(decision_letter_path, "r", encoding="utf-8") as f:
 decision_text = f.read

 parsed = parse_decision_letter(decision_text)
 total = sum(len(r["comments"]) for r in parsed["reviewers"])
 print(f" → : {parsed['editor_decision']}")
 print(f" → peer reviewnumber/count: {len(parsed['reviewers'])}")
 print(f" → number/count: {total}")

 for reviewer in parsed["reviewers"]:
 severity_counts = {}
 for c in reviewer["comments"]:
 severity_counts[c["severity"]] = severity_counts.get(c["severity"], 0) + 1
 print(f" → {reviewer['id']}: {severity_counts}")

 # Phase 2-3: timesgeneration
 print("\n[Phase 2-3] times generation...")
 if responses is None:
 responses = _generate_template_responses(parsed)

 letter = generate_response_letter(parsed, responses, round_number)
 letter_path = BASE_DIR / "manuscript" / "response_to_reviewers.md"
 letter_path.parent.mkdir(parents=True, exist_ok=True)
 with open(letter_path, "w", encoding="utf-8") as f:
 f.write(letter)
 print(f" → timessave: {letter_path}")

 # Phase 4: mappinggeneration
 print("\n[Phase 4] -mapping generation...")
 mapping = generate_response_mapping(parsed, responses)

 # Phase 5: generation
 print("\n[Phase 5] generation...")
 generate_revised_cover_letter(parsed, mapping, journal_name, manuscript_id)

 print("\n" + "=" * 60)
 print("peer reviewsupportDone!")
 print("=" * 60)

 return parsed, mapping


def _generate_template_responses(parsed):
 """input's timestemplate is generated。"""
 responses = []
 for reviewer in parsed["reviewers"]:
 for comment in reviewer["comments"]:
 responses.append({
 "reviewer": reviewer["id"],
 "comment_num": comment["number"],
 "strategy": "accept",
 "response_text": "[times]",
 "revised_location": {
 "section": comment["related_section"],
 "page": "X",
 "lines": "X-Y",
 },
 })
 return responses
```

## ToolUniverse Integration

| TU Key | Tool Name | Integration |
|--------|---------|--------|
| `crossref` | Crossref | literature evidence for review comments |

## References

### Output Files

| File | Format | Generation Timing |
|---|---|---|
| `manuscript/response_to_reviewers.md` | times（Markdown） | pipelinecompletion |
| `manuscript/response_mapping.json` | -mapping | pipelinecompletion |
| `manuscript/cover_letter_revised.md` | | pipelinecompletion |

### classificationcriteria

| classification | | support |
|---|---|---|
| Major | conclusion papers | additionexperiment/analysis |
| Minor | improvementpoint（conclusion） | fixaddition |
| Editorial | formula | fix |

### support

| | forsurface | times |
|---|---|---|
| Accept | →fix | + fixcontent |
| Partially Accept | 、 different | + fix + |
| Rebut | | + basis |
| New Data | additionexperiment/analysisnecessary | + data |

### Related Skills

| Skill | Integration |
|---|---|
| `scientific-academic-writing` | Cover Letter templateResponse to Reviewers shape |
| `scientific-critical-review` | cell → peer review's |
| `scientific-revision-tracker` | 'sdiff generation |
| `scientific-paper-quality` | 's metricsevaluation |
| `scientific-citation-checker` | peer reviewaddition citation'sverification |
