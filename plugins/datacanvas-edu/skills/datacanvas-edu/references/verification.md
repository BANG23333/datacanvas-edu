# Execution and Verification

These commands are for the Agent, not a required instructor interface. Core helpers use Python 3.10+ and its standard library. Reference chart rendering uses Matplotlib. Use the configured host runtime and permitted dependency installation. No paid API, online dataset, or browser connection is required by the helper; the host Agent interprets language and writes the case code.

## Case interface

A case directory contains `specification.json`, `generate.py`, and optional `custom_measurements.py`. The generator accepts `--spec PATH --seed INTEGER --output PATH`, uses the supplied seed, and writes the CSV only to the requested output path. Inspect generated code before running it. The helper is not a sandbox; the host's permission controls still apply.

Custom metrics implement `measure(name, target_rows, comparator_rows, check)` and return `{value: finite_number, usable_n: integer}`, plus `usable_compare_n` when needed. Rows are schema-typed dictionaries. Return measurements, not PASS/FAIL. The helper applies the declared threshold. Inspect custom code and cross-check its calculations.

## Commands

In an instructor session, run `build` only after the instructor has approved the hidden patterns, assignment requirements, and rubric. `check-spec` and review drafts can help prepare a proposal, but passing checks cannot authorize generation. The CLI remains a developer utility and does not verify that a human conversation or approval occurred.

Resolve and quote paths for the current environment:

```text
python SKILL_DIR/scripts/dataset_workflow.py check-spec --spec CASE/specification.json
python SKILL_DIR/scripts/dataset_workflow.py build --case CASE --output NEW_RUN_DIRECTORY --seed 101
python SKILL_DIR/scripts/dataset_workflow.py validate --spec SPEC --data CSV --report NEW_REPORT_JSON
python SKILL_DIR/scripts/dataset_workflow.py verify-package --package RUN_DIRECTORY
```

`validate` also accepts `--custom PATH`. Build uses a copied custom module when present. Each build refuses an existing output directory and retains failed generator logs. Required failed or unexecuted checks produce a nonzero exit code. A technical pass is separate from instructional acceptance and delivery completeness.

By default, build renders reference charts. Missing plotting capability is reported as NEEDS_REVIEW. `--no-charts` permits a labeled measurement-only robustness run; it does not satisfy full chart delivery. Automatic charts are starting evidence. Add domain-appropriate scatterplots, time series, and other views when they communicate the intended relationship better.

## Review and reproduction

Check raw schema before calculating patterns. Malformed data, missing checks, undefined metrics, or sparse required groups must not disappear into zeros or passes. Inspect support, effects, denominators, interactions, and all necessary subclaims. Independently recompute representative values. Review chart labels and scales and verify that explanations do not turn associations into proven causes.

Run the same case twice with the same seed in different directories and compare dataset bytes. Declare fresh seeds before testing, retain every result, and explain failures. Manifests and paths differ naturally across runs; compare the data and recorded inputs rather than expecting all package files to match byte-for-byte.

The helper creates student data/dictionary/assignment; instructor key/rubric/checks/charts/pending acceptance; and reproducibility code/seed/environment/manifest. `verify-package` checks fingerprints and extra student files, not whether prose leaks answers. Review student-facing text before sharing. A discoverability solver should receive only the student directory in a fresh context.

Expand the helper's key and rubric into the approved pattern-by-pattern instructor solution described in [assignment and rubric design](assignment-and-rubric.md). Each major finding needs a usable reference chart, measured evidence, interpretation, and scoring guidance; a PASS table and generic criterion headings do not suffice. Keep approved scope to one assignment and one solution/rubric set unless multiple assignments were explicitly requested.

The helper does not grade students, authenticate human identity, or prove contamination avoidance, ease of use, or educational effectiveness. Design acceptance supplied in a specification is an assertion that must have supporting conversational evidence. Record final instructor decisions only after they occur, with scope and evidence. Put accepted revisions into a new case/package version instead of silently changing frozen artifacts. Building a package does not publish or submit it.
