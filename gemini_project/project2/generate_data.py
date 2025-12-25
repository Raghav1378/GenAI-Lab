import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# === Configuration ===
NUM_ROWS = 2500
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
OUTPUT_DIR = "data"
OUTPUT_FILE = "sales_data_large.csv"

# Ensure data directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

print(f"Generating {NUM_ROWS} rows of synthetic data...")

# === Data Definitions ===
regions = ['North', 'South', 'East', 'West', 'Central']
channels = ['Online', 'In-Store', 'Distributor']
products_map = {
    'Electronics': {
        'Laptop': (800, 2500), 'Smartphone': (400, 1200), 'Headphones': (50, 300), 'Monitor': (150, 500)
    },
    'Furniture': {
        'Office Chair': (100, 500), 'Desk': (200, 800), 'Bookshelf': (80, 250)
    },
    'Office Supplies': {
        'Printer Paper': (10, 30), 'Stapler': (5, 15), 'Binder Pack': (15, 40), 'Pen Box': (5, 20)
    }
}
categories = list(products_map.keys())

# === Generation Logic ===
# 1. Dates
days_diff = (END_DATE - START_DATE).days
random_days = np.random.randint(0, days_diff, NUM_ROWS)
dates = [START_DATE + timedelta(days=int(d)) for d in random_days]

# 2. Categorical Data
chosen_regions = np.random.choice(regions, NUM_ROWS)
chosen_channels = np.random.choice(channels, NUM_ROWS, p=[0.6, 0.3, 0.1]) # Weighted towards Online
chosen_categories = np.random.choice(categories, NUM_ROWS)

# 3. Product & Price Logic (dependent on category)
chosen_products = []
unit_prices = []

for cat in chosen_categories:
    # Pick a random product within the chosen category
    prod_name = np.random.choice(list(products_map[cat].keys()))
    chosen_products.append(prod_name)
    
    # Generate a random price within the defined range for that product
    price_range = products_map[cat][prod_name]
    price = np.round(np.random.uniform(price_range[0], price_range[1]), 2)
    unit_prices.append(price)

# 4. Numerical Data
quantity = np.random.randint(1, 25, NUM_ROWS)
unit_prices = np.array(unit_prices)
total_sales = np.round(quantity * unit_prices, 2)

# Add some "Profit Margin" randomness (e.g., 20% to 50% margin)
profit_margin = np.random.uniform(0.20, 0.50, NUM_ROWS)
profit = np.round(total_sales * profit_margin, 2)

# === Assemble DataFrame ===
df = pd.DataFrame({
    'Order Date': dates,
    'Region': chosen_regions,
    'Sales Channel': chosen_channels,
    'Category': chosen_categories,
    'Product Name': chosen_products,
    'Quantity': quantity,
    'Unit Price': unit_prices,
    'Total Sales': total_sales,
    'Profit': profit
})

# Sort by date for realism
df = df.sort_values('Order Date').reset_index(drop=True)

# === Save to CSV ===
df.to_csv(output_path, index=False)
print(f"Success! Data saved to: {output_path}")
print("-" * 30)
print("Sample Data:")
print(df.head())