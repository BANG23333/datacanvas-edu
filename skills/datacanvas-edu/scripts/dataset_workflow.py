"""Domain-independent helpers for instructor-authored synthetic teaching cases."""

import argparse
import csv
from datetime import date, datetime, timezone
import hashlib
import importlib.util
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import shutil
import statistics
import subprocess
import sys
import textwrap

VERSION = "0.1.0"
TYPES = {"string", "integer", "number", "boolean", "date", "datetime"}
METRICS = {"share", "share_difference", "mean", "mean_difference", "correlation", "custom"}
FILTER_OPS = {"eq", "ne", "in", "not_in", "lt", "le", "gt", "ge", "is_missing"}
BOUND_OPS = {"gt", "ge", "lt", "le", "eq", "between"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def spec_errors(spec):
    errors = []
    if not isinstance(spec, dict):
        return ["Specification must be a JSON object."]

    def require(condition, message):
        if not condition:
            errors.append(message)

    def records(key):
        value = spec.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(x, dict) for x in value):
            errors.append(f"{key} must be a nonempty list of objects.")
            return []
        return value

    for key in ["version", "case_id", "title", "domain", "record_unit", "business_context", "learner_profile", "ai_policy"]:
        require(isinstance(spec.get(key), str) and bool(spec[key].strip()), f"{key} must be a nonempty string.")
    require(type(spec.get("row_count")) is int and spec["row_count"] > 0, "row_count must be a positive integer.")
    require(isinstance(spec.get("parameters"), dict), "parameters must be an object.")
    objectives, columns, patterns, checks = [records(k) for k in ["learning_objectives", "columns", "patterns", "checks"]]

    def ids(items, key, label):
        values = [item.get(key) for item in items]
        require(all(isinstance(v, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", v) for v in values), f"{label} identifiers must start with a letter and contain letters, digits, underscores, or hyphens.")
        strings = [v for v in values if isinstance(v, str)]
        require(len(set(strings)) == len(strings), f"Duplicate {label} identifiers.")
        return set(strings)

    objective_ids = ids(objectives, "id", "objective")
    column_ids = ids(columns, "name", "column")
    ids(patterns, "id", "pattern")
    check_ids = ids(checks, "id", "check")
    column_types = {c.get("name"): c.get("type") for c in columns if isinstance(c.get("name"), str)}
    for item in objectives:
        require(bool(item.get("description")), "Each objective requires a description.")

    def filters(value, label):
        if not isinstance(value, list):
            errors.append(f"{label} must be a filter list, including [] for all rows.")
            return
        for clause in value:
            if not isinstance(clause, dict):
                errors.append(f"{label} contains a non-object filter.")
                continue
            field, op = clause.get("field"), clause.get("op")
            require(isinstance(field, str) and field in column_ids, f"{label}: unknown field {field}.")
            require(op in FILTER_OPS, f"{label}: unknown operation {op}.")
            require("value" in clause, f"{label}: filter value is required.")
            if op in {"in", "not_in"}:
                require(isinstance(clause.get("value"), list), f"{label}: membership value must be a list.")
            if op == "is_missing":
                require(type(clause.get("value")) is bool, f"{label}: is_missing requires a boolean.")
            if "part" in clause:
                require(clause["part"] in {"year", "month", "day", "hour", "weekday"}, f"{label}: unsupported date part.")
                require(column_types.get(field) in {"date", "datetime"}, f"{label}: date part requires a date column.")
                require(clause["part"] != "hour" or column_types.get(field) == "datetime", f"{label}: hour requires datetime.")

    for c in columns:
        require(c.get("type") in TYPES, f"Unsupported type in column {c.get('name')}.")
        require(bool(c.get("description")) and isinstance(c.get("unit"), str), f"Column {c.get('name')} needs description and unit.")
        for flag in ["nullable", "unique"]:
            require(flag not in c or type(c[flag]) is bool, f"{flag} must be boolean.")
        if "categories" in c:
            require(isinstance(c["categories"], list) and bool(c["categories"]), "categories must be a nonempty list.")
        if "missing_when" in c:
            filters(c["missing_when"], f"{c.get('name')} missing_when")
    for p in patterns:
        for key in ["title", "business_question", "generation_rule", "interaction_policy", "interpretation_limits", "credit"]:
            require(isinstance(p.get(key), str) and bool(p[key].strip()), f"Pattern {p.get('id')} requires {key}.")
        for key, known in [("objective_ids", objective_ids), ("check_ids", check_ids)]:
            refs = p.get(key)
            require(isinstance(refs, list) and bool(refs) and all(isinstance(r, str) and r in known for r in refs), f"Pattern {p.get('id')}: invalid {key}.")
        linked = p.get("check_ids", [])
        require(isinstance(linked, list) and any(c.get("id") in linked and c.get("required", True) for c in checks), f"Pattern {p.get('id')} needs a required check.")
    for c in checks:
        label = f"Check {c.get('id')}"
        metric = c.get("metric")
        require(metric in METRICS, f"{label}: unsupported metric.")
        require(bool(c.get("description")), f"{label}: description required.")
        require(type(c.get("min_n")) is int and c["min_n"] > 0, f"{label}: min_n must be positive.")
        require(type(c.get("required", True)) is bool, f"{label}: required must be boolean.")
        filters(c.get("where"), label)
        if metric in {"share", "share_difference"}:
            filters(c.get("event"), f"{label} event")
            require(bool(c.get("event")), f"{label}: share event must not be empty.")
        if metric in {"mean", "mean_difference"}:
            require(column_types.get(c.get("field")) in {"number", "integer"}, f"{label}: numeric field required.")
        if metric == "correlation":
            require(all(column_types.get(c.get(k)) in {"number", "integer"} for k in ["x", "y"]), f"{label}: numeric x/y required.")
        if metric.endswith("_difference") or "compare_where" in c:
            filters(c.get("compare_where"), f"{label} comparator")
            require(type(c.get("min_compare_n")) is int and c["min_compare_n"] > 0, f"{label}: positive min_compare_n required.")
        if metric == "custom":
            require(isinstance(c.get("custom_name"), str) and bool(c["custom_name"]), f"{label}: custom_name required.")
        bound = c.get("acceptance", {})
        if not isinstance(bound, dict):
            errors.append(f"{label}: acceptance must be an object.")
            continue
        require(bound.get("op") in BOUND_OPS, f"{label}: invalid acceptance operation.")
        if bound.get("op") == "between":
            require(finite(bound.get("low")) and finite(bound.get("high")) and bound["low"] <= bound["high"], f"{label}: ordered finite bounds required.")
        else:
            require(finite(bound.get("value")), f"{label}: finite acceptance value required.")
        require(finite(bound.get("atol", 0)) and bound.get("atol", 0) >= 0, f"{label}: invalid tolerance.")
    assignment = spec.get("assignment", {})
    require(isinstance(assignment, dict) and isinstance(assignment.get("requirements"), list) and bool(assignment["requirements"]) and all(isinstance(x, str) and x.strip() for x in assignment["requirements"]), "assignment.requirements must be nonempty text entries.")
    rubric = spec.get("rubric", {})
    if not isinstance(rubric, dict):
        errors.append("rubric must be an object.")
    else:
        require(type(rubric.get("complete")) is bool, "rubric.complete must be boolean.")
        require(finite(rubric.get("total_points")) and rubric["total_points"] > 0, "Rubric total_points must be positive.")
        criteria = rubric.get("criteria", [])
        valid = isinstance(criteria, list) and all(isinstance(x, dict) and bool(x.get("name")) and bool(x.get("description")) and finite(x.get("points")) and x["points"] >= 0 for x in criteria)
        require(valid, "Rubric criteria require name, points, and description.")
        require(isinstance(rubric.get("notes"), list) and all(isinstance(x, str) for x in rubric["notes"]), "Rubric notes must be a list of text.")
        if valid and rubric.get("complete") and finite(rubric.get("total_points")):
            require(bool(criteria) and math.isclose(sum(x["points"] for x in criteria), rubric["total_points"], abs_tol=1e-9), "Complete rubric points do not sum to the total.")
    decisions = spec.get("decisions")
    require(isinstance(decisions, list) and all(isinstance(x, dict) and all(k in x for k in ["topic", "value", "source", "status"]) for x in decisions), "decisions must record topic, value, source, and status.")
    review = spec.get("review", {})
    require(isinstance(review, dict) and review.get("design_status") in {"pending", "accepted"} and isinstance(review.get("evidence"), str), "review requires design_status and evidence.")
    if isinstance(review, dict) and review.get("design_status") == "accepted":
        require(bool(review.get("evidence", "").strip()), "Accepted design requires supporting evidence.")
    return errors


def convert(value, kind):
    if value == "":
        return None
    if kind == "string":
        return value
    if kind == "integer":
        n = float(value)
        if not math.isfinite(n) or not n.is_integer():
            raise ValueError("Expected finite integer")
        return int(n)
    if kind == "number":
        n = float(value)
        if not math.isfinite(n):
            raise ValueError("Expected finite number")
        return n
    if kind == "boolean":
        if value.lower() not in {"true", "false", "1", "0"}:
            raise ValueError("Expected boolean")
        return value.lower() in {"true", "1"}
    return datetime.fromisoformat(value) if kind == "datetime" else date.fromisoformat(value)


def matches(row, clauses):
    for c in clauses:
        value, expected, op = row[c["field"]], c["value"], c["op"]
        if c.get("part") and value is not None:
            value = value.weekday() if c["part"] == "weekday" else getattr(value, c["part"])
        if op == "is_missing":
            ok = (value is None) == expected
        elif value is None:
            ok = False
        else:
            if isinstance(value, (date, datetime)):
                kind = "datetime" if isinstance(value, datetime) else "date"
                expected = [convert(str(v), kind) for v in expected] if op in {"in", "not_in"} else convert(str(expected), kind)
            operations = {"eq": lambda: value == expected, "ne": lambda: value != expected,
                          "in": lambda: value in expected, "not_in": lambda: value not in expected,
                          "lt": lambda: value < expected, "le": lambda: value <= expected,
                          "gt": lambda: value > expected, "ge": lambda: value >= expected}
            ok = operations[op]()
        if not ok:
            return False
    return True


def load_data(spec, path):
    schema, rows, errors = spec["columns"], [], []
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != [c["name"] for c in schema]:
            return [], ["CSV headers/order differ from the specification."]
        for number, raw in enumerate(reader, 2):
            try:
                if None in raw or any(v is None for v in raw.values()):
                    raise ValueError("Wrong number of fields")
                row = {c["name"]: convert(raw[c["name"]], c["type"]) for c in schema}
                rows.append(row)
            except (ValueError, TypeError) as exc:
                errors.append(f"CSV line {number}: {exc}")
    if len(rows) != spec["row_count"]:
        errors.append(f"Expected {spec['row_count']} typed rows; loaded {len(rows)}.")
    for c in schema:
        name = c["name"]
        bad, seen = 0, set()
        for row in rows:
            value = row[name]
            if "missing_when" in c:
                if (value is None) != matches(row, c["missing_when"]):
                    bad += 1
            elif value is None and not c.get("nullable", False):
                bad += 1
            if value is None:
                continue
            if "categories" in c and value not in c["categories"]:
                bad += 1
            for bound, op in [("min", lambda a, b: a < b), ("max", lambda a, b: a > b)]:
                if bound in c:
                    expected = convert(str(c[bound]), c["type"]) if isinstance(value, (date, datetime)) else c[bound]
                    if op(value, expected):
                        bad += 1
            if c.get("unique") and value in seen:
                bad += 1
            seen.add(value)
        if bad:
            errors.append(f"{name}: {bad} constraint violations (a row may violate multiple rules).")
    return rows, errors


def accepts(value, bound):
    op = bound["op"]
    if op == "between":
        return bound["low"] <= value <= bound["high"]
    target = bound["value"]
    return {"gt": lambda: value > target, "ge": lambda: value >= target,
            "lt": lambda: value < target, "le": lambda: value <= target,
            "eq": lambda: math.isclose(value, target, rel_tol=0, abs_tol=bound.get("atol", 0))}[op]()


def measure(rows, c, custom):
    target = [r for r in rows if matches(r, c["where"])]
    comparator = [r for r in rows if matches(r, c["compare_where"])] if "compare_where" in c else []
    result = {"id": c["id"], "description": c["description"], "metric": c["metric"], "required": c.get("required", True),
              "where": c["where"], "compare_where": c.get("compare_where"), "n": len(target), "compare_n": len(comparator),
              "usable_n": len(target), "usable_compare_n": len(comparator), "min_n": c["min_n"],
              "min_compare_n": c.get("min_compare_n"), "acceptance": c["acceptance"], "value": None, "status": "NOT_RUN"}
    try:
        metric = c["metric"]
        if metric.startswith("share"):
            a = sum(matches(r, c["event"]) for r in target) / len(target) if target else None
            b = sum(matches(r, c["event"]) for r in comparator) / len(comparator) if comparator else None
            result.update(target_value=a, comparator_value=b)
            value = a - b if metric.endswith("difference") and a is not None and b is not None else (a if metric == "share" else None)
        elif metric.startswith("mean"):
            a = [r[c["field"]] for r in target if r[c["field"]] is not None]
            b = [r[c["field"]] for r in comparator if r[c["field"]] is not None]
            av, bv = statistics.mean(a) if a else None, statistics.mean(b) if b else None
            result.update(usable_n=len(a), usable_compare_n=len(b), target_value=av, comparator_value=bv)
            value = av - bv if metric.endswith("difference") and av is not None and bv is not None else (av if metric == "mean" else None)
        elif metric == "correlation":
            pairs = [(r[c["x"]], r[c["y"]]) for r in target if r[c["x"]] is not None and r[c["y"]] is not None]
            result["usable_n"] = len(pairs)
            value = statistics.correlation([p[0] for p in pairs], [p[1] for p in pairs]) if len(pairs) > 1 else None
        else:
            if custom is None:
                result["reason"] = "Required custom measurement module is unavailable."
                return result
            measured = custom.measure(c["custom_name"], target, comparator, c)
            value = measured["value"]
            for key, maximum in [("usable_n", len(target)), ("usable_compare_n", len(comparator))]:
                if key == "usable_compare_n" and "compare_where" not in c:
                    continue
                count = measured[key]
                if type(count) is not int or not 0 <= count <= maximum:
                    raise ValueError(f"Invalid custom {key}")
                result[key] = count
        result["value"] = float(value) if finite(value) else None
        support = result["usable_n"] >= c["min_n"] and ("compare_where" not in c or result["usable_compare_n"] >= c["min_compare_n"])
        if not support:
            result.update(status="FAIL", reason="Usable subgroup support is below the declared minimum.")
        elif result["value"] is None:
            result.update(status="FAIL", reason="Measurement is undefined or nonfinite.")
        else:
            result["status"] = "PASS" if accepts(result["value"], c["acceptance"]) else "FAIL"
            result["reason"] = "Declared criterion satisfied." if result["status"] == "PASS" else "Observed value does not satisfy the declared criterion."
    except (Exception,) as exc:
        result.update(status="FAIL", reason=f"Measurement error: {type(exc).__name__}: {exc}")
    return result


def validate(spec_path, data_path, custom_path=None):
    spec = read_json(spec_path)
    errors = spec_errors(spec)
    if errors:
        return {"status": "FAIL", "specification_errors": errors, "checks": []}
    custom = None
    custom_error = None
    if custom_path and Path(custom_path).exists():
        try:
            module_spec = importlib.util.spec_from_file_location("case_measurements", custom_path)
            custom = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(custom)
        except Exception as exc:
            custom_error = f"Custom module failed to load: {exc}"
    try:
        rows, errors = load_data(spec, data_path)
    except Exception as exc:
        rows, errors = [], [f"Data could not be validated: {type(exc).__name__}: {exc}"]
    if errors:
        checks = [{"id": c["id"], "required": c.get("required", True), "status": "NOT_RUN", "reason": "Schema/data checks failed."} for c in spec["checks"]]
    else:
        checks = [measure(rows, c, custom) for c in spec["checks"]]
    outcome = not errors and all(c["status"] == "PASS" for c in checks if c["required"])
    return {"workflow_version": VERSION, "case_id": spec["case_id"], "specification_version": spec["version"],
            "specification_sha256": digest(spec_path), "data_sha256": digest(data_path) if Path(data_path).is_file() else None,
            "status": "PASS" if outcome else "FAIL", "schema": {"status": "FAIL" if errors else "PASS", "typed_rows": len(rows), "errors": errors},
            "custom_module_error": custom_error, "checks": checks,
            "patterns": [{"id": p["id"], "check_ids": p["check_ids"], "status": "PASS" if all(next(c for c in checks if c["id"] == key)["status"] == "PASS" for key in p["check_ids"]) else "FAIL"} for p in spec["patterns"]]}


def md_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def report_markdown(result):
    text = ["# Numerical Validation Report", "", f"Technical status: **{result['status']}**. Instructor acceptance is separate.", ""]
    for error in result.get("schema", {}).get("errors", []) + result.get("specification_errors", []):
        text.append(f"- {error}")
    text += ["", "| Check | Status | Usable target / comparator | Observed value | Criterion |", "| --- | --- | --- | --- | --- |"]
    for c in result["checks"]:
        text.append(f"| {md_cell(c['id'])} | {c['status']} | {c.get('usable_n', 'N/A')} / {c.get('usable_compare_n', 'N/A')} | {c.get('value', 'N/A')} | {md_cell(c.get('acceptance', c.get('reason', '')))} |")
    text += ["", "Read the JSON report for exact filters, support thresholds, and reasons. A technical pass does not validate every narrative interpretation."]
    return "\n".join(text) + "\n"


def chart_checks(result, output, spec, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    output.mkdir(exist_ok=True)
    paths = []
    for check in result["checks"]:
        if check.get("value") is None:
            continue
        fig, ax = plt.subplots(figsize=(7.2, 4.3), layout="constrained")
        if check["metric"] == "correlation":
            rule = next(c for c in spec["checks"] if c["id"] == check["id"])
            group = [r for r in rows if matches(r, rule["where"]) and r[rule["x"]] is not None and r[rule["y"]] is not None]
            ax.scatter([r[rule["x"]] for r in group], [r[rule["y"]] for r in group], s=8, alpha=.25, color="#285f87", rasterized=True)
            units = {c["name"]: c["unit"] for c in spec["columns"]}
            ax.set_xlabel(f"{rule['x']} ({units[rule['x']]})")
            ax.set_ylabel(f"{rule['y']} ({units[rule['y']]})")
            ax.set_title(textwrap.fill(check["description"], 60) + f"\nr = {check['value']:.3f}; n = {len(group):,}", loc="left", fontsize=11)
            ax.spines[["top", "right"]].set_visible(False)
            fig.savefig(output / f"{check['id']}.png", dpi=150)
            fig.savefig(output / f"{check['id']}.svg")
            paths.append(f"{check['id']}.png")
            plt.close(fig)
            continue
        if check.get("target_value") is not None and check.get("comparator_value") is not None:
            labels, values = [f"Target (n={check['usable_n']})", f"Comparator (n={check['usable_compare_n']})"], [check["target_value"], check["comparator_value"]]
        else:
            labels, values = [f"Observed metric (n={check['usable_n']})"], [check["value"]]
        ax.bar(labels, values, color=["#285f87", "#9eacb5"][:len(values)], width=.55)
        spread = max(max(values) - min(values), max(abs(v) for v in values), .1)
        ax.set_ylim(min(0, min(values)) - .12 * spread, max(0, max(values)) + .25 * spread)
        ax.axhline(0, color="#888888", linewidth=.7)
        ax.set_title(textwrap.fill(check["description"], 60), loc="left", fontsize=11)
        rule = next(c for c in spec["checks"] if c["id"] == check["id"])
        field = next((c for c in spec["columns"] if c["name"] == rule.get("field")), None)
        ax.set_ylabel("Proportion (0–1)" if check["metric"].startswith("share") else (f"Mean {field['name']} ({field['unit']})" if field else "Metric value; units defined in the check"))
        ax.spines[["top", "right"]].set_visible(False)
        for i, value in enumerate(values):
            ax.annotate(f"{value:.4g}", (i, value), xytext=(0, 6 if value >= 0 else -13), textcoords="offset points", ha="center")
        fig.savefig(output / f"{check['id']}.png", dpi=150)
        fig.savefig(output / f"{check['id']}.svg")
        paths.append(str((output / f"{check['id']}.png").name))
        plt.close(fig)
    return {"status": "PASS" if paths else "NEEDS_REVIEW", "files": paths, "matplotlib": matplotlib.__version__}


def build(case, output, seed, no_charts=False, timeout=120):
    case, output = Path(case).resolve(), Path(output).resolve()
    spec = read_json(case / "specification.json")
    errors = spec_errors(spec)
    if errors:
        raise ValueError("Invalid specification: " + "; ".join(errors))
    if not (case / "generate.py").is_file():
        raise ValueError("Case is missing generate.py.")
    output.mkdir(parents=True, exist_ok=False)
    student, teacher, repro = [output / name for name in ["student", "instructor", "reproducibility"]]
    for directory in [student, teacher, repro]:
        directory.mkdir()
    shutil.copy2(case / "specification.json", teacher / "specification.json")
    shutil.copy2(case / "generate.py", repro / "generate.py")
    shutil.copy2(Path(__file__), repro / "dataset_workflow.py")
    custom_path = None
    if (case / "custom_measurements.py").exists():
        custom_path = repro / "custom_measurements.py"
        shutil.copy2(case / "custom_measurements.py", custom_path)
    write_json(repro / "parameters.json", {"seed": seed, "parameters": spec["parameters"]})
    data_path, spec_path = student / "dataset.csv", teacher / "specification.json"
    try:
        run = subprocess.run([sys.executable, str(repro / "generate.py"), "--spec", str(spec_path), "--seed", str(seed), "--output", str(data_path)], cwd=output, capture_output=True, text=True, timeout=timeout, check=False)
        (repro / "generation_log.txt").write_text(run.stdout + run.stderr)
        if run.returncode != 0:
            raise RuntimeError(f"Generator exited with code {run.returncode}; see generation_log.txt.")
        result = validate(spec_path, data_path, custom_path)
    except Exception as exc:
        result = {"status": "FAIL", "specification_errors": [f"Generation/execution failed: {type(exc).__name__}: {exc}"], "checks": []}
        if not (repro / "generation_log.txt").exists():
            (repro / "generation_log.txt").write_text(str(exc))
    write_json(teacher / "validation_report.json", result)
    (teacher / "validation_report.md").write_text(report_markdown(result))
    dictionary = [f"# {spec['title']}: Data Dictionary", "", "This dataset is synthetic.", "", f"Record unit: {spec['record_unit']}", "", "| Field | Type | Unit | Meaning | Missingness |", "| --- | --- | --- | --- | --- |"]
    for c in spec["columns"]:
        missing = "Required" if not c.get("nullable") else "Permitted"
        if "missing_when" in c:
            missing = "Missing exactly when " + json.dumps(c["missing_when"])
        dictionary.append("| " + " | ".join(md_cell(v) for v in [c["name"], c["type"], c["unit"], c["description"], missing]) + " |")
    (student / "data_dictionary.md").write_text("\n".join(dictionary) + "\n")
    assignment = [f"# {spec['title']}", "", "This teaching dataset is synthetic.", "", spec["business_context"], "", f"Intended learners: {spec['learner_profile']}", "", spec["ai_policy"], "", "## Learning Objectives", ""]
    assignment += [f"- {x['description']}" for x in spec["learning_objectives"]]
    assignment += ["", "## Assignment Requirements", ""] + [f"{i}. {x}" for i, x in enumerate(spec["assignment"]["requirements"], 1)]
    (student / "assignment.md").write_text("\n".join(assignment) + "\n")
    rubric = [f"# {spec['title']}: Rubric", "", f"Total points: {spec['rubric']['total_points']}", "", f"Arithmetic declared complete: {spec['rubric']['complete']}. Instructor review remains required.", ""]
    for c in spec["rubric"]["criteria"]:
        rubric += [f"## {c['name']} ({c['points']} points)", "", c["description"], ""]
    rubric += ["## Grading Notes", ""] + [f"- {n}" for n in spec["rubric"]["notes"]]
    (teacher / "rubric.md").write_text("\n".join(rubric) + "\n")
    key = [f"# {spec['title']}: Instructor Pattern Key", "", "Review draft. The key is not an exhaustive inventory of valid findings.", ""]
    for p in spec["patterns"]:
        key += [f"## {p['id']}: {p['title']}", "", p["business_question"], "", f"Credit category: {p['credit']}. Objectives: {', '.join(p['objective_ids'])}.", "", f"Generation: {p['generation_rule']}", "", f"Interactions: {p['interaction_policy']}", "", f"Interpretation limits: {p['interpretation_limits']}", ""]
        for check_id in p["check_ids"]:
            c = next((x for x in result["checks"] if x["id"] == check_id), {})
            key += [f"- {check_id}: {c.get('status', 'NOT_RUN')}; observed={c.get('value')}; usable target={c.get('usable_n')}; usable comparator={c.get('usable_compare_n')}"]
        key += [""]
    (teacher / "pattern_key.md").write_text("\n".join(key))
    charts = {"status": "NEEDS_REVIEW", "reason": "Charts intentionally skipped for this run."}
    if not no_charts:
        try:
            typed_rows, _ = load_data(spec, data_path)
            charts = chart_checks(result, teacher / "reference_charts", spec, typed_rows)
        except Exception as exc:
            charts = {"status": "NEEDS_REVIEW", "reason": f"Chart rendering failed: {type(exc).__name__}: {exc}"}
    acceptance = {"design": spec["review"], "final_instructor_acceptance": "pending", "accepted_by": None, "evidence": None,
                  "technical_status": result["status"], "charts": charts, "rubric_arithmetic_complete": spec["rubric"]["complete"],
                  "required_review": ["Business plausibility and objective alignment", "Correctness and usefulness of reference charts", "Narrative/key agreement with checks", "Student-facing answer leakage", "Complete grading decisions", "Difficulty and limitations"]}
    write_json(teacher / "acceptance_record.json", acceptance)
    reference_code = '''"""Recompute this package's numerical reference evidence without regenerating data."""
from pathlib import Path
import json
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "reproducibility"))
from dataset_workflow import validate
custom = HERE.parent / "reproducibility" / "custom_measurements.py"
result = validate(HERE / "specification.json", HERE.parent / "student" / "dataset.csv", custom if custom.exists() else None)
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["status"] == "PASS" else 2)
'''
    (teacher / "reference_analysis.py").write_text(reference_code)
    dependencies = {}
    for name in spec.get("runtime_dependencies", []) + (["matplotlib"] if charts["status"] == "PASS" else []):
        try:
            dependencies[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            dependencies[name] = "not found"
    (repro / "environment.txt").write_text(f"Python: {sys.version}\nPlatform: {platform.platform()}\nWorkflow: {VERSION}\nDependencies: {json.dumps(dependencies)}\nCharts: {json.dumps(charts)}\n")
    (repro / "revision_log.md").write_text(f"# Candidate Record\n\nCase version: {spec['version']}\nSeed: {seed}\nTechnical status: {result['status']}\n\nThis directory records one attempt. Preserve earlier attempts when revising the design or code.\n")
    files = {str(p.relative_to(output)): digest(p) for p in sorted(output.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}
    manifest = {"workflow_version": VERSION, "created_utc": datetime.now(timezone.utc).isoformat(), "case_id": spec["case_id"], "seed": seed,
                "technical_status": result["status"], "delivery_status": "READY_FOR_REVIEW" if result["status"] == "PASS" and charts["status"] == "PASS" and spec["rubric"]["complete"] else "NEEDS_REVIEW",
                "instructional_acceptance": "pending", "files": files}
    write_json(output / "manifest.json", manifest)
    return manifest


def verify_package(path):
    root = Path(path).resolve()
    manifest = read_json(root / "manifest.json")
    errors = []
    for relative, expected in manifest["files"].items():
        target = (root / relative).resolve()
        if not target.is_relative_to(root) or not target.is_file() or digest(target) != expected:
            errors.append(f"Missing, changed, or invalid artifact: {relative}")
    actual_student = {str(p.relative_to(root)) for p in (root / "student").rglob("*") if p.is_file()}
    expected_student = {p for p in manifest["files"] if p.startswith("student/")}
    for extra in sorted(actual_student - expected_student):
        errors.append(f"Unexpected student-facing file: {extra}")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "instructional_acceptance": manifest["instructional_acceptance"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    schema = sub.add_parser("check-spec")
    schema.add_argument("--spec", required=True)
    verify = sub.add_parser("validate")
    verify.add_argument("--spec", required=True)
    verify.add_argument("--data", required=True)
    verify.add_argument("--report", required=True)
    verify.add_argument("--custom")
    create = sub.add_parser("build")
    create.add_argument("--case", required=True)
    create.add_argument("--output", required=True)
    create.add_argument("--seed", required=True, type=int)
    create.add_argument("--no-charts", action="store_true")
    create.add_argument("--timeout", type=int, default=120)
    package = sub.add_parser("verify-package")
    package.add_argument("--package", required=True)
    args = parser.parse_args()
    try:
        if args.command == "check-spec":
            errors = spec_errors(read_json(args.spec))
            result = {"status": "FAIL" if errors else "PASS", "errors": errors}
        elif args.command == "validate":
            if Path(args.report).exists():
                raise FileExistsError("Report already exists; use a new report path.")
            result = validate(args.spec, args.data, args.custom)
            write_json(args.report, result)
        elif args.command == "verify-package":
            result = verify_package(args.package)
        else:
            result = build(args.case, args.output, args.seed, args.no_charts, args.timeout)
        if args.command == "build":
            print(json.dumps({k: v for k, v in result.items() if k != "files"}, indent=2))
        else:
            print(json.dumps(result, indent=2))
        return 0 if result.get("status", result.get("technical_status")) == "PASS" else 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
