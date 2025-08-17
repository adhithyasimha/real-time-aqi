import boto3
import os
import csv
from io import StringIO

s3 = boto3.client("s3")

def parse_station_name(name):
    parts = [p.strip() for p in name.split(",")]
    if len(parts) >= 3:
        country = parts[-1]
        city = parts[-2]
        station = ", ".join(parts[:-2])
    elif len(parts) == 2:
        country = parts[-1]
        city = None
        station = parts[0]
    else:
        country = None
        city = None
        station = name
    return station, city, country

def categorize_aqi(aqi_value):
    try:
        aqi = int(aqi_value)
    except:
        return "Unknown"
    
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read raw CSV from S3
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    csv_content = obj['Body'].read().decode('utf-8')
    reader = csv.DictReader(StringIO(csv_content))
    
    # Prepare processed CSV in memory
    output_buffer = StringIO()
    fieldnames = ["lat", "lon", "uid", "aqi", "aqi_category", "station", "city", "country", "time"]
    writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        station_name = row.get("station_name", "")
        station, city, country = parse_station_name(station_name)
        aqi_category = categorize_aqi(row.get("aqi"))

        writer.writerow({
            "lat": row.get("lat"),
            "lon": row.get("lon"),
            "uid": row.get("uid"),
            "aqi": row.get("aqi"),
            "aqi_category": aqi_category,
            "station": station,
            "city": city,
            "country": country,
            "time": row.get("time")
        })

    # Upload processed CSV to S3
    filename = os.path.basename(key).replace(".csv", "_processed.csv")
    processed_bucket = "processed-aqi-api-data"

    s3.put_object(
        Bucket=processed_bucket,
        Key=filename,
        Body=output_buffer.getvalue(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": f"Processed CSV saved to s3://{processed_bucket}/{filename}"
    }
