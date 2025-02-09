import logging
import os
import subprocess
import re
from flask import Flask, request, render_template, jsonify
from prometheus_client import Counter, Histogram, Gauge, start_http_server

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

SUBFINDER_PATH = os.environ.get("SUBFINDER_PATH", "./subfinder")

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latency of HTTP requests')
SUBFINDER_REQUEST_COUNT = Counter('subfinder_requests_total', 'Total number of Subfinder requests')
SUBFINDER_ERROR_COUNT = Counter('subfinder_errors_total', 'Total number of Subfinder errors')



@app.route("/", methods=["GET"])
def index():
    REQUEST_COUNT.inc()  # Increment request count
    with REQUEST_LATENCY.time():  # Measure request latency
        results = None
        error = None
        domain = None

        # ... (rest of your route code - no changes needed here)

def run_subfinder_locally(domain):
    SUBFINDER_REQUEST_COUNT.inc()
    try:
        command = [SUBFINDER_PATH, "-d", domain, "-silent"]
        logging.debug(f"Running command: {command}")
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)  # Timeout added
        # ... (rest of your subprocess handling)
    except subprocess.CalledProcessError as e:
        SUBFINDER_ERROR_COUNT.inc()
        error_message = f"Subfinder error: {e.stderr.decode()}"
        logging.error(error_message)
        return {"error": error_message}
    except FileNotFoundError:
        SUBFINDER_ERROR_COUNT.inc()
        logging.error("Subfinder not found")
        return {"error": "subfinder not found. Install it or provide the correct path."}
    except Exception as e:  # Catch any other exceptions
        SUBFINDER_ERROR_COUNT.inc()
        logging.exception("Exception in run_subfinder_locally")  # Log the full traceback
        return {"error": str(e)}

if __name__ == "__main__":
    start_http_server(8000)  # This line was missing the if __name__ == "__main__": block
    app.run(debug=False, host='0.0.0.0', port=5000)  # Flask app runs on port 5000
