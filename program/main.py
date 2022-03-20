import cv2
from PIL import ImageGrab, ImageTk, Image
import pyautogui
import keyboard
import tkinter as tk
import threading

from program.ocr import OCRmodule
from program.translator import translatorModule
from program.autoMode import autoMode

from program.components.frame import Frame
from program.components.separator import Separator
from program.components.button import Button
from program.components.label import Label
from program.components.imageLabel import ImageLabel
from program.components.menuBar import MenuBar

from program.windows.credentialsW import CredentialsW
from program.windows.aboutW import AboutW

ocr = OCRmodule(debug=True)
translator = translatorModule(debug=True)
auto = autoMode()

class Application(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry("600x400")
        self.parent.title("PoC Alpha v0.2 - K-AVT - By K")
        self.automodeThread = None

        self.credentialW = CredentialsW(self, translator)
        self.aboutW = AboutW(self)

        #---Main Window---#
        self.cornersLable = Label(self, "Set the zone of the screen to be translate")
        Label(self, "1) Click Set Zone. 2) Move the cursor to the left top corner of the area to capture and press space. \n 3) Move the cursor to the rigth bottom corner of the area to capture and click space")
        self.setZoneButton = Button(self, "Set Zone", self.setWindowZone)

        self.imageCapture = ImageLabel(self)

        self.subFrame1 = Frame(self)
        self.captureWindowButton = Button(
            self, "Capture", self.captureWindow, inFrame=self.subFrame1.frame)
        self.processImgButton = Button(
            self, "Translate", self.processImg, inFrame=self.subFrame1.frame)
        self.captureWindowAndProcessButton = Button(
            self, "Capture and Translate", self.captureAndProcess, inFrame=self.subFrame1.frame)

        self.automodeButton = Button(
            self, "Automode", self.auto, inFrame=self.subFrame1.frame)
        self.automodeButton.changeText("Automode (OFF)")

        Separator(self)
        Label(self, "Sequence of characters detected:")
        self.sentencesJpLable = Label(self, "<None>")
        Separator(self)
        Label(self, "Translated text:")
        self.sentencesLable = Label(self, "<None>")

        self.busyWindowZoneSetting = tk.BooleanVar(value=False)
        self.busyWindowZoneSetting.trace(
            "w", self.busyWindowZoneSettingOnChange)

        self.bbox = tk.Variable(value=None)
        self.bbox.trace("w", self.bboxOnChange)
        self.bbox.set(None)

        self.currentCaptureImg = tk.Variable(value=None)
        self.currentCaptureImg.trace("w", self.currentCaptureImgOnChange)
        self.currentCaptureImg.set(None)

        self.busyImgProcessing = tk.BooleanVar(value=False)
        self.busyImgProcessing.trace("w", self.busyImgProcessingOnChange)
        self.busyImgProcessing.set(False)
        
        #---MenuBar---#
        self.menubar = MenuBar(self)  

        self.ocrType = tk.StringVar(value="paddleOCR")
        self.menubar.addDropdown("OCR")
        self.menubar.addRadioButtonGroup("OCR", {"PaddleOCR":"paddleOCR", "EasyOCR":"easyOCR"}, self.ocrType, self.changeOcrType)

        self.transType = tk.StringVar(value="google")
        self.menubar.addDropdown("Translator")
        self.menubar.addRadioButtonGroup("Translator", {"DeepL":"deepl", "Google":"google"}, self.transType, self.changeTransType)

        self.inputLan = tk.StringVar(value="ja")
        self.menubar.addDropdown("Detection Lenguage")
        self.menubar.addRadioButtonGroup("Detection Lenguage", {"Japanse":"ja"}, self.inputLan)

        self.outLan = tk.StringVar(value="en")
        self.menubar.addDropdown("Translate Lenguage")
        self.menubar.addRadioButtonGroup("Translate Lenguage", {"English":"en", "Spanish": "es"}, self.outLan, self.changeOutLan)

        self.menubar.addDropdown("Config")
        self.menubar.addButton("Config", "Credentials", self.openKeyWindow)
        self.menubar.addButton("Config", "Abaut", self.openAboutWindow)
        #-----#

    #
    def bboxOnChange(self, *args):
        if self.bbox.get() is None or self.bbox.get() == "None":
            self.captureWindowButton.setState("disable")
            self.captureWindowAndProcessButton.setState("disable")
            self.automodeButton.setState("disable")
        else:
            self.captureWindowButton.setState("normal")
            self.captureWindowAndProcessButton.setState("normal")
            self.automodeButton.setState("normal")

    #
    def busyWindowZoneSettingOnChange(self, *args):
        if self.busyWindowZoneSetting.get() is True:
            self.setZoneButton.setState("disable")
            self.captureWindowButton.setState("disable")
            self.captureWindowAndProcessButton.setState("disable")
            self.processImgButton.setState("disable")
            self.automodeButton.setState("disable")
        else:
            self.setZoneButton.setState("normal")
            self.captureWindowButton.setState("normal")
            self.captureWindowAndProcessButton.setState("normal")
            self.processImgButton.setState("normal")
            self.automodeButton.setState("normal")

    #
    def currentCaptureImgOnChange(self, *args):
        if self.bbox.get() is None or self.bbox.get() == "None":
            self.processImgButton.setState("disable")
            self.captureWindowAndProcessButton.setState("disable")
        else:
            self.processImgButton.setState("normal")
            self.captureWindowAndProcessButton.setState("normal")

    #
    def busyImgProcessingOnChange(self, *args):
        if self.busyImgProcessing.get() is True:
            self.setZoneButton.setState("disable")
            self.captureWindowButton.setState("disable")
            self.captureWindowAndProcessButton.setState("disable")
            self.processImgButton.setState("disable")
        else:
            self.busyWindowZoneSettingOnChange()
            self.bboxOnChange()
            self.currentCaptureImgOnChange()

    # When the output leguage in the menubar is changed
    def changeOutLan(self):
        translator.setOutLan(self.outLan.get())

    # When the translate option in the menubar is changed
    def changeTransType(self):
        translator.setTransType(self.transType.get())

    # When the OCR option in the menubar is changed
    def changeOcrType(self):
        ocr.setOcrType(self.ocrType.get())

    # When Config>Credentials button in menuBar is pressed
    def openKeyWindow(self):
        self.credentialW.drawWindow()

    # When Config>About button in menuBar is pressed
    def openAboutWindow(self):
        self.aboutW.drawWindow()

    # Mause detection rutine
    def mauseDetection(self):
        corners = []
        while len(corners) < 2:
            keyboard.wait('space')
            currentMouseX, currentMouseY = pyautogui.position()
            print("Point captured: X", currentMouseX, "- Y", currentMouseY)
            corners.append([currentMouseX, currentMouseY])
        #Xinit, Yinit, Xend, Yend
        self.bbox.set((corners[0][0], corners[0][1],
                       corners[1][0], corners[1][1]))
        self.cornersLable.setLabelText("X: " + str(corners[0][0]) + " Y: " + str(
            corners[0][1]) + ", X:" + str(corners[1][0]) + " Y: " + str(corners[1][1]))
        self.busyWindowZoneSetting.set(False)
        return

    # Screen zone selector
    def setWindowZone(self):
        if self.busyWindowZoneSetting.get() is False:
            print("Screen zone selector")
            self.busyWindowZoneSetting.set(True)
            newthread = threading.Thread(target=self.mauseDetection)
            newthread.daemon = True
            newthread.start()
        return

    # Capture window in file
    def captureWindow(self):
        print("Screen capture")
        if self.bbox.get() is not None or self.bbox.get() == "None":
            file = open('capture.png', 'wb')
            screenshot = ImageGrab.grab(self.bbox.get())
            self.currentCaptureImg.set(screenshot)
            screenshot.save(file, 'PNG')
            file.close()
            self.drawCaptureImage()
        return

    # Draw capture image example
    def drawCaptureImage(self):
        drawHeight = 150
        drawWidth = 500
        img = Image.open("capture.png")
        w, h = img.size
        scale = h / drawHeight
        w = int(w/scale)
        h = int(h/scale)
        if w > drawWidth:
            scale = w / drawWidth
            w = int(w/scale)
            h = int(h/scale)
        img = img.resize((w, h), Image.ANTIALIAS)
        self.imageCapture.setImage(ImageTk.PhotoImage(img))
        return

    # Capture and Process Img
    def captureAndProcess(self):
        self.captureWindow()
        self.processImg()

    # Modo automatico
    def auto(self):
        if self.automodeThread is None:
            self.automodeButton.changeText("Automode (ON)")

            self.captureWindowButton.setState("disable")
            self.captureWindowAndProcessButton.setState("disable")
            self.setZoneButton.setState("disable")
            self.processImgButton.setState("disable")

            self.automodeStopEvent = threading.Event()
            self.automodeThread = threading.Thread(
                target=auto.testComparator, args=([self, ocr, translator, self.automodeStopEvent]))
            self.automodeThread.daemon = True
            self.automodeThread.start()
        else:
            self.automodeStopEvent.set()
            self.automodeThread = None
            self.automodeButton.changeText("Automode (OFF)")

            self.captureWindowButton.setState("normal")
            self.captureWindowAndProcessButton.setState("normal")
            self.setZoneButton.setState("normal")
            self.processImgButton.setState("normal")

    # Main translate async process
    def asyncProcessImg(self):
        # Init
        self.busyImgProcessing.set(True)
        self.sentencesJpLable.setLabelText("<Translating...>")
        self.sentencesLable.setLabelText("<Translating...>")
        # Read Image
        img = cv2.imread("capture.png")
        # OCR
        text = ocr.extractorOCR(img)
        self.sentencesJpLable.setLabelText(text)
        # Translator
        result = translator.translate(text)
        # Display result
        self.sentencesLable.setLabelText(result)
        self.busyImgProcessing.set(False)

    # Post process img request
    def processImg(self):
        if self.busyImgProcessing.get() is False:
            print("Process Img")
            newthread = threading.Thread(target=self.asyncProcessImg)
            newthread.daemon = True
            newthread.start()
        return


def main():
    window = tk.Tk()
    Application(window)
    window.mainloop()