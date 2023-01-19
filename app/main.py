import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# path to current file's parent (folder)
BASE_DIR = pathlib.Path(__file__).parent


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# http GET -> JSON
# fastapi always return json

# now it will return html
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):

    # html file relative to templates folder
    return templates.TemplateResponse("home.html", {"request": request, "name": "John"})

    # return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_detail_view():
    return {"Hello": "World"}