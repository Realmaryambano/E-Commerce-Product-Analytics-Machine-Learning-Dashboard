import pandas as pd
import numpy as np
import os

# 1. Load data
raw_path = "data/raw_products.csv"
if not os.path.exists(raw_path):
    print(f"File not found: {raw_path}")
else:
    df = pd.read_csv(raw_path)
    print(f"Raw data shape: {df.shape}")

    # 2. Basic Cleaning
    df.drop_duplicates(subset=["name", "price", "category"], inplace=True)
    df = df[df["price"] >= 50].copy() # Using .copy() prevents SettingWithCopy warnings
    print(f"After initial filters: {df.shape}")

    # 3. Fix missing ratings
    # If a category has NO ratings at all, transform might fail, so we handle that
    df["rating"] = df["rating"].replace(0, np.nan)
    df["rating"] = df.groupby("category")["rating"].transform(lambda x: x.fillna(x.mean() if x.notnull().any() else 3.0))
    df["rating"] = df["rating"].fillna(3.0).round(1)

    # 4. Fix missing sold/reviews
    df["sold"] = df["sold"].fillna(0).astype(int)
    df["reviews"] = df["reviews"].fillna(0).astype(int)

    # 5. Create Value Score
    df["value_score"] = (df["rating"] / df["price"]) * 10000

    # 6. Create Price Tiers & Overpriced Label (The Stable Way)
    # Instead of complex .apply(), we use transform to keep the 'category' column safe
    
    # Calculate quantiles per category
    df['q33'] = df.groupby('category')['price'].transform(lambda x: x.quantile(0.33))
    df['q66'] = df.groupby('category')['price'].transform(lambda x: x.quantile(0.66))
    df['p75'] = df.groupby('category')['price'].transform(lambda x: x.quantile(0.75))
    df['avg_rating'] = df.groupby('category')['rating'].transform('mean')

    # Assign Price Tier
    def logic_tier(row):
        if row['price'] <= row['q33']: return "Budget"
        if row['price'] <= row['q66']: return "Mid-Range"
        return "Premium"

    df['price_tier'] = df.apply(logic_tier, axis=1)

    # Assign Overpriced Label (Target for Logistic Regression)
    df['is_overpriced'] = ((df['price'] > df['p75']) & (df['rating'] < df['avg_rating'])).astype(int)

    # 7. Cleanup temp columns and save
    df = df.drop(columns=['q33', 'q66', 'p75', 'avg_rating'])
    
    df.to_csv("data/clean_products.csv", index=False)
    
    print("\n✅ Cleaning Successful!")
    print(f"Final shape: {df.shape}")
    print(df["price_tier"].value_counts())
    print(f"Overpriced items detected: {df['is_overpriced'].sum()}")