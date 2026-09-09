# Output Choices and the Instructor Revision Loop

Use this during the pre-generation preview, delivery, and subsequent feedback. Keep the conversation simple: show useful recommendations, ask about the choices that matter, and preserve decisions already made.

## Explain the package before generating it

Cover all four main outputs in a compact table. Identify who uses each item and what it contains. The instructor should not need to discover the package contents or file types after a long run.

| Output | Purpose and audience | Suggested format | Useful alternative |
| --- | --- | --- | --- |
| Dataset and data dictionary | Student analysis data and field explanations | CSV for a Python course; an editable dictionary with the assignment | XLSX if the instructor prefers an Excel workbook, with identifiers and dates preserved |
| One assignment brief | Student-facing context, task, requirements, and submission rules | DOCX for editing | PDF for distribution; Markdown if preferred |
| Reference solution with charts | Instructor-only patterns, measured evidence, figures, interpretations, and grading examples | DOCX with figures embedded | PDF for reading; an executed notebook only if requested |
| Rubric | Clear scoring rules, major/minor discoveries, partial credit, and deductions | DOCX, as a separate file or a clearly labeled section of the instructor solution | XLSX for a grading table, PDF, or Markdown if preferred |

These are recommendations, not settled choices or guarantees of host capability. Offer a simple combined choice, for example: "For your Python course, I recommend CSV data and editable Word files for the assignment, solution, and rubric. Would you like those, or prefer Excel/PDF for any item?" Do not ask four repetitive questions or show a long menu of formats. If the instructor already specified formats, confirm the output preview without reopening those choices. An explicit acceptance of the displayed recommendations covers them.

Mention that generation/verification code and supporting reproducibility files accompany the package; instructors do not need to choose internal log formats. ZIP files are optional download containers, not substitutes for the requested file formats. Do not create every alternative format or extra analytical deliverable by default. Multiple file types for the same approved brief remain one assignment.

Distinguish two decisions: the format of the assignment document delivered to the instructor and the format students must submit. For example, an editable DOCX assignment can require students to submit a PDF report. Python use does not by itself request a notebook, and a PDF student-report requirement does not approve PDF as the only instructor-solution format.

Include an expectation of review in the preview: "You will receive a first version to inspect. We can then return to planning and adjust patterns, difficulty, the assignment, or grading together; you will not need to repeat the initial setup."

## Produce and check the chosen formats

The shared helper produces CSV data, Markdown documents, figures, and reproducibility files. Use appropriate host tools to create requested DOCX/PDF/XLSX/notebook outputs. Keep a consistent source for each artifact so exported versions agree. If a capability is unavailable, explain the concrete limitation and ask the instructor to choose an available alternative before treating the package as complete.

Open or render documents to check readable tables, embedded charts, labels, pagination, and links. For data exports, compare row counts, column names, missing values, dates, identifiers, and relevant measurements against the validated source. Reopen the real file format; do not rename a Markdown or CSV file to imitate another type. Preserve the distinction between student materials and the instructor key in every export and download bundle. Refresh relevant integrity records after adding or revising deliverables.

## End with an easy invitation to review

For every package that has not yet been accepted, the handoff should provide:

- Version and download links, separated into student and instructor materials in the chosen formats.
- A short evidence summary and material issues, without presenting technical success as educational acceptance.
- An explicit invitation to another cycle, with two or three concrete examples tailored to the case.
- One low-effort question that allows both feedback and acceptance.

Example wording to adapt to actual artifacts and checks:

> Here is version 1 for your review, with the data and teaching materials in your chosen formats. After you inspect them, we can return to planning and revise the parts you want—for example, add a pattern, make a relationship harder to spot, or simplify the assignment and rubric. You do not need a new brief. What would you like to keep or change, or is this ready for your class?

Do not imply that revisions require a new chat, advanced terminology, or a formal feedback form. Accept plain-language comments. Do not generate another version without a response, interpret silence as approval, or repeatedly request changes after the instructor has accepted the package.

## Returning to Plan

1. Summarize the instructor's feedback and its scope against the current version. Carry forward approved context, patterns, formats, and course rules that remain applicable.
2. Explain the affected changes and dependencies in plain language. If a decision is ambiguous, offer a small proposal and wait. A specific instruction such as "change the rubric to 40 points and leave the data unchanged" already authorizes that edit; only unresolved scoring allocations need a proposal. A broad request such as "make it harder" needs a concrete difficulty proposal before regeneration.
3. Retain the previous version and its approvals. Record the next version's changes and their actual authorization. Approval of an earlier version does not automatically accept a newly revised teaching package.
4. Revise only what is needed. Adding a pattern or changing its strength may require generation, revalidation of interacting patterns, and updates to the reference solution and rubric. A change to document wording, grading, or file format should preserve approved dataset bytes unless a data change is necessary and agreed.
5. Recheck affected artifacts, their consistency, and any dependent results. Explain what changed and what was checked, then return to Evaluate with the new version and the same easy feedback/acceptance invitation.

This is the ongoing **Plan → Create → Verify → Evaluate → Plan** cycle. The generator's bounded technical retries are separate from instructor-directed revisions. Neither numerical checks nor the number of attempted generations determines whether the instructor is satisfied.
