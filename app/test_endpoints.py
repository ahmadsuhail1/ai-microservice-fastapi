from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

# have to write test_ to run test
def test_get_home():
    # requests.get("/")
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_post_home():
    # requests.get("/")
    response = client.post("/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json() == {"Hello": "World"}