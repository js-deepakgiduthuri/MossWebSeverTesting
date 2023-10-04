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
#DARWIN_URL = os.environ.get('DARWIN_URL')


@app.route('/')
def home():
    return render_template('LoginPage.html')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/configure')
def second_page():
    with open('static/data.json', 'r') as file:
        data = json.load(file)
    return render_template('index.html', data=data)


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
            requests.get("http://gpio_trigger:5002/run_script2")
            return render_template('gsm_on.html')
        except Exception as e:
            logging.error(f"Failed to trigger gpio_trigger: {str(e)}")
            return render_template('gsm_off.html')
    else:
        try:
            requests.get("http://gpio_trigger:5002/turn_off")
            return render_template('gsm_off.html')
        except Exception as e:
            logging.error(f"Failed to trigger gpio_trigger: {str(e)}")
            return render_template('gsm_off.html')


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



