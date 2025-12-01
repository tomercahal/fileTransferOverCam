import time
import cv2
from cv2.typing import MatLike

web_cam = None
qr_code = cv2.QRCodeDetector()

def get_web_cam():
    """Initialize web camera object or return the existing one"""
    if web_cam:
        return web_cam
    else:
        return cv2.VideoCapture(0)


def get_frame(web_cam : cv2.VideoCapture):
    """Capture a single frame from the web camera"""
    ret, frame = web_cam.read()

    if ret:
        return frame
    else:
        print("Failed to grab frame")
        return None


def get_qr_from_frame(frame : MatLike):
    """Detect and decode QR code from a given frame"""
    data, _, _ = qr_code.detectAndDecode(frame)
    return data

def get_next_qr_data(web_cam : cv2.VideoCapture):
    """Continuously capture frames until QR code detected and returns its data"""
    while True:
        # Process OpenCV GUI events so windows (imshow) remain responsive
        # waitkey(1) is necessary on many systems to keep the window responsive
        cv2.waitKey(1)
        frame = get_frame(web_cam)
        if frame is not None:
            data = get_qr_from_frame(frame)
            if data:
                return data
        time.sleep(0.1)
