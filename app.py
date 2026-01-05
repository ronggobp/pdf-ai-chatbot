import streamlit as st
from dotenv import load_dotenv
from src.engine import process_pdf
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os

load_dotenv() # Tambahkan ini untuk membaca file .env

st.set_page_config(page_title="AI PDF Chatbot", layout="centered")
st.title("🤖 Chat dengan Dokumen (Pro) - GTX 1050 Ti Ready")

# Sidebar untuk upload
with st.sidebar:
    st.header("Upload Center")
    uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")

if uploaded_file:
    # Simpan file sementara di WSL
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Sedang mempelajari dokumen..."):
        # Inisialisasi retriever dari engine.py
        retriever = process_pdf("temp.pdf")
        
        # Setup Model (Menggunakan Groq/OpenAI lewat API)
        llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1", # Jika pakai Groq
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile" # Model super cepat
        )
        
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        st.success("Dokumen siap didiskusikan!")

    # Chat Interface
    user_input = st.text_input("Tanyakan sesuatu tentang PDF ini:")
    if user_input:
        with st.chat_message("assistant"):
            response = qa_chain.invoke(user_input)
            st.write(response["result"])