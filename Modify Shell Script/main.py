from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

def apn_parse(apn):
    """Parses the APN string to extract the SIM name and APN value."""
    name = apn.split('[')[1].split(']')[0]
    apn_value = apn.split('=')[1]
    return name, apn_value

@app.route('/to_turn_on', methods=['GET'])
def modify_function():
    sim_name = request.args.get('sim_name')
    apn_name = request.args.get('apn_name')

    if not sim_name or not apn_name:
        return jsonify({"error": "Both sim_name and apn_name must be provided."}), 400

    try:
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {apn_parse(apn)[0]: apn_parse(apn)[1] for apn in apn_dict if '[' in apn}

        sims_list[f'"{sim_name}"'] = f'"{apn_name}"'

        to_add = '\n    '.join([f'[{key}]={value}' for key, value in sims_list.items()])

        with open('template.sh', 'r') as template:
            template_read = template.read()

        file2 = template_read.replace('#PLACEHERE', to_add)

        with open('/etc/modem_autoconnect.sh', 'w') as after_changes_file:
            after_changes_file.write(file2)

        return jsonify({"message": "The modem_autoconnect.sh file has been successfully modified."}), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/remove_apn', methods=['GET'])
def remove_apn_function():
    sim_name = request.args.get('sim_name')

    if not sim_name:
        return jsonify({"error": "sim_name must be provided."}), 400

    try:
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {apn_parse(apn)[0]: apn_parse(apn)[1] for apn in apn_dict if '[' in apn}

        sims_list.pop(f'"{sim_name}"', None)

        to_add = '\n    '.join([f'[{key}]={value}' for key, value in sims_list.items()])

        with open('template.sh', 'r') as template:
            template_read = template.read()

        file2 = template_read.replace('#PLACEHERE', to_add)

        with open('/etc/modem_autoconnect.sh', 'w') as after_changes_file:
            after_changes_file.write(file2)

        return jsonify({"message": "The specified SIM has been removed successfully."}), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5010, host='0.0.0.0')
