import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_pdfs(pdf_paths):
    """Fungsi khusus untuk membaca PDF dan memotongnya menjadi chunk."""
    all_docs = []
    for path in pdf_paths:
        if os.path.exists(path):
            loader = PyPDFLoader(path)
            all_docs.extend(loader.load())
    
    # Membagi teks menjadi potongan 1000 karakter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(all_docs)