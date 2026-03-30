---
name: co-growth-deep-research
description: |
  Deep research skill for growth. Web search, CLI /research command, and MCP-based
  deep research for growth benchmarks, competitive analysis, and market data.
  Use when RESEARCHING growth benchmarks, competitive landscapes, market trends,
  conversion rate baselines, or industry best practices.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research

Growth-focused deep research with web search and MCP integration.

## Use This Skill When

- Researching industry growth benchmarks or conversion baselines.
- Conducting competitive analysis on growth strategies.
- Finding market data to justify MDE or experiment hypotheses.
- Gathering best practices for funnel optimization.

## Workflow

1. Define research question and required evidence type.
2. Select tool: `web_search` (quick), `/research` CLI (structured), or Deep Research MCP (comprehensive).
3. Execute search with specific, targeted queries.
4. Evaluate source quality (prefer peer-reviewed, official reports, reputable benchmarks).
5. Synthesize findings with citations and save to files.

## Deliverables

- `report.md`: research summary with cited sources.
- `results/research-findings.md`: structured findings and evidence.

## Quality Gates

- [ ] Research question is clearly defined before search.
- [ ] At least 2 independent sources corroborate key findings.
- [ ] Sources are cited with URLs and access dates.
- [ ] Findings distinguish between correlation and causation.
- [ ] Benchmark data includes industry, region, and time period context.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- SaaS benchmark reports vary widely by industry and company stage. Always note the benchmark's cohort definition.
- Competitor growth claims are often cherry-picked. Cross-reference with independent sources (e.g., SimilarWeb, app store data).
- "Best practice" without data is opinion. Require at least one quantitative source for any recommendation.

## Validation Loop

1. Execute research and compile findings
2. Check: ≥2 sources, citations present, correlation vs causation noted
3. If any check fails → expand search or add sources
4. Findings ready for use in experiment-design or funnel-analysis
