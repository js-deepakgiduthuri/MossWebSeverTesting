from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json
import requests
import logging


app = Flask(__name__)


db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


@app.route('/')
def home():
    return render_template('LoginPage.html')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/configure')
def second_page():
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    return render_template('mainhomepage.html', data=data)


class Modem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enable_option = db.Column(db.String(64))
    pin_number = db.Column(db.String(64))
    puk_code = db.Column(db.String(64))
    apn = db.Column(db.String(64))


class Lan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address_type = db.Column(db.String(64))
    ip_address = db.Column(db.String(64))
    subnet_mask = db.Column(db.String(64))
    gateway = db.Column(db.String(64))
    dns_server = db.Column(db.String(64))
    dns_secondary = db.Column(db.String(64))


# Add a new model for APN
class APN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sim_name = db.Column(db.String(64))
    apn = db.Column(db.String(64))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address_server = db.Column(db.String(64))
    usernames = db.Column(db.String(64))
    passwords = db.Column(db.String(64))


@app.route('/modem', methods=['POST'])
def modem_config():
    config = Modem(**request.form)
    db.session.add(config)
    db.session.commit()
    enable_option = request.form.get('enable_option')
    print("enable_option:", enable_option)
    if enable_option == 'on':
        try:
            requests.get("http://gpio_trigger:5002/to_turn_on")
            return render_template('gsm_on.html')
        except Exception as e:
            logging.error(f"Failed to trigger gpio_trigger: {str(e)}")
            return render_template('gsm_exception.html')
    else:
        try:
            requests.get("http://gpio_trigger:5002/to_turn_off")
            return render_template('gsm_off.html')
        except Exception as e:
            logging.error(f"Failed to trigger gpio_trigger: {str(e)}")
            return render_template('gsm_exception.html')


@app.route('/add_apn', methods=['GET', 'POST'])
def add_apn():
    if request.method == 'POST':
        sim_name = request.form.get('sim_name')
        apn_name = request.form.get('apn')

        if not sim_name or not apn_name:
            return render_template('apn_dict_exception.html', error="Both SIM Name and APN must be provided.")

        try:
            config = APN(sim_name=sim_name, apn=apn_name)
            db.session.add(config)
            db.session.commit()
            requests.get(f"http://modify_shell:5010/to_turn_on?sim_name={sim_name}&apn_name={apn_name}")
            return render_template('apn_dict_success.html')
        except Exception as e:
            logging.error(f"Failed to modify shell script: {str(e)}")
            return render_template('apn_dict_exception.html', error=str(e))

    return render_template('add_apn.html')


@app.route('/remove_apn', methods=['GET', 'POST'])
def remove_apn():
    if request.method == 'POST':
        sim_name = request.form.get('sim_name')

        if not sim_name:
            return render_template('apn_dict_exception.html', error="SIM Name must be provided.")

        try:
            apn_entry = APN.query.filter_by(sim_name=sim_name).first()
            if apn_entry:
                db.session.delete(apn_entry)
                db.session.commit()
                requests.get(f"http://modify_shell:5010/remove_apn?sim_name={sim_name}")
                return render_template('apn_dict_success.html')
            else:
                return render_template('apn_dict_exception.html', error="No APN found for the given SIM name.")
        except Exception as e:
            logging.error(f"Failed to remove APN: {str(e)}")
            return render_template('apn_dict_exception.html', error=str(e))

    return render_template('remove_apn.html')


@app.route('/get_apn', methods=['GET'])
def get_apn():
    try:
        # Making a GET request to modify_shell.py to fetch the sims_list
        response = requests.get("http://modify_shell:5010/get_apn")  # Update the URL if needed
        if response.status_code == 200:
            sims_list = response.json()  # Assuming the response is in JSON format
            return jsonify(sims_list), 200
        else:
            return jsonify({"error": "Failed to fetch APN list from modify_shell."}), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching APN list: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/lan', methods=['POST'])
def lan_config():
    config = Lan(**request.form)
    db.session.add(config)
    db.session.commit()
    return render_template('afterDataBase.html')


@app.route('/server', methods=['POST'])
def server_config():
    config = Server(**request.form)
    db.session.add(config)
    db.session.commit()
    return render_template('afterDataBase.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Add this line to create all tables
    app.run(host='0.0.0.0', port=5055, debug=True)


