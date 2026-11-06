import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import random
import uuid
import os
from datetime import datetime, timezone

from config.aws_config import s3_client, S3_BUCKET_NAME

# Create local output directory
os.makedirs("data/raw", exist_ok=True)

# Event types
event_types = ["Purchase", "Login", "Signup", "View"]

# Generate 100 sample events
events = []

for _ in range(100):
    event_type = random.choice(event_types)

    amount = random.randint(100, 50000) if event_type == "Purchase" else 0

    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1001, 1100),
        "event_type": event_type,
        "amount": amount,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    events.append(event)

# Save events as JSON Lines
local_file = "data/raw/events.jsonl"

with open(local_file, "w", encoding="utf-8") as file:
    for event in events:
        file.write(json.dumps(event) + "\n")

print(f"Generated {len(events)} events successfully!")

# Upload events to S3
s3_key = "input/events.jsonl"

s3_client.upload_file(
    local_file,
    S3_BUCKET_NAME,
    s3_key
)

print(f"Uploaded successfully to S3: {s3_key}")
