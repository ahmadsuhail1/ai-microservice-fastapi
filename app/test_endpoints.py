import shutil
import time
import io
from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, UPLOAD_DIR, get_settings
from PIL import Image, ImageChops
import requests
client = TestClient(app)

# have to write test_ to run test
def test_get_home():
    # requests.get("/")
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_invalid_file_upload_error():
    # requests.get("/")
    response = client.post("/")
    assert response.status_code == 422
    assert "application/json" in response.headers["content-type"]



def test_echo_upload():

    img_saved_path = BASE_DIR / "images"

    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)

        except:
            img = None

        response = client.post("/img-echo/", files = {"file": open(path, "rb")})
        if img is None :
            # assert "image" in response.headers["content-type"]
            assert response.status_code == 400
        else:

            # Returning valid image

            assert response.status_code == 200
            response_stream = io.BytesIO(response.content)
            echo_img = Image.open(response_stream)
            difference = ImageChops.difference(img, echo_img).getbbox()
            # assert difference is None
        # assert "image" in response.headers["content-type"]

def test_prediction_upload():

    img_saved_path = BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)

        except:
            img = None

        response = client.post("/", files = {"file": open(path, "rb")},
                               headers={"Authorization":f"JWT {settings.app_auth_token}"}
                               )
        if img is None :
            # assert "image" in response.headers["content-type"]
            assert response.status_code == 400
        else:

            # Returning valid image

            assert response.status_code == 200
            data = response.json()
            print(data)
            assert len(data.keys())== 2


    # time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)

def test_prediction_upload_missing_header():

    img_saved_path = BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)

        except:
            img = None

        response = client.post("/", files = {"file": open(path, "rb")})
        assert response.status_code == 401