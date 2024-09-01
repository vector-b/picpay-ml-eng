from apis.app import app
import pytest
import json


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "ok"

def test_load():
    response = client.post("/model/load")
    assert response.status_code == 200
    assert response.json() == {"model": "model"}

def test_predict(client):
    sample_data = {
        "feature1": 3.5,
        "feature2": 42,
        "feature3": 1.8,
    }
    
    response = client.post('/model/predict', json=sample_data)
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert "prediction" in data
    assert isinstance(data["prediction"], float) 

def test_history(client):
    response = client.get("/model/history")
    assert response.status_code == 200