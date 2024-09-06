# PDF RAG

PDF RAG is a Python-based project designed to handle PDF files, extract data, and perform various operations using a set of tools and engines. This project includes functionalities for saving notes to Excel, querying population data, and more.

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

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pdf-rag.git
   cd pdf-rag
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Copy `.env.example` to `.env` and fill in the necessary environment variables.

## Usage

1. **Run the Main Script**:
   ```bash
   python main.py
   ```

2. **Interact with the Agent**:
   - Enter prompts to query data or perform operations. Type `q` to quit.

## Project Structure

```
RAGAgent/
├── .env
├── .env.example
├── canada/
│   ├── default__vector_store.json
│   ├── docstore.json
│   ├── graph_store.json
│   ├── image__vector_store.json
│   └── index_store.json
├── data/
│   ├── archive.zip
│   ├── notes.txt
│   ├── pdf/
│   │   └── Canada.pdf
│   └── WorldPopulation2023.csv
├── engines_generator/
│   ├── excel_note_engine.py
│   ├── pdf_engine.py
│   ├── test_excel_note.py
│   ├── test_pdf_engine.py
│   ├── __init__.py
│   └── __pycache__/
├── main.py
├── note_engine.py
├── pdf.py
├── prompts.py
├── readme.md
├── setup_llm.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
