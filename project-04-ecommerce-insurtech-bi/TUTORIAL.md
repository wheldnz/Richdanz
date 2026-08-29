# TokoAman.id — BI Portfolio Project
### Sales Forecasting • Customer Churn • RFM Segmentation • Marketing ROI
### Stack: PostgreSQL + Python + Power BI

---

## 1. Studi kasus

**TokoAman.id** adalah marketplace e-commerce fiktif yang juga menjual produk
asuransi mikro langsung di checkout (*embedded insurance*) — proteksi gadget,
asuransi pengiriman, dan asuransi perjalanan. Model bisnis ini sengaja dipilih
karena menggabungkan dua hal:

- **Retail/e-commerce** — dataset yang universal dan mudah dipahami rekruter mana pun.
- **Insurtech / embedded insurance** — salah satu tren bisnis yang lagi naik, dan langsung nyambung
  kalau kamu melamar posisi Data/BI di perusahaan asuransi.

Dari data ini kamu akan membangun **5 analisis** yang paling sering dicari untuk
posisi Business Intelligence:

| # | Analisis | Pertanyaan bisnis yang dijawab |
|---|----------|--------------------------------|
| 1 | Sales/Revenue Forecasting | Revenue bulan depan diperkirakan berapa? Tren-nya naik/turun? |
| 2 | Customer Churn | Pelanggan mana yang berisiko berhenti belanja/tidak perpanjang polis? |
| 3 | RFM Segmentation | Siapa pelanggan paling berharga vs yang butuh perhatian? |
| 4 | Marketing ROI | Campaign/channel mana yang paling untung, mana yang buang-buang budget? |
| 5 | A/B Testing | Perubahan desain checkout X benar-benar berdampak, atau cuma noise? |

---

## 2. Struktur folder

```
bi_project/
├── data/                      <- CSV dummy + hasil analisis (auto-generated)
├── sql/
│   ├── schema.sql              <- DDL 7 tabel PostgreSQL
│   └── analysis_queries.sql    <- versi SQL dari ke-4 analisis
├── scripts/
│   ├── db_utils.py              <- helper baca dari Postgres / fallback CSV
│   ├── generate_dummy_data.py   <- generator data dummy
│   ├── load_to_postgres.py       <- load CSV mentah -> PostgreSQL
│   ├── forecasting.py             <- analisis #1
│   ├── churn_analysis.py           <- analisis #2
│   ├── rfm_segmentation.py          <- analisis #3
│   ├── marketing_roi.py              <- analisis #4
│   ├── generate_ab_test_data.py       <- simulasi data eksperimen analisis #5
│   ├── ab_test_analysis.py             <- analisis #5 (uji statistik)
│   └── push_analytics_to_postgres.py <- push hasil Python balik ke Postgres
└── requirements.txt
```

---

## 3. Model data (ERD ringkas)

```
customers ──┬──< orders ──< order_items >── products
            │        │
            │        └──< insurance_policies >── claims
            │                    │
            └────────────────────┘
campaigns ──< orders (campaign_id, nullable)
campaigns ──< insurance_policies (campaign_id, nullable)
```

Poin penting buat cerita ke recruiter: `insurance_policies.order_id` boleh NULL
(polis travel insurance yang dibeli berdiri sendiri, bukan bundling checkout) —
ini pola *nullable foreign key* yang umum di data nyata dan bagus untuk
ditunjukkan kamu paham cara menanganinya (LEFT JOIN, COALESCE, dsb).

---

## 4. Langkah 1 — Generate data dummy

```bash
cd scripts
python generate_dummy_data.py
```

Ini membuat 7 file CSV di `../data/` — sekitar 3.000 pelanggan, 15.000 order,
3.800 polis asuransi, dan 380 klaim, tersebar Januari 2024–Juni 2026 dengan
tren pertumbuhan + musiman (gajian, Ramadan/Lebaran, Harbolnas 11.11 & 12.12).
Datanya sudah saya jalankan dan divalidasi — polanya realistis (mis. revenue
Maret 2024 melonjak karena musim Ramadan).

---

## 5. Langkah 2 — Setup PostgreSQL & load data

1. Install PostgreSQL (kalau belum ada) — https://www.postgresql.org/download/
2. Buat database:
   ```bash
   createdb tokoaman
   ```
3. Jalankan schema:
   ```bash
   psql -d tokoaman -f ../sql/schema.sql
   ```
4. Install dependency Python:
   ```bash
   pip install -r ../requirements.txt
   ```
