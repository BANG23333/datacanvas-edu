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
    channel = rng.choice(["Email", "Social", "Search"])
    segment = rng.choice(["New", "Existing"])
    probability = p["email_existing_probability"] if channel == "Email" and segment == "Existing" else (p["email_new_probability"] if channel == "Email" else p["other_probability"])
    converted = rng.random() < probability
    rows.append(dict(ContactID=f"C{i:06d}", Channel=channel, Segment=segment, Converted=converted, ContactCost=round(max(.01, rng.gauss(p["cost_means"][channel], p["cost_sd"])), 2), PurchaseValue=round(rng.uniform(25, 130), 2) if converted else 0))

with open(args.output, "w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=[c["name"] for c in spec["columns"]])
    writer.writeheader()
    writer.writerows(rows)
