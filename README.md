# DataCanvas EDU

*An AI Agent Skill for Synthetic Data Generation in Analytics Education*

**Turn teaching goals into datasets with instructor-defined patterns, verified reference analyses, and assessment materials.**

DataCanvas EDU helps instructors create synthetic business datasets around the discoveries students should practice making. Describe your teaching goals; the Agent helps define the scenario and patterns, writes generation code, checks the resulting data, and prepares teaching materials for your review.

**Instructor control:** The Agent asks which hidden patterns you want students to discover, proposes options, and waits for your feedback. It then presents one assignment and a matching discovery-based rubric for approval before generating data. The default is one assignment; multiple assignments require an explicit request.

The workflow supports AI-assisted business analytics education: students frame questions, guide exploration, check evidence, and communicate recommendations. The Skill supports the instructor who designs that learning environment.

**Status:** Public prototype for exploration and feedback. Version 0.1.2 revises the interview and assessment workflow after the first instructor trial exposed premature generation and unintended assignment expansion. The numerical helper is unchanged. GitHub marketplace import/update and plugin installation were verified through v0.1.2 using Codex CLI 0.153.4 bundled with ChatGPT desktop on macOS; v0.1.2 is installed and enabled on the development computer. A complete instructor trial of the revised workflow and other platform routes remains necessary. License selection and a formal GitHub Release are pending.

## Try the Skill

1. Follow the [installation guide](docs/INSTALLATION.md) for your Agent tool.
2. Start a fresh conversation and describe a teaching goal. You do not need to write code or complete a technical specification yourself.
3. Choose or revise the proposed hidden patterns, then approve the concrete assignment and rubric. The Agent must wait for those decisions before generation.
4. Inspect the generated teaching package and request revisions before accepting it.

Example starting request:

> Use the DataCanvas EDU Skill to design a synthetic dataset for my introductory business analytics class. Students may use AI. Ask which hidden patterns I want students to discover and propose options. Then show me one assignment and a matching rubric. Wait for my approval before generating the data and reference solution.

Use [this feedback guide](docs/TRY_AND_REPORT.md) to record your trial. For Claude's Skill upload interface, the current download is [datacanvas-edu-v0.1.2.zip](dist/datacanvas-edu-v0.1.2.zip). It contains the Skill folder; the repository's examples and documentation remain separate. The earlier v0.1.1 ZIP remains available as a comparison baseline.

