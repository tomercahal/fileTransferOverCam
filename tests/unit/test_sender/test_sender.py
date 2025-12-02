import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from sender import pick_file, sender_main
from protocol_utils import STARTING_CHUNK_DATA

class TestSender(unittest.TestCase):
    """Test cases for sender.py functions"""

    @patch('sender.read_file_data')
    @patch('sender.select_file_to_send')
    def test_pick_file_success(self, mock_select_file, mock_read_file):
        """Test successful file selection and reading"""
        # Mock file selection
        mock_select_file.return_value = "/path/to/test.txt"
        
        # Mock file reading
        mock_read_file.return_value = ("test.txt", b"file content")
        
        result = pick_file()
        
        mock_select_file.assert_called_once()
        mock_read_file.assert_called_once_with("/path/to/test.txt")
        self.assertEqual(result, ("test.txt", b"file content"))

    @patch('sender.read_file_data')
    @patch('sender.select_file_to_send')
    def test_pick_file_no_selection(self, mock_select_file, mock_read_file):
        """Test when no file is selected"""
        # Mock user canceling file selection
        mock_select_file.return_value = ""
        
        # Mock read_file_data returning None for empty path
        mock_read_file.return_value = (None, b"")
        
        result = pick_file()
        
        mock_select_file.assert_called_once()
        mock_read_file.assert_called_once_with("")
        self.assertEqual(result, (None, b""))

    @patch('sender.read_file_data')
    @patch('sender.select_file_to_send')
    def test_pick_file_read_error(self, mock_select_file, mock_read_file):
        """Test when file reading fails"""
        mock_select_file.return_value = "/path/to/missing.txt"
        
        # Mock file read failure
        mock_read_file.return_value = (None, b"")
        
        result = pick_file()
        
        mock_select_file.assert_called_once()
        mock_read_file.assert_called_once_with("/path/to/missing.txt")
        self.assertEqual(result, (None, b""))

    # No need for unit tests for display_qr_for_chunk and wait_for_chunk_approval
    # as they involve GUI and camera interaction which are better suited for integration tests and there isn't any logical branching to test.

    @patch('sender.close_qr_window')
    @patch('sender.wait_for_chunk_approval')
    @patch('sender.display_qr_for_chunk')
    @patch('sender.create_chunks_to_send')
    @patch('sender.pick_file')
    @patch('sender.get_web_cam')
    def test_sender_main_success(self, mock_get_cam, mock_pick_file, mock_create_chunks, 
                                mock_display_qr, mock_wait_approval, mock_close_window):
        """Test successful sender main workflow"""
        # Mock camera
        mock_cam = MagicMock()
        mock_get_cam.return_value = mock_cam
        
        # Mock file selection
        mock_pick_file.return_value = ("test.txt", b"file content")
        
        # Mock chunks creation
        mock_chunks = [
            {"id": 0, "data": STARTING_CHUNK_DATA},
            {"id": 1, "data": b"chunk1"},
            {"id": 2, "data": b"chunk2"}
        ]
        mock_create_chunks.return_value = mock_chunks
        
        sender_main()
        
        # Verify workflow calls
        mock_get_cam.assert_called_once()
        mock_pick_file.assert_called_once()
        mock_create_chunks.assert_called_once_with("test.txt", b"file content")
        
        # Verify each chunk processed
        self.assertEqual(mock_display_qr.call_count, 3)
        self.assertEqual(mock_wait_approval.call_count, 3)
        self.assertEqual(mock_close_window.call_count, 3)

    @patch('sender.pick_file')
    @patch('sender.get_web_cam')
    def test_sender_main_no_file_selected(self, mock_get_cam, mock_pick_file):
        """Test sender main when no file is selected"""
        # Mock camera
        mock_get_cam.return_value = MagicMock()
        
        # Mock no file selected
        mock_pick_file.return_value = (None, b"")
        
        sender_main()
        
        mock_get_cam.assert_called_once()
        mock_pick_file.assert_called_once()
        # Should return early without further processing

if __name__ == '__main__':
    unittest.main()