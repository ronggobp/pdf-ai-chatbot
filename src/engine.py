import os
from .processor import load_and_split_pdfs
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma # UBAH INI: dari community ke langchain-chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'}
    )

def get_retriever():
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        # Memuat database menggunakan library baru
        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=get_embeddings()
        )
        return vectorstore.as_retriever()
    return None

def process_pdfs(pdf_paths):
    splits = load_and_split_pdfs(pdf_paths) # Memanggil fungsi dari processor.py
    
    # Logika penambahan dokumen tetap sama, hanya class Chroma yang sekarang lebih cepat
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())
        vectorstore.add_documents(splits)
    else:
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=get_embeddings(),
            persist_directory=DB_DIR
        )
    
    return vectorstore.as_retriever()