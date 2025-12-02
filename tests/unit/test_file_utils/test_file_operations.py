import unittest
import tempfile
import os
import sys
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from file_utils import read_file_data, save_file_data, open_file

class TestFileOperations(unittest.TestCase):
    """Test cases for file I/O operations (non-GUI functions)"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(self.cleanup_temp_dir)

    def cleanup_temp_dir(self):
        """Clean up temporary directory"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_read_file_data_text_file(self):
        """Test reading a text file"""
        # Create test file
        test_content = b"Hello World!\nThis is a test file."
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "wb") as f:
            f.write(test_content)

        filename, data = read_file_data(test_file)

        self.assertEqual(filename, "test.txt")
        self.assertEqual(data, test_content)

    def test_read_file_data_binary_file(self):
        """Test reading a binary file"""
        # Create binary test file
        binary_content = bytes([0x00, 0x01, 0xFF, 0x80, 0x7F] * 20)
        test_file = os.path.join(self.temp_dir, "test.bin")
        with open(test_file, "wb") as f:
            f.write(binary_content)

        filename, data = read_file_data(test_file)

        self.assertEqual(filename, "test.bin")
        self.assertEqual(data, binary_content)

    def test_read_file_data_empty_file(self):
        """Test reading an empty file"""
        test_file = os.path.join(self.temp_dir, "empty.txt")
        with open(test_file, "wb") as f:
            pass  # Create empty file

        filename, data = read_file_data(test_file)

        self.assertEqual(filename, "empty.txt")
        self.assertEqual(data, b"")

    def test_read_file_data_unicode_filename(self):
        """Test reading file with unicode filename"""
        test_content = b"Unicode content"
        # Create file with unicode name
        unicode_filename = "tëst_filé_中文.txt"
        test_file = os.path.join(self.temp_dir, unicode_filename)
        with open(test_file, "wb") as f:
            f.write(test_content)

        filename, data = read_file_data(test_file)

        self.assertEqual(filename, unicode_filename)
        self.assertEqual(data, test_content)

    def test_read_file_data_nonexistent_file(self):
        """Test reading a file that doesn't exist"""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")

        filename, data = read_file_data(nonexistent_file)
        self.assertIsNone(filename)
        self.assertEqual(data, b"")

    def test_save_file_data_text_content(self):
        """Test saving text content to file"""
        content = b"Hello World!\nThis is test content."
        filename = "output.txt"
        
        save_path, is_successful = save_file_data(self.temp_dir, filename, content)
        
        expected_path = os.path.join(self.temp_dir, filename)
        self.assertTrue(is_successful)
        self.assertEqual(save_path, expected_path)
        
        # Verify file was created and content is correct
        self.assertTrue(os.path.exists(save_path))
        with open(save_path, "rb") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, content)

    def test_save_file_data_unicode_filename(self):
        """Test saving file with unicode filename"""
        content = b"Unicode test content"
        unicode_filename = "tëst_ñämé_中文.txt"
        
        save_path, is_successful = save_file_data(self.temp_dir, unicode_filename, content)
        
        self.assertTrue(is_successful)
        self.assertTrue(os.path.exists(save_path))
        with open(save_path, "rb") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, content)

    def test_save_file_data_nonexistent_directory(self):
        """Test saving to a directory that doesn't exist"""
        nonexistent_dir = os.path.join(self.temp_dir, "nonexistent")
        content = b"test content"
        
        save_path, is_successful = save_file_data(nonexistent_dir, "test.txt", content)
        
        self.assertFalse(is_successful)
        self.assertIsNone(save_path)

    @patch('file_utils.os.startfile')
    def test_open_file_success(self, mock_startfile):
        """Test successfully opening a file"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        
        open_file(test_file)
        
        mock_startfile.assert_called_once_with(test_file)

    @patch('file_utils.os.startfile')
    def test_open_file_exception(self, mock_startfile):
        """Test handling exception when opening file"""
        mock_startfile.side_effect = OSError("File association not found")
        test_file = os.path.join(self.temp_dir, "test.txt")
        
        # Should not raise exception, just print error
        open_file(test_file)
        
        mock_startfile.assert_called_once_with(test_file)

if __name__ == '__main__':
    unittest.main()