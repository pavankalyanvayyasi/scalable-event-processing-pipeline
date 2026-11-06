
import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from config.aws_config import s3_client, S3_BUCKET_NAME

# Files to upload and their S3 destinations
files_to_upload = {
    "data/processed/events.jsonl": "output/processed/events.jsonl",
    "data/output/event_analytics.csv": "output/analytics/event_analytics.csv"
}

# Upload files
for local_file, s3_key in files_to_upload.items():

    if not os.path.exists(local_file):
        print(f"File not found: {local_file}")
        continue

    s3_client.upload_file(
        local_file,
        S3_BUCKET_NAME,
        s3_key
    )

    print(f"Uploaded successfully: {s3_key}")

print("All available output files uploaded to S3!")
