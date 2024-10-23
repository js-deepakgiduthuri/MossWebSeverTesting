from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

def apn_parse(apn):
    """
    Parses the APN string to extract the SIM name and APN value.
    Example format: '[SIM1]=APN1'
    """
    name = apn.split('[')[1].split(']')[0]
    apn_value = apn.split('=')[1]
    return name, apn_value


@app.route('/to_turn_on', methods=['GET'])
def modify_function():
    """
    Flask route that listens for incoming GET requests with sim_name and apn_name.
    Modifies the modem_autoconnect.sh script with the provided SIM and APN.
    """
    # Get the sim_name and apn_name from the request's query string (GET parameters)
    sim_name = request.args.get('sim_name')
    apn_name = request.args.get('apn_name')

    # Ensure both parameters are provided, otherwise return an error
    if not sim_name or not apn_name:
        return jsonify({"error": "Both sim_name and apn_name must be provided."}), 400

    try:
        # Open and read the existing modem_autoconnect.sh script
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        # Extract the dictionary of SIM and APN values from the script
        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {}
        # Populate the existing SIM-APN dictionary
        for apn in apn_dict:
            if '[' in apn:
                name, apn_value = apn_parse(apn)
                sims_list[name] = apn_value

        # Add or update the SIM-APN pair with the provided values
        sims_list[f'"{sim_name}"'] = f'"{apn_name}"'

        # Rebuild the dictionary string to write back to the script
        to_add = ''
        for key, value in sims_list.items():
            if key != f'"{sim_name}"':
                to_add += f'[{key}]={value}\n    '  # Ensure 4 spaces for correct formatting
            else:
                to_add += f'[{key}]={value}'


        # Read the template file (template.sh) and insert the new dictionary content
        with open('template.sh', 'r') as template:
            template_read = template.read()

        # Replace the placeholder in the template with the updated dictionary string
        file2 = template_read.replace('#PLACEHERE', to_add)

        # Write the updated content to the modem_autoconnect.sh file
        with open('/etc/modem_autoconnect.sh', 'w') as after_changes_file:
            after_changes_file.write(file2)

        return jsonify({"message": "The modem_autoconnect.sh file has been successfully modified with the new SIM and APN."}), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5010, host='0.0.0.0')
