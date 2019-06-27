import pytesseract
from PIL import Image

def img():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    path = input("Enter Image Path: ")
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text
