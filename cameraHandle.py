import time
import cv2
from cv2.typing import MatLike

import qrcode
import os
import base64

webCam = None
qrCode = cv2.QRCodeDetector()

def getWebCam():
    if webCam:
        return webCam
    else:
        return cv2.VideoCapture(0)


def getFrame(webCam : cv2.VideoCapture):
    ret, frame = webCam.read()

    if ret:
        print("Frame captured!")
        return frame
    else:
        print("Failed to grab frame")


def getQRFromFrame(frame : MatLike):
    data, _, _ = qrCode.detectAndDecode(frame)
    return data

def getNextQRData(webCam : cv2.VideoCapture):
    while True:
        frame = getFrame(webCam)
        data = getQRFromFrame(frame)
        if data:
            # extract id
            return data.encode("utf-8")
        else:
            print("No QR code found")
        time.sleep(0.1)



# qrcode.make("Hello, World!").save("qrcode.png")
# os.startfile("qrcode.png")