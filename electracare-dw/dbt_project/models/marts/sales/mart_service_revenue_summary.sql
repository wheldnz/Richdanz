select 
    d.year,
    d.month_name,
    d.year_month,
    sc.center_name,
    g.region,
    g.city,
    sum(f.service_revenue_idr) as total_service_revenue,
    sum(f.parts_revenue_idr) as total_parts_revenue,
    sum(f.gross_revenue_idr) as total_gross_revenue,
    sum(f.cogs_idr) as total_cogs,
    sum(f.gross_profit_idr) as total_gross_profit,
    sum(f.operating_expenses_idr) as total_opex,
    sum(f.net_profit_idr) as total_net_profit,
    round(sum(f.net_profit_idr) * 100.0 / nullif(sum(f.gross_revenue_idr), 0), 2) as net_profit_margin_pct
from electracare_dwh.fact_service_pl_monthly f
join electracare_dwh.dim_date d on f.month_date_key = d.date_key
join electracare_dwh.dim_service_center sc on f.center_key = sc.center_key
join electracare_dwh.dim_geography g on f.geo_key = g.geo_key
group by d.year, d.month_name, d.year_month, sc.center_name, g.region, g.city
