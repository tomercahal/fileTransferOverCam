import cv2
from cameraHandle import getWebCam, getFrame, getQRFromFrame
from reciver import reciverMain
from sender import SenderMain


def main():
    print('Hello, Botera!')
    # reciverMain()
    SenderMain()
    # cam = getWebCam()
    # frame = getFrame(cam)
    # getQRFromFrame(frame)
    # cap = cv2.VideoCapture(0)
    # ret, frame = cap.read()

    # cap.release()

    # if ret:
    #     cv2.imwrite("frame.jpg", frame)
    #     print("Frame captured!")
    # else:
    #     print("Failed to grab frame")



if __name__ == '__main__':
    main()
