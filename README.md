# Prediksi Attrisi Karyawan (HR Employee Attrition Prediction)

Proyek Akhir: Menyelesaikan Permasalahan Human Resources

## Business Understanding

Jaya Jaya Maju adalah perusahaan multinasional yang telah berdiri sejak tahun 2000 dan kini
mempekerjakan lebih dari 1.000 karyawan di berbagai wilayah. Meskipun telah berkembang menjadi
perusahaan besar, perusahaan masih menghadapi kesulitan dalam mengelola karyawannya, yang
tercermin dari **attrition rate (rasio karyawan keluar terhadap total karyawan) yang melebihi
10%**. Attrition yang tinggi berdampak pada biaya rekrutmen dan pelatihan ulang, hilangnya
pengetahuan institusional, serta gangguan produktivitas tim.

Departemen HR membutuhkan pemahaman berbasis data mengenai faktor-faktor yang mendorong
karyawan resign, serta alat monitoring (dashboard) yang dapat digunakan secara berkelanjutan
untuk mengawasi faktor-faktor tersebut.

### Permasalahan Bisnis

1. Faktor apa saja yang paling berpengaruh terhadap tingginya attrition rate di Jaya Jaya Maju?
2. Kelompok karyawan (departemen, job role, status pernikahan, dll.) mana yang memiliki risiko
   resign tertinggi?
3. Bagaimana HR dapat mengidentifikasi karyawan yang berisiko resign secara proaktif, sebelum
   mereka benar-benar keluar?
4. Rekomendasi apa yang dapat diberikan kepada manajemen untuk menekan attrition rate?

### Cakupan Proyek

- **Data understanding & exploratory data analysis (EDA)** terhadap `employee_data.csv` untuk
  mengidentifikasi pola dan faktor yang berhubungan dengan attrition.
- **Data preparation**: penanganan missing value, encoding variabel kategorikal, dan
  train-test split.
- **Modeling**: membangun model klasifikasi (Logistic Regression sebagai baseline dan Random
  Forest sebagai model final) untuk memprediksi kemungkinan seorang karyawan resign, termasuk
  memprediksi 412 karyawan yang status attrition-nya belum diketahui.
- **Evaluation**: mengukur performa model (accuracy, precision, recall, F1-score, ROC-AUC) dan
  mengidentifikasi feature importance sebagai dasar rekomendasi bisnis.
- **Business dashboard**: visualisasi interaktif untuk memonitor attrition rate berdasarkan
  berbagai faktor.
- **Deployment (lokal)**: script `prediction.py` yang dapat dijalankan untuk memprediksi status
  attrition pada data karyawan baru menggunakan model yang telah disimpan.

### Persiapan

Sumber data: `employee_data.csv` (1.470 baris, 35 kolom), disediakan oleh departemen HR Jaya
Jaya Maju. Dataset terdiri dari 1.058 baris berlabel (status `Attrition` diketahui) dan 412
baris yang belum berlabel (diprediksi menggunakan model pada tahap akhir notebook).

Setup environment:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Menjalankan prediksi pada data karyawan baru:

```bash
python prediction.py --input data_karyawan_baru.csv --output hasil_prediksi.csv
```

## Business Dashboard

Business dashboard dibangun menggunakan **Google Looker Studio**, terhubung ke data karyawan
(`employee_data.csv`) yang sudah diberi label status attrition yang mudah dibaca
(`Attrition_Status`) dan rentang pendapatan (`IncomeBracket`).

Link dashboard (dapat diakses reviewer tanpa perlu login):
**https://datastudio.google.com/s/hSVQV0JZfEc**

Screenshot dashboard tersedia pada `zalana9_dicoding-dashboard.png`.

Dashboard menampilkan:

- 4 KPI ringkasan di bagian atas: total karyawan berlabel (1.058), jumlah karyawan resign (179),
  attrition rate keseluruhan (16,92%), dan jumlah karyawan yang statusnya belum diketahui (412).
- Attrition rate berdasarkan **job role**, **status lembur (overtime)**, **departemen**,
  **frekuensi perjalanan dinas**, **status pernikahan**, dan **rentang pendapatan bulanan**.
- Perbandingan rata-rata pendapatan, usia, masa kerja, dan jarak rumah-kantor antara karyawan
  yang bertahan dan yang resign.

## Conclusion

Attrition rate di Jaya Jaya Maju berada di angka **16,9%** pada data berlabel, di atas standar
industri yang wajar (~10%). Analisis menunjukkan bahwa attrition **tidak tersebar merata**,
melainkan terkonsentrasi pada kelompok karyawan tertentu:

- **Lembur (OverTime)** adalah faktor paling dominan — karyawan yang lembur memiliki attrition
  rate ~32%, hampir 3x lipat dibanding yang tidak lembur (~11%).
- **Job role** dengan risiko tertinggi: Sales Representative (~43%) dan Laboratory Technician
  (~26%), jauh di atas rata-rata perusahaan.
- **Pendapatan bulanan rendah** berkorelasi kuat dengan resign; kelompok berpendapatan di bawah
  3 juta memiliki attrition rate ~29%, dibanding ~7% pada kelompok di atas 12 juta.
- Karyawan **single**, yang **sering melakukan perjalanan dinas**, **berusia lebih muda**, dan
  **masa kerjanya masih pendek** juga lebih rentan resign dibanding rekan-rekan mereka.

Model **Random Forest** yang dibangun pada notebook mampu mempelajari pola-pola ini dan berhasil
mengidentifikasi 23 dari 412 karyawan tanpa label sebagai berisiko tinggi untuk resign
(probabilitas risiko tersimpan pada `model/predicted_attrition_unlabeled.csv`), memberikan HR
daftar prioritas untuk intervensi dini.

### Rekomendasi Action Items

- **Tinjau ulang kebijakan lembur** pada departemen dan job role dengan beban kerja tertinggi
  (Sales, Laboratory), termasuk kompensasi lembur yang lebih kompetitif atau penambahan
  headcount untuk mengurangi ketergantungan pada lembur berlebih.
- **Audit struktur kompensasi** untuk job role dengan attrition tertinggi (Sales
  Representative, Laboratory Technician), khususnya karyawan pada kelompok pendapatan
  terendah, untuk memastikan kompetitif terhadap pasar.
- **Program retensi tertarget** bagi karyawan dengan masa kerja di bawah 2 tahun dan usia di
  bawah 30 tahun, misalnya program mentoring dan jalur pengembangan karier yang lebih jelas di
  tahun-tahun awal.
- **Evaluasi kebijakan perjalanan dinas** (`Travel_Frequently`), termasuk opsi pengaturan
  jadwal yang lebih fleksibel atau kompensasi tambahan untuk mengurangi burnout.
- **Manfaatkan model prediksi** (`prediction.py`) secara berkala (misalnya setiap kuartal) untuk
  memperbarui daftar karyawan berisiko tinggi, sehingga HR dan manajer lini dapat melakukan
  percakapan retensi proaktif sebelum karyawan benar-benar mengajukan resign.

## Author

**Salzabila Triana Said**
[LinkedIn](https://www.linkedin.com/in/salzabilatrianasaid) | strianasaid@gmail.com

---

_Proyek ini merupakan submission akhir untuk kelas "Belajar Penerapan Data Science" — Dicoding Indonesia._