5. Set connection string (sesuaikan user/password kamu), lalu load data:
   ```bash
   export DATABASE_URL="postgresql+psycopg2://postgres:password@localhost:5432/tokoaman"
   python load_to_postgres.py
   ```

Kalau kamu belum sempat install PostgreSQL, semua script Python di langkah
berikutnya **tetap jalan** — `db_utils.py` otomatis fallback baca dari CSV di
`../data/` kalau `DATABASE_URL` tidak di-set. Tapi untuk portofolio yang
"menjual", tetap disarankan pakai PostgreSQL sungguhan supaya kamu bisa cerita
soal schema design, indexing, dan query SQL di interview.

---

## 6. Langkah 3 — Eksplorasi & analisis pakai SQL

Buka `sql/analysis_queries.sql` — isinya 4 query siap pakai yang jadi dasar
ke-4 dashboard:

1. **Revenue bulanan** (produk + asuransi digabung) — pakai `FULL OUTER JOIN`
   antara dua CTE karena tidak semua bulan punya data asuransi & produk yang pas sama.
2. **Churn flag** — pelanggan tanpa order >90 hari (dan sudah jadi pelanggan >90 hari).
3. **RFM Segmentation** — pakai `NTILE(4)` untuk scoring kuartil per R/F/M,
   ini pattern SQL yang sering ditanya di technical test BI/Data Analyst.
4. **Marketing ROI per campaign** — join campaign ke revenue produk + asuransi
   yang atributnya lewat `campaign_id`.

Jalankan langsung di `psql` atau DBeaver/pgAdmin untuk latihan SQL kamu:
```bash
psql -d tokoaman -f ../sql/analysis_queries.sql
```

---

## 7. Langkah 4 — Analisis lanjutan pakai Python

Jalankan urut dari folder `scripts/` (masing-masing sudah saya test, jalan tanpa error):

```bash
python forecasting.py
python rfm_segmentation.py
python churn_analysis.py
python marketing_roi.py
python push_analytics_to_postgres.py   # opsional tapi disarankan
```

### 7a. `forecasting.py` — Sales/Revenue Forecasting
- Agregasi revenue bulanan (produk + premi asuransi).
- Fitur: **trend** (index bulan berjalan) + **musiman** (dummy variable per
  bulan 1–12), dilatih pakai `LinearRegression` dari scikit-learn.
- Divalidasi dengan 3 bulan terakhir sebagai test set (MAPE ~14% pada data
  dummy ini — realistis untuk model sederhana di data yang lonjakannya
  event-driven seperti Harbolnas).
- Forecast 6 bulan ke depan, hasil actual+forecast disimpan ke
  `monthly_revenue_actual_vs_forecast.csv` untuk divisualisasikan di Power BI.
- **Poin diskusi interview:** jelaskan trade-off pakai regresi sederhana
  (mudah dijelaskan ke stakeholder non-teknis) vs SARIMA/Prophet (lebih akurat
  untuk pola musiman kompleks, tapi lebih "black box").

### 7b. `rfm_segmentation.py` — Customer Segmentation
- Menggabungkan transaksi e-commerce **dan** pembelian polis asuransi jadi satu
  tabel transaksi, supaya "value" pelanggan mencerminkan keduanya — ini
  pembeda dari tutorial RFM kebanyakan yang cuma pakai data retail.
- Scoring R/F/M pakai kuartil (`pd.qcut`), lalu di-mapping ke label segmen:
  Champions, Loyal Customers, New Customers, At Risk, Hibernating/Lost,
  Need Attention.

### 7c. `churn_analysis.py` — Customer Churn
- Dua lapis: churn e-commerce (90 hari tanpa order) dan lapse rate asuransi
  (tidak diperpanjang) per jenis polis.
- Model risk-scoring pakai `LogisticRegression` (ROC-AUC ~0.72 di data ini) —
  fitur: tenure, frequency, monetary, jumlah polis asuransi yang dimiliki,
  acquisition channel, gender. **Catatan penting:** `days_since_last_order`
  sengaja TIDAK dipakai sebagai fitur karena itu bagian dari definisi churn
  itu sendiri (data leakage) — ini detail yang bagus disebut saat interview
  untuk menunjukkan kamu paham konsep leakage.
- Insight menarik dari koefisien model: pelanggan yang **punya polis asuransi
  cenderung lebih kecil risiko churn-nya** — bisa jadi bahan rekomendasi bisnis
  "cross-sell asuransi sebagai strategi retensi".

