import pytest
import boto3
import sys
import os
import io
sys.path.append('../app manager')
import main
from aws_keys import access_key_id, secret_access_key


client = boto3.client('autoscaling', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')


@pytest.fixture()
def app():
    main.app.config.update({
        "TESTING": True,
    })
    yield main.app


@pytest.fixture()
def client(app):
    return main.app.test_client()


@pytest.fixture()
def runner(app):
    return main.app.test_cli_runner()



# * Test charts page
def test_show_charts_page(client):
    response = client.get("/")
    assert response.status_code == 200
    
    response = client.get("/charts")
    assert response.status_code == 200


# * Test manager page
def test_show_manager_page(client):
    response = client.get("/manager")
    assert response.status_code == 200


# * Test inc success
def test_inc_success(client):
    client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=7)
    
    response = client.post("/inc")
    assert response.status_code == 200

# * Test inc failure
def test_inc_failure(client):
    response = client.post("/inc")
    assert response.status_code == 401


# * Test dec success
def test_dec_success(client):
    response = client.post("/dec")
    assert response.status_code == 200

# * Test dec failure
def test_dec_failure(client):
    client.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=0)
    
    response = client.post("/dec")
    assert response.status_code == 401
