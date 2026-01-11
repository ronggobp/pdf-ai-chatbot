import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"

def get_embeddings():
    """Mengaktifkan model embedding pada GPU GTX 1050 Ti."""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'} # Memastikan penggunaan CUDA
    )

def get_retriever():
    """Memuat database permanen dari disk jika tersedia."""
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=get_embeddings()
        )
        return vectorstore.as_retriever()
    return None

def process_pdfs(pdf_paths):
    """Memproses PDF baru dan menambahkannya ke database ChromaDB."""
    all_docs = []
    for path in pdf_paths:
        if os.path.exists(path):
            loader = PyPDFLoader(path)
            all_docs.extend(loader.load())
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    # Jika database sudah ada, tambahkan dokumen baru. Jika belum, buat baru.
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