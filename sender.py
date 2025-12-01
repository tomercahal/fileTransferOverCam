import tkinter as tk
from tkinter import filedialog
import os
from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import check_qr_chunk_approval, create_chunks_to_send, encode_qr_data
from display_utils import display_qr_centered, close_qr_window

def sender_main():
    """Main sender function that processes outgoing QR codes and sends the file"""
    cam = get_web_cam()
    file_name, file_data = pick_file()
    if not file_name:
        print("No file selected, aborting.")
        return
    chunks_to_send = create_chunks_to_send(file_name, file_data)
    for chunk in chunks_to_send:
        print(f"Sending chunk {chunk['id']}...")
        qr_window_name = f"Chunk {chunk['id']} - Sender QR"
        display_qr_for_chunk(chunk, qr_window_name)
        wait_for_chunk_approval(cam, chunk)
        close_qr_window(qr_window_name)
    print(f"✅ File '{file_name}' sent successfully! All {len(chunks_to_send)} chunks transferred.")

def pick_file():
    """Open file dialog to pick a file and read its data"""
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
        return None, b""

def wait_for_chunk_approval(cam, chunk):
    """Wait for approval QR code from receiver for the given chunk"""
    print(f"Waiting for approval from receiver for chunk {chunk['id']}...")
    received_approval = False
    
    while not received_approval:
        qr_data_string = get_next_qr_data(cam)
        if check_qr_chunk_approval(qr_data_string, chunk):
            print(f"Approval received for chunk {chunk['id']}!")
            received_approval = True
        else:
            print("Waiting for correct approval...")
    print(f"Chunk {chunk['id']} confirmed, moving to next...")

def display_qr_for_chunk(chunk, qr_window_name):
    """Display QR code for the given chunk"""
    qr_data_string = encode_qr_data(chunk)
    display_qr_centered(qr_data_string, qr_window_name)