select 
    c.customer_key,
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.loyalty_tier,
    g.city,
    g.region,
    count(distinct so.service_order_key) as total_service_orders,
    coalesce(sum(so.total_revenue_idr), 0) as total_service_spend,
    count(distinct wc.claim_key) as total_claims_filed,
    coalesce(sum(wc.total_claim_cost_idr), 0) as total_claim_value,
    count(distinct st.ticket_key) as total_support_tickets,
    avg(wc.csat_rating) as avg_csat_rating
from electracare_dwh.dim_customer c
left join electracare_dwh.dim_geography g on c.geo_key = g.geo_key
left join electracare_dwh.fact_service_orders so on c.customer_key = so.customer_key
left join electracare_dwh.fact_warranty_claims wc on c.customer_key = wc.customer_key
left join electracare_dwh.fact_support_tickets st on c.customer_key = st.customer_key
group by c.customer_key, c.customer_id, c.customer_name, c.customer_segment, c.loyalty_tier, g.city, g.region
