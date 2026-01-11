import streamlit as st
import os
from dotenv import load_dotenv
from src.engine import process_pdfs, get_retriever
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("🤖 Pro AI Assistant (GPU Accelerated)")

# --- LOGIKA PENYIMPANAN SESI (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Memuat database secara otomatis saat aplikasi pertama kali dibuka
if "retriever" not in st.session_state:
    existing_retriever = get_retriever()
    if existing_retriever:
        st.session_state.retriever = existing_retriever

# --- SIDEBAR: MANAJEMEN DOKUMEN ---
with st.sidebar:
    st.header("📂 Document Center")
    
    if "retriever" in st.session_state:
        st.success("✅ Database Vektor Aktif (Dokumen Tersimpan)")
    else:
        st.info("ℹ️ Belum ada dokumen. Silakan upload PDF.")

    uploaded_files = st.file_uploader(
        "Upload PDF baru ke Database", 
        type="pdf", 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🚀 Proses & Simpan Permanen"):
            temp_paths = []
            for uploaded_file in uploaded_files:
                temp_path = os.path.join("/tmp", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                temp_paths.append(temp_path)
            
            with st.spinner("Mempelajari dokumen di GTX 1050 Ti..."):
                st.session_state.retriever = process_pdfs(temp_paths)
                st.success("Dokumen berhasil ditambahkan!")
                st.rerun() # Refresh agar status database terupdate

    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE CHAT (Gaya ChatGPT) ---
# Menampilkan riwayat percakapan sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input pertanyaan dari pengguna
if prompt := st.chat_input("Tanyakan sesuatu tentang dokumen Anda..."):
    # Tampilkan & simpan pesan pengguna
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "retriever" in st.session_state:
        # Gunakan Groq Llama 3.3 sebagai otak utama
        llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=st.session_state.retriever
        )
        
        with st.chat_message("assistant"):
            with st.spinner("Menganalisis dokumen..."):
                response = qa_chain.invoke(prompt)
                full_response = response["result"]
                st.markdown(full_response)
        
        # Simpan jawaban AI ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.error("Gagal: Database belum siap. Silakan upload dokumen terlebih dahulu.")