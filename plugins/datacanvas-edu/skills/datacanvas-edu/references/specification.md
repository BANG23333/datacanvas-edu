# Executable Specification Contract

The Agent writes JSON; the instructor reviews business and teaching choices. The v0.1 helper supports Python generation and one CSV table. Other backends or multiple tables require additional implementation and must not be described as tested helper features.

Before generation in an instructor conversation, the hidden patterns, single-assignment scope, and concrete rubric must be reviewed and approved. Keep actual approval evidence and scope in `decisions`; mark `review.design_status` accepted only when supported. Pending specifications may be written as review drafts, but the conversational Skill must wait rather than build them. The technical helper does not authenticate or enforce conversational approval. See [assignment and rubric design](assignment-and-rubric.md) for the student brief, reference solution, and discovery-based scoring structure.

## Case fields

| Field | Contract |
| --- | --- |
| `version`, `case_id`, `title`, `domain` | Nonempty strings; domain is free text, not an enumeration |
| `record_unit`, `business_context`, `learner_profile`, `ai_policy` | Student-readable context without hidden answers |
| `learning_objectives` | List of `{id, description}` records |
| `row_count` | Positive integer |
| `columns` | Schema records described below |
| `patterns` | Discovery records linked to objectives and checks |
| `checks` | Data measurements with explicit criteria |
| `assignment` | `{requirements: [English requirements]}` for one assignment unless multiple assignments were explicitly requested |
| `rubric` | `{complete: bool, total_points: number, criteria: [{name, points, description}], notes: [text]}` |
| `parameters` | Object read by the generator; no prescribed domain-specific keys |
| `decisions` | List of `{topic, value, source, status}`; distinguish instructor instructions, supplied materials, and Agent proposals |
| `review` | `{design_status: "pending" or "accepted", evidence: text}`; only record acceptance supported by the conversation |

For `rubric.complete: true`, criterion points must sum to the total. This checks arithmetic only. Provide substantive descriptors, partial-credit policy, additional findings, duplicates, invalid analyses, and deduction rules in the case notes. Preserve an existing tier/deduction rubric rather than silently replacing it with additive criteria. An incomplete inherited rubric can remain a review draft; the helper does not invent missing rules or grade students.

## Columns and patterns

Columns require `name`, `type`, `description`, and `unit`. Types: `string`, `integer`, `number`, `boolean`, `date`, `datetime`. Dates use ISO formats. Booleans accept true/false or 1/0, case-insensitive. An empty field is missing, not zero.

Optional properties: `nullable` (default false), `unique`, `categories`, `min`, `max`, `missing_when`. The last is a filter list requiring missing values exactly in matching rows and present values elsewhere. Identifiers can be strings. Ranges come from the case; no universal positivity assumption is imposed.

Patterns require `id`, `title`, `objective_ids`, `business_question`, `generation_rule`, `interaction_policy`, `interpretation_limits`, `credit`, and `check_ids`. `credit` is a descriptive label, not a fixed grading tier. Each pattern must link to at least one required check. Composite discoveries require checks for all necessary subclaims.

## Checks and filters

Checks require `id`, `description`, `metric`, `where`, `min_n`, and `acceptance`. `required` defaults to true. Differences also require `compare_where` and `min_compare_n`.

Filter lists combine clauses with AND. A clause is `{field, op, value}`. Operations: `eq`, `ne`, `in`, `not_in`, `lt`, `le`, `gt`, `ge`, `is_missing`. The last uses a boolean value. Optional `part` extracts year, month, day, hour, or weekday from a date/datetime; weekdays use Monday=0 through Sunday=6. Use type-appropriate values. Express more complex logic with documented derived fields or custom measurements.

| Metric | Extra fields | Observed quantity |
| --- | --- | --- |
| `share` | `event` filter list | Proportion of target rows matching the event |
| `share_difference` | `event`, `compare_where`, `min_compare_n` | Target share minus comparator share, on a 0–1 scale |
| `mean` | `field` | Mean of nonmissing target values |
| `mean_difference` | `field`, `compare_where`, `min_compare_n` | Target mean minus comparator mean |
| `correlation` | `x`, `y` | Pearson correlation using complete pairs |
| `custom` | `custom_name` | Finite numeric result from the case measurement function |

Mean/correlation support excludes missing required values. Shares use every filtered row as the denominator; exclude missing rows with filters when that is the intended definition. Missingness can itself be an event. State units and denominators in descriptions. Review agreement between prose and executable filters; structural validation cannot infer a semantic mismatch.

`acceptance.op` supports gt, ge, lt, le, eq, between. Supply `value` for a single bound or `low`/`high` for an inclusive interval. `eq` permits optional `atol` (default zero). Do not call thresholds selected after seeing results prespecified. Example thresholds belong to their example, not all teaching cases.

For custom metrics, the helper filters rows and enforces declared support; the function returns `value` and `usable_n`, plus `usable_compare_n` when a comparator exists. If the function further drops rows, these reduced counts govern acceptance. Do not hide population changes or let custom code decide its own pass status.
