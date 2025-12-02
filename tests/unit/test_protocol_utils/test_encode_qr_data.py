import unittest
import json
import base64
import sys
import os

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from protocol_utils import encode_qr_data


class TestEncodeQrData(unittest.TestCase):
    """Test cases for the encode_qr_data function"""

    def test_encode_simple_text_payload(self):
        """Test encoding a payload with simple text data"""
        payload = {
            "id": 1,
            "data": b"Hello World"
        }
        
        result = encode_qr_data(payload)
        
        # Should return a JSON string
        self.assertIsInstance(result, str)
        
        # Should be valid JSON and match original id for payload
        parsed = json.loads(result)
        self.assertEqual(parsed["id"], 1)
        
        # Data should be base64 encoded
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, b"Hello World")

    def test_encode_empty_data(self):
        """Test encoding a payload with empty data"""
        payload = {
            "id": 0,
            "data": b""
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        
        self.assertEqual(parsed["id"], 0)
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, b"")

    def test_encode_binary_data(self):
        """Test encoding a payload with binary data"""
        binary_data = bytes([0x00, 0x01, 0xFF, 0x80, 0x7F])
        payload = {
            "id": 42,
            "data": binary_data
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        
        self.assertEqual(parsed["id"], 42)
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, binary_data)

    def test_encode_payload_with_metadata(self):
        """Test encoding a payload with additional metadata fields"""
        payload = {
            "id": 0,
            "data": b"STARTING",
            "file_name": "test.txt",
            "total_chunks": 5
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        
        self.assertEqual(parsed["id"], 0)
        self.assertEqual(parsed["file_name"], "test.txt")
        self.assertEqual(parsed["total_chunks"], 5)
        
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, b"STARTING")

    def test_encode_large_data(self):
        """Test encoding a payload with larger data chunk"""
        large_data = b"A" * 1000  # 1KB of data
        payload = {
            "id": 123,
            "data": large_data
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        
        self.assertEqual(parsed["id"], 123)
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, large_data)
        self.assertEqual(len(decoded_data), 1000)

    def test_encode_preserves_original_payload(self):
        """Test that encoding doesn't modify the original payload"""
        original_payload = {
            "id": 1,
            "data": b"test data"
        }
        payload_copy = original_payload.copy()
        
        encode_qr_data(payload_copy)
        
        # Original payload should be unchanged
        self.assertEqual(original_payload, payload_copy)

    def test_encode_unicode_in_metadata(self):
        """Test encoding payload with unicode characters in metadata"""
        payload = {
            "id": 1,
            "data": b"data",
            "file_name": "tëst_filé.txt",  # Unicode characters
            "description": "Tést description 中文"
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        
        self.assertEqual(parsed["file_name"], "tëst_filé.txt")
        self.assertEqual(parsed["description"], "Tést description 中文")

    def test_encode_realistic_file_data(self):
        """Test encoding with realistic file content like JPEG, PDF headers"""
        # JPEG file header
        jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
        payload = {
            "id": 1,
            "data": jpeg_header
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, jpeg_header)
        
        # PDF file header
        pdf_header = b'%PDF-1.4\n%\xf2\xf3\xf4\xf5\xf6\n'
        payload = {
            "id": 2,
            "data": pdf_header
        }
        
        result = encode_qr_data(payload)
        parsed = json.loads(result)
        decoded_data = base64.b64decode(parsed["data"])
        self.assertEqual(decoded_data, pdf_header)

if __name__ == '__main__':
    unittest.main()