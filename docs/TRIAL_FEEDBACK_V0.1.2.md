# First Instructor Trial and v0.1.2 Revision

Date: 2026-09-08. This is formative feedback from one researcher/instructor trial, not a controlled usability study or evidence of learning effects.

## Observed problem

The instructor requested a food-delivery case for undergraduate business analytics students using Python. After the Agent asked whether to include exploration or regression, the instructor answered that both were wanted. The Agent then produced two assignments, two 100-point rubrics, extended management memos, and a generated teaching package. It had proposed possible patterns, but never explicitly asked the instructor which hidden patterns to define or obtained approval of the complete assignment and scoring design.

The supplied case specification recorded detailed design choices and design acceptance as pending even though generation and packaging were complete. This shows why labeling defaults as pending is insufficient: instructor control must happen before execution. Passing nine numerical checks did not resolve the interaction failure. The original trial artifacts are retained privately as the baseline.

## Requested behavior and changes

| Instructor feedback | v0.1.2 change |
| --- | --- |
| The initial context questions were useful, but the central hidden-pattern question was missing | Ask explicitly which hidden patterns students should discover, offer concrete candidates, and wait for choices or edits |
| The Agent was too willing to decide and execute | Require approval of the patterns and the concrete assignment/rubric before writing or executing case-generation code; remove the pending-prototype shortcut |
| The default should be a single assignment | Treat multiple analytical methods as possible contents of one assignment; require an explicit request for multiple assignments |
| Assignment requirements should resemble the concise WindowDash homework | Propose a discovery-oriented report and short business recommendation; do not silently add stages, lengthy memos, extra notebooks, or optional extensions |
| Rubrics should resemble the supplied solution-and-rubric example | Add a reusable guide for pattern-by-pattern reference charts and explanations, major/minor discoveries, duplicate findings, negative examples, and explicit scoring rules |

The instructor still controls domain-specific patterns, counts, difficulty, point totals, and final acceptance. WindowDash remains one reference example, not a fixed schema or a universal eight-pattern/50-point template. An approved design permits routine implementation; the revised workflow does not ask repeatedly about settled decisions or each coding operation.

## Reference materials reviewed

The review used the supplied conversation, the generated assignment/rubric/specification, and retained text snapshots of the WindowDash assignment and instructor solution and rubric. The assignment description and assignment requirements supplied by the instructor establish the short report format. The teaching references are retained privately; the distributed Skill includes a generalized guide and does not require access to those source documents.

The original rubric contains 50 total points, 30 discovery points, major-pattern tiers, minor findings, and deduction examples, but leaves several scoring rules unresolved. The revised Skill requires a proposed reconciliation and instructor approval, rather than silently inventing a scoring system or copying incomplete arithmetic.

## Evidence limits and next trial

The numerical helper and generation code are unchanged. The change is to the interview, approval boundaries, assignment scope, and assessment instructions, distributed as v0.1.2. Structural validators cannot prove conversational compliance, and the helper's direct developer command does not authenticate human approval.

Retest in a fresh conversation. Check that the Agent waits after the pattern proposal, waits again after presenting the assignment and grading plan, then generates only the approved package. Check the actual reference charts, concise interpretations, major/minor credit rules, and final acceptance step. A complete instructor run of the revised Skill is still required.
