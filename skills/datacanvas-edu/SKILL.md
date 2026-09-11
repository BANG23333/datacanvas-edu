---
name: datacanvas-edu
description: Guide instructors to define and approve hidden business patterns, then generate synthetic teaching datasets, checked reference solutions, and a matching assignment and rubric. Use for analytics education across business domains; this is an instructor authoring workflow, not a student assignment solver.
---

# DataCanvas-EDU

Turn a teaching brief into a reviewable, reproducible learning environment through **Plan → Create → Verify / Test Analysis → Evaluate → return to Plan when the instructor requests changes**. Generate new data from scratch and revise the generated case through this loop; augmenting an existing external source dataset requires an agreed extension of scope. Write artifacts and code in English. Discussion may use the instructor's preferred language.

The workflow is domain-independent. Never assume an industry, field name, row count, number of patterns, chart count, or grading scale. Examples are optional starting points. The Agent writes case-specific generation and measurement code; the helper does not restrict the instructor to a menu of datasets.

## Instructor control

**Ask → propose → wait for the instructor's ideas or approval → act within that approval.** Apply this to hidden patterns, assignment scope, grading, output formats, substantive design changes, and final acceptance. Giving a proposal is not receiving approval. A reply to a question about audience, tools, or analytical methods does not approve other proposed details.

While a teaching decision is pending, present a concrete proposal and a focused question, then end the response and wait. Do not generate data, write or execute case-generation code, or produce completed assignments and solutions while waiting. Planning notes and review drafts are appropriate. Labeling an executed design "proposed" or "pending review" does not satisfy this requirement. Do not use the former "authorized prototype with defaults" shortcut.

Reuse decisions the instructor has already confirmed; do not repeatedly seek approval for the same choice. Once the concrete design is approved, implement and verify it without asking about every routine coding operation. Return to the instructor before changing the intended discoveries, workload, deliverables, or grading. A numerical pass never substitutes for instructor acceptance.

## Plan

Reuse information already provided. First establish the business context, learner level, and tools or course constraints. Ask only a few consequential questions at a time. Do not require instructors to supply formulas or complete a technical form.

**Next, explicitly ask what hidden patterns the instructor wants students to discover.** Offer a small set of concrete candidate patterns suited to the context and invite the instructor to keep, modify, reject, or add to them. Describe each proposed relationship, the groups or conditions involved, its business relevance, and intended strength or subtlety in plain language. If the instructor has already supplied patterns, summarize them and ask only about unresolved choices. Wait for their response before moving to the complete design. An instructor who has no pattern ideas should receive proposals to review, not an automatically generated dataset.

After the patterns are agreed, propose a concise complete design: objectives, observation unit, approximate size and fields, approved discoveries and difficulty, one assignment, and the grading plan. Read [assignment and solution design](references/assignment-and-rubric.md) before preparing these review drafts. Show the instructor the assignment requirements and a concrete scoring outline, including point totals, major/minor discovery treatment, and deductions. Ask for approval or edits before Create. Material changes to the patterns require renewed review of affected choices.

**Before starting generation, explain what the instructor will receive and ask their preferred file formats.** Read [output choices and the revision loop](references/outputs-and-revisions.md). Present a short preview covering the dataset, student assignment, instructor reference solution with charts, and rubric, with a suggested format and a useful alternative for each. Include the supporting dictionary and reproducibility files without turning this into a technical questionnaire. Ask one grouped format question and wait; an explicit acceptance of the displayed recommendations is sufficient. Reuse formats already selected. Distinguish these teaching-package formats from the report or code students must submit. Do not silently deliver Markdown because that is what the helper produces.

Introduce the loop in plain language during this preview: the first package is for review; the instructor can request different patterns, difficulty, data size, assignment requirements, rubric, or formats and the Agent will revise the agreed parts. Feedback does not require restarting the whole interview.

**Default to one assignment with one set of student requirements and one matching instructor solution/rubric.** Different tools are submission routes for the same assignment. Do not invent introductory/advanced versions, stages, regression tasks, notebooks, extra memos, or optional extensions. Add methods or deliverables only when requested or accepted in the reviewed design. If the instructor says "both" to exploration versus regression, propose including both in one assignment and confirm the scope; that reply does not request two separate assignments or approve hidden patterns and grading. Multiple assignments require an explicit request for multiple assignments.

Connect objectives to student actions: framing questions, guiding exploration, checking AI output, interpreting relationships, and communicating decisions. A chart alone cannot establish the reasoning process. Preserve existing assignment and rubric rules unless revision is requested.

