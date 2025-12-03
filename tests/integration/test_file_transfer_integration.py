import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sender import wait_for_chunk_approval
from receiver import wait_for_starting_chunk, receive_file_chunks
from protocol_utils import (
    encode_qr_data, create_approval_payload,
    create_chunks_to_send, create_first_qr_payload, create_qr_payload,
)

class TestSenderReceiverIntegration(unittest.TestCase):
    """Integration tests using actual sender and receiver functions - ordered from sender to receiver workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file_path = os.path.join(os.path.dirname(__file__), "test_file.txt")
        
        # Read test file data for use in tests
        with open(self.test_file_path, 'rb') as f:
            self.test_file_data = f.read()

    # ========== The Tests ==========

    def test_receiver_wait_for_starting_chunk_retry_behavior(self):
        """Test receiver retries when encountering non-starting chunks before finding starting chunk"""
        # This tests cross-module integration: protocol validation + receiver retry logic
        test_chunks = [b"chunk1", b"chunk2"]
        starting_payload = create_first_qr_payload("test.txt", test_chunks)
        non_starting_payload = create_qr_payload(b"regular data", 1)
        
        # Create QR strings using real protocol functions
        starting_qr = encode_qr_data(starting_payload)
        non_starting_qr = encode_qr_data(non_starting_payload)
        
        with patch('receiver.get_next_qr_data') as mock_get_qr, \
             patch('receiver.send_approval') as mock_send_approval:
            
            mock_cam = MagicMock()
            # First QR is not starting, second is starting
            mock_get_qr.side_effect = [non_starting_qr, starting_qr]
            
            # Test actual receiver function with real protocol integration
            result = wait_for_starting_chunk(mock_cam)
            
            # Verify retry behavior with real protocol validation
            self.assertEqual(mock_get_qr.call_count, 2)
            mock_send_approval.assert_called_once_with(starting_payload['id'])
            self.assertEqual(result['file_name'], "test.txt")
            self.assertEqual(result['total_chunks'], 2)

    def test_sender_receiver_approval_protocol_integration(self):
        """Test actual sender function waiting for receiver-generated approval QRs"""
        # This tests cross-module integration: sender function + receiver-generated approvals
        test_chunk = create_qr_payload(b"test data", 5)
        
        # Create approval QR like receiver would send
        approval_payload = create_approval_payload(5)
        approval_qr = encode_qr_data(approval_payload)
        
        # Create wrong approval QR 
        wrong_approval = create_approval_payload(3)
        wrong_approval_qr = encode_qr_data(wrong_approval)
        
        # Test actual sender function with receiver-generated approvals
        with patch('sender.get_next_qr_data') as mock_get_qr:
            mock_cam = MagicMock()
            
            # Test sender accepts correct approval from receiver
            mock_get_qr.return_value = approval_qr
            wait_for_chunk_approval(mock_cam, test_chunk)  # Should complete without error
            
            # Test sender rejects wrong approval and retries until correct one
            mock_get_qr.side_effect = [wrong_approval_qr, approval_qr]
            wait_for_chunk_approval(mock_cam, test_chunk)  # Should retry and then succeed
            
            # Verify sender actually called camera twice due to retry
            self.assertEqual(mock_get_qr.call_count, 3)  # 1 from first test + 2 from retry test

    def test_protocol_data_integrity_across_modules(self):
        """Test that data survives the complete sender => protocol => receiver pipeline""" 
        original_data = self.test_file_data
        
        # Sender side: create chunks using protocol functions
        chunks = create_chunks_to_send("test_file.txt", original_data)
        
        # The protocol layer: encode chunks as QR strings (what sender displays)
        transmitted_qr_strings = []
        for chunk in chunks:
            qr_string = encode_qr_data(chunk)  # Sender displays this
            transmitted_qr_strings.append(qr_string)
        
        # The receiver side: use actual receiver functions to process transmitted data
        qr_iterator = iter(transmitted_qr_strings)
        
        with patch('receiver.get_next_qr_data') as mock_get_qr, \
             patch('receiver.send_approval'):
            
            mock_cam = MagicMock()
            mock_get_qr.side_effect = lambda cam: next(qr_iterator)
            
            file_metadata = wait_for_starting_chunk(mock_cam)
            reconstructed_data = receive_file_chunks(mock_cam, file_metadata['total_chunks'])
        
        self.assertIsNotNone(file_metadata)
        self.assertEqual(file_metadata['file_name'], "test_file.txt")
        self.assertEqual(file_metadata['total_chunks'], len(chunks) - 1)  # -1 for starting chunk
        self.assertEqual(reconstructed_data, original_data)

if __name__ == '__main__':
    unittest.main(verbosity=2)