---
name: datacanvas-edu
description: Design and generate synthetic teaching datasets with instructor-defined business patterns, verified reference analyses, assignments, and rubrics. Use for analytics education across business domains; this is an instructor authoring workflow, not a student assignment solver.
---

# DataCanvas EDU

Turn a teaching brief into a reviewable, reproducible learning environment through **Plan → Create → Verify / Test Analysis → Evaluate**. Generate new data from scratch; changing existing source data requires an agreed extension of scope. Write artifacts and code in English. Discussion may use the instructor's preferred language.

The workflow is domain-independent. Never assume an industry, field name, row count, number of patterns, chart count, or grading scale. Examples are optional starting points. The Agent writes case-specific generation and measurement code; the helper does not restrict the instructor to a menu of datasets.

## Plan

Reuse information already provided. Start from the business context, learner level, and analytical decisions students should practice. Ask only a few consequential questions at a time. Do not require instructors to supply formulas or complete a technical form.

Propose a concise design: learning objectives, one-record meaning, management questions, intended discoveries, difficulty, and deliverables. Explain defaults and mark them as proposals. If the instructor has no domain preference, offer a few contrasting examples. For unfamiliar domains, expose uncertain business assumptions rather than inventing industry rules.

Connect objectives to student actions: framing questions, guiding exploration, checking AI output, interpreting relationships, and communicating decisions. A chart alone cannot establish the reasoning process. Preserve existing assignment and rubric rules unless revision is requested.

Read [the specification contract](references/specification.md) when translating the design into executable requirements. Prepare the specification yourself, including populations, comparators, measures, support, thresholds, interactions, and interpretation limits. Review substantive design choices with the instructor; reuse decisions already authorized. Routine implementation choices need not become approval questions. An authorized prototype may use proposed defaults while clearly retaining pending instructional acceptance.

## Create

Place each case in its own directory with `specification.json` and `generate.py`. The helper's first backend is Python and a single CSV table. Write code appropriate to the domain, exposing seeds and parameters. The default does not require an existing source dataset.

Use a custom measurement when built-in metrics do not express the requested pattern. Read [verification and execution](references/verification.md) for interfaces and commands. Examples must remain case configurations, not mandatory fields or logic in the core helper.

Keep earlier artifacts and attempts. Generate into a new run directory. Do not silently lower thresholds, remove failed patterns, or change seeds merely to hide failure. Use the agreed attempt budget; absent a preference, propose up to three candidate cycles including the first. Correct implementation errors within scope, and return material design conflicts to Plan with concrete alternatives.

## Verify / Test Analysis

Measure the exported CSV independently of generation rules. Check every required pattern, subgroup support, denominator, missingness, exception, and interaction. A probability in code is not the realized share after all rules and sampling.

The helper computes common metrics, applies declared criteria, and prepares reference evidence. Its technical pass is not instructor acceptance. Inspect custom measurements and independently cross-check key calculations. Keep undefined results, empty groups, missing checks, and sparse subgroups visible.

Ensure charts and interpretations match the calculations. Treat proposed mechanisms as hypotheses unless the design supports them. Valid unlisted findings are not automatically false positives. Keep discovery coverage, course grades, resource use, and learning evidence separate.

A discoverability pilot uses only the student package in a fresh solver context. Verification with the reference key is a different activity. Retain unsuccessful pilots and easy solutions; do not select a model to manufacture difficulty. Generated data and Agent performance alone do not establish contamination avoidance or learning benefits.

## Evaluate

Deliver student data, dictionary, and assignment; instructor specification, key, numerical evidence, reference charts, rubric, and validation report; and reproducibility code, parameters, seeds, environment, fingerprints, and revisions.

Review plausibility, objective coverage, difficulty, answers, and rubric completeness with the instructor. Record the actual decision and scope. Never invent acceptance, reviewer feedback, or student results. If acceptance is already explicit, record it without asking again. Keep remaining decisions visible in the package. Publishing or submitting materials is a separate action governed by the user's request.

Before claiming cross-domain operation, demonstrate the same core workflow on different business briefs and report tested boundaries. Engineering examples are not a usability study or evidence of student learning.
