from prefect import flow
from pathlib import Path

source = str(Path.cwd())
entrypoint = f"pipeline.py:main_flow"
print(f'entrypoint:{entrypoint}, source:{source}')

if __name__ == "__main__":
    flow.from_source(
        source=source,
        entrypoint=entrypoint,
    ).deploy(
        name="air4thai_pipeline_deployment",
        work_pool_name="default-agent-pool",
        cron="40 * * * *", # Runs at the start of the hour (minute 40).
    )
