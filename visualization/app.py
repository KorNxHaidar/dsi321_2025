import os
import pandas as pd
import streamlit as st
import pyarrow.parquet as pq
import s3fs

# ตั้งค่าการเชื่อมต่อกับ LakeFS
lakefs_endpoint = os.getenv("LAKEFS_ENDPOINT", "http://lakefs-dev:8000")
ACCESS_KEY = os.getenv("LAKEFS_ACCESS_KEY")
SECRET_KEY = os.getenv("LAKEFS_SECRET_KEY")

# ตั้งค่า S3FileSystem เพื่อเข้าถึง LakeFS
fs = s3fs.S3FileSystem(
    key=ACCESS_KEY,
    secret=SECRET_KEY,
    client_kwargs={'endpoint_url': lakefs_endpoint}
)

# ตำแหน่งไฟล์ Parquet ใน LakeFS
lakefs_s3_path = 's3a://air-quality/main/airquality.parquet/year=2025/month=5/day=4/hour=2/7400decd6afd4d1caa00b19993ed2e7a-0.parquet'

@st.cache_data
def load_data():
    # โหลดไฟล์ Parquet จาก LakeFS
    parquet_file = pq.ParquetFile(fs.open(lakefs_s3_path))
    df = parquet_file.read().to_pandas()
    return df

st.title("Air Quality Dashboard from LakeFS")
df = load_data()
st.write(df.head())
