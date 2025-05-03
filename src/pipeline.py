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
        response = requests.get(url=base_url + path)
        response.raise_for_status()
        AQI_stats = response.json()
        data = AQI_stats['stations']
        #logger.info(AQI_stats)
        num_records = len(data)
        num_columns = len(next(iter(data), {}))

        logger.info(f"Data contains {num_records} records and {num_columns} columns.")
        logger.info(f"Successfully fetched data from {base_url + path}")

        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None
    except KeyError as e:
        logger.error(f"Error processing data: Missing key {e}")
        return None


@task
def data_processing(data:list[dict]) -> pd.DataFrame:
    """
    Process data, convert data types, minor cleaning, and keep necessary columns.
    """
    logger = get_run_logger()
    df = pd.DataFrame(data)

    # Normalize AQILast with prefix to avoid column name conflict
    expanded_aqi = pd.json_normalize(df['AQILast'])
    df = pd.concat([df, expanded_aqi], axis=1)
    df['time'] = df['time'].mode()[0]
    df['date'] = df['date'].mode()[0]
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    # Extract datetime components
    df[['year', 'month', 'day', 'hour']] = df['timestamp'].apply(
        lambda ts: pd.Series([ts.year, ts.month, ts.day, ts.hour])
    )

    # Convert numeric columns
    df[['PM25.color_id', 'PM25.aqi']] = df[['PM25.color_id', 'PM25.aqi']].astype(int)

    # Select columns
    df = df[[
        'timestamp', 'year', 'month', 'day', 'hour',
        'stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN',
        'stationType', 'lat', 'long', 'PM25.color_id', 'PM25.aqi'
        ]]
    
    logger.info(f"Data processed, resulting DataFrame shape: {df.shape}")
    return df


@task
def load_to_lakefs(df: pd.DataFrame, lakefs_s3_path: str, storage_options: dict):
    """
    Load data into lakeFS storage in S3 (Amazon Simple Storage Service) and in a parquet format.
    Partitions the parquet file based on 'year', 'month', 'day' and 'hour'.

    Parameters: 
    df: Target DataFrame that will be loaded into the storage.
    lakefs_s3_path: S3-Supported API Gateway, layer in lakeFS responsible for the compatibility with S3.
    storage_options: configured options for accessing lakeFS storage.

    Returns:
    None
    """
    logger = get_run_logger()
    
    try:
        df.to_parquet(
            lakefs_s3_path,
            storage_options=storage_options,
            partition_cols=['year', 'month', 'day', 'hour'],
        )
        logger.info(f"✅ Data successfully loaded to: {lakefs_s3_path}")
    except Exception as e:
        logger.error(f"Error loading data to lakeFS: {e}")

@flow(name='main-flow', log_prints=True)
def main_flow(
    base_url: str="http://air4thai.pcd.go.th",
    path: str="/services/getNewAQI_JSON.php"
):
    # Task 1: Fetch data from the API
    data = retrieve_from_api(
        base_url,
        path
    )

    # Task 2: Data Process
    df = data_processing(data)

    # lakeFS setup
    ACCESS_KEY = "access_key"
    SECRET_KEY = "secret_key"
    lakefs_endpoint = "http://lakefs-dev:8000/"
    repo = "air-quality"
    branch = "main"
    file_path = "airquality.parquet"
    lakefs_s3_path = f"s3a://{repo}/{branch}/{file_path}"

    storage_options = {
        "key": ACCESS_KEY,
        "secret": SECRET_KEY,
        "client_kwargs": {
            "endpoint_url": lakefs_endpoint
        }
    }

    # Task 3: Load data into lakeFS storage in a parquet format
    load_to_lakefs(df, lakefs_s3_path, storage_options)

# def main():
#     main_flow.serve("air4thai-collection-deployment")

# if __name__ == "__main__":
#     main()