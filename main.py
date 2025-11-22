import cv2
from camera_handler import get_web_cam, get_frame, get_qr_from_frame
from reciver import receiver_main
from sender import sender_main

def main():
    print('Hello, file-Transfer-over-cam!')
    # receiver_main()
    sender_main()

if __name__ == '__main__':
    main()