Read [the specification contract](references/specification.md) when translating the approved design into executable requirements. Prepare the specification yourself, including populations, comparators, measures, support, thresholds, interactions, and interpretation limits. Record which patterns, assignment, rubric, and output formats the instructor approved, with the actual reply and its scope in `decisions` and `review`. Never fabricate approval. Before Create, verify that no substantive design decision is still pending. The helper's ability to build a pending specification is for technical development, not permission to bypass the instructor interview.

## Create

Place each case in its own directory with `specification.json` and `generate.py`. The helper's first backend is Python and a single CSV table. Write code appropriate to the domain, exposing seeds and parameters. The default does not require an existing source dataset.

Use a custom measurement when built-in metrics do not express the requested pattern. Read [verification and execution](references/verification.md) for interfaces and commands. Examples must remain case configurations, not mandatory fields or logic in the core helper.

Prepare the approved output formats using available host tools. The helper starts with CSV and Markdown; document, spreadsheet, or notebook exports require additional work and verification. Check available capabilities before promising an export, and obtain agreement on an alternative if the requested format cannot be produced. A changed file extension is not conversion.

Keep earlier artifacts and attempts. Generate into a new run directory. Do not silently lower thresholds, remove failed patterns, or change seeds merely to hide failure. Include a bounded attempt budget in the design proposal; up to three candidate cycles including the first is an optional starting proposal. Correct implementation errors within scope, and return material design conflicts to Plan with concrete alternatives.

This technical retry budget is distinct from the instructor's review-and-revision loop. Do not automatically generate more teaching versions while awaiting feedback or treat a retry limit as a ban on later instructor-requested revisions.

## Verify / Test Analysis

Measure the exported CSV independently of generation rules. Check every required pattern, subgroup support, denominator, missingness, exception, and interaction. A probability in code is not the realized share after all rules and sampling.

The helper computes common metrics, applies declared criteria, and prepares reference evidence. Its technical pass is not instructor acceptance. Inspect custom measurements and independently cross-check key calculations. Keep undefined results, empty groups, missing checks, and sparse subgroups visible.

Ensure charts and interpretations match the calculations. Treat proposed mechanisms as hypotheses unless the design supports them. Valid unlisted findings are not automatically false positives. Keep discovery coverage, course grades, resource use, and learning evidence separate.

A discoverability pilot uses only the student package in a fresh solver context. Verification with the reference key is a different activity. Retain unsuccessful pilots and easy solutions; do not select a model to manufacture difficulty. Generated data and Agent performance alone do not establish contamination avoidance or learning benefits.

## Evaluate

Assemble the approved single assignment and its teaching package: student data, dictionary, and assignment; instructor specification, pattern-by-pattern reference solution with charts and explanations, rubric, and validation report; and reproducibility code, parameters, seeds, environment, fingerprints, and revisions. Follow [assignment and solution design](references/assignment-and-rubric.md). A generic list of criteria or a numerical validation table alone is not the instructor solution and rubric.

Review plausibility, objective coverage, difficulty, answers, and rubric completeness with the instructor. Record the actual decision and scope. Never invent acceptance, reviewer feedback, or student results. If acceptance is already explicit, record it without asking again. Keep remaining decisions visible in the package. Publishing or submitting materials is a separate action governed by the user's request.

**Make the revision invitation part of every unaccepted package handoff.** Name the case version, link the files in the chosen formats, summarize what was checked and any unresolved issue, and say that this is a version for review. Explicitly explain that the instructor can return to Plan with feedback. Offer a few relevant examples, such as making a pattern subtler, adding a discovery, shortening the assignment, or changing rubric weights. Finish with one easy question asking what to keep or change, or whether the package is ready for use. A download list, "all checks passed," or a generic "let me know" alone is insufficient. Wait for the response; do not invent acceptance or start another iteration automatically.

When feedback arrives, summarize the requested changes, preserve settled choices, and show the affected plan for confirmation where choices remain unresolved. Follow [the revision procedure](references/outputs-and-revisions.md#returning-to-plan). Revise only the agreed parts in a new case version, recheck affected evidence and dependencies, update the matching assignment/solution/rubric, and return to Evaluate. Clear instructions for a specific edit count as authorization for that edit; do not ask the instructor to reconfirm it or repeat the original interview. If the instructor accepts the package, record that decision and finish without pressuring them to keep revising.

Before claiming cross-domain operation, demonstrate the same core workflow on different business briefs and report tested boundaries. Engineering examples are not a usability study or evidence of student learning.
