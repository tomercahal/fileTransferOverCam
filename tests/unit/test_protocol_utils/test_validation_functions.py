import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from protocol_utils import (
    is_starting_chunk, is_data_chunk, check_qr_chunk_approval,
    create_qr_payload, create_first_qr_payload, create_approval_payload,
    encode_qr_data, FIRST_CHUNK_ID, STARTING_CHUNK_DATA, APPROVED_CHUNK_DATA
)

class TestValidationFunctions(unittest.TestCase):
    """Test cases for validation functions"""

    def test_is_starting_chunk_valid(self):
        """Test is_starting_chunk with valid starting chunk"""
        starting_payload = {
            "id": FIRST_CHUNK_ID,
            "data": STARTING_CHUNK_DATA,
            "file_name": "test.txt",
            "total_chunks": 5
        }
        
        result = is_starting_chunk(starting_payload)
        
        self.assertTrue(result)

    def test_is_starting_chunk_wrong_id(self):
        """Test is_starting_chunk with wrong ID"""
        payload = {
            "id": 1,  # Should be 0
            "data": STARTING_CHUNK_DATA,
            "file_name": "test.txt",
            "total_chunks": 5
        }
        
        result = is_starting_chunk(payload)
        
        self.assertFalse(result)

    def test_is_starting_chunk_wrong_data(self):
        """Test is_starting_chunk with wrong data"""
        payload = {
            "id": FIRST_CHUNK_ID,
            "data": b"WRONG_DATA",
            "file_name": "test.txt",
            "total_chunks": 5
        }
        
        result = is_starting_chunk(payload)
        
        self.assertFalse(result)

    def test_is_starting_chunk_missing_fields(self):
        """Test is_starting_chunk with missing required fields"""
        payload = {
            "id": FIRST_CHUNK_ID
            # Missing data field
        }
        
        result = is_starting_chunk(payload)
        
        self.assertFalse(result)

    def test_is_starting_chunk_none_payload(self):
        """Test is_starting_chunk with None payload"""
        result = is_starting_chunk(None)
        
        self.assertFalse(result)

    def test_is_data_chunk_valid(self):
        """Test is_data_chunk with valid data chunk"""
        data_payload = {
            "id": 1,
            "data": b"Hello World"
        }
        
        result = is_data_chunk(data_payload)
        
        self.assertTrue(result)

    def test_is_data_chunk_starting_chunk(self):
        """Test is_data_chunk with starting chunk (should be false)"""
        starting_payload = {
            "id": FIRST_CHUNK_ID,
            "data": STARTING_CHUNK_DATA
        }
        
        result = is_data_chunk(starting_payload)
        
        self.assertFalse(result)

    def test_is_data_chunk_approval_chunk(self):
        """Test is_data_chunk with approval chunk (should be false)"""
        approval_payload = {
            "id": 1,
            "data": APPROVED_CHUNK_DATA
        }
        
        result = is_data_chunk(approval_payload)
        
        self.assertFalse(result)

    def test_is_data_chunk_none_payload(self):
        """Test is_data_chunk with None payload"""
        result = is_data_chunk(None)
        
        self.assertFalse(result)

    def test_is_data_chunk_missing_id(self):
        """Test is_data_chunk with missing ID field"""
        payload = {
            "data": b"some data"
            # Missing id field
        }
        
        result = is_data_chunk(payload)
        
        self.assertFalse(result)

    def test_is_data_chunk_negative_id(self):
        """Test is_data_chunk with negative ID"""
        payload = {
            "id": -5,
            "data": b"some data"
        }
        
        result = is_data_chunk(payload)
        
        self.assertFalse(result)

    def test_check_qr_chunk_approval_valid(self):
        """Test check_qr_chunk_approval with valid approval"""
        # Create a data chunk
        current_chunk = create_qr_payload(b"some data", 5)
        
        # Create approval for that chunk
        approval_payload = create_approval_payload(5)
        approval_qr_string = encode_qr_data(approval_payload)
        
        result = check_qr_chunk_approval(approval_qr_string, current_chunk)
        
        self.assertTrue(result)

    def test_check_qr_chunk_approval_wrong_id(self):
        """Test check_qr_chunk_approval with wrong chunk ID"""
        current_chunk = create_qr_payload(b"some data", 5)
        
        # Create approval for different chunk
        approval_payload = create_approval_payload(3)
        approval_qr_string = encode_qr_data(approval_payload)
        
        result = check_qr_chunk_approval(approval_qr_string, current_chunk)
        
        self.assertFalse(result)

    def test_check_qr_chunk_approval_wrong_data(self):
        """Test check_qr_chunk_approval with wrong data (not approval)"""
        current_chunk = create_qr_payload(b"some data", 5)
        
        # Create regular data chunk, not approval
        fake_approval = create_qr_payload(b"wrong data", 5)
        fake_qr_string = encode_qr_data(fake_approval)
        
        result = check_qr_chunk_approval(fake_qr_string, current_chunk)
        
        self.assertFalse(result)

    def test_check_qr_chunk_approval_invalid_qr(self):
        """Test check_qr_chunk_approval with invalid QR string"""
        current_chunk = create_qr_payload(b"some data", 5)
        invalid_qr_string = "invalid json data"
        
        result = check_qr_chunk_approval(invalid_qr_string, current_chunk)
        
        self.assertFalse(result)

    def test_check_qr_chunk_approval_first_chunk(self):
        """Test check_qr_chunk_approval with first chunk approval"""
        current_chunk = create_qr_payload(STARTING_CHUNK_DATA, FIRST_CHUNK_ID)
        
        approval_payload = create_approval_payload(FIRST_CHUNK_ID)
        approval_qr_string = encode_qr_data(approval_payload)
        
        result = check_qr_chunk_approval(approval_qr_string, current_chunk)
        
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()