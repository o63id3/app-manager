import pytest
import boto3

import main
from aws_keys import access_key_id, secret_access_key


autoscaling_clinet = boto3.client('autoscaling', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
autoscaling_clinet.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=7)

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
    assert response.status_code == 302
    
    response = client.get("/charts")
    assert response.status_code == 200


# * Test manager page
def test_show_manager_page(client):
    response = client.get("/manager")
    assert response.status_code == 200


# * Test inc success
def test_inc_success(client):
    # number of instances = 7
    response = client.post("/inc")
    assert response.status_code == 200

# * Test inc failure
def test_inc_failure(client):
    # number of instances = 8
    response = client.post("/inc")
    assert response.status_code == 401


# * Test dec success
def test_dec_success(client):
    # number of instances = 8
    response = client.post("/dec")
    assert response.status_code == 200

# * Test dec failure
def test_dec_failure(client):
    # number of instances = 7
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 6
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 5
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 4
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 3
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 2
    response = client.post("/dec")
    assert response.status_code == 200
    
    # number of instances = 1
    response = client.post("/dec")
    assert response.status_code == 200
    
    response = client.post("/dec")
    assert response.status_code == 401
