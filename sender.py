
import json
import os
import qrcode
from camera_handler import get_next_qr_data, get_web_cam, get_frame, get_qr_from_frame

def sender_main():
    cam = get_web_cam()
    # pick file func
    with open("frame.jpg", "rb") as file:
        image_data = file.read()
    chunks = divide_into_chunks(image_data) # add id and total number to each chunk
    # add first qr code as metadata
    for chunk in chunks:
        qr = qrcode.make(chunk)
        qr.show()
        wait_for_approval_from_receiver(cam)
        # receive approval to go to next qr
        input("Press Enter to continue...")

def divide_into_chunks(data, size=100):
    return [data[i:i+size] for i in range(0, len(data), size)]

def wait_for_approval_from_receiver(cam):
    print("Waiting for approval from receiver...")
    received_approval = False
    while not received_approval:
        qr_data = get_next_qr_data(cam)
        if qr_data == b'APPROVED':
            print("Approval received!")
            break