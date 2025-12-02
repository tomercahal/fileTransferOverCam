import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from protocol_utils import divide_into_chunks, create_chunks_to_send, FIRST_CHUNK_ID, STARTING_CHUNK_DATA

class TestChunking(unittest.TestCase):
    """Test cases for chunking functions"""

    def test_divide_into_chunks_default_size(self):
        """Test dividing data with default chunk size (100), should create 3 chunks"""
        data = b"A" * 250  # 250 bytes
        
        chunks = divide_into_chunks(data)
        
        self.assertEqual(len(chunks), 3)  # 100 + 100 + 50
        self.assertEqual(chunks[0], b"A" * 100)
        self.assertEqual(chunks[1], b"A" * 100)
        self.assertEqual(chunks[2], b"A" * 50)

    def test_divide_into_chunks_custom_size(self):
        """Test dividing data with custom chunk size"""
        data = b"Hello World!"  # 12 bytes
        
        chunks = divide_into_chunks(data, size=5)
        
        self.assertEqual(len(chunks), 3)  # 5 + 5 + 2
        self.assertEqual(chunks[0], b"Hello")
        self.assertEqual(chunks[1], b" Worl")
        self.assertEqual(chunks[2], b"d!")

    def test_divide_into_chunks_exact_fit(self):
        """Test dividing data that fits exactly into chunks"""
        data = b"A" * 100  # Exactly 100 bytes
        
        chunks = divide_into_chunks(data, size=50)
        
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], b"A" * 50)
        self.assertEqual(chunks[1], b"A" * 50)

    def test_divide_into_chunks_empty_data(self):
        """Test dividing empty data, should not create any chunks"""
        data = b""
        
        chunks = divide_into_chunks(data)
        
        # Empty data produces no chunks (range(0, 0, 100) is empty)
        self.assertEqual(len(chunks), 0)
        self.assertEqual(chunks, [])

    def test_divide_into_chunks_single_byte(self):
        """Test dividing single byte"""
        data = b"A"
        
        chunks = divide_into_chunks(data, size=100)
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], b"A")

    def test_create_chunks_to_send_large_file(self):
        """Test creating chunks for a larger file"""
        file_name = "large.bin"
        file_data = b"A" * 250  # 250 bytes, will be split into 3 chunks (100+100+50)
        
        chunks = create_chunks_to_send(file_name, file_data)
        
        # Should have 4 chunks: starting chunk + 3 data chunks
        self.assertEqual(len(chunks), 4)
        
        # Starting chunk
        starting_chunk = chunks[0]
        self.assertEqual(starting_chunk["id"], FIRST_CHUNK_ID)
        self.assertEqual(starting_chunk["data"], STARTING_CHUNK_DATA)
        self.assertEqual(starting_chunk["file_name"], "large.bin")
        self.assertEqual(starting_chunk["total_chunks"], 3)  # 3 data chunks
        
        # Data chunks
        self.assertEqual(chunks[1]["id"], 1)
        self.assertEqual(chunks[1]["data"], b"A" * 100)
        
        self.assertEqual(chunks[2]["id"], 2)
        self.assertEqual(chunks[2]["data"], b"A" * 100)
        
        self.assertEqual(chunks[3]["id"], 3)
        self.assertEqual(chunks[3]["data"], b"A" * 50)

    def test_create_chunks_to_send_empty_file(self):
        """Test creating chunks for an empty file"""
        file_name = "empty.txt"
        file_data = b""
        
        chunks = create_chunks_to_send(file_name, file_data)
        
        # Should have 1 chunk: only starting chunk (no data chunks for empty file)
        self.assertEqual(len(chunks), 1)
        
        starting_chunk = chunks[0]
        self.assertEqual(starting_chunk["file_name"], "empty.txt")
        self.assertEqual(starting_chunk["total_chunks"], 0)  # No data chunks

if __name__ == '__main__':
    unittest.main()