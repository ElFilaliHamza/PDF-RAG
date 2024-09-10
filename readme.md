# PDF RAG

PDF RAG is a Python-based project designed to handle PDF files, extract data, and perform various operations using a set of tools and engines. This project includes functionalities for saving notes to Excel, querying population data, and more. The application features a modern Tkinter-based graphical user interface for ease of use.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Excel Note Engine**: Save and organize notes in an Excel file.
- **PDF Engine**: Create and manage indices from PDF files.
- **Population Data Query**: Query world population data using a Pandas-based engine.
- **Canada Data Query**: Access detailed information about Canada.
- **Graphical User Interface**: Interact with the application through a modern Tkinter-based interface.

## Installation

1. **Clone the Repository**:
   - Open your terminal or command prompt.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/yourusername/pdf-rag.git
     cd pdf-rag
     ```

2. **Set Up a Virtual Environment**:
   - Create a virtual environment to manage dependencies:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS and Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

3. **Install Dependencies**:
   - Ensure you are in the project directory and the virtual environment is activated.
   - Install the required packages using:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Up Environment Variables**:
   - Copy the example environment file to a new `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file in a text editor and fill in the necessary environment variables as required by your application.

5. **Create Necessary Folders**:
   - Ensure the following directory structure exists. If not, create the directories:
     ```bash
     mkdir -p data/csv
     mkdir -p data/pdf
     ```

## Usage

1. **Run the Application**:
   - Execute the main script to start the Tkinter-based application:
     ```bash
     python app.py
     ```

2. **Interact with the Interface**:
   - Use the graphical interface to add PDFs, submit prompts, and view responses.
   - The interface includes buttons for adding PDFs, clearing the chat, and submitting prompts.
   - Type your prompt in the input field and press Enter or click Submit to interact with the agent.

## Project Structure

```
RAGAgent
├── .env
├── .env.example
├── .gitignore
├── app.py
├── data
│   ├── csv
│   │   └── WorldPopulation2023.csv
│   └── pdf
│       └── Maroc.pdf
├── engines_factory
│   ├── excel_note_engine.py
│   ├── pdf_engine.py
│   ├── test_excel_note.py
│   ├── test_pdf_engine.py
│   └── __init__.py
├── LICENSE
├── llm_core
│   ├── agent_builder.py
│   ├── agent_helpers.py
│   ├── llm_setup.py
│   ├── prompts_setup.py
│   ├── run_agent.py
│   └── __init__.py
├── readme.md
├── requirements.txt
└── __init__.py
```

- **RAGAgent**: Main directory containing all project files.
- **data**: Directory for storing data files such as CSVs and PDFs.
- **engines_factory**: Contains the core engines for handling Excel and PDF operations.
- **llm_core**: Contains logic for building and running the language model agent.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them with clear messages.
4. Push your changes to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.