# InfluxDB-v1-Speedtest-Logger

This script runs a speedtest-cli test, parses the JSON output, and writes the results (download speed, upload speed, ping, IP) to an InfluxDB v1 database. It includes error handling for HTTP 403 errors and retries on other failures.

## Configuration Variables
- `NAMESPACE`: Optional namespace for InfluxDB (default: 'None')
- `DB_ADDRESS`: InfluxDB server IP
- `DB_PORT`: InfluxDB port (default: 8086)
- `DB_USER`: InfluxDB username
- `DB_PASSWORD`: InfluxDB password
- `DB_DATABASE`: Target database name
- `DB_TAGS`: Optional tags for InfluxDB (default: None)
- `TEST_FAIL_INTERVAL`: Retry interval in seconds (default: 300)
- `SERVER_ID`: Optional specific server ID for speedtest

## Usage
1. Edit configuration variables at the top of the script
2. Install requirements: `pip install influxdb speedtest-cli`
3. Run manually: `python3 Run-SpeedTestToInfluxdb.py`
4. Set up cron job (example):
   ```
   */5 * * * * /usr/bin/python3 /path/to/Run-SpeedTestToInfluxdb.py
