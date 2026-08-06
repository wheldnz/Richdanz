with raw_orders as (
    select * from electracare_dwh.fact_service_orders
)

select
    service_order_key,
    order_id,
    order_date_key,
    completion_date_key,
    customer_key,
    device_key,
    center_key,
    technician_key,
    brand_partner_key,
    geo_key,
    service_category,
    service_fee_idr,
    parts_revenue_idr,
    total_revenue_idr,
    total_cost_idr,
    profit_idr,
    turnaround_time_hours,
    case 
        when turnaround_time_hours <= 24 then 'Same Day'
        when turnaround_time_hours <= 48 then '2 Days'
        else 'Standard (>2 Days)'
    end as tat_speed_category
from raw_orders
