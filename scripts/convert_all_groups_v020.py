#!/usr/bin/env python3
"""
Batch harness optimization script for all non-scientist skill groups.
Upgrades to v0.2.0 with:
- Verification loop sections added to every SKILL.md
- Japanese text in frontmatter/body converted to English
- skill.json version bumped to v0.2.0
- main.py updated with harness metadata
- source/SKILL.md synced
"""

import json
import re
from pathlib import Path

SKILLS_DIR = Path("coreclaw-skills-hub/skills")

# Groups to process (skip scientist - already done)
GROUPS = [
    "agent-skills-builder",
    "compliance",
    "consultant",
    "consultant-acn",
    "consultant-bcg",
    "consultant-mck",
    "consultant-pwc",
    "diligence",
    "educationalist",
    "enterprise",
    "growth",
    "learning",
    "sales",
    "secops",
    "supply",
]

# ── Japanese → English common replacements ──
JP_EN_REPLACEMENTS = [
    # Section headers
    ("## ワークフロー", "## Workflow"),
    ("## プロンプト一覧", "## Prompt List"),
    ("## スキル一覧", "## Skills"),
    ("## 使い方", "## Usage"),
    ("## フレームワーク", "## Frameworks"),
    ("## 品質ゲート", "## Quality Gates"),
    ("## 品質基準", "## Quality Criteria"),
    ("## MCP連携", "## MCP Integration"),
    ("## 対応学校種", "## Supported School Levels"),
    ("## 学習指導要領", "## Curriculum Standards"),
    ("## データベース", "## Database"),
    ("## 機能一覧", "## Feature List"),
    ("## 目的", "## Purpose"),
    ("## 対話方針", "## Interaction Policy"),
    ("## 想定ワークフロー", "## Expected Workflow"),
    ("## 入力", "## Input"),
    ("## 出力", "## Output"),
    ("## 文字数制約", "## Character Limits"),

    # Sub-section headers
    ("### プロンプト（教育コンテンツ生成）", "### Prompts (Education Content Generation)"),
    ("### スキル（内部支援機能）", "### Skills (Internal Support Functions)"),
    ("### 例", "### Examples"),
    ("### curriculum.db の使い方", "### Using curriculum.db"),
    ("### 参照スキル", "### Related Skills"),
    ("### 出力ファイル", "### Output Files"),

    # Table headers
    ("| スキル | 説明 |", "| Skill | Description |"),
    ("| スキル | 説明 | 主な教育理論 |", "| Skill | Description | Key Theory |"),
    ("| プロンプト | フェーズ | 説明 |", "| Prompt | Phase | Description |"),
    ("| カテゴリ | 件数 | 代表例 |", "| Category | Count | Examples |"),
    ("| ファイル | サイズ | 内容 |", "| File | Size | Contents |"),
    ("| フレームワーク | 説明 |", "| Framework | Description |"),
    ("| フェーズ | 内容 |", "| Phase | Description |"),
    ("| 項目 | 内容 |", "| Item | Description |"),
    ("| TU Key | ツール名 | 連携内容 |", "| TU Key | Tool Name | Integration |"),
    ("| TU Key | ツール名 | 用途 |", "| TU Key | Tool Name | Usage |"),
    ("| ファイル | 形式 | 生成タイミング |", "| File | Format | Generated When |"),
    ("| テキスト要素 | 規則 |", "| Text Element | Rule |"),
    ("| 成果物の種類 | 保存形式 | 保存先の例 |", "| Artifact Type | Format | Example Path |"),
    ("| パラメータ | 説明 |", "| Parameter | Description |"),
    ("| メトリクス | 説明 |", "| Metric | Description |"),
    ("| ステップ | 内容 |", "| Step | Description |"),

    # Common inline text
    ("で発火。", "triggers this skill."),
    ("で発火", "triggers this skill"),
    ("## ToolUniverse 連携", "## ToolUniverse Integration"),
    ("## パイプライン統合", "## Pipeline Integration"),
    ("## パイプライン出力", "## Pipeline Output"),
    ("## 標準パイプライン", "## Standard Pipeline"),
    ("## 利用可能ツール (ToolUniverse SMCP)", "## Available Tools (ToolUniverse SMCP)"),
    ("## 利用可能ツール", "## Available Tools"),
]

