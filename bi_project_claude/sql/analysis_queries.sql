-- =========================================================
-- Query analisis untuk TokoAman.id
-- Jalankan setelah schema.sql + data sudah di-load ke PostgreSQL
-- =========================================================

-- ---------------------------------------------------------
-- 1) SALES / REVENUE: Total revenue bulanan (produk + asuransi)
-- ---------------------------------------------------------
WITH product_rev AS (
    SELECT date_trunc('month', o.order_date)::date AS bulan,
           SUM(oi.quantity * oi.unit_price) AS product_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY 1
),
insurance_rev AS (
    SELECT date_trunc('month', start_date)::date AS bulan,
           SUM(premium) AS insurance_revenue
    FROM insurance_policies
    GROUP BY 1
)
SELECT COALESCE(p.bulan, i.bulan) AS bulan,
       COALESCE(p.product_revenue, 0)   AS product_revenue,
       COALESCE(i.insurance_revenue, 0) AS insurance_revenue,
       COALESCE(p.product_revenue, 0) + COALESCE(i.insurance_revenue, 0) AS total_revenue
FROM product_rev p
FULL OUTER JOIN insurance_rev i ON p.bulan = i.bulan
ORDER BY 1;


-- ---------------------------------------------------------
-- 2) CHURN: flag pelanggan yang tidak order >90 hari
--    (snapshot date = tanggal terakhir di data: 2026-06-30)
-- ---------------------------------------------------------
WITH last_order AS (
    SELECT customer_id, MAX(order_date) AS last_order_date
    FROM orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
)
SELECT c.customer_id, c.full_name, c.acquisition_channel,
       c.signup_date, lo.last_order_date,
       DATE '2026-06-30' - c.signup_date AS tenure_days,
       DATE '2026-06-30' - COALESCE(lo.last_order_date, c.signup_date) AS days_since_last_order,
       CASE
           WHEN (DATE '2026-06-30' - c.signup_date) > 90
            AND (DATE '2026-06-30' - COALESCE(lo.last_order_date, c.signup_date)) > 90
           THEN 1 ELSE 0
       END AS is_churned
FROM customers c
LEFT JOIN last_order lo ON lo.customer_id = c.customer_id;


-- ---------------------------------------------------------
-- 2b) Lapse rate asuransi per jenis polis (tidak diperpanjang)
-- ---------------------------------------------------------
SELECT policy_type,
       COUNT(*) FILTER (WHERE policy_status = 'Expired')::numeric
         / NULLIF(COUNT(*) FILTER (WHERE policy_status IN ('Expired', 'Renewed')), 0) AS lapse_rate
FROM insurance_policies
GROUP BY policy_type
ORDER BY lapse_rate DESC;


-- ---------------------------------------------------------
-- 3) RFM SEGMENTATION (versi SQL, hasilnya setara rfm_segmentation.py)
-- ---------------------------------------------------------
WITH transactions AS (
    SELECT o.customer_id, o.order_date AS txn_date, oi.quantity * oi.unit_price AS amount
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    UNION ALL
    SELECT customer_id, start_date AS txn_date, premium AS amount
    FROM insurance_policies
),
rfm_base AS (
    SELECT customer_id,
           DATE '2026-06-30' - MAX(txn_date) AS recency_days,
           COUNT(*) AS frequency,
           SUM(amount) AS monetary
    FROM transactions
    GROUP BY customer_id
),
rfm_scored AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- makin kecil recency_days = makin baru = skor tinggi
           NTILE(4) OVER (ORDER BY frequency ASC)     AS f_score,
           NTILE(4) OVER (ORDER BY monetary ASC)       AS m_score
    FROM rfm_base
)
SELECT customer_id, recency_days, frequency, monetary, r_score, f_score, m_score,
       CASE
           WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
           WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
           WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
           WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
           WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Hibernating / Lost'
           ELSE 'Need Attention'
       END AS segment
FROM rfm_scored
ORDER BY monetary DESC;


-- ---------------------------------------------------------
-- 4) MARKETING ROI per campaign
-- ---------------------------------------------------------
WITH product_rev AS (
    SELECT o.campaign_id, SUM(oi.quantity * oi.unit_price) AS product_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed' AND o.campaign_id IS NOT NULL
    GROUP BY o.campaign_id
),
insurance_rev AS (
    SELECT campaign_id, SUM(premium) AS insurance_revenue
    FROM insurance_policies
    WHERE campaign_id IS NOT NULL
    GROUP BY campaign_id
)
SELECT c.campaign_id, c.campaign_name, c.channel, c.objective, c.budget,
       COALESCE(p.product_revenue, 0) + COALESCE(i.insurance_revenue, 0) AS total_attributed_revenue,
       ROUND(
           (COALESCE(p.product_revenue, 0) + COALESCE(i.insurance_revenue, 0)) / c.budget, 2
       ) AS roas
FROM campaigns c
LEFT JOIN product_rev p ON p.campaign_id = c.campaign_id
LEFT JOIN insurance_rev i ON i.campaign_id = c.campaign_id
ORDER BY roas DESC;