**Importing a GitHub plugin marketplace:** Add `https://github.com/BANG23333/datacanvas-edu` in your Codex/ChatGPT desktop plugin interface, then install **DataCanvas EDU** from that marketplace. This repository includes the marketplace manifest and a self-contained plugin. See the [GitHub import instructions](docs/INSTALLATION.md#github-marketplace-import-codexchatgpt-desktop) for the interface that reported a missing manifest.

## How it works

| Phase | Agent work | Instructor decision |
| --- | --- | --- |
| Plan | Ask about hidden patterns, propose choices, then draft one assignment and its discovery-based rubric | Approve the patterns and concrete teaching design before generation |
| Create | Write and execute generation code, retaining parameters and random seeds | Resolve substantive design tradeoffs |
| Verify / Test Analysis | Measure the exported data, check constraints and intended patterns, and prepare reference evidence | Review failures, interpretations, and proposed revisions |
| Evaluate | Assemble the data, assignment, reference key, rubric, and reproducibility files | Accept or revise the teaching package |

The resulting package includes:

- **Student materials:** dataset, data dictionary, business context, and assignment.
- **Instructor materials:** a pattern-by-pattern solution with measured evidence, charts and interpretations; major/minor discovery credit, duplicate and invalid-finding examples, a matching rubric, and a review record.
- **Reproducibility materials:** generation and verification code, seeds, parameters, environment information, and file fingerprints.

A numerical pass means the declared checks passed. Final educational suitability remains an instructor judgment.

## Examples across business domains

| Example | Teaching context | Rows | Pattern categories |
| --- | --- | --- | --- |
| [Marketing campaigns](examples/marketing-campaigns/teaching_brief.md) | Conversion and contact cost | 5,000 | 2 |
| [Hotel bookings](examples/hotel-bookings/teaching_brief.md) | Cancellations and quoted room rates | 4,000 | 3 |
| [Equipment rental](examples/equipment-rental/teaching_brief.md) | Turnaround time and repair risk | 3,000 | 2 |
| [WindowDash](examples/windowdash/teaching_brief.md) | Food-delivery operations and customer behavior | 15,000 | 8 |

These are editable development cases, not the limits of the Skill. The Agent can write new case code and custom measurements. WindowDash is one example; its variables, chart requirements, and grading scale are not global defaults. Its inherited rubric still requires instructor reconciliation.

## Repository contents

```text
skills/datacanvas-edu/   Installable Skill: SKILL.md, scripts, and references
.agents/plugins/        Manifest for importing this GitHub repository as a marketplace
plugins/datacanvas-edu/  Plugin manifest and generated copy of the complete Skill
examples/              Four case configurations and teaching briefs
docs/                  Installation, trial guidance, and evidence boundaries
tests/                 Behavioral checks for the shared helper
scripts/               Rebuild the Skill archive and synchronize the plugin bundle
dist/                  Versioned Skill ZIP and its file manifest
```

## Run a reproducible example

The natural-language Skill is the instructor interface. The commands below are optional developer/researcher checks that run supplied example specifications directly. They do not perform the instructor interview or establish approval. In a teaching conversation, the Agent must obtain design approval before running a build. Run from the repository root with Python 3.10 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python skills/datacanvas-edu/scripts/dataset_workflow.py build --case examples/hotel-bookings --output outputs/hotel-trial-01 --seed 101
python skills/datacanvas-edu/scripts/dataset_workflow.py verify-package --package outputs/hotel-trial-01
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1`. Use a new output directory for each build. Plotting uses Matplotlib; the WindowDash generator also uses NumPy and pandas. The common numerical helper itself uses the Python standard library. Python package installation is handled by the host environment; installing a Skill does not automatically configure every dependency.

Run the behavioral checks or rebuild the archive:

```sh
python -m unittest discover -s tests -v
python scripts/package_skill.py
python scripts/package_plugin.py
python scripts/package_plugin.py --check
```

Edit the canonical Skill under `skills/datacanvas-edu/`, then rebuild both distribution formats. The bundled copy under `plugins/` is generated; the check above catches missing files and stale copies.

## Evidence and development plan

The original implementation was checked across four configurations, with 16 runs and 64 required numerical check evaluations. All met their configured criteria. Same-seed repeats reproduced dataset bytes, and 18 behavioral tests passed. These are scoped engineering results, not a teacher usability study or evidence of student learning. See [validation and research status](docs/VALIDATION.md).

The first instructor trial and the v0.1.2 response are documented in [trial feedback](docs/TRIAL_FEEDBACK_V0.1.2.md). Next steps are a fresh-conversation trial of the revised Skill, further feedback-driven revisions, platform checks, and a formal versioned release. The intended preprint will document the framework and measured artifact evidence. Analysis-Agent comparisons and student learning studies remain separate research stages.

## Contributing and release status

See [CONTRIBUTING.md](CONTRIBUTING.md) for useful feedback and example contributions, and [CHANGELOG.md](CHANGELOG.md) for version history. All repository artifacts and code use English; instructor conversations may use the instructor's preferred language.

The repository became public on 2026-09-08. A license and formal citation will be added when those decisions are finalized. The source, v0.1.2 Skill ZIP, prior v0.1.1 ZIP, and repository-hosted plugin marketplace are available here. This does not imply a paper, formal GitHub Release, or listing in an official curated plugin catalog.
