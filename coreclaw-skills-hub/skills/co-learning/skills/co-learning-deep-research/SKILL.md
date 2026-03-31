---
name: co-learning-deep-research
description: |
  Deep research skill for learning science. Web search, CLI /research command, and
  MCP-based deep research for pedagogical evidence, learning benchmarks, and theory.
  Use when RESEARCHING learning science, pedagogical evidence, instructional design
  benchmarks, or educational theory foundations.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research

Learning-focused deep research with web search and MCP integration.

## Use This Skill When

- Researching learning science evidence or pedagogical theory.
- Finding instructional design benchmarks or effectiveness data.
- Gathering evidence to justify design decisions.
- Reviewing literature on assessment methods or learning strategies.

## Workflow

1. Define research question and required evidence type.
2. Select tool: `web_search` (quick), `/research` CLI (structured), or Deep Research MCP (comprehensive).
3. Execute search with specific, targeted queries.
4. Evaluate source quality (prefer peer-reviewed, meta-analyses, systematic reviews).
5. Synthesize findings with citations and save to files.

## Deliverables

- `report.md`: research summary with cited sources.
- `results/research-findings.md`: structured findings and evidence.

## Quality Gates

- [ ] Research question is clearly defined before search.
- [ ] At least 2 independent sources corroborate key findings.
- [ ] Sources are cited with URLs and access dates.
- [ ] Findings distinguish between correlation and causation.
- [ ] Educational context (level, subject, population) is noted.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 教育研究のエフェクトサイズは分野・対象者・文脈で大きく異なる。メタ分析の結果をそのまま適用しないこと
- "Best practice" without empirical evidence is opinion. Require at least one quantitative source
- 学習スタイル理論（VAK等）は科学的根拠が弱い。エビデンスベースの理論を優先すること

## Validation Loop

1. Execute research and compile findings
2. Check: ≥2 sources, citations present, correlation vs causation noted
3. If any check fails → expand search or add sources
4. Findings ready for use in objective-designer or curriculum-builder
