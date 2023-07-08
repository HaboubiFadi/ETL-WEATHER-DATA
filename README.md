# ETL-WEATHER-DATA
Automation Data Pipeline for Weather Data Analysis

This project implements an automated data pipeline for gathering, processing, and analyzing weather data using Python, Apache Airflow, PostgreSQL database,SQL, SQLAlchemy ORM . The pipeline fetches weather data from external API ([Weather Api] (https://www.weatherapi.com/)),
performs data preprocessing and cleaning,and stores the processed data in a PostgreSQL database. The data is then transformed and analyzed using various statistical and machine learning techniques.
The project leverages Apache Airflow to schedule and execute the pipeline tasks, ensuring efficient data ingestion, processing, and storage.

Key Features:

# Data ingestion: 
Fetches weather data from external API , such as OpenWeatherMap, using Python requests library.
# Data preprocessing:
Cleans and transforms the raw weather data,handle missing and duplicated data 
# Database integration: 
Utilizes a PostgreSQL database for storing the processed weather data, leveraging the SQLAlchemy ORM for efficient data management.
# Apache Airflow integration:
Set up an Apache Airflow DAG to schedule and automate the pipeline tasks.
# Data analysis: (still working on)
Performs exploratory data analysis, statistical analysis, and potentially applies machine learning algorithms to extract insights from the weather data.
# Visualization: (still working on)
Generates visualizations, such as plots and charts, to present the analyzed weather data and trends.

This is my first project in the data engineering domain , and it aims to provide a scalable and automated solution for weather data analysis, enabling users to easily retrieve, process, and analyze weather information for various purposes, such as forecasting, research.



ScreenShots presentation :

These are the DAGs :


![dag_img](https://github.com/HaboubiFadi/ETL-WEATHER-DATA/assets/138848259/7755c153-33cb-4306-8a6b-3baceb26fff9)


1) First we start with initiating the database with hisorical_day data and Forecast_day data (@scheduled only once ):
  



![init_database](https://github.com/HaboubiFadi/ETL-WEATHER-DATA/assets/138848259/ca7ad863-56cd-4fe9-9224-c13992a408a1)

   

2) Lunch the historical_day and forecast_day data update (@scheduled daily):



![update_forc_hist](https://github.com/HaboubiFadi/ETL-WEATHER-DATA/assets/138848259/e2fe8de5-180a-4e72-9197-fafd96095e06)




3) Lunch the current data extracting and database update (@scheduled every 20 minutes):




![current](https://github.com/HaboubiFadi/ETL-WEATHER-DATA/assets/138848259/d1acdba9-7fa3-413a-8963-4e0ac5835972)




4) A screenshot of the database:



![Screenshot from 2023-07-08 09-34-40](https://github.com/HaboubiFadi/ETL-WEATHER-DATA/assets/138848259/1b0e026f-c7a9-49c0-94dc-bed674531217)



