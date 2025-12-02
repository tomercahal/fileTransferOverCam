import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from protocol_utils import (
    create_qr_payload, create_first_qr_payload, create_approval_payload,
    FIRST_CHUNK_ID, STARTING_CHUNK_DATA, APPROVED_CHUNK_DATA
)

class TestPayloadCreation(unittest.TestCase):
    """Test cases for payload creation functions"""

    def test_create_qr_payload_basic(self):
        """Test creating a basic QR payload"""
        chunk_data = b"Hello World"
        chunk_id = 5
        
        payload = create_qr_payload(chunk_data, chunk_id)
        
        self.assertEqual(payload["id"], 5)
        self.assertEqual(payload["data"], b"Hello World")
        self.assertEqual(len(payload), 2)  # Only id and data

    def test_create_qr_payload_empty_data(self):
        """Test creating QR payload with empty data"""
        chunk_data = b""
        chunk_id = 0
        
        payload = create_qr_payload(chunk_data, chunk_id)
        
        self.assertEqual(payload["id"], 0)
        self.assertEqual(payload["data"], b"")

    def test_create_qr_payload_binary_data(self):
        """Test creating QR payload with binary data"""
        chunk_data = bytes([0x00, 0x01, 0xFF, 0x80, 0x7F])
        chunk_id = 42
        
        payload = create_qr_payload(chunk_data, chunk_id)
        
        self.assertEqual(payload["id"], 42)
        self.assertEqual(payload["data"], chunk_data)

    def test_create_qr_payload_large_data(self):
        """Test creating QR payload with large data chunk"""
        chunk_data = b"A" * 1000
        chunk_id = 123
        
        payload = create_qr_payload(chunk_data, chunk_id)
        
        self.assertEqual(payload["id"], 123)
        self.assertEqual(payload["data"], chunk_data)
        self.assertEqual(len(payload["data"]), 1000)

    def test_create_first_qr_payload_basic(self):
        """Test creating first QR payload with metadata"""
        file_name = "test.txt"
        file_chunks = [b"chunk1", b"chunk2", b"chunk3"]
        
        payload = create_first_qr_payload(file_name, file_chunks)
        
        self.assertEqual(payload["id"], FIRST_CHUNK_ID)
        self.assertEqual(payload["data"], STARTING_CHUNK_DATA)
        self.assertEqual(payload["file_name"], "test.txt")
        self.assertEqual(payload["total_chunks"], 3)

    def test_create_first_qr_payload_large_file(self):
        """Test creating first QR payload for large file with many chunks"""
        file_name = "large.bin"
        file_chunks = [b"chunk" + str(i).encode() for i in range(100)]  # 100 chunks
        
        payload = create_first_qr_payload(file_name, file_chunks)
        
        self.assertEqual(payload["file_name"], "large.bin")
        self.assertEqual(payload["total_chunks"], 100)

    def test_create_first_qr_payload_unicode_filename(self):
        """Test creating first QR payload with unicode filename"""
        file_name = "tëst_filé_中文.pdf"
        file_chunks = [b"content"]
        
        payload = create_first_qr_payload(file_name, file_chunks)
        
        self.assertEqual(payload["file_name"], "tëst_filé_中文.pdf")
        self.assertEqual(payload["total_chunks"], 1)

    def test_create_approval_payload_basic(self):
        """Test creating approval payload"""
        chunk_id = 5
        
        payload = create_approval_payload(chunk_id)
        
        self.assertEqual(payload["id"], 5)
        self.assertEqual(payload["data"], APPROVED_CHUNK_DATA)
        self.assertEqual(len(payload), 2)  # Only id and data

if __name__ == '__main__':
    unittest.main()