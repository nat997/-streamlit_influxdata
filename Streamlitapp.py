import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.express as px
from influxdb_client import InfluxDBClient

# Automatically rerun the app every 5000 milliseconds (5 seconds)
st_autorefresh(interval=5000, key="data_refresh")

# Function to fetch data from InfluxDB
def fetch_data(client, bucket, org, lookback='1h'):
    query_api = client.query_api()
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -{lookback})
      |> filter(fn: (r) => r._measurement == "system_metrics")
    '''
    result = query_api.query(org=org, query=query)

    # Process the results into a DataFrame
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_field(), record.get_value()))

    df = pd.DataFrame(results, columns=['Time', 'Field', 'Value'])
    return df

# Streamlit app setup
st.title('System Metrics in Real-Time')

# InfluxDB configurations
token = os.environ.get("INFLUXDB_TOKEN")
org = "dev"
bucket = "PC"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient(url=host, token=token, org=org)

# Fetch and display data
df = fetch_data(client, bucket, org)

if not df.empty:
    df['Time'] = pd.to_datetime(df['Time'])  # Convert Time from string to datetime
    fig = px.line(df, x='Time', y='Value', color='Field', title='System Metrics Over Time')
    st.plotly_chart(fig)
else:
    st.write("No data available.")
