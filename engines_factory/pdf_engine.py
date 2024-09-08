import os
import logging
from typing import List
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    SimpleDirectoryReader,
)


logger = logging.getLogger(__name__)
PDF_DATA_FOLDER = "data/pdf"


def get_index(data, index_name):
    """
    Given a set of data and an index name, returns a VectorStoreIndex that is
    built from the data. If the index_name already exists, it loads the index
    from the existing file. If the index_name does not exist, it builds the index
    from the data and saves it to the given index name.

    Args:
        data (iterable): The data to build the index from.
        index_name (str): The name of the index to build or load.

    Returns:
        VectorStoreIndex: The VectorStoreIndex built from the data.
    """
    index = None
    if not os.path.exists(index_name):
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


def get_pdf_engine(pdf_file: str, index_name: str):
    """
    Given a PDF file and an index name, returns a VectorStoreQueryEngine that is
    built from the PDF file. If the index_name already exists, it loads the index
    from the existing file. If the index_name does not exist, it builds the index
    from the PDF file and saves it to the given index name.

    Args:
        pdf_file (str): The name of the PDF file.
        index_name (str): The name of the index to build or load.

    Returns:
        Optional[VectorStoreQueryEngine]: The VectorStoreQueryEngine built from the PDF file.
            If there is an error while building the index, it returns None.
    """
    try:
        # Build the path to the PDF file
        pdf_path = os.path.join(PDF_DATA_FOLDER, pdf_file)

        # Load the PDF file using the SimpleDirectoryReader
        pdf_reader = SimpleDirectoryReader(input_files=[pdf_path])
        pdf_data = pdf_reader.load_data()

        # Build the index from the PDF data
        pdf_index = get_index(pdf_data, index_name)

        # Log a success message
        logger.info(f"Successfully created index for {pdf_file}")

        # Return the QueryEngine built from the index
        return pdf_index.as_query_engine()
    except Exception as e:
        # Log an error message if there is an error while building the index
        logger.error(f"Failed to create index for {pdf_file}. Error was {e}")

        # Return None if there is an error
        return None


def get_pdf_engines_from_folder(
    pdf_folder: str,
) -> List:
    """
    Creates a list of VectorStoreQueryEngines from all PDF files in a given folder.
    The index name for each PDF is derived from the PDF file name.

    Args:
        pdf_folder (str): The path to the folder containing PDF files.

    Returns:
        List[Optional[VectorStoreQueryEngine]]: A list of VectorStoreQueryEngines for each PDF file.
            If an engine cannot be created for a PDF, None is added to the list for that file.
    """
    pdf_engines = []

    # Iterate over all files in the specified folder
    for pdf_file in os.listdir(pdf_folder):
        # Check if the file is a PDF
        if pdf_file.endswith(".pdf"):
            # Use the file name (without extension) as the index name
            index_name = os.path.splitext(pdf_file)[0]

            # Get the PDF engine for the current file
            pdf_engine = get_pdf_engine(pdf_file, index_name)

            # Append the result to the list
            pdf_engines.append(pdf_engine)

    return pdf_engines
