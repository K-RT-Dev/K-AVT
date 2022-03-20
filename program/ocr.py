import os
import imutils
import numpy as np
from paddleocr import PaddleOCR
import easyocr

project_path = os.getcwd()

class OCRmodule():
    def __init__(self, debug=False):
        # OCR Model Init
        self.debug = debug
        self.paddleOcr = PaddleOCR(
            use_angle_cls=True,
            lang='japan', 
            use_gpu=True,
        )
        self.paddleConfidenceLevel = 0.7
        self.easyOcr = easyocr.Reader(
            lang_list=['ja'], 
            gpu=True,
        )
        self.easyConfidenceLevel = 0.4
        self.paragraph = True
        self.ocrType = "paddleOCR"
    
    def setOcrType(self, ocrType):
        self.ocrType = ocrType

    # OCR extractor
    def applyOCR(self, img):
        fullText = ""
        if self.ocrType == "paddleOCR":
            print("paddleOCR")
            result = self.paddleOcr.ocr(img, det=True, rec=True, cls=True)
            for line in result:
                if self.debug:
                    print(line)
                if line[1][1] > self.paddleConfidenceLevel:
                    fullText += line[1][0] + "\n"
            return fullText
        elif self.ocrType == "easyOCR":
            print("easyOCR")
            result = self.easyOcr.readtext(img, paragraph=True)
            if self.paragraph is False:
                for r in result:
                    if self.debug:
                        print(r)
                    if r[2] > self.easyConfidenceLevel:
                        fullText = fullText + r[1] + "\n"
            else:
                for r in result:
                    if self.debug:
                        print(r)
                    fullText = fullText + r[1] + "\n"
        else:
            print("Invalid OCR")
        return fullText

    # Img modification for enhance OCR detection (only paddlerOCR)
    # TODO: Ver si el or den Zoom->Org->MargeExpand es bueno para los dos OCRs
    def preProcessing(self, img):

        # Zoom in Img
        text = self.applyOCR(imutils.resize(img, width=1800))
        if len(text) == 0:

            # Org Img
            text = self.applyOCR(img)
            if len(text) == 0 :

                # Margin reduction via expand
                #imgBig = imutils.resize(img, width=1800)
                imgBig = img
                big_canvas = np.zeros(
                    (imgBig.shape[0] * 4, imgBig.shape[1] * 4, 3), np.uint8)
                big_canvas[0:imgBig.shape[0], 0:imgBig.shape[1]] = imgBig
                text = self.applyOCR(big_canvas)

        return text

    # Main
    def extractorOCR(self, img):
        print("OCR")
        return self.preProcessing(img)
