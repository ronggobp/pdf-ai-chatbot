#!/bin/bash

echo "🚀 Memulai setup otomatis Pro AI Assistant..."

# 1. Mengecek apakah Conda sudah terinstal
if ! command -v conda &> /dev/null
then
    echo "❌ Conda tidak ditemukan. Silakan instal Miniconda/Anaconda terlebih dahulu."
    exit
fi

# 2. Membuat environment baru jika belum ada
echo "📦 Membuat environment Conda: ai_proyek (Python 3.11)..."
conda create -n ai_proyek python=3.11 -y

# 3. Mengaktifkan environment dan menginstal library
echo "🛠️ Menginstal library dari requirements.txt..."
# Menggunakan path langsung ke pip di dalam environment untuk menghindari konflik global
~/miniconda3/envs/ai_proyek/bin/pip install -r requirements.txt

# 4. Membuat file .env jika belum ada (Template)
if [ ! -f .env ]; then
    echo "🔑 Membuat template file .env..."
    echo "GROQ_API_KEY=masukkan_api_key_anda_disini" > .env
    echo "⚠️  Jangan lupa edit file .env dan masukkan GROQ_API_KEY Anda!"
fi

echo "Berikan Izin Eksekusi: chmod +x setup.sh"
echo "Jalankan Script: ./setup.sh"
echo "✅ Setup selesai! Jalankan perintah berikut untuk memulai:"
echo "conda activate ai_proyek && streamlit run app.py"
