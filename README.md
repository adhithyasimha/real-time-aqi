# AQI Data Pipeline - Global Air Quality Analytics

A data pipeline that automatically ingests, processes, and visualizes global air quality data from the World Air Quality Index (WAQI) API using AWS services.

## Architecture

<img width="985" height="637" alt="Screenshot 2025-08-17 at 8 43 52 PM" src="https://github.com/user-attachments/assets/ba578f9a-366a-4e24-86bc-84a50a58b59c" />

The pipeline consists of:
- **Data Ingestion**: AWS Lambda function triggered daily via EventBridge
- **Data Processing**: Serverless transformation with categorization and geographic parsing
- **Data Storage**: Raw and processed data stored in separate S3 buckets
- **Data Cataloging**: AWS Glue crawlers for automatic schema discovery
- **Data Analytics**: Amazon Athena for SQL queries
- **Data Visualization**: QuickSight dashboards with geospatial mapping

## Features

- **Automated Daily Data Collection**: Pulls global AQI data from global air quality monitoring stations
- **Data Enrichment**: Categorizes AQI levels (Good, Moderate, Unhealthy, etc.)
- **Geographic Processing**: Parses station locations into country, city, and station name
- **Geospatial Visualization**: Interactive world map showing air quality patterns

## Data Flow

1. **EventBridge** triggers Lambda function daily
2. **API Ingestion Lambda** fetches data from WAQI API and stores raw CSV in S3
3. **S3 Event** triggers transformation Lambda automatically
4. **Transformation Lambda** processes and enriches data, stores in processed S3 bucket
5. **Glue Crawler** catalogs data schema for querying
6. **Athena** enables SQL analytics on processed data
7. **QuickSight** provides interactive dashboards and geospatial visualizations


## Quicksight dashboard 
<img width="1247" height="858" alt="Screenshot 2025-08-17 at 8 41 59 PM" src="https://github.com/user-attachments/assets/fa10d6d9-aef3-4c93-93d6-91a086017069" />
