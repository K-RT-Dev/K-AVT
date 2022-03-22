from os import read
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import time
from PIL import ImageGrab, ImageTk, Image


class autoMode():
    def __init__(self):
        self.ssimLog = [0, 0, 0]
        self.lastTranslateText = ""
        pass

    def addLog(self, newVal):
        self.ssimLog = self.ssimLog[1:] + [newVal]

    def checkLog(self):
        ready = True
        #print(self.ssimLog)
        for i in range(len(self.ssimLog)):
            if i == 0 and self.ssimLog[i] == 1:
                ready = False
            if i != 0 and self.ssimLog[i] < 0.9:
                ready = False
        return ready

    def testComparator(self, app, ocr, translator, automodeStopEvent):
        # Condiciones para poder hacer captura de pantalla
        if app.bbox.get() is not None or app.bbox.get() == "None":
            imgPrev = None
            imgNow = None
            # Captura nueva cada poco rato
            while not automodeStopEvent.is_set():
                # Comparamos la actual y la anterior
                imgPrev = imgNow
                imgNow = ImageGrab.grab(app.bbox.get())
                # Si ambas exiten aplicamos SSIM
                if imgPrev is not None and imgNow is not None:
                    s = ssim(cv2.cvtColor(np.array(imgNow), cv2.COLOR_BGR2GRAY),
                             cv2.cvtColor(np.array(imgPrev), cv2.COLOR_BGR2GRAY))
                    # Guardamos el resultado en una cola
                    self.addLog(s)
                # Si la cola cumple las condiciones, proseguimos con la traduccion
                if self.checkLog():
                    # Aplicamos el OCR
                    text = ocr.extractorOCR(np.array(imgNow))
                    # Si el OCR nos da algun resultado y este es distinto a la ultima traduccion, proseguimos con la traduccion
                    if len(text) > 0 and self.lastTranslateText != text:
                        self.lastTranslateText = text
                        app.sentencesJpLable.setLabelText(text)

                        # Guardamos y desplegamos la ultima captura que vamos a analizar
                        file = open('kavt_data/capture.png', 'wb')
                        app.currentCaptureImg.set(imgNow)
                        imgNow.save(file, 'PNG')
                        file.close()
                        app.drawCaptureImage()

                        # Traducimos
                        app.sentencesLable.setLabelText("<Translating...>")
                        result = translator.translate(text)
                        app.sentencesLable.setLabelText(result)

                time.sleep(0.2)
