import json
import base64

FIRST_CHUNK_ID = 0
STARTING_CHUNK_DATA = b"STARTING"
APPROVED_CHUNK_DATA = b"APPROVED"

def encode_qr_data(payload):
    """Serialize payload to JSON string for QR code"""
    # Convert bytes to base64 for JSON serialization
    serializable_payload = payload.copy()
    serializable_payload["data"] = base64.b64encode(serializable_payload["data"]).decode('utf-8')
    return json.dumps(serializable_payload)

def decode_qr_data(qr_data_str):
    """Deserialize JSON string from QR code back to payload"""
    try:
        payload = json.loads(qr_data_str)
        # Convert base64 back to bytes
        payload["data"] = base64.b64decode(payload["data"])
        return payload
    except (json.JSONDecodeError, ValueError):
        return None

def create_chunks_to_send(file_name, file_data):
    """Divide file data into chunks and create payloads for each chunk"""
    file_chunks = divide_into_chunks(file_data)
    first_chunk = create_first_qr_payload(file_name, file_chunks)
    return [first_chunk] + [create_qr_payload(chunk, i) for i, chunk in enumerate(file_chunks, start=1)]

def divide_into_chunks(data, size=100):
    """Divide data into chunks of given size"""
    return [data[i:i+size] for i in range(0, len(data), size)]

def create_first_qr_payload(file_name, file_chunks):
    """Create the first QR payload containing the file metadata"""
    payload = create_qr_payload(STARTING_CHUNK_DATA, FIRST_CHUNK_ID)
    payload["file_name"] = file_name
    payload["total_chunks"] = len(file_chunks)
    return payload

def create_qr_payload(chunk, chunk_id):
    """Create QR payload for a given chunk"""
    return {
        "id": chunk_id,
        "data": chunk
    }

def check_qr_chunk_approval(qr_data_str, current_chunk):
    """Check if received QR data is approval for current chunk"""
    decoded_data = decode_qr_data(qr_data_str)
    if not decoded_data:
        return False
    return decoded_data.get("id") == current_chunk.get("id") and decoded_data.get("data") == APPROVED_CHUNK_DATA

def create_approval_payload(chunk_id):
    """Create approval payload for a received chunk"""
    return {
        "id": chunk_id,
        "data": APPROVED_CHUNK_DATA
    }

def is_starting_chunk(payload):
    """Check if payload is the starting chunk with metadata"""
    return payload.get("id") == FIRST_CHUNK_ID and payload.get("data") == STARTING_CHUNK_DATA

def is_data_chunk(payload):
    """Check if payload contains file data (not starting or approval)"""
    if not payload:
        return False
    return (payload.get("id", -1) > FIRST_CHUNK_ID and 
            payload.get("data") not in [STARTING_CHUNK_DATA, APPROVED_CHUNK_DATA])
