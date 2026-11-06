
import boto3

# AWS configuration
AWS_REGION = "eu-north-1"

# S3 bucket name
S3_BUCKET_NAME = "pyspark-event-pipeline-661491975302-eu-north-1-an"

# Create S3 client using your existing AWS credentials
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)

print("AWS S3 configuration loaded successfully!")
