import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from file_utils import select_file_to_send, select_save_directory

class TestDialogFunctions(unittest.TestCase):
    """Test cases for GUI dialog functions"""

    @patch('file_utils.filedialog.askopenfilename')
    @patch('file_utils.tk.Tk')
    def test_select_file_to_send_success(self, mock_tk, mock_askopenfilename):
        """Test successful file selection"""
        # Mock the tkinter root
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock file dialog return
        test_file_path = "/path/to/test/file.txt"
        mock_askopenfilename.return_value = test_file_path
        
        result = select_file_to_send()
        
        # Verify tkinter setup
        mock_tk.assert_called_once()
        mock_root.withdraw.assert_called_once()
        mock_root.attributes.assert_called_once_with('-topmost', True)
        mock_root.update.assert_called_once()
        mock_root.destroy.assert_called_once()
        
        # Verify dialog called correctly
        mock_askopenfilename.assert_called_once_with(
            title="Select file to transfer",
            parent=mock_root
        )
        
        self.assertEqual(result, test_file_path)

    @patch('file_utils.filedialog.askopenfilename')
    @patch('file_utils.tk.Tk')
    def test_select_file_to_send_cancel(self, mock_tk, mock_askopenfilename):
        """Test when user cancels file selection"""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock user canceling dialog (returns empty string)
        mock_askopenfilename.return_value = ""
        
        result = select_file_to_send()
        
        self.assertEqual(result, "")
        mock_root.destroy.assert_called_once()

    @patch('file_utils.filedialog.askdirectory')
    @patch('file_utils.tk.Tk')
    @patch('file_utils.os.getcwd')
    def test_select_save_directory_success(self, mock_getcwd, mock_tk, mock_askdirectory):
        """Test successful directory selection"""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        test_directory = "/path/to/save/directory"
        mock_askdirectory.return_value = test_directory
        
        result = select_save_directory()
        
        # Verify tkinter setup
        mock_tk.assert_called_once()
        mock_root.withdraw.assert_called_once()
        mock_root.attributes.assert_called_once_with('-topmost', True)
        mock_root.update.assert_called_once()
        mock_root.destroy.assert_called_once()
        
        # Verify dialog called correctly
        mock_askdirectory.assert_called_once_with(
            title="Choose the directory to save the file",
            parent=mock_root
        )
        
        self.assertEqual(result, test_directory)
        # Should not call getcwd() when directory is selected
        mock_getcwd.assert_not_called()

    @patch('file_utils.filedialog.askdirectory')
    @patch('file_utils.tk.Tk')
    @patch('file_utils.os.getcwd')
    def test_select_save_directory_cancel(self, mock_getcwd, mock_tk, mock_askdirectory):
        """Test when user cancels directory selection"""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock user canceling dialog
        mock_askdirectory.return_value = ""
        
        # Mock current working directory
        current_dir = "/current/working/directory"
        mock_getcwd.return_value = current_dir
        
        result = select_save_directory()
        
        # Should return current working directory as fallback
        self.assertEqual(result, current_dir)
        mock_getcwd.assert_called_once()

if __name__ == '__main__':
    unittest.main()