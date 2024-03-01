import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
import subprocess
from influxdb_client.client.write_api import SYNCHRONOUS
import re
from datetime import datetime, timedelta
import pandas as pd

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip()

def get_cpu_usage():
    command = "top -l 1 | grep 'CPU usage'"
    result = run_command(command)
    user_usage = re.search(r'(\d+\.\d+)% user', result, timeout=0.5)
    return float(user_usage.group(1)) if user_usage else None  # Convert to float

def get_ram_usage():
    command = "vm_stat"
    result = run_command(command)
    free_memory_pages = re.search(r'Pages free:\s+(\d+)', result)
    free_memory_pages = int(free_memory_pages.group(1)) if free_memory_pages else 0
    return (free_memory_pages / (1000))  # Convert pages to GB and return as float

def get_battery_status():
    command = "pmset -g batt"
    result = run_command(command)
    battery_percentage = re.search(r'(\d+)%', result)
    return float(battery_percentage.group(1)) if battery_percentage else None  # Convert to float

def send_metrics():
    while True:  # Infinite loop to continuously send data
        cpu_usage = get_cpu_usage()
        ram_usage = get_ram_usage()
        battery_status = get_battery_status()

        point = Point("system_metrics").tag("host", "local")
        if cpu_usage is not None:
            point = point.field("cpu_usage", cpu_usage)
        if ram_usage is not None:
            point = point.field("ram_usage", ram_usage)
        if battery_status is not None:
            point = point.field("battery_status", battery_status)

        write_api.write(bucket=bucket, org=org, record=point, write_precision=WritePrecision.NS)
        print("Metrics pushed to InfluxDB successfully.")

        time.sleep(5)
        
token = os.environ.get("INFLUXDB_TOKEN")
org = "dev"
bucket = "PC"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient(url=host, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)  
query_api = client.query_api()

if __name__ == "__main__":
    print(token)
    send_metrics()

