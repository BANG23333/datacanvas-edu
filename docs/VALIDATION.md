# Validation and Research Status

Updated: 2026-09-09. This record separates engineering evidence from planned user and research evaluations.

## Existing engineering evidence

The original prototype's common Python helper was exercised on marketing campaigns, hotel bookings, equipment rental, and WindowDash. Each case had a primary run, same-seed repeat, and two fresh seeds (202 and 303): 16 runs and 64 required numerical check evaluations. All passed the configured numerical criteria, and each same-seed repeat reproduced the CSV bytes. The WindowDash seed-42 result reproduced its original case data.

The existing 18 behavioral checks cover known measurements, empty and sparse groups, invalid numeric inputs, missingness, custom-metric failures, incomplete rubrics, failure reporting, and package integrity. The tests are included in this repository for rerunning. Key reference calculations and the rental custom median calculation were checked independently during development.

The v0.1.1 naming and packaging revision preserves the original generation and measurement code. Verification of the relocated package is recorded in [repository checks](repository_checks.json).

## Plugin packaging checks

The GitHub import fix adds the repository marketplace manifest and plugin manifest that were missing from the original standalone Skill distribution. The plugin-creator validator passed on the new plugin, and the bundle check confirmed that all five bundled Skill files match the canonical standalone Skill byte for byte. The standalone v0.1.1 ZIP is unchanged.

On 2026-09-08, Codex CLI 0.153.4 bundled with ChatGPT desktop on macOS successfully imported the public GitHub repository and installed `datacanvas-edu@datacanvas-edu` version 0.1.1. The plugin listing reported **installed, enabled**. All six installed files (the plugin manifest and five Skill files) matched the source byte for byte. See the [installation check record](plugin_installation_checks.json).

This verifies the actual GitHub marketplace import and local plugin installation path that previously failed. It does not establish a completed instructor conversation, UI walkthrough, Claude installation, or cross-platform runtime compatibility. Start a new conversation for the instructor trial.

## v0.1.2 interview and assessment revision

The first instructor trial exposed a conversational failure despite successful numerical checks: the Agent generated a two-assignment package before obtaining approval of the hidden patterns and detailed grading. [Trial feedback](TRIAL_FEEDBACK_V0.1.2.md) records the observation and response.

The revised canonical Skill and plugin passed their format validators. All six files in the new v0.1.2 ZIP match the canonical Skill, the plugin bundle matches the same source, and the Skill's relative reference links resolve. The numerical helper retains its prior file hash; the prior 18 numerical tests and case runs are historical evidence for that unchanged code, not fresh tests of conversational behavior.

An independent agent completed two simulated response checks: first continuing the reported conversation after "both," then continuing after the simulated instructor approved one assignment and three patterns. The first response proposed one combined assignment and asked for pattern choices. The second proposed the remaining assignment and rubric details and asked for approval before creation. These checks used a harness that prohibited generation and external actions; they evaluate the responses and stated intended actions, not an unconstrained end-to-end execution. The rubric guide also clarifies concise scoring and single application of each deduction.

The GitHub marketplace was refreshed and v0.1.2 installed through the same Codex CLI on macOS. The plugin is listed as installed and enabled; all seven installed files match source. All 44 repository files at the v0.1.2 implementation commit matched the local file hashes. See the update entry in [installation checks](plugin_installation_checks.json).

The approval requirements are Skill instructions. The direct Python developer utility does not authenticate or enforce human approval. A fresh instructor conversation must verify that the host follows these instructions through generation, reference-solution review, and final acceptance. Cross-platform use and educational outcomes remain unestablished.

## v0.1.3 output choices and instructor revision loop

Follow-up feedback requested a clear pre-generation explanation of the outputs, instructor choice of file formats, and a visible invitation to repeat the planning/revision cycle after inspecting results. Version 0.1.3 adds that conversation to the Skill, its reference guides, and the public README. The numerical helper is unchanged; DOCX/PDF/XLSX exports remain work for the host's available tools, not newly implemented helper capabilities.

The Skill and plugin validators passed. All seven Skill files match between the canonical source, plugin bundle, and v0.1.3 ZIP; version identifiers agree and relative reference links resolve. Earlier ZIPs and the numerical helper remain unchanged.

An independent agent produced three isolated simulated responses using the revised Skill: (1) approved teaching design with formats not yet discussed; (2) first-package delivery with checks passed but no instructional acceptance; and (3) a request to simplify the assignment/rubric while keeping the data and patterns. The responses respectively previewed all four outputs and waited for format choices; invited review and a return to Plan; and proposed a scoped document revision that preserved the data and awaited unresolved decisions.

On 2026-09-09, the GitHub marketplace update and plugin installation succeeded for v0.1.3 through Codex CLI 0.153.4 on macOS. The plugin is installed and enabled, and all eight installed files match source. All 47 repository files at the implementation commit matched the local hashes. See [installation checks](plugin_installation_checks.json).

These were response-only simulations with generation, document production, and external actions prohibited. They support the observed messages and stated intended actions, not actual conversion quality, data preservation during a real revision, or full instructor usability. The next trial should include real format choices, exported files, feedback on version 1, a revised package, and final acceptance.

## Boundaries

- The three new domains are development examples with Agent-proposed defaults, not recorded instructor interviews or an independent domain sample.
- Two fresh seeds per case are a limited stability check, not a general reliability estimate.
- The tested backend uses Python and a single CSV table. R, multiple linked tables, arbitrary domains, and every Agent platform are not established capabilities.
- Numerical checks do not establish business plausibility, educational suitability, or human acceptance.
- The WindowDash rubric remains incomplete, and operational thresholds are proposed calibration choices. All examples require instructor review.
- Code execution by the implementing Agent does not establish that another Agent follows the Skill correctly or that teachers find it easy to use.
- Newly generated data do not guarantee contamination avoidance, difficult AI analysis, deeper reasoning, or improved student learning.

## Planned research

The primary contribution is an instructor-guided educational data-generation framework linking teaching goals, predefined discoveries, numerical validation, and assessment materials. The first preprint will describe the framework and implementation with measured artifact evidence.

An exploratory comparison of AI analyses on generated and public real-world data is planned once the comparison sample, model choices, budgets, and scoring protocol are available. Differences between datasets will limit causal interpretation. Student engagement, learning, and transfer remain future empirical questions.

The repository is public as of 2026-09-08. The immediate next step is the researcher's own trial, followed by feedback-driven revision and platform checks. License selection, a formal versioned release, and a formal paper citation remain pending.
