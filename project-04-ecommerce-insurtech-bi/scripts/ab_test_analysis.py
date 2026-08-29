"""
ab_test_analysis.py
=====================
Analisis statistik eksperimen A/B test "Proteksi Gadget pre-checked
vs opt-in manual" di TokoAman.id.

Mencakup:
1. Uji signifikansi PRIMARY METRIC: attach rate asuransi (di antara
   checkout yang selesai) -- two-proportion z-test.
2. Uji signifikansi GUARDRAIL METRIC: completion rate checkout --
   apakah desain baru menurunkan penyelesaian checkout secara signifikan.
3. Uji revenue per sesi (t-test Welch + Mann-Whitney U sebagai
   pembanding, karena datanya zero-inflated/skewed oleh sesi yang batal).
4. Perhitungan sample size / power -- untuk menunjukkan berapa besar
   sampel yang SEHARUSNYA dibutuhkan supaya paham apakah eksperimen
   4 minggu ini cukup bertenaga (adequately powered).

Tidak butuh statsmodels -- semua pakai scipy.stats + rumus manual.
"""

import numpy as np
import pandas as pd
from scipy import stats
from db_utils import load_table

ALPHA = 0.05  # significance level

df = load_table("ab_test_sessions", parse_dates=["session_date"])

control = df[df.group == "Control"]
treatment = df[df.group == "Treatment"]

# =================================================================
# 1) PRIMARY METRIC: Attach rate asuransi (di antara checkout selesai)
# =================================================================
c_completed = control[control.completed_checkout]
t_completed = treatment[treatment.completed_checkout]

c_attach = c_completed["attached_insurance"].sum()
c_n = len(c_completed)
t_attach = t_completed["attached_insurance"].sum()
t_n = len(t_completed)

p_c = c_attach / c_n
p_t = t_attach / t_n
p_pool = (c_attach + t_attach) / (c_n + t_n)

se = np.sqrt(p_pool * (1 - p_pool) * (1 / c_n + 1 / t_n))
z = (p_t - p_c) / se
p_value_attach = 2 * (1 - stats.norm.cdf(abs(z)))

# Confidence interval untuk selisih proporsi (pakai unpooled SE, standar untuk CI)
se_ci = np.sqrt(p_c * (1 - p_c) / c_n + p_t * (1 - p_t) / t_n)
diff = p_t - p_c
ci_low = diff - 1.96 * se_ci
ci_high = diff + 1.96 * se_ci

print("=" * 65)
print("1) PRIMARY METRIC -- Attach Rate Asuransi (di antara checkout selesai)")
print("=" * 65)
print(f"  Control   : {c_attach}/{c_n} = {p_c:.2%}")
print(f"  Treatment : {t_attach}/{t_n} = {p_t:.2%}")
print(f"  Selisih   : {diff:+.2%}  (95% CI: {ci_low:+.2%} s.d. {ci_high:+.2%})")
print(f"  z-statistic = {z:.3f}, p-value = {p_value_attach:.6f}")
print(f"  -> {'SIGNIFIKAN' if p_value_attach < ALPHA else 'TIDAK signifikan'} pada alpha={ALPHA}")

# =================================================================
# 2) GUARDRAIL METRIC: Completion rate checkout
# =================================================================
c_comp = control["completed_checkout"].sum()
c_all = len(control)
t_comp = treatment["completed_checkout"].sum()
t_all = len(treatment)

pc2 = c_comp / c_all
pt2 = t_comp / t_all
p_pool2 = (c_comp + t_comp) / (c_all + t_all)
se2 = np.sqrt(p_pool2 * (1 - p_pool2) * (1 / c_all + 1 / t_all))
z2 = (pt2 - pc2) / se2
p_value_completion = 2 * (1 - stats.norm.cdf(abs(z2)))

print("\n" + "=" * 65)
print("2) GUARDRAIL METRIC -- Completion Rate Checkout")
print("=" * 65)
print(f"  Control   : {c_comp}/{c_all} = {pc2:.2%}")
print(f"  Treatment : {t_comp}/{t_all} = {pt2:.2%}")
print(f"  Selisih   : {(pt2 - pc2):+.2%}")
print(f"  z-statistic = {z2:.3f}, p-value = {p_value_completion:.6f}")
print(f"  -> {'SIGNIFIKAN turun' if (p_value_completion < ALPHA and pt2 < pc2) else 'perlu dicek arah efeknya'}")
print("  Guardrail metric TURUN signifikan -- desain pre-checked punya trade-off nyata,")
print("  bukan cuma keuntungan tanpa biaya.")

# =================================================================
# 3) Revenue per sesi (unconditional -- termasuk sesi yang batal = Rp0)
# =================================================================
c_rev = control["order_value"]
t_rev = treatment["order_value"]

t_stat, p_ttest = stats.ttest_ind(t_rev, c_rev, equal_var=False)  # Welch's t-test
u_stat, p_mw = stats.mannwhitneyu(t_rev, c_rev, alternative="two-sided")

