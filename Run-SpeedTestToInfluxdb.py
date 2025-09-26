# InfluxDB Settings
NAMESPACE = 'None'
DB_ADDRESS = ''
DB_PORT = ''
DB_USER = ''
DB_PASSWORD = ''
DB_DATABASE = ''
DB_TAGS = None

# Speedtest Settings
# Time before retrying a failed Speedtest (in seconds).
TEST_FAIL_INTERVAL = 300
# Specific server ID
SERVER_ID = ''

import subprocess
import json
import time
import socket
from influxdb import InfluxDBClient

def run_speedtest():
    try:
        # Run speedtest-cli with JSON output
        result = subprocess.run(['speedtest-cli', '--json'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Extract required metrics
        download_speed = data['download']
        upload_speed = data['upload']
        ip_address = data['client']['ip']
        hostname = socket.gethostname()
        server_id = data['server']['id']
        ping = data['ping']
        
        # Prepare InfluxDB data point
        json_body = [
            {
                "measurement": "speedtest_results",
                "tags": {
                    "hostname": hostname,
                    "server_id": server_id
                },
                "fields": {
                    "download_speed": download_speed,
                    "upload_speed": upload_speed,
                    "ping": ping,
                    "ip": ip_address
                }
            }
        ]
        
        # Connect to InfluxDB and write data
        client = InfluxDBClient(
            host=DB_ADDRESS,
            port=DB_PORT,
            username=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        client.write_points(json_body)
        
        print("Speedtest data successfully written to InfluxDB")
    
    except subprocess.CalledProcessError as e:
        # Check for HTTP 403 error specifically
        if "HTTP 403" in e.stderr:
            print("Speedtest failed with HTTP 403 error. Exiting gracefully.")
            return
        print(f"Speedtest failed with error: {e}")
        time.sleep(TEST_FAIL_INTERVAL)
        run_speedtest()  # Retry after interval

if __name__ == "__main__":
    run_speedtest()