# ── Consultant-specific full body translations ──
CONSULTANT_BODY_TRANSLATIONS = {
    "consultant": {
        "深層リサーチ＆コンサルティング分析のためのAIアシスタントスキルパッケージです。":
            "AI assistant skill package for deep research and consulting analysis.",
        "4つのフェーズで構成されるコンサルティングワークフローを提供します。":
            "Provides a consulting workflow composed of 4 phases.",
        "各フェーズ間に品質ゲートを設けて、分析品質を担保します。":
            "Quality gates between phases ensure analysis quality.",
        "ユーザーのリクエストに応じて、orchestrator が適切なフェーズを自動選択します。":
            "The orchestrator automatically selects the appropriate phase based on user requests.",
    },
    "consultant-acn": {
        "アクセンチュアのメソドロジーを活用した深層リサーチ＆コンサルティング分析スキルです。":
            "Deep research and consulting analysis skill using Accenture methodologies.",
        "DX戦略、コスト変革、オペレーション最適化、価値創造に特化したフレームワークを提供します。":
            "Provides frameworks for DX strategy, cost transformation, operations optimization, and value creation.",
    },
    "consultant-bcg": {
        "ボストンコンサルティンググループ（BCG）のメソドロジーを活用した深層リサーチ＆コンサルティング分析スキルです。":
            "Deep research and consulting analysis skill using BCG methodologies.",
        "ポートフォリオ戦略、コスト・オペレーション、戦略立案、価値創造に特化したフレームワークを提供します。":
            "Provides frameworks for portfolio strategy, cost operations, strategy formulation, and value creation.",
    },
    "consultant-mck": {
        "マッキンゼーのコンサルティング手法を活用した深層リサーチ＆コンサルティング分析スキルです。":
            "Deep research and consulting analysis skill using McKinsey methodologies.",
        "仮説駆動、MECE、ピラミッド原則、7Sフレームワークを中核としたアプローチを提供します。":
            "Provides hypothesis-driven, MECE, Pyramid Principle, and 7S Framework-centered approaches.",
    },
    "consultant-pwc": {
        "PwCのコンサルティング手法を活用した深層リサーチ＆コンサルティング分析スキルです。":
            "Deep research and consulting analysis skill using PwC methodologies.",
        "「Fit for Growth」「Strategy&」「BXT」「TIMM」を中核としたアプローチを提供します。":
            "Provides Fit for Growth, Strategy&, BXT, and TIMM-centered approaches.",
    },
}

# ── Consultant titles ──
CONSULTANT_TITLES = {
    "consultant": ("# Consultant Assistant", "# Consultant Assistant"),
    "consultant-acn": ("# Consultant ACN（アクセンチュア式コンサルティング）", "# Consultant ACN (Accenture-Style Consulting)"),
    "consultant-bcg": ("# Consultant BCG（BCG式コンサルティング）", "# Consultant BCG (BCG-Style Consulting)"),
    "consultant-mck": ("# Consultant McK（マッキンゼー式コンサルティング）", "# Consultant McK (McKinsey-Style Consulting)"),
    "consultant-pwc": ("# Consultant PwC（PwC式コンサルティング）", "# Consultant PwC (PwC-Style Consulting)"),
}

# ── Educationalist-specific translations ──
EDUCATIONALIST_TRANSLATIONS = {
    "教育者のための包括的なAIアシスタントスキルパッケージです。":
        "A comprehensive AI assistant skill package for educators.",
    "ユーザーのリクエストに応じて、orchestrator が適切なスキルを自動選択します。":
        "The orchestrator automatically selects the appropriate skill based on user requests.",
    "小中高の教育コンテンツ生成時は、学習指導要領に基づいた内容を生成します。":
        "Education content for elementary/middle/high school is generated based on curriculum standards.",
    "以下のデータベースが `data/` ディレクトリに格納されています：":
        "The following databases are stored in the `data/` directory:",
}

EDUCATIONALIST_TITLE = ("# Teaching Assistant", "# Teaching Assistant")

