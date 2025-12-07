from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import (
    decode_qr_data, encode_qr_data, create_approval_payload,
    is_starting_chunk, is_data_chunk
)
from display_utils import display_qr_centered, close_all_qr_windows
from file_utils import select_save_directory, save_file_data, open_file
import time

def receiver_main():
    """Main receiver function that processes incoming QR codes and reconstructs the file"""
    cam = get_web_cam()
    directory_to_save_in = select_save_directory()
    if not directory_to_save_in:
        print("No directory selected, aborting.")
        return
    
    print("Waiting for file transfer to start")
    
    file_metadata = wait_for_starting_chunk(cam)
    print(f"Received starting chunk with metadata.")
    print(f"Receiving file: {file_metadata['file_name']}")
    print(f"Total chunks expected: {file_metadata['total_chunks']}")
    
    file_data = receive_file_chunks(cam, file_metadata['total_chunks'])
    save_path, is_successful = save_file_data(directory_to_save_in, file_metadata['file_name'], file_data)
    
    if is_successful:
        print(f"File saved successfully to: {save_path}")
        open_file(save_path)
    else:
        print(f"Failed to save file '{file_metadata['file_name']}'")


def wait_for_starting_chunk(cam):
    """Wait for starting chunk and process the chunk that contains the file metadata"""
    while True:
        print("Scanning for starting chunk")
        qr_data_string = get_next_qr_data(cam)
        payload = decode_qr_data(qr_data_string)
        
        if is_starting_chunk(payload):
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
        print(f"Progress: {progress:.1f}% - Waiting for chunk {received_count + 1}/{total_chunks}")
        
        qr_data_string = get_next_qr_data(cam)
        payload = decode_qr_data(qr_data_string)
        
        if is_data_chunk(payload):
            chunk_id = payload['id']
            chunk_data = payload['data']
            
            # Store chunk data if it's a new one
            if chunk_id not in chunks_data:
                chunks_data[chunk_id] = chunk_data
                received_count += 1
                progress = (received_count / total_chunks) * 100
                send_approval(chunk_id)
            else:
                print(f"Duplicate chunk {chunk_id} received, ignoring")
    time.sleep(1.5) # Added small sleep delay to ensure approval QR is seen by sender
    # Reconstruct file data in correct order
    print("Reconstructing the file from received chunks")
    file_data = b""
    for chunk_id in sorted(chunks_data.keys()):
        file_data += chunks_data[chunk_id]
    
    return file_data

def send_approval(chunk_id):
    """Send approval QR code for received chunk"""
    approval_payload = create_approval_payload(chunk_id)
    approval_qr_string = encode_qr_data(approval_payload)
    close_all_qr_windows() # Close previous approval windows
    
    window_name = f"Approval for chunk {chunk_id}"
    display_qr_centered(approval_qr_string, window_name)
    print(f"Approval QR displayed for chunk {chunk_id} - keeping it visible until next chunk arrives")
