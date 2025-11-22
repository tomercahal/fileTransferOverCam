
from camera_handler import get_next_qr_data, get_web_cam



def receiver_main():
    cam = get_web_cam()
    received_file = False
    file_in_bytes = b""
    while not received_file:
        data = get_next_qr_data(cam)
        file_in_bytes += data
        
        received_file = True

    with open("temp.txt", "wb") as f:
        f.write(file_in_bytes)



