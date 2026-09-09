# Assignment, Reference Solution, and Rubric

Read this when proposing the assignment and grading plan, and again when assembling the instructor package. Use the instructor's supplied assignment or rubric as the primary reference. The WindowDash example below supplies a preferred discovery-oriented structure; its domain, numbers, and scoring choices are not mandatory for every course.

## One concise student assignment

Default to one business case and one assignment. Alternative Colab and agent-tool submission routes belong to the same assignment. Combining approved exploration and regression topics does not create separate assignments, stages, point totals, or solutions unless the instructor explicitly requests that structure.

For an introductory business analytics / data visualization course, propose this WindowDash-style structure for instructor review:

1. A short fictional business context and an open-ended goal: uncover useful patterns and advise management.
2. Dataset overview and data dictionary, without disclosing hidden relationships or the solution key.
3. A PDF or DOCX report with at least five distinct visualizations, each supporting a different finding; one or two sentences explaining each insight; a final management recommendation of at most 200 words.
4. A course-specific tool and AI policy. The supplied WindowDash assignment allows AI throughout and holds students responsible for their answers. Its Colab route asks for a shared Python script; its agent-tool route asks for a Markdown conversation record. Propose relevant routes for the current course and confirm them. Do not submit files or publish a student's script yourself.

The five-chart count, word limit, submission routes, and any chart-type minimum are proposed settings to confirm or adapt. Keep the task focused on discovery and business interpretation. Do not prescribe every chart and comparison so precisely that students simply reproduce the instructor key. Include regression, extra notebooks, long memos, model comparisons, or new AI-disclosure exercises only when specifically requested or approved. A request to use Python alone does not request a coding-heavy or regression assignment.

## Instructor reference solution

Organize the solution around the approved hidden patterns. For each major pattern provide:

- Pattern identifier, intended relationship, relevant subgroups or conditions, and why it matters to a business decision.
- An actual reference visualization and the filtering, aggregation, units, denominators, and group sizes needed to reproduce it.
- Measured evidence from the exported dataset, with a concise explanation and a bounded business interpretation. A plausible explanation is a hypothesis unless the evidence supports causality.
- What a student must demonstrate to receive credit, acceptable alternative visualizations, and examples of partial or incorrect interpretations.

Show the chart and explain its insight; do not deliver only a pattern title, code, validation numbers, or a chart file link with no solution narrative. The helper's automatic charts are starting material and may need better business labels or a different visual form. After generation, use observed values in the solution rather than presenting generator parameters as results.

Also include concrete minor-finding examples and common invalid analyses, with a short explanation of their credit treatment. Helpful negative examples include an unreadable noisy plot, a near-flat series exaggerated by a narrow axis, an unsupported subgroup comparison, and two charts expressing the same discovery. Judge evidence and instructional value; do not reject a well-supported unexpected discovery merely because it is absent from the key.

Keep the pattern identities, answers, generation rules, and instructor scoring examples out of student materials. A student-facing rubric may explain general criteria without revealing the intended relationships. Reference analyses for two approved methods may be sections of one solution.

## A discovery-oriented rubric

Propose a concrete rubric for approval before generating the case. Its primary component should reward reliable, distinct, business-relevant discoveries. Connect it directly to the approved major patterns and the reference solution. Also address chart quality, concise interpretation, and the final recommendation as appropriate to the instructor's objectives.

Make these rules explicit and reviewable:

- Total score, component weights or discovery tiers, and the zero-discovery case.
- How many approved major patterns receive full discovery credit; full and partial credit for each pattern's essential claims.
- How valid minor or unexpected findings earn credit, any cap, and how fractional discovery credit interacts with tier thresholds.
- Duplicate findings: changing chart type does not create a second discovery.
- Treatment of noise, misleading scales, unsupported claims, incorrect denominators, missing charts, chart-type requirements, and excessive interpretation length.
- The order and scope of deductions, score floors, and how to avoid penalizing the same error twice.

Prefer a small, understandable scoring table to unnecessary fractional tiers or elaborate deductions. For each requirement, choose whether its score is earned within a component or deducted from that component; do not do both for the same missing chart or error. Present the key teaching choices concisely and put longer scoring detail in a review draft when helpful. The instructor must still be able to inspect and approve the complete policy before generation.

The original WindowDash rubric illustrates the requested style: 50 total points; 30 for unique patterns; eight predefined major patterns; full discovery credit for at least four major patterns, then 25/20/15 discovery points for three/two/one; minor findings described as 0.5 patterns; positive and negative chart examples. It also discusses five charts, three chart types, and deductions. These are case-specific rules, not universal defaults.

That source does not fully resolve the remaining 20 points, the zero-major case, conversion of fractional minor discoveries into tiers, or interactions among deductions. When adapting it, propose a complete reconciliation and ask the instructor to accept or edit it. Do not silently replace it with generic 100-point categories, invent missing rules as settled, or copy an incomplete score calculation into a supposedly ready rubric. Arithmetic completion is distinct from instructor approval.

The current helper can render additive criterion rows and free-text notes. If the approved rubric uses tiers and deductions, retain those rules in the instructor document; do not claim the helper automatically implements that scoring scheme. If its additive representation is incomplete, keep `rubric.complete` false and explain the representation limit. A complete reviewed tier-based rubric can be provided as a separate document; the helper does not grade students.

## Approval and final review

Before Create, show the proposed assignment and complete scoring policy alongside the agreed pattern list. Wait for approval or edits. After the data and reference solution exist, show measured patterns, representative charts, the matching rubric, and any remaining limitations for final instructor acceptance. If the measurements require a material change to a pattern or grading rule, return that change for review first. Preserve the instructor's actual decisions and the scope of each approval.
