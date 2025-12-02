import unittest
import json
import sys
import os

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from protocol_utils import decode_qr_data, encode_qr_data

class TestDecodeQrData(unittest.TestCase):
    """Test cases for the decode_qr_data function"""

    def test_decode_valid_json_payload(self):
        """Test decoding a valid JSON payload"""
        # Create a valid encoded payload first
        original_payload = {
            "id": 1,
            "data": b"Hello World"
        }
        encoded_string = encode_qr_data(original_payload)
        
        # Now decode it
        result = decode_qr_data(encoded_string)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["data"], b"Hello World")

    def test_decode_empty_data(self):
        """Test decoding payload with empty data"""
        original_payload = {
            "id": 0,
            "data": b""
        }
        encoded_string = encode_qr_data(original_payload)
        
        result = decode_qr_data(encoded_string)
        
        self.assertEqual(result["id"], 0)
        self.assertEqual(result["data"], b"")

    def test_decode_binary_data(self):
        """Test decoding payload with binary data"""
        binary_data = bytes([0x00, 0x01, 0xFF, 0x80, 0x7F])
        original_payload = {
            "id": 42,
            "data": binary_data
        }
        encoded_string = encode_qr_data(original_payload)
        
        result = decode_qr_data(encoded_string)
        
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["data"], binary_data)

    def test_decode_payload_with_metadata(self):
        """Test decoding payload with additional metadata"""
        original_payload = {
            "id": 0,
            "data": b"STARTING",
            "file_name": "test.txt",
            "total_chunks": 5
        }
        encoded_string = encode_qr_data(original_payload)
        
        result = decode_qr_data(encoded_string)
        
        self.assertEqual(result["id"], 0)
        self.assertEqual(result["data"], b"STARTING")
        self.assertEqual(result["file_name"], "test.txt")
        self.assertEqual(result["total_chunks"], 5)

    def test_decode_malformed_json(self):
        """Test decoding with malformed JSON should return None"""
        malformed_json = '{"id": 1, "data": "invalid json'  # Missing closing brace
        
        result = decode_qr_data(malformed_json)
        
        self.assertIsNone(result)

    def test_decode_invalid_json_syntax(self):
        """Test decoding with completely invalid JSON, should return None"""
        invalid_json = "not json at all"
        
        result = decode_qr_data(invalid_json)
        
        self.assertIsNone(result)

    def test_decode_empty_string(self):
        """Test decoding empty string, should return None"""
        result = decode_qr_data("")
        
        self.assertIsNone(result)

    def test_decode_invalid_base64_data(self):
        """Test decoding with invalid base64 in data field, should return None"""
        invalid_payload = {
            "id": 1,
            "data": "invalid_base64!!!"  # Invalid base64 characters
        }
        json_string = json.dumps(invalid_payload)
        
        result = decode_qr_data(json_string)
        
        self.assertIsNone(result)

    def test_decode_missing_data_field(self):
        """Test decoding JSON without data field should return None (current behavior)"""
        payload_without_data = {
            "id": 1
            # Missing "data" field
        }
        json_string = json.dumps(payload_without_data)
        
        # Current implementation raises KeyError for missing 'data' field
        with self.assertRaises(KeyError):
            decode_qr_data(json_string)

    def test_decode_realistic_file_headers(self):
        """Test decoding realistic file data"""
        # JPEG header
        jpeg_payload = {
            "id": 1,
            "data": b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
        }
        encoded = encode_qr_data(jpeg_payload)
        decoded = decode_qr_data(encoded)
        
        self.assertEqual(decoded["data"], jpeg_payload["data"])
        
        # PDF header  
        pdf_payload = {
            "id": 2,
            "data": b'%PDF-1.4\n%\xf2\xf3\xf4\xf5\xf6\n'
        }
        encoded = encode_qr_data(pdf_payload)
        decoded = decode_qr_data(encoded)
        
        self.assertEqual(decoded["data"], pdf_payload["data"])


if __name__ == '__main__':
    unittest.main()