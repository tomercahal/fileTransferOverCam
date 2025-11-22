FIRST_CHUNK_ID = 0
STARTING_CHUNK_DATA = b"STARTING"
APPROVED_CHUNK_DATA = b"APPROVED"

def decode_qr_data(qr_data):
    # Dummy implementation for decoding QR data
    return qr_data

def create_chunks_to_send(file_name, file_data):
    file_chunks = divide_into_chunks(file_data)
    first_chunk = create_first_qr_payload(file_name, file_chunks)
    return [first_chunk] + [create_qr_payload(chunk, i) for i, chunk in enumerate(file_chunks, start=1)]

def divide_into_chunks(data, size=100):
    return [data[i:i+size] for i in range(0, len(data), size)]

def create_first_qr_payload(file_name, file_chunks):
    payload = create_qr_payload(STARTING_CHUNK_DATA, FIRST_CHUNK_ID)
    payload["file_name"] = file_name
    payload["total_chunks"] = len(file_chunks)
    return payload

def create_qr_payload(chunk, chunk_id):
    return {
        "id": chunk_id,
        "data": chunk
    }

def check_qr_chunk_approval(qr_data, current_chunk):
    decoded_data = decode_qr_data(qr_data)
    return decoded_data.get("id") == current_chunk.get("id") and decoded_data.get("data") == APPROVED_CHUNK_DATA