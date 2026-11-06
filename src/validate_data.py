
import os
import json
import csv

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

processed_file = os.path.join(
    PROJECT_ROOT, "data", "processed", "events.jsonl"
)

analytics_file = os.path.join(
    PROJECT_ROOT, "data", "output", "event_analytics.csv"
)

# Check whether files exist
if not os.path.exists(processed_file):
    raise FileNotFoundError("Processed events file not found!")

if not os.path.exists(analytics_file):
    raise FileNotFoundError("Analytics CSV file not found!")

# Read processed events
events = []

with open(processed_file, "r", encoding="utf-8") as file:
    for line in file:
        events.append(json.loads(line))

required_fields = [
    "event_id",
    "user_id",
    "event_type",
    "amount",
    "timestamp",
    "event_category"
]

# Validate required fields and categories
for event in events:
    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing field: {field}")

    expected_category = (
        "Revenue"
        if event["event_type"].strip().upper() == "PURCHASE"
        else "Non-Revenue"
    )

    if event["event_category"] != expected_category:
        raise ValueError(
            f"Incorrect category for event {event['event_id']}"
        )

# Calculate expected analytics
expected = {
    "Revenue": {"total_events": 0, "total_amount": 0},
    "Non-Revenue": {"total_events": 0, "total_amount": 0}
}

for event in events:
    category = event["event_category"]
    expected[category]["total_events"] += 1
    expected[category]["total_amount"] += event["amount"]

# Read CSV analytics
actual = {}

with open(analytics_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        actual[row["event_category"]] = {
            "total_events": int(row["total_events"]),
            "total_amount": int(row["total_amount"])
        }

# Compare results
if len(events) != sum(
    values["total_events"] for values in actual.values()
):
    raise ValueError("Event count does not match analytics CSV!")

if actual != expected:
    raise ValueError("Analytics CSV does not match processed events!")

print("All data validation checks passed!")
print("Total events:", len(events))
print("Revenue events:", expected["Revenue"]["total_events"])
print("Non-Revenue events:", expected["Non-Revenue"]["total_events"])
print("Total revenue:", expected["Revenue"]["total_amount"])
print("Data validation completed successfully!")
