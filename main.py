import boto3
from db import _USER, _PASSWORD, _HOST, _DATABASE

import pymysql
from flask import Flask, redirect, render_template, request, url_for
from aws_keys import access_key_id, secret_access_key


HOST = "0.0.0.0"
PORT = 80


client = boto3.client('autoscaling', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')


app = Flask(__name__)


def connection():
    conn = pymysql.connect(host=_HOST,
                           user=_USER,
                           password=_PASSWORD,
                           database=_DATABASE,
                           autocommit=True)
    return conn


response = client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        'imagey_autoscaling_group',
    ]
)

number_of_instances = response["AutoScalingGroups"][0]['DesiredCapacity']


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
    if number_of_instances > 7:
        return render_template("manager.html", number_of_instances=number_of_instances, error=True), 401
    else:
        # Do the work
        client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=number_of_instances+1)
        
        number_of_instances += 1

        return render_template("manager.html", number_of_instances=number_of_instances), 200
    
@app.route('/dec', methods=['POST'])
def dec():
    global number_of_instances
    if number_of_instances <= 1:
        return render_template("manager.html", number_of_instances=number_of_instances, error=True), 401
    else:
        # Do the work
        client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=number_of_instances-1)
        
        number_of_instances -= 1
        
        return render_template("manager.html", number_of_instances=number_of_instances), 200


# app.run(debug=True)
app.run(debug=True, port=PORT, host=HOST)
# app.run(debug=True, port=PORT, host=HOST, ssl_context=('cert.pem', 'key.pem'))
