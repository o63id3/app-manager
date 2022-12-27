import boto3
from db import _USER, _PASSWORD, _HOST, _DATABASE

import pymysql
from flask import Flask, redirect, render_template, request, url_for
from aws_keys import access_key_id, secret_access_key
import time


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


scaling_policy = "manual"
max_miss_rate_threshold = 80
min_miss_rate_threshold = 40
expand_ratio = 2
shrink_ratio = 0.5


def one_minute_sce():
    time.sleep(60)
    auto_scaling()


def auto_scaling():
    if scaling_policy == "auto":
        pass
    
    one_minute_sce()


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('charts'))


@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html'), 200


@app.route('/manager', methods=['GET'])
def manager():
    if request.method == 'GET':
        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, ), 200


@app.route('/inc', methods=['POST'])
def inc():
    global number_of_instances
    if number_of_instances > 7:
        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, error=True), 401
    else:
        client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=number_of_instances+1)
        
        number_of_instances += 1

        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, ), 200


@app.route('/dec', methods=['POST'])
def dec():
    global number_of_instances
    if number_of_instances <= 1:
        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, error=True), 401
    else:
        client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=number_of_instances-1)
        
        number_of_instances -= 1
        
        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, ), 200


#! not ready
@app.route('/pool-config', methods=['POST'])
def pool_config():
    global scaling_policy
    global max_miss_rate_threshold
    global min_miss_rate_threshold
    global expand_ratio
    global shrink_ratio
    
    if 'scalingPolicyOptions' in request.form:
        if request.form["scalingPolicyOptions"] == "manual":
            scaling_policy = "manual"
        else:
            if request.form["max_miss_rate_threshold"] == "":
                return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, max_miss_rate_threshold_error_msg='Max miss rate threshold should be between 1 and 99.'), 401
            elif request.form["min_miss_rate_threshold"] == "":
                return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, min_miss_rate_threshold_error_msg='Min miss rate threshold should be between 1 and 99.'), 401
            elif request.form["expand_ratio"] == "":
                return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, expand_ratio_error_msg='Expand ratio should be greater than 1.'), 401
            elif request.form["shrink_ratio"] == "":
                return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, shrink_ratio_error_msg='Shrink ratio should be between 0 and 1.'), 401
            else:
                scaling_policy = "automatic"
                max_miss_rate_threshold = int(request.form["max_miss_rate_threshold"])
                min_miss_rate_threshold = int(request.form["min_miss_rate_threshold"])
                expand_ratio = int(request.form["expand_ratio"])
                shrink_ratio = float(request.form["shrink_ratio"])
                return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, scaling_policy_set_success_msg='Scaling policy has been set successfully.'), 200
        
        
    else:
        return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, scaling_policy_error_msg='You have to choose scaling policy.'), 401
    
    return render_template("manager.html", number_of_instances=number_of_instances, mode=scaling_policy, ), 200


#! not ready
@app.route('/instances-config', methods=['POST'])
def instances_config():
    pass

#! not ready
@app.route('/delete', methods=['POST'])
def delete_app_data():
    pass


#! not ready
@app.route('/clear', methods=['POST'])
def clear_memecache():
    pass


# app.run(debug=True)
app.run(debug=True, port=PORT, host=HOST)
# app.run(debug=True, port=PORT, host=HOST, ssl_context=('cert.pem', 'key.pem'))
