import qrcode
import tkinter as tk
from tkinter import filedialog
import os
from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import check_qr_chunk_approval, create_chunks_to_send, create_qr_payload, encode_qr_data

def sender_main():
    cam = get_web_cam()
    file_name, file_data = pick_file()
    if not file_name:
        print("No file selected.")
        return
    chunks_to_send = create_chunks_to_send(file_name, file_data)
    for chunk in chunks_to_send:
        print(f"Sending chunk {chunk['id']}...")
        qr_data_string = encode_qr_data(chunk)
        qr = qrcode.make(qr_data_string)
        qr.show()
        print(f"QR displayed for chunk {chunk['id']} - listening for approval...")
        wait_for_chunk_approval(cam, chunk)
        print(f"Chunk {chunk['id']} confirmed, moving to next...")

def pick_file():
    root = tk.Tk()
    root.withdraw()
    
    # Bring dialog to front and make it focused
    root.attributes('-topmost', True)
    root.update()
    
    file_path = filedialog.askopenfilename(
        title="Select file to transfer",
        parent=root
    )
    
    root.destroy()
    file_name = os.path.basename(file_path)
    if file_path:
        with open(file_path, "rb") as f:
            return file_name, f.read()
    else:
        print("No file selected.")
        return None, b""

def wait_for_chunk_approval(cam, chunk):
    print(f"Waiting for approval from receiver for chunk {chunk['id']}...")
    received_approval = False
    
    while not received_approval:
        qr_data_string = get_next_qr_data(cam)
        if check_qr_chunk_approval(qr_data_string, chunk):
            print(f"Approval received for chunk {chunk['id']}!")
            received_approval = True
        else:
            print("Waiting for correct approval...")
