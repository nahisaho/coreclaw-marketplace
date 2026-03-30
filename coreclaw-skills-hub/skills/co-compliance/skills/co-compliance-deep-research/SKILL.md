---
name: co-compliance-deep-research
description: |
  Regulatory and compliance research with web_search, /research command, and MCP.
  Framework comparison, regulatory updates, and best practice investigation.
  Use when RESEARCHING regulatory requirements, comparing compliance frameworks,
  investigating regulatory updates, or gathering compliance best practices.
tu_tools:
  - key: deep-research
    name: Deep Research MCP
---

# Deep Research (Compliance)

Regulatory research with multi-tool search capability.

## Use This Skill When

- Researching regulatory requirements for a new framework.
- Comparing frameworks (e.g., SOC 2 vs ISO 27001 overlap).
- Investigating recent regulatory updates or enforcement actions.

## Research Tools (Priority Order)

### 1. `web_search` (Built-in — Always Available)
```
web_search("GDPR Article 32 technical measures requirements")
web_search("SOC 2 Type II vs ISO 27001 control mapping")
```

### 2. `/research` command (CLI — Interactive)
```
/research What are the key differences between PCI DSS v4.0 and v3.2.1?
```

### 3. `deep-research` MCP (When Configured)
Full pipeline for comprehensive regulatory research.

## Deliverables

- `results/regulatory-research.md`: findings with regulatory citations.

## Quality Gates

- [ ] Regulatory citations include clause/section numbers.
- [ ] Framework versions explicitly stated.
- [ ] 2+ sources for key regulatory interpretations.

If any gate fails: identify the issue, fix, and re-validate.

## Gotchas

- 規制の引用は必ず条文番号まで明記（例: GDPR Art. 32(1)(a)）。「GDPRに準拠」だけでは不十分
- `web_search` は常に利用可能。MCP なしでも規制リサーチは実行できる
- フレームワークのバージョンが更新されている可能性がある。常に最新版を確認すること

## Validation Loop

1. リサーチを実行
2. チェック: 条文番号、バージョン明記、2+ソース
3. 不合格なら追加検索
4. 合格後のみ完了
