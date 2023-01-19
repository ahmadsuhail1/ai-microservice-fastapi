import pathlib
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

BASEDIR = pathlib.Path(__file__).parent
IMG_DIR = BASEDIR / "images"
img_path = IMG_DIR / "1.jpeg"

img = Image.open(img_path)



preds = pytesseract.image_to_string(img)
predictions = [x for x in preds.split("\n")]

print(predictions)