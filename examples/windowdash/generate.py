import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_windowdash_data(num_rows=15000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    # --- 1. Base Setup ---
    # Zip Codes & Archetypes
    # 10003: NYU (Campus Late-Nighters)
    # 11215: Park Slope (Family Suburbs)
    # 10036: Midtown (Office Lunch Rush)
    # 10011: Chelsea (General)
    # 11201: Brooklyn Heights (General)
    zips = ['10003', '11215', '10036', '10011', '11201']
    zip_weights = [0.25, 0.20, 0.25, 0.15, 0.15]
    
    data = {
        'OrderID': [f'WD-{100000+i}' for i in range(num_rows)],
        'ZipCode': np.random.choice(zips, size=num_rows, p=zip_weights)
    }
    df = pd.DataFrame(data)

    # --- 2. Temporal Generation ---
    # Full year 2024
    start_date = datetime(2024, 1, 1)
    # Weighted dates? Maybe slight weekend bias
    days_in_year = 366
    
    # Generate random timestamps
    dates = []
    for _ in range(num_rows):
        day_offset = random.randint(0, days_in_year-1)
        hour = random.randint(10, 23) # 10 AM to 11 PM base
        minute = random.randint(0, 59)
        d = start_date + timedelta(days=day_offset, hours=hour, minutes=minute)
        dates.append(d)
        
    df['Date'] = dates
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month
    df['Hour'] = df['Date'].dt.hour
    
    # --- 3. Demographics ---
    # Age: 18-75
    df['CustomerAge'] = np.random.randint(18, 75, size=num_rows)
    
    # --- 4. Logic Loop (Cuisine, Price, Type) ---
    cuisines = ['Pizza', 'Asian', 'Burger', 'Mexican', 'Healthy', 'Dessert']
    order_types = []
    cuisine_choices = []
    prices = []
    tips = []
    ratings = []
    times = []
    
    # Pre-select "Rainy Days" -> REMOVED
    # Pattern 5 is now Geo-Spatial (Healthy Enclave)
    
    for idx, row in df.iterrows():
        zip_code = row['ZipCode']
        date_obj = row['Date']
        hour = row['Hour']
        day = row['DayOfWeek']
        age = row['CustomerAge']
        month = row['Month']
        
        # Default Probs
        c_probs = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1] 
        # ['Pizza', 'Asian', 'Burger', 'Mexican', 'Healthy', 'Dessert']
        
        o_type = np.random.choice(['Delivery', 'Pickup'], p=[0.7, 0.3])
        
        # --- PATTERN 1: Campus Late-Nighters (10003) ---
        if zip_code == '10003' and (hour >= 22 or hour <= 3):
            # Boost Asian/Burger drastically
            c_probs = [0.05, 0.45, 0.45, 0.05, 0.0, 0.0]
            
        # --- PATTERN 2: Family Suburbs (11215) ---
        if zip_code == '11215':
             # General Price Boost for Park Slope
             base_price_boost = 20 
             if day == 'Friday':
                # Boost Pizza significantly on Fridays
                c_probs = [0.7, 0.05, 0.05, 0.1, 0.05, 0.05]
                base_price_boost = 60 # Massive boost on Friday Pizza night
             
        # --- PATTERN 3: Office Lunch Rush (10036) ---
        if zip_code == '10036' and day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and 11 <= hour <= 13:
            # Boost Pickup significantly
            o_type = np.random.choice(['Delivery', 'Pickup'], p=[0.1, 0.9])
            # Boost Healthy/Mexican
            c_probs = [0.05, 0.15, 0.05, 0.35, 0.40, 0.0]
            
        # --- PATTERN 4: Sunday Scaries (Dessert) ---
        if day == 'Sunday' and 18 <= hour <= 22:
            # Boost Dessert
            c_probs = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
            
        # --- PATTERN 6: New Year's Resolution (Jan Healthy) ---
        if month == 1:
            # Boost Healthy globaly
            c_probs[4] += 0.2 # Healthy
            # Normalize
            c_probs = np.array(c_probs) / np.sum(c_probs)
            
        # --- PATTERN 8: Age-Cuisine Split ---
        if age > 50:
            # Drop Mexican/Burger at night
            if hour > 20:
                c_probs[2] = 0.0 # Burger
                c_probs[3] = 0.0 # Mexican
                c_probs = np.array(c_probs) / np.sum(c_probs)
        elif age < 25:
            # Boost Dessert
            c_probs[5] += 0.3
            c_probs = np.array(c_probs) / np.sum(c_probs)

        # --- PATTERN 5: The Healthy Enclave (10011) ---
        if zip_code == '10011':
            # Boost Healthy Significantly (>50%)
            c_probs = [0.05, 0.1, 0.05, 0.1, 0.60, 0.1]
            
        # Select Cuisine
        cuisine = np.random.choice(cuisines, p=c_probs)
        cuisine_choices.append(cuisine)
        
        # Order Price
        base = np.random.normal(25, 10)
        
        # Family Suburbs Price Logic Update
        if zip_code == '11215':
            base += 40 # Richer neighborhood baseline
            if day == 'Friday' and cuisine == 'Pizza':
                 base += 30 # The big Friday order
                 
        if cuisine == 'Dessert':
            base = np.random.normal(15, 5)
            
        price = max(8.0, base)
            
        order_types.append(o_type)
        prices.append(round(price, 2))
        
        # Delivery Time
        d_time = np.nan
        if o_type == 'Delivery':
            base_time = np.random.normal(30, 10)
            d_time = max(10, base_time)
        times.append(round(d_time, 1) if pd.notna(d_time) else np.nan)
        
        # --- PATTERN 7: Tipping Curve ---
        tip = 0.0
        if o_type == 'Delivery':
            # Linear 15% + noise
            tip = price * 0.15 + np.random.normal(0, 1)
            # Campus Late Nighters (10003) low tip
            if zip_code == '10003' and (hour >= 22 or hour <= 3):
                tip = np.random.uniform(0, 2)
        else:
            # Pickup - mostly zero
            if np.random.random() < 0.1: # 10% chance of small tip
                tip = np.random.uniform(1, 4)
                
        tips.append(max(0.0, round(tip, 2)))
        
        # --- PATTERN 9: Price-Rating Inverse ---
        rating_prob = [0.05, 0.05, 0.1, 0.3, 0.5] # Skew to 5
        if price > 100 and pd.notna(d_time) and d_time > 45:
             # Punish expensive slow orders
             rating_prob = [0.4, 0.3, 0.2, 0.1, 0.0]
             
        ratings.append(np.random.choice([1,2,3,4,5], p=rating_prob))

    df['OrderType'] = order_types
    df['Cuisine'] = cuisine_choices
    df['OrderPrice'] = prices
    df['TipAmount'] = tips
    df['CustomerRating'] = ratings
    df['DeliveryTime'] = times
    
    # Drop temp cols
    df = df.drop(columns=['DayOfWeek', 'Month', 'Hour'])
    
    print("WindowDash Data Generated!")
    print(df.head())
    return df

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.spec) as handle:
        specification = json.load(handle)
    generate_windowdash_data(specification["row_count"], args.seed).to_csv(args.output, index=False)
