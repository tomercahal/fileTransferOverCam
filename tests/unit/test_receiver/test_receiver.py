import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from receiver import wait_for_starting_chunk, receive_file_chunks, send_approval, receiver_main
from protocol_utils import STARTING_CHUNK_DATA, APPROVED_CHUNK_DATA

class TestReceiver(unittest.TestCase):
    """Test cases for receiver.py functions"""

    @patch('receiver.send_approval')
    @patch('receiver.is_starting_chunk')
    @patch('receiver.decode_qr_data')
    @patch('receiver.get_next_qr_data')
    def test_wait_for_starting_chunk_success(self, mock_get_qr, mock_decode, mock_is_starting, mock_send_approval):
        """Test successful starting chunk reception"""
        cam = MagicMock()
        
        # Mock QR data reception
        mock_get_qr.return_value = "starting_qr_string"
        
        # Mock payload decoding
        starting_payload = {
            'id': 0,
            'data': STARTING_CHUNK_DATA,
            'file_name': 'test.txt',
            'total_chunks': 3
        }
        mock_decode.return_value = starting_payload
        
        # Mock starting chunk validation
        mock_is_starting.return_value = True
        
        result = wait_for_starting_chunk(cam)
        
        # Verify calls
        mock_get_qr.assert_called_once_with(cam)
        mock_decode.assert_called_once_with("starting_qr_string")
        mock_is_starting.assert_called_once_with(starting_payload)
        mock_send_approval.assert_called_once_with(0)
        
        # Verify returned metadata
        expected_metadata = {
            'file_name': 'test.txt',
            'total_chunks': 3
        }
        self.assertEqual(result, expected_metadata)

    @patch('receiver.send_approval')
    @patch('receiver.is_starting_chunk')
    @patch('receiver.decode_qr_data')
    @patch('receiver.get_next_qr_data')
    def test_wait_for_starting_chunk_retry(self, mock_get_qr, mock_decode, mock_is_starting, mock_send_approval):
        """Test starting chunk reception with retry"""
        cam = MagicMock()
        
        # Mock QR data reception - first wrong, then correct
        mock_get_qr.side_effect = ["wrong_qr", "starting_qr"]
        
        # Mock payload decoding - first None, then valid
        starting_payload = {
            'id': 0,
            'data': STARTING_CHUNK_DATA,
            'file_name': 'test.txt',
            'total_chunks': 2
        }
        mock_decode.side_effect = [None, starting_payload]
        
        # Mock starting chunk validation - called twice, first False (None payload), then True
        mock_is_starting.side_effect = [False, True]
        
        result = wait_for_starting_chunk(cam)
        
        # Should retry until valid starting chunk
        self.assertEqual(mock_get_qr.call_count, 2)
        self.assertEqual(mock_decode.call_count, 2)
        mock_send_approval.assert_called_once_with(0) # Didn't go inside the if

    @patch('receiver.send_approval')
    @patch('receiver.is_data_chunk')
    @patch('receiver.decode_qr_data')
    @patch('receiver.get_next_qr_data')
    def test_receive_file_chunks_success(self, mock_get_qr, mock_decode, mock_is_data, mock_send_approval):
        """Test successful file chunk reception"""
        cam = MagicMock()
        total_chunks = 2
        
        # Mock chunk payloads
        chunk1_payload = {'id': 1, 'data': b'chunk1_data'}
        chunk2_payload = {'id': 2, 'data': b'chunk2_data'}
        
        # Mock QR reception and decoding
        mock_get_qr.side_effect = ["chunk1_qr", "chunk2_qr"]
        mock_decode.side_effect = [chunk1_payload, chunk2_payload]
        mock_is_data.return_value = True
        
        result = receive_file_chunks(cam, total_chunks)
        
        # Verify reconstructed file data
        expected_data = b'chunk1_datachunk2_data'
        self.assertEqual(result, expected_data)
        
        # Verify approval sent for each chunk
        self.assertEqual(mock_send_approval.call_count, 2)
        mock_send_approval.assert_any_call(1)
        mock_send_approval.assert_any_call(2)

    @patch('receiver.send_approval')
    @patch('receiver.is_data_chunk')
    @patch('receiver.decode_qr_data')
    @patch('receiver.get_next_qr_data')
    def test_receive_file_chunks_with_duplicates(self, mock_get_qr, mock_decode, mock_is_data, mock_send_approval):
        """Test file chunk reception with duplicate chunks"""
        cam = MagicMock()
        total_chunks = 2
        
        # Mock chunk payloads (including duplicate)
        chunk1_payload = {'id': 1, 'data': b'chunk1_data'}
        chunk1_duplicate = {'id': 1, 'data': b'chunk1_data'}
        chunk2_payload = {'id': 2, 'data': b'chunk2_data'}
        
        # Mock QR reception and decoding
        mock_get_qr.side_effect = ["chunk1_qr", "chunk1_duplicate_qr", "chunk2_qr"]
        mock_decode.side_effect = [chunk1_payload, chunk1_duplicate, chunk2_payload]
        mock_is_data.return_value = True
        
        result = receive_file_chunks(cam, total_chunks)
        
        # Should ignore duplicate and reconstruct correctly
        expected_data = b'chunk1_datachunk2_data'
        self.assertEqual(result, expected_data)
        
        # Should only send approval for unique chunks
        self.assertEqual(mock_send_approval.call_count, 2)
        mock_send_approval.assert_any_call(1)
        mock_send_approval.assert_any_call(2)

    @patch('receiver.send_approval')
    @patch('receiver.is_data_chunk')
    @patch('receiver.decode_qr_data')
    @patch('receiver.get_next_qr_data')
    def test_receive_file_chunks_out_of_order(self, mock_get_qr, mock_decode, mock_is_data, mock_send_approval):
        """Test file chunk reception with out-of-order chunks"""
        cam = MagicMock()
        total_chunks = 3
        
        # Mock chunk payloads (out of order)
        chunk3_payload = {'id': 3, 'data': b'chunk3'}
        chunk1_payload = {'id': 1, 'data': b'chunk1'}
        chunk2_payload = {'id': 2, 'data': b'chunk2'}
        
        # Mock QR reception and decoding
        mock_get_qr.side_effect = ["chunk3_qr", "chunk1_qr", "chunk2_qr"]
        mock_decode.side_effect = [chunk3_payload, chunk1_payload, chunk2_payload]
        mock_is_data.return_value = True
        
        result = receive_file_chunks(cam, total_chunks)
        
        # Should reconstruct in correct order regardless of reception order
        expected_data = b'chunk1chunk2chunk3'
        self.assertEqual(result, expected_data)

    @patch('receiver.display_qr_centered')
    @patch('receiver.close_all_qr_windows')
    @patch('receiver.encode_qr_data')
    @patch('receiver.create_approval_payload')
    def test_send_approval(self, mock_create_approval, mock_encode_qr, mock_close_windows, mock_display_qr):
        """Test sending approval QR code"""
        chunk_id = 5
        
        # Mock approval payload creation
        approval_payload = {'id': 5, 'data': APPROVED_CHUNK_DATA}
        mock_create_approval.return_value = approval_payload
        
        # Mock QR encoding
        mock_encode_qr.return_value = "approval_qr_string"
        
        send_approval(chunk_id)
        
        # Verify workflow
        mock_create_approval.assert_called_once_with(chunk_id)
        mock_encode_qr.assert_called_once_with(approval_payload)
        mock_close_windows.assert_called_once()
        
        expected_window_name = "Approval for chunk 5"
        mock_display_qr.assert_called_once_with("approval_qr_string", expected_window_name)

    @patch('receiver.open_file')
    @patch('receiver.save_file_data')
    @patch('receiver.receive_file_chunks')
    @patch('receiver.wait_for_starting_chunk')
    @patch('receiver.select_save_directory')
    @patch('receiver.get_web_cam')
    def test_receiver_main_success(self, mock_get_cam, mock_select_dir, mock_wait_start, 
                                  mock_receive_chunks, mock_save_file, mock_open_file):
        """Test successful receiver main workflow"""
        # Mock camera and directory
        mock_cam = MagicMock()
        mock_get_cam.return_value = mock_cam
        mock_select_dir.return_value = "/save/directory"
        
        # Mock starting chunk
        file_metadata = {'file_name': 'test.txt', 'total_chunks': 2}
        mock_wait_start.return_value = file_metadata
        
        # Mock file chunks reception
        mock_receive_chunks.return_value = b"complete file data"
        
        # Mock successful file save
        mock_save_file.return_value = ("/save/directory/test.txt", True)
        
        receiver_main()
        
        # Verify workflow
        mock_get_cam.assert_called_once()
        mock_select_dir.assert_called_once()
        mock_wait_start.assert_called_once_with(mock_cam)
        mock_receive_chunks.assert_called_once_with(mock_cam, 2)
        mock_save_file.assert_called_once_with("/save/directory", "test.txt", b"complete file data")
        mock_open_file.assert_called_once_with("/save/directory/test.txt")

    @patch('receiver.open_file')
    @patch('receiver.save_file_data')
    @patch('receiver.receive_file_chunks')
    @patch('receiver.wait_for_starting_chunk')
    @patch('receiver.select_save_directory')
    @patch('receiver.get_web_cam')
    def test_receiver_main_save_failure(self, mock_get_cam, mock_select_dir, mock_wait_start,
                                       mock_receive_chunks, mock_save_file, mock_open_file):
        """Test receiver main when file save fails"""
        # Mock camera and directory
        mock_cam = MagicMock()
        mock_get_cam.return_value = mock_cam
        mock_select_dir.return_value = "/save/directory"
        
        # Mock starting chunk
        file_metadata = {'file_name': 'test.txt', 'total_chunks': 1}
        mock_wait_start.return_value = file_metadata
        
        # Mock file chunks reception
        mock_receive_chunks.return_value = b"file data"
        
        # Mock failed file save
        mock_save_file.return_value = (None, False)
        
        receiver_main()
        
        # Verify workflow - should not try to open file on save failure
        mock_save_file.assert_called_once_with("/save/directory", "test.txt", b"file data")
        mock_open_file.assert_not_called()

if __name__ == '__main__':
    unittest.main()