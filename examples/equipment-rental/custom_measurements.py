"""Case-specific robust measurement, independent of generation code."""
from statistics import median

def measure(name, target_rows, comparator_rows, check):
    if name != "median_turnaround_difference":
        raise ValueError("Unknown custom measurement")
    target = [r["TurnaroundHours"] for r in target_rows if r["TurnaroundHours"] is not None]
    comparator = [r["TurnaroundHours"] for r in comparator_rows if r["TurnaroundHours"] is not None]
    return {"value": median(target) - median(comparator) if target and comparator else None,
            "usable_n": len(target), "usable_compare_n": len(comparator)}
