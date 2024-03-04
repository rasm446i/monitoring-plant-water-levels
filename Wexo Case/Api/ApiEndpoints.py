import prometheus_client as prom
from flask import Flask, request, jsonify, Response
import requests
from datetime import date, timedelta, datetime
from flask_cors import CORS
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from ControllerLayer import Controller
import numpy as np
from scipy import stats

# alle terminal commands man skal run
# pip install sqlalchemy
# pip install pyodbc
# pip install flask-cors
# pip install prometheus_client
# flask run --host=0.0.0.0
# $env:FLASK_APP = "ApiEndpoints.py"

app = Flask(__name__)
CORS(app)
ctrl = Controller
moisture_gauge = Gauge('moisture_level_metric', 'Moisture level from microcontroller', ['microcontroller_id'])


# This endpoint validates the incoming JSON data and stores it locally for prometheus to collect
@app.route('/api', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        mc_id = data.get('microcontrollerid')
        moisture_level = data.get('moisturelevel')

        if mc_id is not None and moisture_level is not None:
            # Update Prometheus Gauge with the received data
            moisture_gauge.labels(microcontroller_id=mc_id).set(moisture_level)
            return "Data Received and Metric Updated", 200
        else:
            return "Invalid JSON Data", 400

    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500


# This is the endpoint that prometheus uses to collect data from the API
@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# This endpoint retrieves soil moisture data hourly from the prometheus database
@app.route('/get_soil_moisture_hourly')
def get_soil_moisture_hourly():
    prometheus_server = 'localhost:9090'  # IP and port of the Prometheus server
    soil_moisture_query = 'moisture_level_metric'  # Metric name to query

    # Set start and end times for the past hour
    query_end_date = datetime.now()
    query_start_date = query_end_date - timedelta(hours=1)

    # Convert times to UNIX timestamps
    start_timestamp = int(query_start_date.timestamp())
    end_timestamp = int(query_end_date.timestamp())
    data_interval = '1m'  # Step size for data

    # URL for the Prometheus query
    query_url = f"http://{prometheus_server}/api/v1/query_range"
    query_parameters = {
        'query': soil_moisture_query,
        'start': start_timestamp,
        'end': end_timestamp,
        'step': data_interval
    }

    try:
        # Send a GET request to Prometheus
        prometheus_response = requests.get(query_url, params=query_parameters)

        # For debugging Purposes
        print(prometheus_response.text)

        # Make sure the status code is 200
        if prometheus_response.status_code == 200:
            response_data = prometheus_response.json()

            # Dictionary to store the latest moisture reading for each microcontroller
            latest_readings = []

            # Extract microcontroller IDs and moisture values from the response
            for metric_result in response_data['data']['result']:
                mc_id = metric_result['metric'].get('microcontroller_id', 'unknown')

                # Extract moisture value
                timestamp, moisture_value = metric_result['values'][-1]

                # Convert timestamp to readable format
                timestamp = datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

                # Update the latest reading for the microcontroller
                latest_readings.append({
                    'microcontroller_id': mc_id,
                    'moisture_level': float(moisture_value)
                })

            # Return the latest moisture readings along with microcontroller IDs
            return jsonify(latest_readings)

        else:

            return jsonify({
                "error": f"Error response from Prometheus: {prometheus_response.text}"
            }), prometheus_response.status_code


    except requests.exceptions.RequestException as request_error:

        return jsonify({"error": f"Request error: {request_error}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
