---
name: co-sales-proposal-builder
description: |
  Stakeholder-aligned proposal builder with value proposition, ROI justification,
  and implementation planning. Customized per stakeholder role with executive summary,
  business case, and technical fit sections. Use when BUILDING proposals,
  creating business cases, developing ROI justifications, or preparing executive summaries.
---

# Proposal Builder

Build stakeholder-aligned proposals with ROI justification and implementation plans.

## Use This Skill When

- Building a proposal for a qualified opportunity.
- Creating executive summaries for decision makers.
- Developing ROI justification and business case documents.
- Customizing proposal sections for different stakeholder roles.

## Workflow

1. Review all prior phase outputs: account brief, stakeholder map, discovery findings, objection playbook.
2. Structure proposal using `assets/proposal-template.md`.
3. Customize per stakeholder:
   - Economic Buyer: ROI, payback period, strategic alignment.
   - Technical Evaluator: Architecture fit, integration, security.
   - User Buyer: Adoption ease, training, day-to-day impact.
   - Champion: Internal selling points, quick wins, risk mitigation.
4. Build ROI model with buyer's own metrics.
5. Draft implementation plan with phases, milestones, and resource requirements.
6. Add risk assessment and mitigation strategies.
7. Save to `results/proposal.md`.

## Deliverables

- `results/proposal.md`: Stakeholder-aligned proposal with ROI justification.

## Quality Gates

- [ ] Executive summary matches buyer's stated priorities and pain points.
- [ ] ROI justification uses buyer's own metrics (not generic projections).
- [ ] Each stakeholder section addresses their specific decision criteria.
- [ ] Implementation plan is phased with realistic timelines.
- [ ] Risk assessment includes mitigation strategies.

If any gate fails: identify misalignment, revise with stakeholder-specific data, and re-validate.

## Gotchas

- 汎用提案は競合との差別化ができない。ステークホルダーごとに価値訴求を変えること
- ROI は顧客自身の指標で計算すること。自社の標準 ROI テンプレートをそのまま使わない
- 実装計画は現実的であること。過度に楽観的なタイムラインは信頼を損なう

## Validation Loop

1. 提案書を生成
2. エグゼクティブサマリーの一致・ROI の顧客指標・ステークホルダー個別対応をチェック
3. 不合格なら修正、全基準を満たしてから完了
