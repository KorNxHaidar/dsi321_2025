from prefect import flow, get_run_logger
from pathlib import Path

source = str(Path.cwd())
entrypoint = "pipeline.py:main_flow"

logger = get_run_logger
logger.info(f'entrypoint:{entrypoint}, source:{source}')

if __name__ == "__main__":
    flow.from_source(
        source=source,
        entrypoint=entrypoint,
    ).deploy(
        name="air4thai_pipeline_deployment",
        work_pool_name="default-agent-pool",
        cron="*30 * * * *", # Runs at the start of the hour (minute 30).
    )
