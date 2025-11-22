
import json
import os
import qrcode
from cameraHandle import getNextQRData, getWebCam, getFrame, getQRFromFrame

# pick file func

def SenderMain():
    with open("frame.jpg", "rb") as file:
        imageData = file.read()
    chunks = splitIntoBatches(imageData)
    # add first qr code as metadata
    for chunk in chunks:
        qr = qrcode.make(chunk)
        qr.show()
        waitForApprovalFromReceiver()
        # receive approval to go to next qr
        input("Press Enter to continue...")
6

def splitIntoBatches(data, size=100):
    return [data[i:i+size] for i in range(0, len(data), size)]

def waitForApprovalFromReceiver():