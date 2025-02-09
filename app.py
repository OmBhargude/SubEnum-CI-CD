from flask import Flask, request, render_template, jsonify
import subprocess
import re
import os # Import the os module

app = Flask(__name__)

DEBUG_PRINT = True   # Set to False to disable debug prints
PORT = int(os.environ.get('PORT', 5000)) # Get PORT from environment variable, default to 5000

def debug_print(message):
    if DEBUG_PRINT:
        print(message)

# --- Health Check Endpoint - ADDED ---
@app.route('/health')
def health_check():
    return "OK", 200
# --- End Health Check Endpoint ---

@app.route("/", methods=["GET"])
def index():
    results = None
    error = None
    domain = None

    debug_print("Request received")

    if "domain" in request.args:
        domain = request.args.get("domain")
        debug_print(f"Domain received: {domain}")

        if not domain:
            error = "Please enter a domain."
        elif "." not in domain:
            error = "Invalid domain format."
        else:
            try:
                debug_print("About to call run_subfinder_locally")
                results = run_subfinder_locally(domain)
                debug_print(f"Results from run_subfinder_locally: {results}")

                best_type = request.accept_mimetypes.best_match(['application/json', 'text/html'])

                if best_type == 'application/json':
                    debug_print("Returning JSON")
                    return jsonify(results), 200
                elif best_type == 'text/html':
                    debug_print("Returning HTML")
                    return render_template("index.html", results=results, error=error, domain=domain), 200
                else:  # Default to HTML
                    debug_print("Returning HTML (default)")
                    return render_template("index.html", results=results, error=error, domain=domain), 200

            except Exception as e:
                error = f"An error occurred: {str(e)}"
                debug_print(f"Error: {error}")
                best_type = request.accept_mimetypes.best_match(['application/json', 'text/html'])
                if best_type == 'application/json':
                    return jsonify({"error": error}), 500
                elif best_type == 'text/html':
                    return render_template("index.html", error=error, domain=domain), 500
                else:
                    return
