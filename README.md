# 🤖 Pro AI Research Assistant - GPU Accelerated (GTX 1050 Ti)

Aplikasi Chatbot PDF cerdas berbasis **RAG (Retrieval-Augmented Generation)** yang dioptimasi untuk menjalankan proses berat secara lokal pada hardware NVIDIA namun tetap memiliki kecepatan respon kilat menggunakan teknologi Cloud.



## 🌟 Fitur Utama
- **Multi-PDF Support**: Mampu mengunggah dan menganalisis banyak dokumen sekaligus secara simultan.
- **Persistent Memory**: Menggunakan **ChromaDB** untuk menyimpan database vektor secara permanen di disk, sehingga data tetap ada meskipun aplikasi dimatikan.
- **Chat History**: Memiliki ingatan percakapan layaknya ChatGPT, memungkinkan diskusi yang mengalir dan kontekstual.
- **GPU Inference**: Proses *embedding* (konversi teks ke vektor) dilakukan 100% pada **NVIDIA GTX 1050 Ti** menggunakan CUDA untuk performa maksimal.
- **Lightning Fast Response**: Menggunakan **Groq API (Llama 3.3-70b)** sebagai otak penalaran utama dengan kecepatan ribuan token per menit.

## 🛠️ Tech Stack
- **Framework**: LangChain v0.3.13 (LTS Version).
- **Vector Store**: `langchain-chroma` (Partner Package terbaru 2026).
- **Embedding Model**: `all-MiniLM-L6-v2` (Running on Local CUDA).
- **LLM**: Meta Llama 3.3 via Groq Cloud.
- **Interface**: Streamlit.

## 📋 Prasyarat Sistem
- **OS**: Windows 11 dengan WSL2 (Ubuntu 24.04 LTS).
- **GPU**: NVIDIA GeForce GTX 1050 Ti (Min. 4GB VRAM).
- **Python**: v3.11 (Conda Environment).

## 🚀 Instalasi & Penggunaan

1. **Kloning Proyek & Masuk ke Folder**
   ```bash
   git clone [https://github.com/ronggobp/pdf-ai-chatbot.git](https://github.com/ronggobp/pdf-ai-chatbot.git)
   cd pdf-ai-chatbot

2. **Setup Environment**
   conda activate ai_proyek
   pip install -r requirements.txt

3. **Konfigurasi API Key Buat file .env dan masukkan kunci Groq Anda:**
   GROQ_API_KEY=gsk_your_key_here

4. **Jalankan Aplikasi**
   streamlit run app.py