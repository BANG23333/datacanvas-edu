"""Generate one synthetic teaching case from explicit parameters."""
import argparse
import csv
import json
import random
from datetime import date, timedelta
parser = argparse.ArgumentParser()
parser.add_argument("--spec", required=True)
parser.add_argument("--seed", required=True, type=int)
parser.add_argument("--output", required=True)
args = parser.parse_args()
with open(args.spec) as handle:
    spec = json.load(handle)
rng = random.Random(args.seed)
p = spec["parameters"]
rows = []
for i in range(spec["row_count"]):
    equipment = rng.choice(["PowerTool", "Lift", "Generator"])
    days = rng.randint(1, 30)
    tier = rng.choice(["Basic", "Priority"])
    hours = p["base_hours"] + p["duration_quadratic"] * days ** 2 + rng.gauss(0, p["noise_sd"]) - (p["priority_reduction"] if tier == "Priority" else 0)
    repair = rng.random() < (p["power_tool_repair"] if equipment == "PowerTool" else p["other_repair"])
    rows.append(dict(RentalID=f"R{i:06d}", EquipmentClass=equipment, DaysBooked=days, ServiceTier=tier, TurnaroundHours=round(max(0, hours), 2), RepairNeeded=repair))

with open(args.output, "w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=[c["name"] for c in spec["columns"]])
    writer.writeheader()
    writer.writerows(rows)
