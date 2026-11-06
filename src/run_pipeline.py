
import os
import sys
import subprocess

# Find project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Scripts to execute in pipeline order
pipeline_steps = [
    ("Generate Events", "src/generate_events.py"),
    ("Process Events with PySpark", "src/process_events.py"),
    ("Validate Processed Data", "src/validate_data.py"),
    ("Upload Results to S3", "src/upload_results.py")
]

print("\n========== EVENT PROCESSING PIPELINE ==========\n")

try:
    for step_name, script_path in pipeline_steps:

        print(f"\n========== {step_name} ==========\n")

        subprocess.run(
            [sys.executable, script_path],
            cwd=PROJECT_ROOT,
            check=True
        )

        print(f"\n{step_name} completed successfully!")

    print("\n==============================================")
    print("COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
    print("==============================================")

except subprocess.CalledProcessError as error:
    print("\nPIPELINE FAILED!")
    print("Failed script:", error.cmd)
    sys.exit(error.returncode)
