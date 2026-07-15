import csv
import random

def unify_sales_and_pl():
    random.seed(2026)
    
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
    retail_brands = ["Erafone Store", "iBox Store", "Digimap Store", "Blibli Store", "Sentra Ponsel", "Global Teleshop", "Megafon Store"]
    retail_partners = [f"{random.choice(retail_brands)} #{i}" for i in range(1, 51)]
    
    stores = []
    # 1 - 16: Brand Partners
    for i, b in enumerate(brand_partners, 1):
        stores.append([i, b, "Brand Partner", "Jakarta", "Central"])
        
    # 17 - 25: Infinix Service Centers
    cities = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar", "Palembang", "Denpasar", "Yogyakarta"]
    for i, (sc, city) in enumerate(zip(service_centers, cities), 17):
        stores.append([i, sc, "Infinix Service Center", city, "National"])
        
    # 26 - 75: Retail Partners
    for i, rp in enumerate(retail_partners, 26):
        c = random.choice(cities)
        r = random.choice(["North", "South", "East", "West"])
        stores.append([i, rp, "Retail Partner", c, r])
        
    # 76 - 500: Other Outlets
    for i in range(76, 501):
        c = random.choice(cities)
        r = random.choice(["North", "South", "East", "West"])
        stores.append([i, f"Retail Outlet #{i}", "Retail Outlet", c, r])
        
    # Save unified stores.csv
    stores_path = "c:/Users/USER/Documents/present/potrfolio/project-01-sales/data/processed/stores_unified.csv"
    with open(stores_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["store_id", "store_name", "channel_type", "city", "region"])
        writer.writerows(stores)
        
    print(f"Successfully unified 500 stores with 16 Brand Partners, 9 Infinix Service Centers, and 50 Retail Partners in {stores_path}")

if __name__ == "__main__":
    unify_sales_and_pl()
