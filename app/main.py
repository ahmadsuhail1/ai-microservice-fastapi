import pathlib
import os
import io
import uuid
import pytesseract
from functools import lru_cache
from fastapi import (FastAPI, Header, Depends, Request, UploadFile, File, HTTPException )
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from PIL import Image

## NOT EFFICIENT WAY --------------

class Settings(BaseSettings):
    app_auth_token : str
    debug: bool = False
    echo_active : bool = True
    app_auth_token_prod :str = None
    skip_auth : bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug

# path to current file's parent (folder)
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def verify_auth(authorization = Header(None), settings:Settings = Depends(get_settings)):
    if settings.debug and settings.skip_auth:
        return
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    label, token = authorization.split()
    if token != settings.app_auth_token:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    if settings.skip_auth:
        return True
    if settings.app_auth_token_prod:
        return authorization == settings.app_auth_token_prod
    else:
        return authorization == settings.app_auth_token

# http GET -> JSON
# fastapi always return json

# now it will return html
@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings: Settings() = Depends(get_settings)):

    # html file relative to templates folder
    return templates.TemplateResponse("home.html", {"request": request, "name": "John"})

    # return templates.TemplateResponse("home.html", {"request": request})

# A file response
@app.post("/")
async def prediction_view(file:UploadFile = File(...), authorization = Header(None), settings: Settings() = Depends(get_settings)):
    verify_auth(authorization, settings)
    bytes_str = io.BytesIO(await file.read())
    try:
        # Can use OpenCV too
        img = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")

    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    preds = pytesseract.image_to_string(img)
    predictions = [x for x in preds.split("\n")]
    return {"results" : predictions , "original": preds}


# A file response
@app.post("/img-echo/", response_class=FileResponse )
async def img_echo_view(file:UploadFile = File(...), settings: Settings() = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(status_code=400, detail="Invalid endpoint")

    UPLOAD_DIR.mkdir(exist_ok=True)

    bytes_str = io.BytesIO(await file.read())

    try:

        # Can use OpenCV too
        img = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")

    fname = pathlib.Path(file.filename)
    file_ext = fname.suffix

    dest = UPLOAD_DIR / f"{uuid.uuid1()}{file_ext}"
    img.save(dest)
    return dest