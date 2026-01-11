import streamlit as st
import os
from dotenv import load_dotenv
from src.engine import process_pdfs, get_retriever
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

st.set_page_config(page_title="Pro AI Research Assistant", layout="wide")
st.title("🤖 Pro AI Assistant (GPU & Chroma Optimized)")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    existing_retriever = get_retriever()
    if existing_retriever:
        st.session_state.retriever = existing_retriever

with st.sidebar:
    st.header("📂 Document Center")
    if "retriever" in st.session_state:
        st.success("✅ Database Vektor Aktif")
    
    uploaded_files = st.file_uploader("Upload PDF baru", type="pdf", accept_multiple_files=True)
    if uploaded_files and st.button("🚀 Proses Dokumen"):
        temp_paths = []
        for uploaded_file in uploaded_files:
            temp_path = os.path.join("/tmp", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_paths.append(temp_path)
        
        with st.spinner("Mengoptimasi database di GTX 1050 Ti..."):
            st.session_state.retriever = process_pdfs(temp_paths)
            st.success("Berhasil diupdate!")
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "retriever" in st.session_state:
        llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=st.session_state.retriever
        )
        
        with st.chat_message("assistant"):
            response = qa_chain.invoke(prompt)
            full_response = response["result"]
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})