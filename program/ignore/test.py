# IGNORE THIS FILE
import easyocr
from datetime import datetime

a = datetime.now()
reader = easyocr.Reader(lang_list=['ja'], gpu=True)
b = datetime.now()
c = b - a
print(c.microseconds/1000)

paragraph = True

a = datetime.now()
result = reader.readtext('./x.png', paragraph=paragraph)
b = datetime.now()
c = b - a
print(c.microseconds/1000)

print(result)

fullText = ""
if len(result) > 0:
    if paragraph is False:
        for r in result:
            if r[2] > 0.4:
                fullText = fullText + r[1] + "\n"
        print(fullText)
    else:
        for r in result:
            fullText = fullText + r[1] + "\n"
        print(fullText)