### 7d. `marketing_roi.py` — Marketing ROI
- Revenue diatribusikan ke campaign lewat `campaign_id` yang tertaut di order
  maupun polis (atribusi *last-touch* sederhana — sebutkan ini sebagai
  simplifikasi kalau ditanya soal multi-touch attribution).
- Menghitung ROAS (Revenue/Spend) dan ROI% per campaign, dan ringkasan per channel.
- Di data ini, channel **Organic** dan **TikTok Ads** punya ROAS tertinggi,
  sementara beberapa campaign **Google Ads** & **Instagram Ads** rugi besar —
  bahan cerita "budget reallocation recommendation" yang konkret.

### 7e. `generate_ab_test_data.py` + `ab_test_analysis.py` — A/B Testing

**Penting untuk dipahami dulu:** ke-4 analisis di atas (forecasting, churn,
RFM, marketing ROI) semuanya **observational** — dihitung dari data historis
yang terjadi apa adanya, tanpa ada pengacakan (randomization). Itu bagus untuk
menjawab "apa yang terjadi" dan "siapa yang berisiko", tapi TIDAK bisa dipakai
untuk klaim sebab-akibat yang kuat (mis. "insurance menyebabkan customer lebih
loyal" — bisa saja customer yang lebih loyal memang dari awal lebih cenderung
beli asuransi, bukan asuransinya yang membuat mereka loyal).

**A/B testing itu berbeda secara fundamental**: butuh pengacakan (randomized
control/treatment) supaya perbedaan hasil antar grup bisa diklaim disebabkan
oleh perubahan yang diuji, bukan faktor lain. Data historis TokoAman.id yang
sudah kamu punya **tidak bisa dipakai untuk A/B test beneran** karena tidak
ada kolom pengacakan di dalamnya — makanya dua script ini membuat **dataset
eksperimen terpisah** yang memang didesain dengan pengacakan sejak awal.

**Skenario eksperimen:** TokoAman.id menguji apakah mengubah checkbox
"Proteksi Gadget" di checkout dari opt-in manual (kosong) menjadi *pre-checked*
(opt-out) meningkatkan attach rate asuransi — dengan completion rate checkout
sebagai *guardrail metric* (supaya tidak "menang" attach rate tapi banyak orang
malah batal checkout).

```bash
python generate_ab_test_data.py
python ab_test_analysis.py
```

Yang dilakukan `ab_test_analysis.py` (sudah saya jalankan, hasil nyata):

1. **Two-proportion z-test** untuk primary metric (attach rate): Treatment
   36.4% vs Control 24.4% → selisih **+12.0 poin, signifikan** (p < 0.001).
2. **Two-proportion z-test** untuk guardrail metric (completion rate):
   Treatment 89.6% vs Control 92.7% → selisih **-3.1 poin, signifikan** (p < 0.001).
3. **Welch's t-test + Mann-Whitney U test** untuk revenue per sesi: selisihnya
   **TIDAK signifikan** (p = 0.17) — walau attach rate naik besar, penurunan
   completion rate cukup untuk membuat efek ke revenue keseluruhan jadi tidak
   meyakinkan.
4. **Sample size / power calculation**: menghitung berapa sesi yang dibutuhkan
   untuk mendeteksi berbagai ukuran efek (MDE), lalu membandingkan dengan
   jumlah sesi aktual — untuk menilai apakah eksperimen ini "adequately powered".

**Ini poin paling berharga untuk portofolio kamu**: kesimpulannya BUKAN "desain
baru menang, langsung rollout", tapi jauh lebih nuanced — signifikan naik di
satu metrik, signifikan turun di metrik lain, dan efek ke revenue keseluruhan
tidak terbukti. Kemampuan menyampaikan hasil yang **tidak hitam-putih** seperti
ini justru yang paling dicari dari kandidat BI/Data Analyst yang matang,
dibanding yang cuma bilang "p-value < 0.05, menang."

Tambahan sudut pandang bisnis (bagus disebut kalau interview di perusahaan asuransi):
desain *pre-checked/opt-out* untuk produk asuransi berisiko masalah kepatuhan
karena regulator (OJK) mensyaratkan persetujuan nasabah yang jelas dan tidak
menyesatkan — jadi rekomendasinya bukan langsung rollout, tapi uji varian lain
(mis. copy yang lebih persuasif dengan tetap opt-in).

---

## 8. Langkah 5 — Bangun dashboard di Power BI

### 8a. Connect ke PostgreSQL
`Get Data` → `Database` → `PostgreSQL database` → masukkan host `localhost`,
database `tokoaman`. Power BI butuh **Npgsql** driver untuk PostgreSQL — kalau
belum ada, Power BI akan kasih link download saat pertama kali connect.

