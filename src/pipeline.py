import requests
import pandas as pd
from prefect import flow, task, get_run_logger

@task
def retrieve_from_api(
    base_url: str,
    path: str
):
    try:    
        logger = get_run_logger()
        response = requests.get(url=base_url+path)
        response.raise_for_status()
        AQI_stats = response.json()
        data = AQI_stats['stations']
        logger.info(AQI_stats)

        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except KeyError as e:
        print(f"Error processing data: Missing key {e}")
        return None

@flow
def collect_api_data(
    base_url: str="http://air4thai.pcd.go.th",
    path: str="/services/getNewAQI_JSON.php"
):
    AQI_stats = retrieve_from_api(
        base_url,
        path
    )

def main():
    collect_api_data.serve("air4thai-collection-deployment")

if __name__ == "__main__":
    main()