import pytest
import boto3
from aws_keys import access_key_id, secret_access_key


autoscaling_clinet = boto3.client('autoscaling', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
autoscaling_clinet.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=7)


import main


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
    # no ins = 7
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 6
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 5
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 4
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 3
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 2
    response = client.post("/dec")
    assert response.status_code == 200
    
    # no ins = 1
    response = client.post("/dec")
    assert response.status_code == 401
    
    autoscaling_clinet.set_desired_capacity(AutoScalingGroupName='imagey_autoscaling_group', DesiredCapacity=0)
