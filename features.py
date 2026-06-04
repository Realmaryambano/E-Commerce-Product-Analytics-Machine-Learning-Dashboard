import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import pickle 
import os

def prepare_features():
    print("🧪 Starting Phase 5: Feature Engineering & PCA...")
    
    if not os.path.exists('data/clean_products.csv'):
        print("❌ Error: data/clean_products.csv not found!")
        return

    df = pd.read_csv('data/clean_products.csv')

    # 1. Encode Categorical Data
    le_cat = LabelEncoder()
    df['category_encoded'] = le_cat.fit_transform(df['category'])
    
    le_tier = LabelEncoder()
    df['tier_encoded'] = le_tier.fit_transform(df['price_tier'])

    # 2. Select features for Scaling and PCA
    # We use these to find similar products and train models
    feature_cols = ['price', 'rating', 'reviews', 'sold', 'category_encoded']
    X = df[feature_cols]

    # 3. Standardize the data (Mean=0, Variance=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Apply PCA (Reduce to 2 dimensions for visualization)
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(X_scaled)
    df['pca_1'] = pca_results[:, 0]
    df['pca_2'] = pca_results[:, 1]

    # 5. Save the prepared data
    df.to_csv('data/features_ready.csv', index=False)

    # 6. Save the Scaler, Encoder, and PCA for the App
    os.makedirs('models', exist_ok=True)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('models/le_cat.pkl', 'wb') as f:
        pickle.dump(le_cat, f)
    with open('models/pca_model.pkl', 'wb') as f:
        pickle.dump(pca, f)

    print("✅ Feature Engineering Complete!")
    print(f"- Scaler saved to models/scaler.pkl")
    print(f"- PCA components added to data/features_ready.csv")
    print(f"- Variance explained by PCA: {np.sum(pca.explained_variance_ratio_):.2f}")

if __name__ == "__main__":
    prepare_features()