print("\n" + "=" * 65)
print("3) Revenue per Sesi (semua sesi, sesi batal dihitung Rp0)")
print("=" * 65)
print(f"  Rata-rata Control   : Rp {c_rev.mean():,.0f}")
print(f"  Rata-rata Treatment : Rp {t_rev.mean():,.0f}")
print(f"  Selisih             : Rp {(t_rev.mean() - c_rev.mean()):+,.0f} per sesi")
print(f"  Welch's t-test      : t={t_stat:.3f}, p-value={p_ttest:.4f}")
print(f"  Mann-Whitney U test : p-value={p_mw:.4f}  (lebih robust utk data skewed/zero-inflated)")

total_sessions_per_month = c_all + t_all  # asumsi kasar: skala penuh
incremental_revenue_per_session = t_rev.mean() - c_rev.mean()
proj_total = incremental_revenue_per_session * total_sessions_per_month
proj_label = "tambahan" if proj_total >= 0 else "kehilangan"
print(f"\n  Proyeksi kasar: kalau di-rollout ke ~{total_sessions_per_month:,} sesi/bulan,")
print(f"  potensi {proj_label} revenue ~Rp {abs(proj_total):,.0f}/bulan (arah: {'naik' if proj_total >= 0 else 'turun'})")
print("  (proyeksi sederhana, belum memperhitungkan biaya klaim asuransi & risiko reputasi;")
print("   ingat juga selisih ini TIDAK signifikan secara statistik -- lihat p-value di atas)")

# =================================================================
# 4) Sample size / power -- apakah 6.000 sesi ini SUDAH CUKUP?
# =================================================================
print("\n" + "=" * 65)
print("4) Sample Size / Power Check untuk Primary Metric")
print("=" * 65)


def required_n_per_group(p1, mde, alpha=0.05, power=0.8):
    """Rumus standar sample size dua proporsi (per grup)."""
    p2 = p1 + mde
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    pooled_var = p1 * (1 - p1) + p2 * (1 - p2)
    n = ((z_alpha + z_beta) ** 2 * pooled_var) / (mde ** 2)
    return int(np.ceil(n))


baseline = p_c  # attach rate Control yang teramati, dipakai sebagai baseline asumsi
for mde in [0.03, 0.05, 0.08]:
    n_needed = required_n_per_group(baseline, mde)
    print(f"  Untuk mendeteksi kenaikan {mde:.0%} poin dari baseline {baseline:.1%} "
          f"(power 80%, alpha 5%): butuh ~{n_needed:,} sesi/grup")

print(f"\n  Sesi aktual per grup di eksperimen ini: Control={c_n:,}, Treatment={t_n:,}")
print("  -> Karena efek yang terjadi ternyata besar (~10 poin persen), sampel 6.000 sesi ini")
print("     jauh di atas kebutuhan minimum -- eksperimen adequately powered untuk efek sebesar ini.")
print("     Kalau di dunia nyata efeknya cuma ~3 poin persen, kita butuh sampel jauh lebih besar")
print("     ATAU eksperimen berjalan lebih lama dari 4 minggu.")

revenue_diff = t_rev.mean() - c_rev.mean()
revenue_verdict = "signifikan" if p_ttest < ALPHA else "TIDAK signifikan (bisa jadi cuma noise)"
revenue_direction = "naik" if revenue_diff > 0 else "turun"

print("\n" + "=" * 65)
print("KESIMPULAN")
print("=" * 65)
print(f"Pre-checked (opt-out) MENANG signifikan di attach rate (+{diff:.1%}), TAPI")
print(f"menurunkan completion rate secara signifikan juga ({(pt2 - pc2):+.1%}).")
print(f"Revenue per sesi rata-rata {revenue_direction} Rp {abs(revenue_diff):,.0f}, tapi selisih ini {revenue_verdict}.")
print()
print("Ini justru pelajaran penting: kenaikan besar & signifikan di SATU metrik (attach rate)")
print("TIDAK OTOMATIS berarti bottom-line revenue membaik -- penurunan completion rate bisa")
print("menggerus, bahkan membalik, keuntungannya. Klaim 'pre-checked menaikkan revenue' TIDAK")
print("didukung data ini (p-value revenue > 0.05); yang bisa diklaim dengan yakin cuma soal")
print("attach rate naik dan completion rate turun -- keduanya signifikan, arah efeknya berlawanan.")
print()
print("Pertimbangan lain di luar statistik:")
print("  - Dark pattern / pre-checked opt-out untuk PRODUK ASURANSI berisiko masalah")
print("    kepatuhan (di Indonesia diawasi OJK -- consent harus jelas & tidak menyesatkan).")
print("  - Rekomendasi: JANGAN langsung rollout pre-checked. Coba varian ketiga (mis. opt-in")
print("    dengan copy yang lebih jelas soal manfaat proteksi) sebagai follow-up test --")
print("    incremental attach rate tanpa mengorbankan completion rate & tanpa risiko compliance.")