Pilih semua tabel operasional (`customers`, `products`, `campaigns`, `orders`,
`order_items`, `insurance_policies`, `claims`) **dan** tabel analytics kalau
kamu sudah menjalankan `push_analytics_to_postgres.py`
(`rfm_segments`, `churn_customers`, `churn_by_policy_type`, `campaign_roi`,
`channel_roi_summary`, `monthly_revenue_actual_vs_forecast`).

Kalau belum sempat setup PostgreSQL, kamu tetap bisa `Get Data` → `Text/CSV`
dan import langsung file-file di folder `data/`.

### 8b. Data modeling (relationships)

Di Model view, buat relasi (biasanya Power BI auto-detect sebagian, cek ulang):

- `customers[customer_id]` 1 → * `orders[customer_id]`
- `orders[order_id]` 1 → * `order_items[order_id]`
- `products[product_id]` 1 → * `order_items[product_id]`
- `customers[customer_id]` 1 → * `insurance_policies[customer_id]`
- `orders[order_id]` 1 → * `insurance_policies[order_id]` (nullable — pastikan cardinality tetap kebaca)
- `insurance_policies[policy_id]` 1 → * `claims[policy_id]`
- `campaigns[campaign_id]` 1 → * `orders[campaign_id]`
- `campaigns[campaign_id]` 1 → * `insurance_policies[campaign_id]`
- `rfm_segments[customer_id]` & `churn_customers[customer_id]` → 1-1 ke `customers[customer_id]`
- `campaign_roi[campaign_id]` → 1-1 ke `campaigns[campaign_id]`

Buat juga **Date table** (praktik wajib BI): `Modeling` → `New Table`:
```dax
DimDate = CALENDAR(DATE(2024,1,1), DATE(2026,12,31))
```
Tambahkan kolom `Year`, `MonthName`, `MonthNumber`, lalu mark as Date Table
(klik tabel → `Mark as Date Table`). Relasikan ke `orders[order_date]` dan
`insurance_policies[start_date]`.

### 8c. DAX measures per dashboard

**Halaman 1 — Sales & Revenue Forecasting**
```dax
Total Product Revenue = SUMX(order_items, order_items[quantity] * order_items[unit_price])

Total Insurance Revenue = SUM(insurance_policies[premium])

Total Revenue = [Total Product Revenue] + [Total Insurance Revenue]

Revenue MoM Growth % =
VAR CurrMonth = [Total Revenue]
VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))
RETURN DIVIDE(CurrMonth - PrevMonth, PrevMonth)
```
Untuk garis forecast, langsung pakai kolom `revenue` dari tabel
`monthly_revenue_actual_vs_forecast` (sudah berisi actual+forecast dengan
kolom `type`), plot sebagai line chart dengan `type` sebagai legend.

**Halaman 2 — Customer Churn**
```dax
Total Customers = DISTINCTCOUNT(customers[customer_id])

Churned Customers = CALCULATE(COUNTROWS(churn_customers), churn_customers[is_churned] = 1)

Churn Rate % = DIVIDE([Churned Customers], [Total Customers])

Avg Churn Risk Score = AVERAGE(churn_customers[churn_risk_score])
```
Insurance lapse rate langsung dari tabel `churn_by_policy_type[lapse_rate]`,
tampilkan sebagai bar chart per `policy_type`.

**Halaman 3 — RFM Segmentation**
```dax
Customers per Segment = DISTINCTCOUNT(rfm_segments[customer_id])

Total Monetary = SUM(rfm_segments[monetary])

Avg Monetary per Segment = AVERAGE(rfm_segments[monetary])

% of Total Revenue =
DIVIDE([Total Monetary], CALCULATE([Total Monetary], ALL(rfm_segments[segment])))
```
Visual yang cocok: treemap (segment vs monetary), scatter plot Recency vs
Frequency dengan warna = segment.

**Halaman 4 — Marketing ROI**
```dax
Total Budget = SUM(campaign_roi[budget])

Total Attributed Revenue = SUM(campaign_roi[total_attributed_revenue])

ROAS = DIVIDE([Total Attributed Revenue], [Total Budget])

ROI % = DIVIDE([Total Attributed Revenue] - [Total Budget], [Total Budget])
```
Visual: bar chart ROAS per channel (dari `channel_roi_summary`), dan tabel
campaign detail dengan conditional formatting (merah untuk ROAS < 1).

**Halaman 5 — A/B Test Results**

