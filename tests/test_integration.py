from apis.app import app
import random
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

def test_load_model(client):
    model_path = "models/trained_models/model-2024-09-02-00-22-05"
    
    response = client.post('/model/load', json={"model_path": model_path})
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Model successfully loaded"

def test_predict(client):
    sample_data = {
        "distance": random.randint(0, 1000),
        "dep_delay": random.randint(-20, 10),
        "air_time": random.randint(0, 200)
    }
    response = client.post('/model/predict', json=sample_data)
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    assert isinstance(data, list) and len(data) == 1
    assert "prediction" in data[0]
    assert isinstance(data[0]["prediction"], float)

def test_history(client):
    response = client.get("/model/history")
    assert response.status_code == 200