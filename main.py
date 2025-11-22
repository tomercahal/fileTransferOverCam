import cv2
from camera_handler import get_web_cam, get_frame, get_qr_from_frame
from reciver import receiver_main
from sender import sender_main

def main():
    print('Hello, Botera!')
    # receiver_main()
    sender_main()
    # cam = get_web_cam()
    # frame = get_frame(cam)
    # get_qr_from_frame(frame)
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
