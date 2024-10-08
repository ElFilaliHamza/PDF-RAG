import os
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    SimpleDirectoryReader,
)


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

pdf_path = os.path.join("data", "pdf", "Canada.pdf")

reader = SimpleDirectoryReader(input_files=[pdf_path])
canada_pdf = reader.load_data()
canada_index = get_index(canada_pdf, "canada")
canada_engine = canada_index.as_query_engine()

