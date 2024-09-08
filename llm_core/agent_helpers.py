import os
import pandas as pd
from typing import List
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    SimpleDirectoryReader,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata

from .prompts_setup import new_prompt
from .llm_setup import groq_llm

def create_csv_query_engines_from_folder(folder_path, verbose=False, prompt=new_prompt):
    """
    Creates a list of PandasQueryEngine instances for all CSV files in the specified folder.

    Parameters:
    - folder_path (str): The path to the folder containing CSV files.
    - verbose (bool): Whether to enable verbose mode for the query engines.

    Returns:
    - List[PandasQueryEngine]: A list of PandasQueryEngine instances.
    """
    query_engines = []

    try:
        # Iterate over all files in the specified folder
        for file_name in os.listdir(folder_path):
            # Check if the file is a CSV file
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(file_path)
                except Exception as e:
                    print(f"Error occurred while reading {file_name}: {e}")
                    continue

                try:
                    # Create a PandasQueryEngine instance
                    query_engine = PandasQueryEngine(df=df, verbose=verbose)
                    query_engine.update_prompts({"pandas_prompt": prompt})

                    # Add the query engine to the list
                    query_engines.append(query_engine)
                except Exception as e:
                    print(
                        f"Error occurred while creating query engine for {file_name}: {e}"
                    )
    except Exception as e:
        print(
            f"Error occurred while creating query engines from folder {folder_path}: {e}"
        )

    return query_engines


def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


def create_pdf_engines_from_folder(folder_path):
    """
    Creates a list of query engines for all PDF files in the specified folder.

    Parameters:
    - folder_path (str): The path to the folder containing PDF files.

    Returns:
    - List: A list of query engines for each PDF file.
    """
    query_engines = []

    # Iterate over all files in the specified folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a PDF file
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            # Read the PDF file
            reader = SimpleDirectoryReader(input_files=[file_path])
            pdf_data = reader.load_data()
            # Create an index for the PDF data
            index_name = os.path.splitext(file_name)[
                0
            ]  # Use the file name without extension as index name
            index = get_index(pdf_data, index_name)
            # Convert the index to a query engine
            query_engine = index.as_query_engine()
            # Add the query engine to the list
            query_engines.append(query_engine)

    return query_engines


def generate_description(engine, file_type, index):
    # Extract a sample of content from the query engine
    # This could be a summary, the first few lines, or any other relevant snippet
    sample_content = engine.query(
        "Provide a brief summary or key points of this document."
    )

    # Generate a prompt based on the file type, index, and sample content
    prompt = (
        f"Based on the following content from {file_type} data file {index}, "
        f"provide a brief description: {sample_content}"
    )

    # Use the LLM to generate a description
    response = groq_llm.complete(prompt)
    
    print("This is a description for PDF: ", response.text.strip())
    return response.text.strip()


def create_tools_from_query_engines(csv_engines: List, pdf_engines: List) -> List:
    """
    Creates a list of tools from CSV and PDF query engines.

    Parameters:
    - csv_engines (List): A list of query engines for CSV files.
    - pdf_engines (List): A list of query engines for PDF files.

    Returns:
    - List: A list of QueryEngineTool instances.
    """
    tools = []

    # Create tools for CSV query engines
    for i, engine in enumerate(csv_engines):
        description = generate_description(engine, "CSV", i + 1)
        tool = QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name=f"csv_data_{i+1}",
                description=f"This tool provides insights from CSV data file {i+1}. {description}",
            ),
        )
        tools.append(tool)

    # Create tools for PDF query engines
    for i, engine in enumerate(pdf_engines):
        description = generate_description(engine, "PDF", i + 1)
        tool = QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name=f"pdf_data_{i+1}",
                description=f"This tool provides insights from PDF data file {i+1}. {description}",
            ),
        )
        tools.append(tool)

    return tools
