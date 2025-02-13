# System Information Stealer & Security Monitoring Stealer

## 📌 Deskripsi
Script ini digunakan untuk mengumpulkan informasi sistem secara mendalam serta melakukan monitoring keamanan dan forensik digital dan bisa juga digunakan sebagai InfoStealer. Hasil dari pengambilan data ini dapat dikirim langsung ke Pastebin untuk analisis lebih lanjut.

## 🛠️ Fitur Utama
- **Informasi Sistem**: Host Name, OS Name, OS Version, BIOS, Processor, RAM, Virtual Memory, dll.
- **Encoding**: Obfuscate Content dengan Base64
- **Monitoring Keamanan**:
  - Deteksi proses mencurigakan
  - Cek file startup (AutoRun programs)
  - Cek user dengan akses admin
  - Deteksi DNS hijacking
  - Cek status Windows Defender
  - Log perintah command prompt yang dieksekusi
  - Monitoring penggunaan CPU, RAM, dan Disk
- **Monitoring Jaringan**:
  - Deteksi koneksi mencurigakan ke IP luar negeri
  - Cek aplikasi yang menggunakan bandwidth besar
  - Monitoring status kartu jaringan (NIC)

## 📥 Instalasi
1. **Clone Repository**:
   ```sh
   git clone https://github.com/ArenaldyP/Pastebin-InfoStealer.git
   ```
2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## 🔧 Konfigurasi Pastebin API
Untuk mengirim data ke Pastebin, masukkan API Key dan kredensial akun di dalam script:
```python
username = "Username"
password = "Password"
api_dev_key = "your_pastebin_api_key"
```

## 📋 Output
Script akan menghasilkan output berupa file log yang berisi informasi sistem dan keamanan. Jika dikonfigurasi, data ini juga dapat langsung dikirim ke Pastebin.

## 🛡️ Legal Disclaimer
Script ini dibuat untuk tujuan edukasi dan penelitian keamanan siber. **Dilarang digunakan untuk aktivitas ilegal!**