# ── Agent Skills Builder translations ──
BUILDER_TRANSLATIONS = {
    "CoreClaw向けのSkillを、対話ベースで要件発見しながら作るビルダーです。":
        "A builder that creates CoreClaw Skills through dialogue-based requirements discovery.",
    "Skill作成の標準化":
        "Standardization of skill creation",
    "ユーザーニーズの深掘り":
        "Deep exploration of user needs",
    "表面的な要求の背後にある「真の目的」を特定する":
        "Identify the 'true objective' behind surface-level requests",
    "表面的な要求の裏にある真の目的を見極める":
        "Identify the true objective behind surface-level requests",
}

# ── Workflow phase translations (consultant-style) ──
WORKFLOW_PHASE_TRANSLATIONS = [
    ("Phase 1: Purpose Discovery（目的探索）", "Phase 1: Purpose Discovery"),
    ("Phase 2: Deep Research（深層リサーチ）", "Phase 2: Deep Research"),
    ("Phase 3: Framework Analysis（フレームワーク分析）", "Phase 3: Framework Analysis"),
    ("Phase 4: Report Writing（レポート生成）", "Phase 4: Report Writing"),
    ("Phase 1: 問題定義", "Phase 1: Problem Definition"),
    ("Phase 2: 仮説構築", "Phase 2: Hypothesis Construction"),
    ("Phase 3: イシュー分解", "Phase 3: Issue Decomposition"),
    ("Phase 4: データ収集・分析", "Phase 4: Data Collection & Analysis"),
    ("Phase 5: 統合・提言", "Phase 5: Integration & Recommendations"),
    ("Phase 1: 課題診断", "Phase 1: Problem Diagnosis"),
    ("Phase 2: 戦略立案（Strategy&）", "Phase 2: Strategy Formulation (Strategy&)"),
    ("Phase 3: Fit for Growth 分析", "Phase 3: Fit for Growth Analysis"),
    ("Phase 4: トータルインパクト測定（TIMM）", "Phase 4: Total Impact Measurement (TIMM)"),
    ("Phase 5: 実行＆変革", "Phase 5: Execution & Transformation"),

    # Arrow descriptions
    ("↓ 5 Whys / JTBD で「真の目的」を発見", "↓ Discover true objective via 5 Whys / JTBD"),
    ("↓ Think→Action→Report サイクルで情報収集", "↓ Gather information via Think→Action→Report cycle"),
    ("↓ 53フレームワークで構造化分析", "↓ Structured analysis with 53 frameworks"),
    ("↓ ピラミッド原則に基づくレポート作成", "↓ Report writing based on Pyramid Principle"),
    ("↓ Hypothesis-Driven Approach で課題特定", "↓ Problem identification via Hypothesis-Driven Approach"),
    ("↓ Think→Action→Report サイクル", "↓ Think→Action→Report cycle"),
    ("↓ ACN独自フレームワークで構造化分析", "↓ Structured analysis with ACN frameworks"),
    ("↓ アクションプランを含む提言レポート", "↓ Recommendation report with action plan"),
    ("↓ BCG Hypothesis-Driven Approach で仮説設定", "↓ Hypothesis setting via BCG approach"),
    ("↓ BCG独自フレームワークで構造化分析", "↓ Structured analysis with BCG frameworks"),
    ("↓ ファクトベースのピラミッド構造レポート", "↓ Fact-based pyramid-structured report"),
    ("↓ クライアントの真の課題特定、成功の定義", "↓ Identify true client issues, define success"),
    ("↓ Day 1 Answer 設定、支持論拠の整理", "↓ Set Day 1 Answer, organize supporting arguments"),
    ("↓ Issue Tree でMECE分解、優先順位付け", "↓ MECE decomposition via Issue Tree, prioritization"),
    ("↓ 80/20分析、So What? で洞察抽出", "↓ 80/20 analysis, insight extraction via So What?"),
    ("↓ ピラミッド原則で構造化、アクションプラン策定", "↓ Structure via Pyramid Principle, formulate action plan"),
    ("↓ ビジネス・エクスペリエンス・テクノロジーの3軸で診断", "↓ Diagnose across Business/Experience/Technology axes"),
    ("↓ ケイパビリティ駆動戦略の構築", "↓ Build capability-driven strategy"),
    ("↓ コスト構造のRight-sizing、差別化投資の特定", "↓ Right-size cost structure, identify differentiated investments"),
    ("↓ 経済・社会・環境・税の4次元でインパクト評価", "↓ Impact assessment across economic/social/environmental/tax dimensions"),
    ("↓ ディールバリュー創出、リスク管理の統合実行", "↓ Deal value creation, integrated risk management execution"),
]

