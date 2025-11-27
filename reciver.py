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
    
    print("Waiting for file transfer to start...")
    
    file_metadata = wait_for_starting_chunk(cam)
    if not file_metadata:
        print("Failed to receive file metadata")
        return
    
    print(f"Receiving file: {file_metadata['file_name']}")
    print(f"Total chunks expected: {file_metadata['total_chunks']}")
    
    save_path = choose_save_location(file_metadata['file_name'])
    if not save_path:
        # Use default location if no selection made
        save_path = f"received_{file_metadata['file_name']}"
        print(f"Using default save location: {save_path}")
    
    # Receive all data chunks
    file_data = receive_file_chunks(cam, file_metadata['total_chunks'])
    
    if file_data:
        # Save the reconstructed file
        with open(save_path, "wb") as f:
            f.write(file_data)
        print(f"File saved successfully to: {save_path}")
    else:
        print("Failed to receive complete file data")

def wait_for_starting_chunk(cam):
    """Wait for and process the starting chunk containing file metadata"""
    while True:
        print("Scanning for starting chunk...")
        qr_data_string = get_next_qr_data(cam)
        payload = decode_qr_data(qr_data_string)
        
        if payload and is_starting_chunk(payload):
            print("Starting chunk received!")
            print(f"File: {payload.get('file_name', 'unknown_file')}")
            print(f"Total chunks: {payload.get('total_chunks', 0)}")
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
        
        if payload and is_data_chunk(payload):
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
        elif payload:
            print(f"⚠ Unexpected payload type received, ignoring...")
    
    # Reconstruct file data in correct order
    print("📁 Reconstructing file...")
    file_data = b""
    for chunk_id in sorted(chunks_data.keys()):
        file_data += chunks_data[chunk_id]
    
    print(f"✓ File reconstruction complete - {len(file_data)} bytes total")
    return file_data

def send_approval(chunk_id):
    """Send approval QR code for received chunk"""
    approval_payload = create_approval_payload(chunk_id)
    approval_qr_string = encode_qr_data(approval_payload)
    
    # Create and display approval QR code - keep it displayed
    qr = qrcode.make(approval_qr_string)
    qr.show()
    print(f"Approval QR displayed for chunk {chunk_id} - keeping it visible until next chunk arrives")

def choose_save_location(suggested_filename):
    """Let user choose directory to save the received file"""    
    root = tk.Tk()
    root.withdraw()

    # Bring dialog to front and make it focused
    root.attributes('-topmost', True)
    root.update()
    
    # Let user choose directory only
    directory = filedialog.askdirectory(
        title=f"Choose directory to save: {suggested_filename}"
    )
    
    root.destroy()
    
    if directory:
        # Combine directory with original filename
        save_path = os.path.join(directory, suggested_filename)
        return save_path
    else:
        # Use current directory if no selection made
        current_dir = os.getcwd()
        save_path = os.path.join(current_dir, suggested_filename)
        return save_path
