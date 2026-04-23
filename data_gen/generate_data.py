import os
import duckdb
import pandas as pd
import random
from datetime import datetime, timedelta

def main():
    # Ensure directories exist
    os.makedirs('data_gen/csv', exist_ok=True)
    os.makedirs('dbt_project', exist_ok=True)

    # Generate dates
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(180)]

    verticals = ['Ride Hailing', 'Food Delivery', 'Courier']

    # 1. Sales Data
    sales_data = []
    for d in dates:
        for v in verticals:
            orders = random.randint(100, 1000)
            revenue = orders * random.uniform(500, 2000)
            rider_payouts = revenue * random.uniform(0.6, 0.8)
            sales_data.append({
                'date': d.strftime('%Y-%m-%d'),
                'vertical': v,
                'orders': orders,
                'revenue': round(revenue, 2),
                'rider_payouts': round(rider_payouts, 2),
                'messy_col_ignore': random.choice(['null', 'N/A', ''])
            })
    
    # 2. Marketing Data
    marketing_data = []
    for d in dates:
        for v in verticals:
            marketing_spend = random.uniform(5000, 50000)
            marketing_data.append({
                'campaign_date': d.strftime('%m/%d/%Y'), # Messy date format
                'business_vertical': v.lower(), # Messy casing
                'direct_marketing_spend': round(marketing_spend, 2)
            })

    # 3. Logistics Data
    logistics_data = []
    for d in dates:
        for v in verticals:
            distance_km = random.uniform(500, 5000)
            fuel_consumed_liters = distance_km / random.uniform(10, 40) # 10 to 40 km/l
            logistics_data.append({
                'dt': d.strftime('%Y-%m-%d'),
                'vert': v.upper(), # Messy casing
                'distance_km': round(distance_km, 2),
                'fuel_consumed_liters': round(fuel_consumed_liters, 2)
            })

    # Save to CSV
    pd.DataFrame(sales_data).to_csv('data_gen/csv/sales.csv', index=False)
    pd.DataFrame(marketing_data).to_csv('data_gen/csv/marketing.csv', index=False)
    pd.DataFrame(logistics_data).to_csv('data_gen/csv/logistics.csv', index=False)

    # Initialize DuckDB and load into raw schema
    db_path = 'dbt_project/analytics.duckdb'
    
    # Connect to DuckDB (creates the file if it doesn't exist)
    conn = duckdb.connect(db_path)
    
    # Create schema
    conn.execute('CREATE SCHEMA IF NOT EXISTS raw;')
    
    # Load data into DuckDB tables
    conn.execute('''
        CREATE OR REPLACE TABLE raw.sales AS 
        SELECT * FROM read_csv_auto('data_gen/csv/sales.csv');
    ''')
    
    conn.execute('''
        CREATE OR REPLACE TABLE raw.marketing AS 
        SELECT * FROM read_csv_auto('data_gen/csv/marketing.csv');
    ''')
    
    conn.execute('''
        CREATE OR REPLACE TABLE raw.logistics AS 
        SELECT * FROM read_csv_auto('data_gen/csv/logistics.csv');
    ''')

    print("Data generated and loaded into DuckDB 'raw' schema successfully.")
    conn.close()

if __name__ == "__main__":
    main()
