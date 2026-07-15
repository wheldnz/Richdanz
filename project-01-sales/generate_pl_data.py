import csv
import random
from datetime import datetime

def generate_pl_dataset():
    random.seed(101)
    
    # 1. 16 Brand Partners
    brand_partners = [
        "Samsung Electronics", "Xiaomi Official", "Apple Authorized", "Infinix Mobility",
        "OPPO Mobile", "Vivo Communication", "Realme Official", "ASUS Technology",
        "Lenovo Group", "HP Indonesia", "Dell Technologies", "Tecno Mobile",
        "itel Mobile", "Sony Electronics", "LG Electronics", "Anker Innovations"
    ]
    
    # 2. 9 Infinix Service Centers
    service_centers = [
        "Infinix Service Center - Jakarta Central",
        "Infinix Service Center - Surabaya",
        "Infinix Service Center - Bandung",
        "Infinix Service Center - Medan",
        "Infinix Service Center - Semarang",
        "Infinix Service Center - Makassar",
        "Infinix Service Center - Palembang",
        "Infinix Service Center - Denpasar",
        "Infinix Service Center - Yogyakarta"
    ]
    
    # 3. 50 Retail Partners
    retail_partners = [f"Retail Partner - {brand} #{i}" for i in range(1, 51) for brand in ["Erafone", "iBox", "Digimap", "Blibli Store", "Sentra Ponsel"]]
    retail_partners = list(set(retail_partners))[:50]
    
    all_partners = []
    for b in brand_partners:
        all_partners.append((b, "Brand Partner"))
    for s in service_centers:
        all_partners.append((s, "Infinix Service Center"))
    for r in retail_partners:
        all_partners.append((r, "Retail Partner"))
        
    months = []
    for year in [2024, 2025]:
        for month in range(1, 13):
            months.append(f"{year}-{month:02d}-01")
            
    raw_rows = []
    clean_rows = []
    
    partner_id_counter = 1
    partner_id_map = {}
    
    for partner_name, channel_type in all_partners:
        partner_id = f"PTR-{partner_id_counter:03d}"
        partner_id_map[partner_name] = partner_id
        partner_id_counter += 1
        
        # Base financial scale per channel type
        if channel_type == "Brand Partner":
            base_rev = random.randint(1_500_000_000, 4_500_000_000) # 1.5B - 4.5B
            cogs_ratio = random.uniform(0.60, 0.72)
            opex_ratio = random.uniform(0.12, 0.18)
        elif channel_type == "Infinix Service Center":
            base_rev = random.randint(400_000_000, 1_200_000_000) # 400M - 1.2B
            cogs_ratio = random.uniform(0.45, 0.55) # Higher margin service
            opex_ratio = random.uniform(0.20, 0.30)
        else: # Retail Partner
            base_rev = random.randint(200_000_000, 800_000_000) # 200M - 800M
            cogs_ratio = random.uniform(0.70, 0.80)
            opex_ratio = random.uniform(0.10, 0.15)
            
        for m_date in months:
            # Seasonal variation
            season_factor = random.uniform(0.90, 1.25)
            gross_rev = int(base_rev * season_factor)
            cogs = int(gross_rev * cogs_ratio)
            gross_profit = gross_rev - cogs
            opex = int(gross_rev * opex_ratio)
            net_profit = gross_profit - opex
            net_margin_pct = round((net_profit / gross_rev) * 100, 2)
            
            # Raw string anomalies
            raw_rows.append([
                partner_id, partner_name, channel_type, m_date,
                f"Rp {gross_rev:,}", f"Rp {cogs:,}", f"Rp {gross_profit:,}",
                f"Rp {opex:,}", f"Rp {net_profit:,}", f"{net_margin_pct}%"
            ])
            
            # Clean numeric rows
            clean_rows.append([
                partner_id, partner_name, channel_type, m_date,
                gross_rev, cogs, gross_profit, opex, net_profit, net_margin_pct
            ])
            
    # Write RAW CSV
    raw_path = "c:/Users/USER/Documents/present/potrfolio/project-01-sales/data/raw/pl_multi_channel_raw.csv"
    with open(raw_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "partner_id", "partner_name", "channel_type", "month_date",
            "gross_revenue", "cogs", "gross_profit", "operating_expenses", "net_profit", "net_profit_margin_pct"
        ])
        writer.writerows(raw_rows)
        
    # Write CLEAN CSV
    clean_path = "c:/Users/USER/Documents/present/potrfolio/project-01-sales/data/processed/pl_multi_channel_clean.csv"
    with open(clean_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "partner_id", "partner_name", "channel_type", "month_date",
            "gross_revenue_idr", "cogs_idr", "gross_profit_idr", "operating_expenses_idr", "net_profit_idr", "net_profit_margin_pct"
        ])
        writer.writerows(clean_rows)

    print(f"Generated {len(clean_rows)} P&L records across 75 partners in {raw_path} and {clean_path}")

if __name__ == "__main__":
    generate_pl_dataset()