# ── MCP Integration section translation ──
MCP_JP_EN = [
    ("`deep-research` MCP サーバーが有効な場合、教育理論の調査や最新の教育研究の探索時に\nMCP の `deep-research` プロンプトテンプレートを活用してください。\n特に教育理論の比較、エビデンスベースの教育実践の調査、カリキュラム改訂の背景調査などで\n有効です。MCP が利用できない場合は、内蔵の theories.db と curriculum.db を使用します。",
     "When the `deep-research` MCP server is available, use the `deep-research` prompt template\nfor education theory research and latest pedagogical study exploration.\nParticularly effective for education theory comparison, evidence-based practice surveys, and\ncurriculum revision background research. When MCP is unavailable, use the built-in theories.db and curriculum.db."),
    ("`deep-research` MCP サーバーが有効な場合、文献調査・先行研究調査・トピックの網羅的調査時に\nMCP の `deep-research` プロンプトテンプレートを活用してください。",
     "When the `deep-research` MCP server is available, use the `deep-research` prompt template\nfor literature surveys, prior research, and comprehensive topic investigation."),
]


# ── Harness verification footer ──
HARNESS_FOOTER_SUITE = """
---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run analysis / generation pipeline
VERIFY  → check outputs against quality gates
REPORT  → deliver structured artifacts with traceable reasoning
```

### Quality Gates

- [ ] All outputs include explicit assumptions and constraints
- [ ] Traceable reasoning between steps
- [ ] Final recommendation with clear next actions
- [ ] Artifacts saved as files (not chat-only output)
"""

HARNESS_FOOTER_SINGLE = """
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
"""

HARNESS_FOOTER_SUBSUB = """
---

## Verification Loop (v0.2.0)

```
PLAN   → define scope, inputs, expected outputs
EXECUTE → run skill logic
VERIFY  → check outputs against quality gates
REPORT  → structured result for downstream skills
```

### Quality Gates

- [ ] Explicit assumptions and constraints documented
- [ ] Clear decisions and rationale
- [ ] Actionable next steps provided
"""


def has_harness_footer(text: str) -> bool:
    return "## Verification Loop (v0.2.0)" in text


def apply_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    """Apply text replacements outside code blocks."""
    lines = text.split("\n")
    result = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code:
            for jp, en in replacements:
                line = line.replace(jp, en)
        result.append(line)
    return "\n".join(result)


def apply_multiline_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    """Apply multi-line text replacements."""
    for jp, en in replacements:
        text = text.replace(jp, en)
    return text


def process_skill_md(filepath: Path, group_name: str, is_sub_skill: bool = False) -> bool:
    """Process a SKILL.md file. Returns True if modified."""
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Apply common replacements
    content = apply_replacements(content, JP_EN_REPLACEMENTS)
    content = apply_replacements(content, WORKFLOW_PHASE_TRANSLATIONS)

    # Apply group-specific body translations
    if group_name in CONSULTANT_BODY_TRANSLATIONS:
        for jp, en in CONSULTANT_BODY_TRANSLATIONS[group_name].items():
            content = content.replace(jp, en)

    if group_name in CONSULTANT_TITLES:
        jp_title, en_title = CONSULTANT_TITLES[group_name]
        content = content.replace(jp_title, en_title)

    if group_name == "educationalist":
        for jp, en in EDUCATIONALIST_TRANSLATIONS.items():
            content = content.replace(jp, en)

    if group_name == "agent-skills-builder":
        for jp, en in BUILDER_TRANSLATIONS.items():
            content = content.replace(jp, en)

    # Apply MCP translations
    content = apply_multiline_replacements(content, MCP_JP_EN)

    # Add harness footer
    if not has_harness_footer(content):
        if is_sub_skill:
            content = content.rstrip() + "\n" + HARNESS_FOOTER_SUBSUB
        elif group_name in ["compliance", "diligence", "enterprise", "growth",
                            "learning", "sales", "secops", "supply"]:
            content = content.rstrip() + "\n" + HARNESS_FOOTER_SUITE
        else:
            content = content.rstrip() + "\n" + HARNESS_FOOTER_SINGLE

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def bump_skill_json(filepath: Path) -> bool:
    """Bump version to v0.2.0."""
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return False

    changed = False
    if data.get("version") != "v0.2.0":
        data["version"] = "v0.2.0"
        changed = True

    filepath.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return changed


