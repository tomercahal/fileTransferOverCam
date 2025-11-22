import qrcode
import tkinter as tk
from tkinter import filedialog
import os
from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import check_qr_chunk_approval, create_chunks_to_send, create_qr_payload

def sender_main():
    cam = get_web_cam()
    file_name, file_data = pick_file()
    if not file_name:
        print("No file selected.")
        return
    chunks_to_send = create_chunks_to_send(file_name, file_data)
    # add first qr code as metadata
    for chunk in chunks_to_send:
        print(f"Sending chunk!")
        qr = qrcode.make(chunk)
        qr.show()
        wait_for_chunk_approval(cam, chunk)

def pick_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    if file_path:
        with open(file_path, "rb") as f:
            return file_name, f.read()
    else:
        print("No file selected.")
        return None, b""

def wait_for_chunk_approval(cam, chunk):
    print("Waiting for approval from receiver...")
    input("Press Enter to continue...")
    # received_approval = False
    received_approval = True
    while not received_approval:
        qr_data = get_next_qr_data(cam)
        if check_qr_chunk_approval(qr_data, chunk):
            print("Approval received for chunk", chunk)
            received_approval = True
