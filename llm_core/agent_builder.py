import os
from llama_index.core.agent import ReActAgent
from .llm_setup import groq_llm
from .agent_helpers import (
    create_tools_from_query_engines,
    create_csv_query_engines_from_folder,
    create_pdf_engines_from_folder,
)
from .prompts_setup import context
from engines_factory.excel_note_engine import excel_note_engine

DATA_FOLDER = "data"
CSV_FOLDER_NAME = "csv"
PDF_FOLDER_NAME = "pdf"


def build_agent(
    data_folder=DATA_FOLDER,
    csv_folder_name=CSV_FOLDER_NAME,
    pdf_folder_name=PDF_FOLDER_NAME,
):
    """
    Builds and returns a ReActAgent with tools created from CSV and PDF query engines.

    Parameters:
    - data_folder (str): The base folder where data is stored.
    - csv_folder_name (str): The folder name for CSV files.
    - pdf_folder_name (str): The folder name for PDF files.

    Returns:
    - ReActAgent: An instance of the ReActAgent configured with the necessary tools.
    """
    print("Setting up the agent...")

    # Create query engines for CSV files
    csv_files_folder = os.path.join(data_folder, csv_folder_name)
    csv_query_engines_list = create_csv_query_engines_from_folder(csv_files_folder)
    print(
        f"{len(csv_query_engines_list)} CSV query engines have been created successfully."
    )

    # Create query engines for PDF files
    pdf_files_folder = os.path.join(data_folder, pdf_folder_name)
    pdf_query_engines_list = create_pdf_engines_from_folder(pdf_files_folder)
    print(
        f"{len(pdf_query_engines_list)} PDF query engines have been created successfully."
    )

    # Create tools from query engines
    tools = create_tools_from_query_engines(
        csv_query_engines_list, pdf_query_engines_list
    )

    # Add excel engine tool to save notes
    tools.append(excel_note_engine)

    # Create the agent
    agent = ReActAgent.from_tools(tools, llm=groq_llm, verbose=True, context=context)

    print("Agent setup is done.")
    return agent


# Example usage
# if __name__ == "__main__":
#     agent = build_agent()
