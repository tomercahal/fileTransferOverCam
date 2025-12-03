from camera_handler import get_next_qr_data, get_web_cam
from protocol_utils import check_qr_chunk_approval, create_chunks_to_send, encode_qr_data
from display_utils import display_qr_centered, close_qr_window
from file_utils import select_file_to_send, read_file_data

def sender_main():
    """Main sender function that processes outgoing QR codes and sends the file"""
    cam = get_web_cam()
    file_name, file_data = pick_file()
    if not file_name:
        print("No file selected, aborting.")
        return

    chunks_to_send = create_chunks_to_send(file_name, file_data)
    for chunk in chunks_to_send:
        print(f"Sending chunk {chunk['id']}")
        qr_window_name = f"Chunk {chunk['id']} - Sender QR"
        display_qr_for_chunk(chunk, qr_window_name)
        wait_for_chunk_approval(cam, chunk)
        close_qr_window(qr_window_name)
    print(f"File '{file_name}' sent successfully! All {len(chunks_to_send)} chunks transferred.")

def pick_file():
    """Let's user select a file from the file explorer and reads the file content"""
    file_path = select_file_to_send()
    return read_file_data(file_path)

def wait_for_chunk_approval(cam, chunk):
    """Wait for approval QR code from receiver for the given chunk"""
    print(f"Waiting for approval from receiver for chunk {chunk['id']}")
    received_approval = False
    
    while not received_approval:
        qr_data_string = get_next_qr_data(cam)
        if check_qr_chunk_approval(qr_data_string, chunk):
            print(f"Approval received for chunk {chunk['id']}!")
            received_approval = True
        else:
            print("Waiting for correct approval")
    print(f"Chunk {chunk['id']} confirmed, moving to next")

def display_qr_for_chunk(chunk, qr_window_name):
    """Display QR code for the given chunk"""
    qr_data_string = encode_qr_data(chunk)
    display_qr_centered(qr_data_string, qr_window_name)
