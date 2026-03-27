---
name: teaching-assistant
description: |
  AI assistant skill for educators. Built with reference to the SHIDEN project,
  featuring 10 specialized sub-skills for lesson planning, material creation,
  assessment design, individualized instruction, feedback generation,
  student guidance, and meta-prompt generation. Provides practical educational
  support grounded in 175 education theories and curriculum guidelines.
---

# Teaching Assistant

A comprehensive AI assistant skill package for educators.

## Feature List

### Prompts (Education Content Generation)

| Skill | Description | 主な教育理論 |
|--------|------|-------------|
| **meta-prompt** | Meta-prompt generation (context collection) | Structured question design |
| **lesson-plan** | Bloom's Taxonomy-based lesson planning | Bloom's Taxonomy, Gagné's Nine Events |
| **materials** | Material creation (worksheets, slides, quizzes) | Gagné's Nine Events, ARCS Model, UDL |
| **assessment** | Assessment design (rubrics, tests, formative assessment) | Constructive Alignment, Bloom's Taxonomy |
| **individual** | Individualized instruction plan (learner profile-based) | ZPD, Differentiated Instruction |
| **feedback** | Growth Mindset-based feedback | Growth Mindset, Self-Regulated Learning |
| **guidance** | Student guidance plan (developmental stage-aware) | Erikson, Kohlberg, Piaget, PBIS |

### Skills (Internal Support Functions)

| Skill | Description |
|--------|------|
| **orchestrator** | Intent analysis and skill routing |
| **theory-lookup** | Reference 175 education theories |
| **context-manager** | Cross-skill context management |

## Usage

The orchestrator automatically selects the appropriate skill based on user requests.

### Examples

- "Create lesson plan for 8th grade linear functions" → lesson-plan
- "Create 3rd grade science worksheet" → materials
- "Create an English rubric" → assessment
- "Design instruction plan for this student" → individual
- "Write feedback on this essay" → feedback
- "Plan response for student with truancy tendency" → guidance

## Supported School Levels

- Elementary school (lower/upper grades)
- Middle school
- High school
- University

## Curriculum Standards

Education content for elementary/middle/high school is generated based on curriculum standards.

## Database

The following databases are stored in the `data/` directory:

## MCP Integration

When the `deep-research` MCP server is available, use the `deep-research` prompt template
for education theory research and latest pedagogical study exploration.
Particularly effective for education theory comparison, evidence-based practice surveys, and
curriculum revision background research. When MCP is unavailable, use the built-in theories.db and curriculum.db.

| File | Size | Contents |
|---------|--------|------|
| `theories.db` | 1.5MB | 175 education theories (SQLite FTS5 trigram) |
| `theories.json` | 315KB | Education theories in JSON |
| `relations.json` | 9.4KB | Inter-theory relationships (77 entries) |
| `curriculum.db` | 13MB | Curriculum standards SQLite DB (2657 sections, FTS5 trigram) |

### Using curriculum.db

学習指導要領を検索する場合は **必ず `curriculum.db` を使用** してください。
`curriculum/*.md` を grep で検索してはいけません（5.2MB のファイルスキャンは非常に遅いため）。

```sql
-- 3文字以上のキーワード: FTS5検索（高速）
SELECT s.school_level, s.heading, s.body
FROM sections_fts f JOIN sections s ON f.rowid = s.rowid
WHERE sections_fts MATCH 'キーワード（3文字以上）'
LIMIT 10;

-- 2文字のキーワード: LIKE フォールバック
SELECT school_level, heading, body
FROM sections
WHERE (heading LIKE '%キーワード%' OR body LIKE '%キーワード%')
LIMIT 10;

-- 学校種で絞り込み
SELECT school_level, heading, body
FROM sections
WHERE school_level = '小学校'
AND (heading LIKE '%体育%' OR body LIKE '%体育%')
LIMIT 10;
```

**school_level の値**: `小学校`, `中学校`, `高等学校`

---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis pipeline
VERIFY  → check outputs against quality gates
REPORT  → save all artifacts, generate report
```

### Quality Gates

- [ ] All outputs include explicit assumptions and constraints
- [ ] Traceable reasoning between steps
- [ ] Final recommendation with clear next actions
- [ ] Artifacts saved as files (not chat-only output)
