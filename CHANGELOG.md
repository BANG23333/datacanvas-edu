# Changelog

## Display name refresh — 2026-09-10

- Standardize the displayed product name as **DataCanvas-EDU** across current documentation, the marketplace, the plugin, and the Skill.
- Rebuild the current v0.1.3 Skill ZIP and its integrity manifest; the workflow and numerical helper are unchanged.
- Preserve the `datacanvas-edu` installation identifiers and URLs, earlier ZIPs, and historical validation records.

## 0.1.3 — 2026-09-09 — Output choices and instructor revision loop

- Preview the data, assignment, instructor solution, rubric, and supporting files before generation; recommend useful formats and wait for the instructor's choice or acceptance.
- Distinguish teaching-package file formats from student submission requirements. Describe CSV/Markdown helper outputs separately from host-assisted document/spreadsheet exports.
- Explain the repeated Plan → Create → Verify → Evaluate → Plan cycle during planning and at each unaccepted package handoff.
- Invite feedback with concrete examples and one easy question; revise agreed parts, preserve earlier versions and settled choices, and avoid regenerating approved data for document-only edits.
- Keep the numerical helper unchanged and preserve earlier Skill ZIPs. A complete instructor trial of format exports and the revision loop remains necessary.

## 0.1.2 — 2026-09-08 — Instructor control and assessment design

- Ask which hidden patterns the instructor wants, offer concrete proposals, and wait for their choices before preparing the complete design.
- Require approval of the patterns, assignment, and rubric before case generation; remove the shortcut that allowed executing a proposed design while acceptance remained pending.
- Default to one assignment and one matching solution/rubric. A request for both exploration and regression does not create two assignments or approve unrelated details.
- Add WindowDash-inspired guidance for concise student requirements and pattern-by-pattern reference charts, explanations, discovery credit, minor findings, duplicates, and negative examples.
- Preserve the numerical helper and original trial outputs; package the revised instructions as a new Skill ZIP and plugin version while retaining v0.1.1.
- Document the first formative instructor feedback and the fresh-conversation retest plan.

## GitHub marketplace import fix — 2026-09-08

- Add `.agents/plugins/marketplace.json` so the GitHub repository can be discovered by the plugin marketplace importer.
- Add a Codex plugin manifest and a self-contained copy of the v0.1.1 Skill under `plugins/datacanvas-edu/`.
- Add a reproducible plugin bundling command with a check for missing or stale Skill files.
- Document marketplace import separately from standalone Skill folder installation and Claude Skill ZIP upload.
- Preserve the v0.1.1 standalone Skill, ZIP, and numerical behavior. The plugin is a new distribution wrapper for that same Skill.
- Verify import from the public GitHub URL and installation through Codex CLI 0.153.4 bundled with ChatGPT desktop on macOS; the plugin is installed and enabled, with all six installed files matching the source.

## Repository publication — 2026-09-08

- Make the repository public at the researcher's request.
- Update documentation to reflect public availability while retaining prototype and validation limits.
- Keep the v0.1.1 Skill and numerical code unchanged. A formal GitHub Release and license selection remain pending.

## 0.1.1 — 2026-09-08 — Private testing package

- Adopt DataCanvas EDU as the project name and `datacanvas-edu` as the distributed Skill name.
- Package the unchanged numerical helper with the existing specification and verification references.
- Add repository documentation, platform setup guidance, trial feedback instructions, four separate business examples, and relocated behavioral tests.
- Supply a downloadable Skill ZIP and a reproducible packaging command.
- Preserve the earlier v0.1.0 local prototype. This revision does not claim new teaching evidence or completed cross-platform trials.

## 0.1.0 — 2026-09-08 — Original local prototype

- Implement the four-phase instructor workflow, shared generation/validation helper, custom measurements, and teaching-package outputs.
- Complete scoped four-case engineering validation and 18 behavioral checks.
- Use the earlier Skill name `design-analytics-datasets`.
