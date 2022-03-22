# IGNORE THIS FILE
from PIL import Image
import pytesseract

r = pytesseract.image_to_string(Image.open('x.png'), lang='jpn')
print(r)