Import `ab_test_sessions.csv` (atau push dulu ke Postgres seperti tabel
analytics lain). Tabel ini BERDIRI SENDIRI — tidak perlu direlasikan ke
tabel lain, karena eksperimennya independen dari data historis.

```dax
Sessions = COUNTROWS(ab_test_sessions)

Completion Rate =
DIVIDE(CALCULATE(COUNTROWS(ab_test_sessions), ab_test_sessions[completed_checkout] = TRUE),
       [Sessions])

Attach Rate (Completed Only) =
VAR CompletedSessions = CALCULATE(COUNTROWS(ab_test_sessions), ab_test_sessions[completed_checkout] = TRUE)
VAR AttachedSessions = CALCULATE(COUNTROWS(ab_test_sessions),
                                  ab_test_sessions[completed_checkout] = TRUE,
                                  ab_test_sessions[attached_insurance] = TRUE)
RETURN DIVIDE(AttachedSessions, CompletedSessions)

Avg Revenue per Session = AVERAGE(ab_test_sessions[order_value])
```
Visual: KPI card per grup (pakai `group` sebagai slicer atau small multiples),
bar chart perbandingan Control vs Treatment untuk ketiga metrik di atas.
Tambahkan text box berisi p-value dari hasil `ab_test_analysis.py` — Power BI
sendiri tidak menghitung p-value secara native, jadi angka statistiknya
ditempel dari output Python (ini praktik umum: Python untuk *statistical
rigor*, Power BI untuk *storytelling visual*).

### 8d. Struktur halaman yang disarankan

| Halaman | Visual utama |
|---|---|
| Overview | KPI cards (Total Revenue, Total Customers, Churn Rate, ROAS rata-rata) + tren revenue |
| Sales Forecasting | Line chart actual vs forecast, breakdown product vs insurance revenue |
| Customer Churn | Churn rate by acquisition channel, lapse rate by policy type, tabel top-N pelanggan berisiko tinggi (sort by churn_risk_score) |
| RFM Segmentation | Treemap segment, scatter Recency vs Frequency, tabel pelanggan per segmen |
| Marketing ROI | Bar chart ROAS per channel & per campaign, tabel campaign detail |
| A/B Test Results | KPI cards Control vs Treatment (attach rate, completion rate, revenue/sesi), catatan signifikansi |

---

## 9. Kemas jadi portofolio yang menjual

1. **README di GitHub**: jelaskan masalah bisnis (bukan cuma "bikin dashboard"),
   arsitektur (PostgreSQL → Python → Power BI), dan screenshot tiap halaman dashboard.
2. **Publish** dashboard-nya (Power BI Service, atau screenshot + video singkat
   kalau tidak punya lisensi Pro) dan upload `.pbix` + semua kode ke GitHub.
3. **Framing sebagai studi kasus**, bukan latihan: "Bagaimana TokoAman.id bisa
   menurunkan churn 5% dan mengalokasikan ulang budget marketing yang boros di
   3 campaign dengan ROAS < 1?" — jauh lebih kuat daripada "ini dashboard sales".
4. Kalau melamar ke perusahaan **asuransi**, tonjolkan bagian churn/lapse rate
   polis dan insight "kepemilikan polis menurunkan risiko churn e-commerce" —
   itu langsung relevan dengan bahasa bisnis asuransi (retention, cross-sell,
   persistency ratio).

---

## 10. Ringkasan insight siap-pakai untuk interview

- Revenue tumbuh dengan pola musiman jelas (Ramadan, Harbolnas, gajian) — model
  forecasting sederhana sudah bisa menangkap trend dengan MAPE ~14%.
- ~43% pelanggan lama masuk kategori "belum order 90 hari terakhir" — sinyal
  butuh program reaktivasi.
- Lapse rate asuransi ~63–66% di semua jenis polis — artinya mayoritas
  pelanggan tidak memperpanjang, peluang besar untuk program retensi/reminder.
- Pelanggan yang punya polis asuransi punya risiko churn e-commerce lebih
  rendah → cross-sell asuransi bisa jadi strategi retensi, bukan cuma revenue tambahan.
- ROAS antar campaign bervariasi ekstrem (dari <0.1 sampai >30x) → ada peluang
  realokasi budget yang jelas dan terukur.
- A/B test checkout pre-checked vs opt-in: attach rate naik signifikan (+12
  poin), tapi completion rate turun signifikan (-3 poin), dan efeknya ke
  revenue keseluruhan TIDAK terbukti signifikan → keputusan rollout butuh
  pertimbangan di luar satu metrik saja, termasuk risiko kepatuhan (OJK).
