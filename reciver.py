
from cameraHandle import getNextQRData, getWebCam, getFrame, getQRFromFrame



def reciverMain():
    cam = getWebCam()
    receivedFile = False
    fileInBytes = b""
    while not receivedFile:
        data = getNextQRData(cam)
        fileInBytes += data
        
        receivedFile = True

    with open("temp.txt", "wb") as f:
        f.write(fileInBytes)



