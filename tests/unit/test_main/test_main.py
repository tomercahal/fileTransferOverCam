import unittest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from main import main

class TestMain(unittest.TestCase):
    """Test cases for main.py entry point"""

    @patch('main.sender_main')
    @patch('sys.argv', ['main.py', 'sender'])
    def test_main_sender_mode(self, mock_sender_main):
        """Test main function calls sender_main for sender mode"""
        main()
        mock_sender_main.assert_called_once()

    @patch('main.receiver_main')
    @patch('sys.argv', ['main.py', 'receiver'])
    def test_main_receiver_mode(self, mock_receiver_main):
        """Test main function calls receiver_main for receiver mode"""
        main()
        mock_receiver_main.assert_called_once()

    @patch('main.sender_main')
    @patch('main.receiver_main')
    @patch('sys.argv', ['main.py', 'invalid'])
    def test_main_invalid_mode(self, mock_receiver_main, mock_sender_main):
        """Test main function with invalid mode"""
        main()
        
        # Neither function should be called
        mock_sender_main.assert_not_called()
        mock_receiver_main.assert_not_called()

    @patch('main.sender_main')
    @patch('main.receiver_main')
    @patch('sys.argv', ['main.py'])  # Missing mode argument
    def test_main_missing_argument(self, mock_receiver_main, mock_sender_main):
        """Test main function with missing mode argument"""
        with self.assertRaises(IndexError):
            main()
            
        # Neither function should be called
        mock_sender_main.assert_not_called()
        mock_receiver_main.assert_not_called()

    @patch('main.sender_main')
    @patch('sys.argv', ['main.py', 'sender', 'extra', 'args'])
    def test_main_extra_arguments(self, mock_sender_main):
        """Test main function ignores extra arguments"""
        main()
        
        mock_sender_main.assert_called_once()

if __name__ == '__main__':
    unittest.main()