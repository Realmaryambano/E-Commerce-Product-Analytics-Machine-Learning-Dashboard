import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_absolute_error, accuracy_score
import pickle
import os

def train_models():
    print("🧠 Starting Phase 6: Training ML Models...")
    
    df = pd.read_csv('data/features_ready.csv')
    
    # Define features (X) 
    features = ['price', 'rating', 'reviews', 'sold', 'category_encoded']
    X = df[features]

    # --- 1. Linear Regression (Predicting Value Score) ---
    y_reg = df['value_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    
    reg_model = LinearRegression()
    reg_model.fit(X_train, y_train)
    reg_preds = reg_model.predict(X_test)
    print(f"✅ Linear Regression MAE: {mean_absolute_error(y_test, reg_preds):.4f}")

    # --- 2. Logistic Regression (Predicting Overpriced Status) ---
    y_cls = df['is_overpriced']
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_cls, test_size=0.2, random_state=42)
    
    clf_model = LogisticRegression(max_iter=1000)
    clf_model.fit(X_train_c, y_train_c)
    clf_preds = clf_model.predict(X_test_c)
    print(f"✅ Logistic Regression Accuracy: {accuracy_score(y_test_c, clf_preds):.2%}")

    # --- 3. KNN (For "Similar Product" Recommendations) ---
    # We use the PCA coordinates for KNN as it's great for spatial similarity
    X_knn = df[['pca_1', 'pca_2']]
    knn_model = NearestNeighbors(n_neighbors=5)
    knn_model.fit(X_knn)
    print("✅ KNN Model trained for recommendations.")

    # --- Save All Models ---
    os.makedirs('models', exist_ok=True)
    with open('models/linear_reg.pkl', 'wb') as f:
        pickle.dump(reg_model, f)
    with open('models/logistic_clf.pkl', 'wb') as f:
        pickle.dump(clf_model, f)
    with open('models/knn_model.pkl', 'wb') as f:
        pickle.dump(knn_model, f)

    print("\n🚀 All models saved to the /models folder!")

if __name__ == "__main__":
    train_models()