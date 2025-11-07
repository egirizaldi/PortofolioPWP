Personal Portfolio Website

Website ini adalah portfolio pribadi yang dibuat menggunakan Python Flask dan database SQLite/MySQL/PostgreSQL.
Tujuan proyek ini adalah menampilkan profil, daftar skill, dan project secara dinamis, serta memberikan halaman admin untuk mengelola data.

Fitur
Halaman Publik

Menampilkan profil pribadi (nama, bio, foto)

Menampilkan daftar skill dengan level dan ikon

Menampilkan daftar project dengan deskripsi, gambar, dan link

Halaman Admin (Login Required)

Login & logout untuk admin

CRUD (Create, Read, Update, Delete) untuk:

Skill

Project

Edit profil admin (nama, bio, foto)

Upload gambar untuk project, skill, dan foto profil

Teknologi yang Digunakan

Backend: Python 3 + Flask

Database: SQLite / MySQL / PostgreSQL

Frontend: HTML, CSS, Bootstrap

Template Engine: Jinja2

Form Handling & File Upload: Flask-WTF / Flask request.form & request.files

Cara Menjalankan Aplikasi

Clone repository:

git clone <link-repo-anda>
cd <nama-folder-project>


Buat virtual environment dan install dependencies:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Import database:

# jika menggunakan SQLite, biasanya file sudah termasuk
# jika MySQL/PostgreSQL, gunakan file export .sql


Jalankan server Flask:

flask run


Buka browser:

http://127.0.0.1:5000

Struktur Project
project-folder/
│
├─ app.py / myapp.py       # file utama Flask
├─ templates/              # folder HTML template
├─ static/                 # folder CSS, JS, images
├─ database.db             # SQLite database (atau .sql export)
├─ requirements.txt        # daftar library Python
└─ README.md               # dokumentasi project

Screenshoot
![Deskripsi Gambar](https://Screenshot/1.png)
![Deskripsi Gambar](https://Screenshot/2.png)
![Deskripsi Gambar](https://Screenshot/3.png)
![Deskripsi Gambar](https://Screenshot/4.png)
![Deskripsi Gambar](https://Screenshot/5(1).png)
![Deskripsi Gambar](https://Screenshot/5(3).png)
![Deskripsi Gambar](https://Screenshot/6.png)



