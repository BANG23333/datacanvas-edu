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
    property_type = rng.choice(["City", "Resort"])
    channel = rng.choice(["Direct", "OTA"])
    lead = rng.randint(0, 180)
    arrival = date(2025, 1, 1) + timedelta(days=rng.randrange(365))
    cancelled = rng.random() < (p["ota_long_cancel"] if channel == "OTA" and lead > 60 else p["other_cancel"])
    rate = p["base_rate"] + rng.gauss(0, p["rate_sd"])
    if property_type == "Resort" and arrival.month in [6, 7, 8]:
        rate += p["resort_summer_premium"]
    if property_type == "City" and arrival.weekday() < 5:
        rate += p["city_weekday_premium"]
    rows.append(dict(BookingID=f"B{i:06d}", PropertyType=property_type, BookingChannel=channel, LeadDays=lead, ArrivalDate=arrival.isoformat(), QuotedRate=round(max(20, rate), 2), Cancelled=cancelled))

with open(args.output, "w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=[c["name"] for c in spec["columns"]])
    writer.writeheader()
    writer.writerows(rows)
