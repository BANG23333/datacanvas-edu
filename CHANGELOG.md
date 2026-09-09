# Changelog

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
