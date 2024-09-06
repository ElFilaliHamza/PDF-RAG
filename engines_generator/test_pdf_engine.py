import unittest
import os
from unittest.mock import patch, MagicMock
from pdf_engine import (
    get_pdf_engine,
    get_pdf_engines_from_folder,
)  # Adjust the import as needed


class TestPDFEngines(unittest.TestCase):

    def setUp(self):
        # Define a temporary directory for testing
        self.test_pdf_folder = "test_pdfs"
        os.makedirs(self.test_pdf_folder, exist_ok=True)

        # Create a mock PDF file
        self.mock_pdf_file = os.path.join(self.test_pdf_folder, "test_document.pdf")
        with open(self.mock_pdf_file, "w") as f:
            f.write("%PDF-1.4\n%Mock PDF content")

    def tearDown(self):
        # Remove the temporary directory and its contents after each test
        if os.path.exists(self.test_pdf_folder):
            for file in os.listdir(self.test_pdf_folder):
                os.remove(os.path.join(self.test_pdf_folder, file))
            os.rmdir(self.test_pdf_folder)

    @patch("pdf_engine.SimpleDirectoryReader")
    @patch("pdf_engine.get_index")
    def test_get_pdf_engine(self, mock_get_index, mock_reader):
        # Mock the behavior of SimpleDirectoryReader and get_index
        mock_reader_instance = MagicMock()
        mock_reader.return_value = mock_reader_instance
        mock_reader_instance.load_data.return_value = "mock data"

        mock_index = MagicMock()
        mock_get_index.return_value = mock_index
        mock_index.as_query_engine.return_value = "mock query engine"

        # Test the get_pdf_engine function
        engine = get_pdf_engine("test_document.pdf", "test_index")
        self.assertEqual(engine, "mock query engine")

    @patch("pdf_engine.get_pdf_engine")
    def test_get_pdf_engines_from_folder(self, mock_get_pdf_engine):
        # Mock the behavior of get_pdf_engine
        mock_get_pdf_engine.return_value = "mock query engine"

        # Test the get_pdf_engines_from_folder function
        pdf_engine = get_pdf_engines_from_folder(self.test_pdf_folder)
        self.assertEqual(len(pdf_engine), 1)
        self.assertEqual(pdf_engine[0], "mock query engine")


if __name__ == "__main__":
    unittest.main()
