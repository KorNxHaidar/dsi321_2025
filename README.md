# Automate Data Pipelines for Real-Time Analytics using Prefect.io

![Create at](https://img.shields.io/github/created-at/KorNxHaidar/dsi321_2025)
![GitHub last commit](https://img.shields.io/github/last-commit/KorNxHaidar/dsi321_2025)
![GitHub License](https://img.shields.io/github/license/KorNxHaidar/dsi321_2025)

### 📌 Project Overview
This project is part of the <b>DSI321: BIG DATA INFRASTRUCTURE</b> course.The objective is to design and implement automated data pipelines using Prefect.io for real-time analytics. The system is containerized with Docker and supports visualizing data insights with Python libraries.

### 🧾 Introduction 
In recent years, air pollution—especially fine particulate matter (PM2.5)—has become a critical environmental issue in Thailand <img src="https://flagcdn.com/w40/th.png" alt="Thailand Flag" width="16" height="12"> . Accurate and timely monitoring of air quality is essential for public awareness, health decision-making, and long-term policy planning. To support this need, this project focuses on building an automated data pipeline that continuously collects, processes, and analyzes air quality data in near real-time.
<br>
<br>
The pipeline utilizes the <a href=https://envilink.go.th/dataset/air-quality-pm2point5/resource/156ca885-4f38-4c58-8745-397552105c1e><b>Air Quality API</b></a>, which provides hourly average PM2.5 concentration data from automatic air quality monitoring stations operated by the <b>Air4Thai</b> network across the country. This API is officially maintained by the <b>Pollution Control Department of Thailand</b>, offering reliable access to high-quality environmental data.
<br>
<br>
By leveraging <a href=https://www.prefect.io><b> Prefect.io</b></a> for workflow orchestration and <a href=https://www.docker.com><b>Docker</b></a> for containerization, this project ensures scalability, reproducibility, and seamless automation.
<br>
<br>
To make insights more accessible and interactive, the processed data is visualized through a user-friendly web dashboard built with Streamlit. The dashboard allows users to explore real-time PM2.5 levels across various regions in Thailand, view historical trends, and better understand the country’s air quality through an intuitive web interface.


### 🚀 Getting Started
To run it locally:

   ```bash
   $ git clone <this-repo-url>

   $ cd <this-repo-folder>

   $ docker compose up -d --build
   ```    