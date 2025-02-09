from flask import Flask, request, render_template, jsonify

import subprocess

import re



app = Flask(__name__)



DEBUG_PRINT = True  # Set to False to disable debug prints



def debug_print(message):

    if DEBUG_PRINT:

        print(message)



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

                else:  # Default to HTML

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

                    return render_template("index.html", error=error, domain=domain), 500



    debug_print("Returning initial HTML")

    return render_template("index.html", results=results, error=error, domain=domain)





def run_subfinder_locally(domain):

    try:

        command = ["./subfinder", "-d", domain, "-silent"]  # Or adjust as needed

        debug_print(f"Running command: {command}")

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        stdout = result.stdout.strip()

        stderr = result.stderr.strip()



        if stderr:

            debug_print(f"Subprocess stderr: {stderr}")



        ansi_escape = re.compile(r'\x1b\[[0-9;]*[mG]')

        cleaned_stdout = ansi_escape.sub('', stdout)



        subdomains = cleaned_stdout.splitlines()



        # Remove the first line (AS number info) if it exists (usually not needed for subfinder)

        # if subdomains and subdomains[0].startswith("AS"):  # Commented out, as subfinder usually doesn't have this

        #     subdomains = subdomains[1:]



        debug_print(f"Subdomains: {subdomains}")

        return {"subdomains": subdomains}

    except subprocess.CalledProcessError as e:

        debug_print(f"CalledProcessError: {e}")

        return {"error": str(e)}

    except FileNotFoundError:

        debug_print("FileNotFoundError: subfinder not found")

        return {"error": "subfinder not found. Install it or provide the correct path."}

    except Exception as e:  # Catch any other exceptions

        debug_print(f"Exception in run_subfinder_locally: {e}")

        return {"error": str(e)}





if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0')  # Important: Add host='0.0.0.0'
