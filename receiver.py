import os
import qrcode
import tkinter as tk
from tkinter import filedialog
from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import (
    decode_qr_data, encode_qr_data, create_approval_payload,
    is_starting_chunk, is_data_chunk
)

def receiver_main():
    """Main receiver function that processes incoming QR codes and reconstructs the file"""
    cam = get_web_cam()
    directory_to_save_in = choose_save_location()
    
    print("Waiting for file transfer to start...")
    
    file_metadata = wait_for_starting_chunk(cam)
    print(f"Received starting chunk with metadata.")
    print(f"Receiving file: {file_metadata['file_name']}")
    print(f"Total chunks expected: {file_metadata['total_chunks']}")
    save_path = os.path.join(directory_to_save_in, file_metadata['file_name'])
    
    # Receive all data chunks
    file_data = receive_file_chunks(cam, file_metadata['total_chunks'])
    
    # Save the reconstructed file
    with open(save_path, "wb") as f:
        f.write(file_data)
    print(f"File saved successfully to: {save_path}")
    # open the file
    os.startfile(save_path) # @TODO: Check for corrupted files before opening


def wait_for_starting_chunk(cam):
    """Wait for starting chunk and process the chunk that contains the file metadata"""
    while True:
        print("Scanning for starting chunk...")
        qr_data_string = get_next_qr_data(cam)
        payload = decode_qr_data(qr_data_string)
        
        if payload and is_starting_chunk(payload):
            send_approval(payload['id'])
            return {
                'file_name': payload.get('file_name', 'unknown_file'),
                'total_chunks': payload.get('total_chunks', 0)
            }

def receive_file_chunks(cam, total_chunks):
    """Receive and reconstruct file data from chunks"""
    chunks_data = {}
    received_count = 0
    
    while received_count < total_chunks:
        progress = (received_count / total_chunks) * 100
        print(f"Progress: {progress:.1f}% - Waiting for chunk {received_count + 1}/{total_chunks}...")
        
        qr_data_string = get_next_qr_data(cam)
        payload = decode_qr_data(qr_data_string)
        
        if payload and is_data_chunk(payload): # @TODO: Move the payload check to is_data_chunk
            chunk_id = payload['id']
            chunk_data = payload['data']
            
            # Store chunk data (chunks should be numbered starting from 1)
            if chunk_id not in chunks_data:
                chunks_data[chunk_id] = chunk_data
                received_count += 1
                progress = (received_count / total_chunks) * 100
                print(f"✓ Received chunk {chunk_id} ({len(chunk_data)} bytes) - {progress:.1f}% complete")
                
                # Send approval for this chunk
                send_approval(chunk_id)
            else:
                print(f"⚠ Duplicate chunk {chunk_id} received, ignoring")
    
    # Reconstruct file data in correct order
    print("📁 Reconstructing file...")
    file_data = b""
    for chunk_id in sorted(chunks_data.keys()): #@TODO: concat the file data the whole time should come ordered
        file_data += chunks_data[chunk_id]
    
    return file_data

def send_approval(chunk_id):
    """Send approval QR code for received chunk"""
    approval_payload = create_approval_payload(chunk_id)
    approval_qr_string = encode_qr_data(approval_payload)
    
    # @TODO: Change to cv2 like the receiver and close all windows upon sending next approval
    qr = qrcode.make(approval_qr_string)
    qr.show()
    print(f"Approval QR displayed for chunk {chunk_id} - keeping it visible until next chunk arrives")

def choose_save_location():
    """Let the user choose the directory to save the received file"""    
    root = tk.Tk()
    root.withdraw()

    # Bring dialog to front and make it focused
    root.attributes('-topmost', True)
    root.update()

    directory = filedialog.askdirectory(
        title=f"Choose the directory to save the file",
        parent=root
    )
    
    root.destroy()            
    if directory:
        return directory
    return os.getcwd()