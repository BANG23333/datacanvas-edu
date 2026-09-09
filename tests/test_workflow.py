"""Behavioral checks for numerical validity and package integrity."""

import copy
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "skills/datacanvas-edu/scripts/dataset_workflow.py"
ms = importlib.util.spec_from_file_location("workflow", MODULE)
w = importlib.util.module_from_spec(ms)
ms.loader.exec_module(w)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.spec = w.read_json(ROOT / "examples/marketing-campaigns/specification.json")
        self.spec.update(row_count=4, columns=[
            {"name": "Group", "type": "string", "description": "Group", "unit": "category"},
            {"name": "Value", "type": "number", "description": "Value", "unit": "units", "nullable": True},
            {"name": "Flag", "type": "boolean", "description": "Outcome", "unit": "boolean"}],
            checks=[{"id": "GAP", "description": "Mean difference", "metric": "mean_difference", "where": [{"field": "Group", "op": "eq", "value": "A"}], "compare_where": [{"field": "Group", "op": "eq", "value": "B"}], "field": "Value", "min_n": 2, "min_compare_n": 2, "acceptance": {"op": "ge", "value": 2}}])
        self.spec["patterns"] = [self.spec["patterns"][0]]
        self.spec["patterns"][0]["check_ids"] = ["GAP"]
        self.rows = [["A", 4, True], ["A", 6, False], ["B", 1, True], ["B", 3, False]]

    def tearDown(self):
        self.temp.cleanup()

    def evaluate(self, custom=None):
        w.write_json(self.root / "spec.json", self.spec)
        with (self.root / "data.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([c["name"] for c in self.spec["columns"]])
            writer.writerows(self.rows)
        return w.validate(self.root / "spec.json", self.root / "data.csv", custom)

    def test_known_mean_difference(self):
        result = self.evaluate()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"][0]["value"], 3)

    def test_empty_comparator_fails(self):
        self.spec["checks"][0]["compare_where"][0]["value"] = "absent"
        result = self.evaluate()
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["checks"][0]["usable_compare_n"], 0)

    def test_sparse_group_cannot_pass_large_effect(self):
        self.spec["checks"][0]["min_n"] = 3
        self.assertEqual(self.evaluate()["status"], "FAIL")

    def test_missing_values_reduce_usable_support(self):
        self.rows[0][1] = ""
        result = self.evaluate()
        self.assertEqual(result["checks"][0]["usable_n"], 1)
        self.assertEqual(result["status"], "FAIL")

    def test_nonfinite_value_blocks_pattern_evaluation(self):
        self.rows[0][1] = "nan"
        result = self.evaluate()
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["checks"][0]["status"], "NOT_RUN")

    def test_constant_correlation_is_not_success(self):
        c = self.spec["checks"][0]
        c.update(metric="correlation", where=[], x="Value", y="Value")
        c.pop("compare_where")
        for r in self.rows:
            r[1] = 5
        self.assertEqual(self.evaluate()["status"], "FAIL")

    def test_known_share_difference(self):
        c = self.spec["checks"][0]
        c.update(metric="share_difference", event=[{"field": "Flag", "op": "eq", "value": True}], acceptance={"op": "eq", "value": 0})
        self.assertEqual(self.evaluate()["checks"][0]["value"], 0)

    def test_structural_missingness_is_exact(self):
        self.spec["columns"][1]["missing_when"] = [{"field": "Group", "op": "eq", "value": "A"}]
        result = self.evaluate()
        self.assertEqual(result["schema"]["status"], "FAIL")

    def test_unlinked_or_duplicate_checks_rejected(self):
        self.spec["patterns"][0]["check_ids"] = ["MISSING"]
        self.assertTrue(w.spec_errors(self.spec))
        self.spec["patterns"][0]["check_ids"] = ["GAP"]
        self.spec["checks"].append(copy.deepcopy(self.spec["checks"][0]))
        self.assertTrue(w.spec_errors(self.spec))

    def test_incomplete_rubric_not_silently_completed(self):
        self.spec["rubric"]["criteria"] = self.spec["rubric"]["criteria"][:1]
        self.assertTrue(w.spec_errors(self.spec))
        self.spec["rubric"]["complete"] = False
        self.assertFalse(w.spec_errors(self.spec))

    def test_missing_custom_implementation_cannot_pass(self):
        self.spec["checks"][0].update(metric="custom", custom_name="robust_gap")
        result = self.evaluate()
        self.assertEqual(result["checks"][0]["status"], "NOT_RUN")
        self.assertEqual(result["status"], "FAIL")

    def test_custom_cannot_inflate_support(self):
        self.spec["checks"][0].update(metric="custom", custom_name="robust_gap")
        custom = self.root / "custom.py"
        custom.write_text('def measure(*args):\n    return {"value": 100, "usable_n": 999, "usable_compare_n": 2}\n')
        result = self.evaluate(custom)
        self.assertEqual(result["status"], "FAIL")

    def test_timezone_comparisons_use_instants(self):
        row = {"When": w.convert("2025-01-01T01:00:00+02:00", "datetime")}
        self.assertTrue(w.matches(row, [{"field": "When", "op": "lt", "value": "2025-01-01T00:00:00+00:00"}]))

    def test_month_and_weekday_filters(self):
        row = {"When": w.convert("2025-06-02", "date")}
        self.assertTrue(w.matches(row, [{"field": "When", "part": "month", "op": "eq", "value": 6}, {"field": "When", "part": "weekday", "op": "eq", "value": 0}]))

    def test_optional_failure_remains_visible(self):
        extra = copy.deepcopy(self.spec["checks"][0])
        extra.update(id="OPTIONAL", required=False, acceptance={"op": "ge", "value": 999})
        self.spec["checks"].append(extra)
        result = self.evaluate()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"][1]["status"], "FAIL")

    def test_package_tamper_and_extra_student_answer_detected(self):
        (self.root / "student").mkdir()
        file = self.root / "student/data.csv"
        file.write_text("x\n1\n")
        w.write_json(self.root / "manifest.json", {"files": {"student/data.csv": w.digest(file)}, "instructional_acceptance": "pending"})
        self.assertEqual(w.verify_package(self.root)["status"], "PASS")
        file.write_text("x\n2\n")
        self.assertEqual(w.verify_package(self.root)["status"], "FAIL")
        file.write_text("x\n1\n")
        (self.root / "student/answers.md").write_text("Hidden answers")
        self.assertEqual(w.verify_package(self.root)["status"], "FAIL")

    def test_cli_failure_returns_nonzero(self):
        self.spec["checks"][0]["acceptance"]["value"] = 999
        self.evaluate()
        run = subprocess.run([sys.executable, str(MODULE), "validate", "--spec", str(self.root / "spec.json"), "--data", str(self.root / "data.csv"), "--report", str(self.root / "cli_result.json")], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(w.read_json(self.root / "cli_result.json")["status"], "FAIL")

    def test_failed_generator_retained_and_destination_not_overwritten(self):
        w.write_json(self.root / "specification.json", self.spec)
        (self.root / "generate.py").write_text('import sys\nprint("Intentional failing fixture")\nsys.exit(9)\n')
        output = self.root / "run"
        result = w.build(self.root, output, 101, no_charts=True)
        self.assertEqual(result["technical_status"], "FAIL")
        self.assertIn("Intentional failing fixture", (output / "reproducibility/generation_log.txt").read_text())
        original_hash = w.digest(output / "manifest.json")
        with self.assertRaises(FileExistsError):
            w.build(self.root, output, 101, no_charts=True)
        self.assertEqual(w.digest(output / "manifest.json"), original_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
