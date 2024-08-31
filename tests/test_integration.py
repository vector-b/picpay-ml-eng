from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


#test load, predict, history
def test_load():
    response = client.post("/model/load")
    assert response.status_code == 200
    assert response.json() == {"model": "model"}

def test_predict():
    response = client.post("/model/predict")
    assert response.status_code == 200
    assert response.json() == {"prediction": "prediction"}

def test_history():
    response = client.get("/model/history")
    assert response.status_code == 200
    assert response.json() == {"history": "history"}