import csv
import random
from datetime import datetime, timedelta

def generate_claims_dataset():
    random.seed(42)
    
    # 9 Insurance Partners
    insurance_partners = [
        "Qoala Insurtech", "Igloo Insurance", "PasarPolis", 
        "Chubb Insurance", "ACA Asuransi", "Tokio Marine", 
        "Zurich Insurance", "Allianz Indonesia", "BCA Insurance"
    ]
    
    # 9 Infinix & Partner Service Centers
    service_centers = [
        "Infinix Care Center - Jakarta Central",
        "Infinix Care Center - Surabaya",
        "Infinix Care Center - Bandung",
        "Infinix Care Center - Medan",
        "Infinix Care Center - Semarang",
        "Infinix Care Center - Makassar",
        "Infinix Care Center - Palembang",
        "Infinix Care Center - Denpasar",
        "Infinix Care Center - Yogyakarta"
    ]
    
    # Device Models
    device_models = [
        ("Infinix", "GT 20 Pro"), ("Infinix", "Note 40 Pro"), ("Infinix", "Zero 30 5G"), 
        ("Infinix", "Hot 40 Pro"), ("Infinix", "Smart 8"), ("Samsung", "Galaxy A55"), 
        ("Xiaomi", "Redmi Note 13"), ("OPPO", "Reno 11"), ("Vivo", "V30 5G")
    ]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days
    
    claims_raw = []
    claims_clean = []
    
    # Target 3,840 claims (~160 claims per month for 24 months = 3,840 rows)
    total_claims = 3840
    
    for i in range(1, total_claims + 1):
        claim_id = f"CLM-{20240000 + i}"
        partner = random.choice(insurance_partners)
        center = random.choice(service_centers)
        brand, model = random.choice(device_models)
        
        # Claim date distributed across 2024-2025
        random_days = random.randint(0, total_days)
        c_date = start_date + timedelta(days=random_days)
        
        # Turnaround Time (TAT): Averaging between 5.4 to 5.8 days to meet the 5-6 days SLA requirement
        # TAT distribution: 65% (3-6 days), 25% (7 days), 10% (8-12 days)
        rand_val = random.random()
        if rand_val < 0.65:
            tat = random.randint(3, 6)
        elif rand_val < 0.90:
            tat = 7
        else:
            tat = random.randint(8, 12)
            
        approval_date = c_date + timedelta(days=random.randint(0, 1))
        comp_date = c_date + timedelta(days=tat)
        
        sla_target = 7
        sla_status = "Met SLA" if tat <= sla_target else "Breached SLA"
        
        # 90% Resolved, 6% Pending, 4% Rejected
        status_rand = random.random()
        if status_rand < 0.90:
            status = "Resolved"
        elif status_rand < 0.96:
            status = "Pending"
            comp_date_str = ""
            tat_str = ""
            sla_status = "In Progress"
        else:
            status = "Rejected"
            comp_date_str = comp_date.strftime("%Y-%m-%d")
            sla_status = "Rejected Claim"
            tat_str = str(tat)

        if status != "Pending":
            comp_date_str = comp_date.strftime("%Y-%m-%d")
            tat_str = str(tat)
            
        repair_cost = random.randint(250000, 2500000)
        sparepart_cost = int(repair_cost * random.uniform(0.55, 0.75))
        csat = random.choices([5, 4, 3, 2, 1], weights=[50, 35, 10, 3, 2])[0]
        
        # Raw row (contains deliberate string anomalies for ELT learning)
        raw_row = [
            claim_id, partner, center, brand, model,
            c_date.strftime("%Y-%m-%d"),
            approval_date.strftime("%Y-%m-%d"),
            comp_date_str,
            tat_str,
            f"Rp {repair_cost:,}", # Deliberate string anomaly 'Rp '
            status,
            sla_status,
            csat
        ]
        claims_raw.append(raw_row)
        
        # Clean row
        clean_row = [
            claim_id, partner, center, brand, model,
            c_date.strftime("%Y-%m-%d"),
            approval_date.strftime("%Y-%m-%d"),
            comp_date_str,
            tat if status != "Pending" else None,
            sla_target,
            repair_cost,
            sparepart_cost,
            status,
            sla_status,
            csat
        ]
        claims_clean.append(clean_row)
        
    # Write RAW CSV
    raw_path = "c:/Users/USER/Documents/present/potrfolio/project-05-repair/data/raw/claims_sla_raw.csv"
    with open(raw_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "claim_id", "insurance_partner", "service_center", "brand", "model",
            "claim_date", "approval_date", "completion_date", "turnaround_time_days",
            "repair_cost", "status", "sla_status", "csat_rating"
        ])
        writer.writerows(claims_raw)
        
    # Write CLEAN CSV
    clean_path = "c:/Users/USER/Documents/present/potrfolio/project-05-repair/data/processed/claims_sla_clean.csv"
    with open(clean_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "claim_id", "insurance_partner", "service_center", "brand", "model",
            "claim_date", "approval_date", "completion_date", "turnaround_time_days",
            "sla_target_days", "repair_cost_idr", "sparepart_cost_idr", "status", "sla_status", "csat_rating"
        ])
        writer.writerows(claims_clean)

    print(f"Generated {total_claims} claims in {raw_path} and {clean_path}")

if __name__ == "__main__":
    generate_claims_dataset()
