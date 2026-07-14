import csv
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, 'data', 'raw')
proc_dir = os.path.join(base_dir, 'data', 'processed')
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(proc_dir, exist_ok=True)

print("--- Enriching Project 03: DataCo Supply Chain Dataset ---")

dataco_file = os.path.join(base_dir, 'DataCoSupplyChainDataset.csv')

customers = {}
products = {}
warehouses = {}
orders = []
shipments = []

counter = 1

with open(dataco_file, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Extract Customer
        cust_id = row.get('Customer Id', '').strip()
        if cust_id and cust_id not in customers:
            customers[cust_id] = {
                'customer_id': cust_id,
                'first_name': row.get('Customer Fname', '').strip(),
                'last_name': row.get('Customer Lname', '').strip(),
                'city': row.get('Customer City', '').strip(),
                'country': row.get('Customer Country', '').strip(),
                'segment': row.get('Customer Segment', '').strip()
            }
            
        # Extract Product
        prod_id = row.get('Product Card Id', '').strip()
        if prod_id and prod_id not in products:
            products[prod_id] = {
                'product_id': prod_id,
                'category_id': row.get('Category Id', '').strip(),
                'category_name': row.get('Category Name', '').strip(),
                'product_name': row.get('Product Name', '').strip(),
                'price': row.get('Product Price', '').strip()
            }
            
        # Extract Order Fact
        order_id = row.get('Order Id', '').strip()
        order_date = row.get('order date (DateOrders)', '').strip()
        if not order_date:
            order_date = row.get('Order Date', '').strip()
            
        # Format date string (YYYY-MM-DD)
        if order_date and ' ' in order_date:
            order_date = order_date.split(' ')[0]
            
        real_days = row.get('Days for shipping (real)', '0').strip()
        sched_days = row.get('Days for shipment (scheduled)', '0').strip()
        late_risk = row.get('Late_delivery_risk', '0').strip()
        deliv_status = row.get('Delivery Status', '').strip()
        profit = row.get('Benefit per order', '0').strip()
        sales = row.get('Sales per customer', '0').strip()
        region = row.get('Order Region', '').strip()
        
        orders.append({
            'order_id': order_id,
            'order_date': order_date,
            'customer_id': cust_id,
            'product_id': prod_id,
            'order_region': region,
            'sales_amount': sales,
            'profit_amount': profit,
            'real_shipping_days': real_days,
            'scheduled_shipping_days': sched_days,
            'late_delivery_risk': late_risk,
            'delivery_status': deliv_status
        })

print(f"Extracted {len(customers)} unique customers and {len(products)} unique products.")
print(f"Processing {len(orders)} order line items into relational tables...")

# Save normalized tables
with open(os.path.join(raw_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'first_name', 'last_name', 'city', 'country', 'segment'])
    writer.writeheader()
    writer.writerows(customers.values())

with open(os.path.join(raw_dir, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'category_id', 'category_name', 'product_name', 'price'])
    writer.writeheader()
    writer.writerows(products.values())

with open(os.path.join(raw_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'order_date', 'customer_id', 'product_id', 'order_region', 'sales_amount', 'profit_amount', 'real_shipping_days', 'scheduled_shipping_days', 'late_delivery_risk', 'delivery_status'])
    writer.writeheader()
    writer.writerows(orders[:50000]) # Limit to 50k for high performance

print("SUCCESS: Supply chain dataset normalized into relational Star Schema tables!")
