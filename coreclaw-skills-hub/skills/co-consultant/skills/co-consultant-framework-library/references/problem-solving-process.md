# Problem Solving & Process Frameworks — Detailed Reference

Read this reference when applying problem-solving, root cause analysis, or process improvement frameworks.

## Logic Tree (Detailed)

### 3 Types
| Type | Purpose | Structure |
|------|---------|-----------|
| **What Tree** | Decompose elements | Break a concept into MECE components |
| **Why Tree** | Root cause analysis | Drill into causes layer by layer |
| **How Tree** | Solution generation | Expand action options at each level |

### Application Rules
1. Each branch must be MECE at every level.
2. Maximum 3-4 levels deep (deeper = diminishing returns).
3. Label each node clearly: is it a fact, hypothesis, or action?
4. Validate: cover the node with child nodes? (CE check)

---

## Issue Tree (Detailed)

### Structure
```
Core Issue: [Main business question]
├── Sub-issue 1: [MECE decomposition]
│   ├── Hypothesis 1a: [Testable statement]
│   └── Hypothesis 1b: [Testable statement]
├── Sub-issue 2: [MECE decomposition]
│   ├── Hypothesis 2a
│   └── Hypothesis 2b
└── Sub-issue 3: [MECE decomposition]
    ├── Hypothesis 3a
    └── Hypothesis 3b
```

### Application Rules
1. Core issue must be a question, not a statement.
2. Sub-issues must be MECE and at the same abstraction level.
3. Each hypothesis must be testable with available data.
4. Prioritize hypotheses by impact × testability.

---

## 5 Whys (Detailed)

### Structure
```
Problem: [Observed symptom]
Why 1: [Direct cause] → Answer leads to...
Why 2: [Deeper cause] → Answer leads to...
Why 3: [Systemic cause] → Answer leads to...
Why 4: [Process cause] → Answer leads to...
Why 5: [Root cause] → This is where to intervene
```

### Application Rules
1. Stop when you reach a cause you can **act on**.
2. Not always exactly 5 — could be 3 or 7.
3. Distinguish symptoms from causes.
4. Verify each "because" link: is it actually causal, not just correlational?

---

## Fishbone / Ishikawa (Detailed)

### Standard Categories (6M)
| Category | Examples |
|----------|---------|
| **Man** (People) | Skills, training, motivation, staffing |
| **Machine** (Equipment) | Tools, technology, capacity, maintenance |
| **Method** (Process) | Procedures, standards, workflows |
| **Material** (Inputs) | Raw materials, data quality, suppliers |
| **Measurement** (Metrics) | KPIs, accuracy, calibration |
| **Milieu** (Environment) | Culture, regulations, market conditions |

### Application Rules
1. Categories are a starting framework — adapt to context.
2. Brainstorm causes within each category before prioritizing.
3. Mark the most likely root causes for validation.
4. Combine with 5 Whys for deep causes.

---

## PDCA Cycle (Detailed)

### Phases
| Phase | Activities | Output |
|-------|-----------|--------|
| **Plan** | Define problem, set goals, design solution | Action plan |
| **Do** | Implement on small scale / pilot | Pilot results |
| **Check** | Compare results to goals, analyze gaps | Gap analysis |
| **Act** | Standardize if successful, adjust if not | Updated standard |

### Application Rules
1. "Plan" is the most important phase — invest time here.
2. "Do" should be a limited pilot, not full rollout.
3. "Check" must use measurable criteria defined in "Plan".
4. Iterate: PDCA is a cycle, not a one-time exercise.

---

## ECRS (Detailed)

### Priority Order
| Step | Question | Action |
|------|----------|--------|
| **Eliminate** | Can we remove this step entirely? | Delete unnecessary steps |
| **Combine** | Can we merge two steps? | Reduce handoffs |
| **Rearrange** | Can we reorder for efficiency? | Optimize sequence |
| **Simplify** | Can we make this step easier? | Reduce complexity |

### Application Rules
1. Apply in E→C→R→S order (highest impact first).
2. Map the current process before optimizing.
3. Quantify time/cost savings for each change.
4. Validate that elimination doesn't remove quality checks.
