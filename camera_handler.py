import time
import cv2
from cv2.typing import MatLike

import qrcode
import os
import base64

web_cam = None
qr_code = cv2.QRCodeDetector()

def get_web_cam():
    if web_cam:
        return web_cam
    else:
        return cv2.VideoCapture(0)


def get_frame(web_cam : cv2.VideoCapture):
    ret, frame = web_cam.read()

    if ret:
        print("Frame captured!")
        return frame
    else:
        print("Failed to grab frame")


def get_qr_from_frame(frame : MatLike):
    data, _, _ = qr_code.detectAndDecode(frame)
    return data

def get_next_qr_data(web_cam : cv2.VideoCapture):
    while True:
        frame = get_frame(web_cam)
        data = get_qr_from_frame(frame)
        if data:
            # extract id
            return data.encode("utf-8")
        else:
            print("No QR code found")
        time.sleep(0.1)



# qrcode.make("Hello, World!").save("qrcode.png")
# os.startfile("qrcode.png")