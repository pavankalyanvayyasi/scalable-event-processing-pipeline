# Scalable Event Processing Pipeline

## Project Overview

The Scalable Event Processing Pipeline is a Python and Apache PySpark-based data engineering project that generates, processes, validates, and analyzes event data using AWS S3 for cloud storage.

The project simulates real-world event processing by generating user activities such as purchases, logins, signups, and page views. It processes the events using PySpark, calculates revenue analytics, validates the results, and stores the output files in Amazon S3.

## Architecture

```text
Python Event Generator
        |
        v
AWS S3 - Input Storage
        |
        v
Python / Boto3 Download
        |
        v
Apache PySpark Processing
        |
        v
Event Categorization
        |
        v
Revenue Analytics
        |
        v
Processed JSON + Analytics CSV
        |
        v
Data Validation
        |
        v
AWS S3 - Output Storage
```

## Technologies Used

- Python
- Apache PySpark
- AWS S3
- AWS IAM
- Boto3
- SQL
- JSON / JSONL
- CSV
- Pandas

## Project Features

- Generates 100 sample user events using Python.
- Creates unique event IDs using UUID.
- Stores generated events in JSON Lines format.
- Uploads raw event data to Amazon S3.
- Downloads event data from S3 using Boto3.
- Processes events using Apache PySpark.
- Categorizes Purchase events as Revenue.
- Categorizes Login, Signup, and View events as Non-Revenue.
- Calculates total events and revenue.
- Generates event category analytics.
- Saves processed events as JSONL.
- Exports analytics as CSV.
- Validates processed data and analytics.
- Uploads processed results to AWS S3.
- Executes all stages through a master pipeline script.

## Project Structure

```text
Scalable-Event-Processing-Pipeline/
|
|-- config/
|   |-- aws_config.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- output/
|
|-- logs/
|
|-- sql/
|
|-- src/
|   |-- generate_events.py
|   |-- process_events.py
|   |-- upload_results.py
|   |-- validate_data.py
|   |-- run_pipeline.py
|
|-- tests/
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## Prerequisites

- Python 3.14
- Java compatible with your installed PySpark version
- Apache Spark / PySpark
- AWS account
- AWS CLI
- Amazon S3 bucket
- IAM user or role with appropriate S3 permissions

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Scalable-Event-Processing-Pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## AWS Configuration

Configure AWS CLI with credentials for an IAM identity that has the required S3 permissions:

```bash
aws configure
```

Configure the following values:

- AWS Access Key ID
- AWS Secret Access Key
- Default region: `eu-north-1`
- Output format: `json`

Never commit AWS credentials or secret keys to GitHub.

Update the S3 bucket name and AWS region in `config/aws_config.py` if using a different AWS account or bucket.

## Run the Project

Execute the complete pipeline:

```bash
python src/run_pipeline.py
```

The master script automatically performs:

1. Event generation.
2. Raw event upload to AWS S3.
3. Event download from S3.
4. PySpark processing.
5. Revenue analytics.
6. Processed data generation.
7. Data validation.
8. Processed output upload to S3.

## Output Files

Local processed events:

```text
data/processed/events.jsonl
```

Local analytics:

```text
data/output/event_analytics.csv
```

AWS S3 output locations:

```text
output/processed/events.jsonl
output/analytics/event_analytics.csv
```

## Sample Analytics

Example output from one execution:

| Event Category | Total Events | Total Amount |
|---|---:|---:|
| Revenue | 24 | 651314 |
| Non-Revenue | 76 | 0 |

Total events: 100

Total revenue: 651314

Note: Event counts and revenue change between executions because the generator creates random events.

## Data Validation

Run validation separately:

```bash
python src/validate_data.py
```

The validation script checks:

- Required event fields.
- Correct event categorization.
- Event count consistency.
- Revenue calculation consistency.
- CSV analytics against processed JSON data.

## Future Enhancements

- Apache Kafka integration for real-time event ingestion.
- Apache Airflow for workflow orchestration.
- AWS Glue for managed ETL processing.
- Amazon CloudWatch for monitoring.
- Automated unit and integration testing.
- CI/CD integration using GitHub Actions.
