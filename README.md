# 📚 Sistem Kegiatan Mahasiswa

Aplikasi ini dibangun dengan **Python + Streamlit** untuk mengelola kegiatan mahasiswa. Terdapat 3 peran pengguna: **Admin**, **Pengelola**, dan **Mahasiswa**.

---

## Fitur Aplikasi

### Admin
- Kelola data **pengelola**
- Kelola data **mahasiswa**

### Pengelola
- Kelola **kegiatan**
- Kelola **pendaftaran kegiatan**
- Kelola **absensi**
- Kelola **sertifikat**
- Kelola **notifikasi**

### Mahasiswa
- Melihat dan mendaftar kegiatan yang tersedia
- Melihat **riwayat kegiatan**
- Melihat **absensi**, **sertifikat**, dan **notifikasi**

---

## Login & Registrasi

Di halaman utama, pengguna bisa **login** atau **register**.

### Contoh Akun:
| Peran       | Username / NIM | Password   |
|-------------|----------------|------------|
| Admin       | isa            | isa123     |
| Pengelola   | laila          | laila123   |
| Mahasiswa   | 123            | tata123    |

---

## Penjelasan Folder
- `app.py`: file utama untuk menjalankan aplikasi.
- `koneksi.py`: konfigurasi koneksi ke database.
- Folder `hal/`: berisi halaman untuk Admin, Pengelola, dan Mahasiswa.


---

## Cara Menjalankan Aplikasi

### 1. **Install dependensi**
Buka terminal dan jalankan:

```bash
pip install -r requirements.txt
```

### 2. **Jalankan Aplikasi**
Di terminal (pada folder proyek):

```bash
streamlit run app.py
```

---

## Teknologi yang Digunakan
- Python
- Streamlit
- MySQL
- bcrypt
- pandas
- streamlit-aggrid
- streamlit-extras

---

## Catatan
Pastikan database sudah dikonfigurasi di file `koneksi.py`.
