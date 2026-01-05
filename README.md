# 🤖 AI PDF Chatbot - GTX 1050 Ti Optimized

Aplikasi Full Stack Machine Learning yang memungkinkan pengguna berdiskusi dengan dokumen PDF secara cerdas menggunakan arsitektur RAG (Retrieval-Augmented Generation).

## 🚀 Fitur Unggulan
- **Hybrid Inference**: Pemrosesan dokumen dilakukan secara lokal di GPU **GTX 1050 Ti**, sementara logika bahasa menggunakan **Groq API (Llama 3)** untuk kecepatan maksimal.
- **Local Embedding**: Menggunakan `all-MiniLM-L6-v2` yang berjalan di CUDA untuk efisiensi VRAM.
- **Persistent Knowledge**: (Coming Soon) Rencana integrasi ChromaDB untuk penyimpanan dokumen jangka panjang.

## 🛠️ Tech Stack
- **Framework**: LangChain (v0.3.13 LTS)
- **Interface**: Streamlit
- **Model**: Llama 3 via Groq Cloud
- **Vector DB**: FAISS
- **Hardware**: NVIDIA GeForce GTX 1050 Ti (4GB VRAM)

## 📦 Cara Instalasi
1. Clone repository ini.
2. Buat environment Conda dengan Python 3.11.
3. Instal library: `pip install langchain langchain-community langchain-openai streamlit pypdf faiss-cpu python-dotenv`.
4. Tambahkan `GROQ_API_KEY` Anda di file `.env`.
5. Jalankan aplikasi: `streamlit run app.py`.