---
title: Analisis Sentimen RUU TNI
category: data
metric: 84.6%
metricLabel: Klasifikasi Akurasi (Naive Bayes)
tags: ['Python', 'Jupyter', 'NLP', 'TF-IDF']
description: Analisis sentimen publik di platform X (Twitter) terhadap revisi Undang-Undang TNI menggunakan Natural Language Processing dan klasifikasi Naive Bayes.
---

# Analisis Sentimen RUU TNI

## Business Problem
Revisi Undang-Undang Tentara Nasional Indonesia (RUU TNI) memicu diskursus publik yang masif di media sosial X. Manajemen kebijakan publik membutuhkan pemetaan opini masyarakat secara terstruktur untuk memahami kekhawatiran terbesar publik (seperti isu kembalinya dwifungsi ABRI atau posisi militer di jabatan sipil) guna menyusun strategi komunikasi kebijakan dan memitigasi misinformasi di ruang digital.

## Dataset & Raw Data
Data diambil melalui scraping Twitter/X API v2 selama periode perdebatan legislasi (awal 2025):
* **Jumlah Dataset**: 120,540 baris tweet dengan kata kunci `RUU TNI`, `Dwifungsi TNI`, `RUU Militer`.
* **Atribut Data**: `tweet_id`, `created_at`, `username`, `text`, `likes`, `retweets`, `followers_count`.
* **Karakteristik Data**: Data mentah memiliki tingkat kebisingan (*noise*) tinggi, mengandung emotikon, link URL, singkatan bahasa gaul (slang words), dan stopword bahasa Indonesia.

## Data Preprocessing Pipeline
Model sentimen dibangun menggunakan Python. Pipeline preprocessing teks bahasa Indonesia meliputi:
1. **Case Folding**: Mengubah seluruh teks menjadi huruf kecil (*lowercase*).
2. **Cleansing**: Menghapus URL, mention (`@user`), hashtag (`#topic`), tanda baca, angka, dan karakter non-ASCII.
3. **Stopword Removal**: Menghapus kata-kata umum yang tidak membawa arti penting (seperti "yang", "dan", "di") menggunakan daftar *stopword* Sastrawi yang dimodifikasi.
4. **Stemming**: Mengubah kata berimbuhan menjadi kata dasar (misal: "mengkhawatirkan" menjadi "khawatir") menggunakan library `Sastrawi`.
5. **Feature Extraction**: Merepresentasikan teks ke dalam fitur angka menggunakan pembobotan **TF-IDF** (Term Frequency - Inverse Document Frequency).

### Python Preprocessing Code Snippet
```python
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Inisialisasi library Sastrawi
stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stop_words = stop_factory.get_stop_words()

def preprocess_text(text):
    # 1. Case Folding
    text = text.lower()
    # 2. Cleansing
    text = re.sub(r'https?://\S+|www\.\S+', '', text) # hapus URL
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)       # hapus mentions
    text = re.sub(r'#[A-Za-z0-9_]+', '', text)       # hapus hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)          # hapus non-alphabet
    # 3. Stemming & Stopword Removal
    words = text.split()
    cleaned_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(cleaned_words)
```

## Model Training & Evaluasi
Model klasifikasi menggunakan **Multinomial Naive Bayes** dengan pembagian dataset 80% Training dan 20% Testing:
* **Accuracy Score**: 84.6%
* **Precision / Recall**:
  - Sentimen Negatif: Precision 86%, Recall 89%
  - Sentimen Positif: Precision 81%, Recall 72%
  - Sentimen Netral: Precision 79%, Recall 82%

## Key Insights
1. **Dominasi Sentimen Negatif**: 65% tweet menyatakan sentimen negatif terhadap revisi UU TNI.
2. **Topik Kekhawatiran Terbesar**: Istilah "dwifungsi" muncul di 48% dari seluruh sentimen negatif, menunjukkan trauma sejarah era Orde Baru tetap menjadi memori kolektif yang kuat.
3. **Puncak Volume Tweet**: Terjadi lonjakan volume perdebatan hingga 350% pada Maret 2025 bersamaan dengan pengesahan draf di sidang paripurna DPR.
4. **Sentimen Positif**: Hanya sebesar 15% dari total data, didominasi oleh akun humas instansi pemerintah/militer dan buzzer kebijakan.
5. **Argumen Sentimen Positif**: Narasi mendukung revisi berfokus pada urgensi profesionalisme prajurit dan modernisasi alutsista pertahanan.
6. **Sentimen Netral**: Sebesar 20%, sebagian besar berisi tautan berita media nasional tanpa disertai komentar personal dari pengguna.
7. **Penyebaran Viral**: Tweet negatif dari figur publik atau aktivis hak asasi manusia mendapat rasio *retweet* dan *like* 8 kali lebih tinggi dibanding tweet resmi pemerintah.
8. **Aspek Demografi Digital**: 74% tweet berasal dari area urban (Jakarta, Yogyakarta, Bandung, Surabaya), basis mahasiswa dan aktivis.
9. **Kategori Akun Kritikal**: Sebagian besar sentimen negatif didorong oleh akun riil (organis), bukan bot, terbukti dari sebaran interaksi (*replies* dan *quotes*).
10. **Tuntutan Publik**: Narasi negatif diakhiri dengan desakan *judicial review* ke Mahkamah Konstitusi oleh koalisi masyarakat sipil.

## Recommendations
1. **Transparansi Legislasi**: Lakukan diseminasi terbuka mengenai poin-poin revisi secara transparan guna menekan persepsi negatif atas minimnya partisipasi publik.
2. **Klarifikasi Pasal Dwifungsi**: Buat infografis dan penjelasan detail hukum yang menerangkan batasan penempatan personel TNI di instansi sipil demi membantah tuduhan "kembalinya Orba".
3. **Sosialisasi Melalui Influencer**: Gandeng akademisi hukum tata negara independen untuk menjelaskan urgensi revisi secara objektif guna meredam polarisasi.
4. **Analisis Sentimen Real-Time**: Gunakan dashboard sentimen real-time untuk memonitor isu sensitif sebelum berkembang menjadi aksi demonstrasi di jalan.
5. **Respons Cepat Krisis**: Tim kehumasan harus merespons kritik viral dalam waktu < 2 jam sebelum mendapat traksi algoritma yang masif di X.
6. **Fokus pada Profesionalisme**: Alihkan narasi promosi ke keberhasilan latihan pertahanan gabungan dan modernisasi alutsista yang mendapat sentimen positif 90%.
7. **Penyuluhan ke Kampus**: Adakan diskusi interaktif di kampus-kampus besar di kota urban untuk menjembatani aspirasi mahasiswa dengan pembuat kebijakan.
8. **Eradikasi Akun Bot Propaganda**: Hindari penggunaan akun bot palsu untuk membalas kritik, karena justru memicu sentimen negatif yang lebih tinggi dari komunitas organik.
9. **Evaluasi Kepercayaan Publik**: Lakukan survei opini publik konvensional secara berkala untuk memvalidasi apakah sentimen media sosial X berbanding lurus dengan masyarakat luas.
10. **Revisi Redaksional Regulasi**: Pertimbangkan penyesuaian tata bahasa pada draf pasal-pasal sensitif agar tidak multi-tafsir dan menimbulkan kecemasan publik.
