import csv

def format_pl_for_db():
    input_file = "c:/Users/USER/Documents/present/potrfolio/project-01-sales/data/processed/pl_multi_channel_clean.csv"
    output_file = "c:/Users/USER/Documents/present/potrfolio/project-01-sales/data/processed/pl_unified_clean.csv"
    
    rows = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            store_id = int(row["partner_id"].replace("PTR-", ""))
            rows.append([
                i, # pl_id (1 to 1800)
                store_id,
                row["month_date"],
                row["gross_revenue_idr"],
                row["cogs_idr"],
                row["gross_profit_idr"],
                row["operating_expenses_idr"],
                row["net_profit_idr"],
                row["net_profit_margin_pct"]
            ])
            
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "pl_id", "store_id", "month_date", "gross_revenue_idr", "cogs_idr",
            "gross_profit_idr", "operating_expenses_idr", "net_profit_idr", "net_profit_margin_pct"
        ])
        writer.writerows(rows)
        
    print(f"Successfully generated {len(rows)} database-ready P&L records with pl_id in {output_file}")

if __name__ == "__main__":
    format_pl_for_db()
