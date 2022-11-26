import boto3
from db import _USER, _PASSWORD, _HOST, _DATABASE

import pymysql
from flask import Flask, redirect, render_template, request, url_for


HOST = "0.0.0.0"
PORT = 80


app = Flask(__name__)


def connection():
    conn = pymysql.connect(host=_HOST,
                           user=_USER,
                           password=_PASSWORD,
                           database=_DATABASE,
                           autocommit=True)
    return conn


number_of_instances = 5


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('charts'))


@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html'), 200


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'GET':
        return render_template("manager.html", number_of_instances=number_of_instances), 200


@app.route('/inc', methods=['POST'])
def inc():
    global number_of_instances
    if number_of_instances == 8:
        return render_template("manager.html", number_of_instances=number_of_instances, error=True), 401
    else:
        # Do the work
        
        
        number_of_instances += 1
        return render_template("manager.html", number_of_instances=number_of_instances), 200
    
@app.route('/dec', methods=['POST'])
def dec():
    global number_of_instances
    if number_of_instances == 1:
        return render_template("manager.html", number_of_instances=number_of_instances, error=True), 401
    else:
        # Do the work
        
        
        number_of_instances -= 1
        return render_template("manager.html", number_of_instances=number_of_instances), 200


app.run(debug=True)
# app.run(debug=True, port=PORT, host=HOST)
# app.run(debug=True, port=PORT, host=HOST, ssl_context=('cert.pem', 'key.pem'))
