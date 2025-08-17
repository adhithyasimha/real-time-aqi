import json
import urllib.request
import boto3
import csv
from io import StringIO
from datetime import datetime

s3 = boto3.client("s3")
BUCKET_NAME = "raw-aqi-api-data"

def lambda_handler(event, context):
    url = "https://api.waqi.info/map/bounds/"
    params = {
        "token": "7f8f5c70d3f644cf863339a5ae48e56e3f1efec5",
        "latlng": "-90,-180,90,180"
    }

    
    full_url = f"{url}?{'&'.join([f'{k}={v}' for k,v in params.items()])}"

    # Fetch data
    with urllib.request.urlopen(full_url) as response:
        data = json.loads(response.read())

    
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write header
    writer.writerow([
        "lat", "lon", "uid", "aqi", "station_name", "time"
    ])

    for entry in data.get("data", []):
        station_info = entry.get("station", {})
        writer.writerow([
            entry.get("lat"),
            entry.get("lon"),
            entry.get("uid"),
            entry.get("aqi"),
            station_info.get("name", ""),
            station_info.get("time", "")
        ])


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"aqi_data_{timestamp}.csv"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Raw CSV saved to S3 as {file_name}"})
    }