def update_main_py(filepath: Path, skill_name: str, skill_path: str) -> bool:
    """Update main.py with harness metadata."""
    content = filepath.read_text(encoding="utf-8")
    if '"version": "v0.2.0"' in content:
        return False  # Already updated

    new_content = f'''#!/usr/bin/env python3
"""Entrypoint for imported skill: {skill_path} (v0.2.0).

Harness-optimized with verification loops and quality gates.
"""


def run(input_data: dict | None = None) -> dict:
    return {{
        "skill": "{skill_name}",
        "version": "v0.2.0",
        "skill_path": "{skill_path}",
        "status": "imported",
        "capabilities": [
            "verification-loop",
            "quality-gates",
            "harness-optimized",
        ],
        "harness": {{
            "verification_loop": "PLAN → EXECUTE → VERIFY → REPORT",
            "quality_gates": [
                "explicit-assumptions",
                "traceable-reasoning",
                "actionable-next-steps",
                "artifacts-saved-as-files",
            ],
        }},
        "input": input_data or {{}},
    }}


if __name__ == "__main__":
    print(run())
'''
    filepath.write_text(new_content, encoding="utf-8")
    return True


def sync_source(skill_dir: Path):
    """Copy SKILL.md to source/SKILL.md."""
    src = skill_dir / "SKILL.md"
    dst = skill_dir / "source" / "SKILL.md"
    if src.exists() and dst.parent.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def get_skill_name_from_json(filepath: Path) -> str:
    """Get skill name from skill.json."""
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return data.get("name", "unknown")
    except Exception:
        return "unknown"


def main():
    total_md = 0
    total_json = 0
    total_main = 0

    for group_name in GROUPS:
        group_dir = SKILLS_DIR / group_name
        if not group_dir.exists():
            print(f"WARNING: {group_dir} not found, skipping")
            continue

        print(f"\n=== Processing: {group_name} ===")

        # 1. Process root SKILL.md
        root_skill_md = group_dir / "SKILL.md"
        if root_skill_md.exists():
            if process_skill_md(root_skill_md, group_name, is_sub_skill=False):
                total_md += 1
                print(f"  Updated: SKILL.md")

        # 2. Bump root skill.json
        root_json = group_dir / "skill.json"
        if root_json.exists():
            if bump_skill_json(root_json):
                total_json += 1
                print(f"  Bumped: skill.json → v0.2.0")

        # 3. Update root main.py
        root_main = group_dir / "main.py"
        if root_main.exists():
            skill_name = get_skill_name_from_json(root_json)
            if update_main_py(root_main, skill_name, group_name):
                total_main += 1
                print(f"  Updated: main.py")

        # 4. Sync root source/SKILL.md
        sync_source(group_dir)

        # 5. Process sub-skills (if any)
        sub_skill_count = 0
        for sub_dir in sorted(group_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
            if sub_dir.name in ("source", "__pycache__"):
                continue

            # Process sub-skill SKILL.md
            sub_skill_md = sub_dir / "SKILL.md"
            if sub_skill_md.exists():
                if process_skill_md(sub_skill_md, group_name, is_sub_skill=True):
                    total_md += 1
                    sub_skill_count += 1

            # Bump sub-skill skill.json
            sub_json = sub_dir / "skill.json"
            if sub_json.exists():
                if bump_skill_json(sub_json):
                    total_json += 1

            # Sync sub-skill source/SKILL.md
            sync_source(sub_dir)

        if sub_skill_count > 0:
            print(f"  Sub-skills updated: {sub_skill_count}")

    print(f"\n{'='*50}")
    print(f"Total SKILL.md updated: {total_md}")
    print(f"Total skill.json bumped: {total_json}")
    print(f"Total main.py updated: {total_main}")
    print(f"All source/SKILL.md synced")
    print(f"Done! All groups upgraded to v0.2.0")


if __name__ == "__main__":
    main()
