import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import os

# Set Page Config
st.set_page_config(page_title="AI E-Commerce Intelligence", layout="wide")

# --- Load Data and Models ---
@st.cache_resource
def load_assets():
    df = pd.read_csv('data/features_ready.csv')
    with open('models/linear_reg.pkl', 'rb') as f: reg = pickle.load(f)
    with open('models/logistic_clf.pkl', 'rb') as f: clf = pickle.load(f)
    with open('models/knn_model.pkl', 'rb') as f: knn = pickle.load(f)
    with open('models/le_cat.pkl', 'rb') as f: le = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f: scaler = pickle.load(f)
    return df, reg, clf, knn, le, scaler

df, reg_model, clf_model, knn_model, le_cat, scaler = load_assets()

# --- Title ---
st.title("🛍️ AI E-Commerce Intelligence Dashboard")
st.markdown("Exploring Daraz Market Data with Machine Learning")

# --- Sidebar ---
st.sidebar.header("Filter Data")
category = st.sidebar.selectbox("Select Category", df['category'].unique())
price_range = st.sidebar.slider("Price Range (Rs.)", 
                                 int(df['price'].min()), 
                                 int(df['price'].max()), 
                                 (int(df['price'].min()), int(df['price'].max())))

filtered_df = df[(df['category'] == category) & 
                 (df['price'].between(price_range[0], price_range[1]))]

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Product Analysis: {category}")
    fig = px.scatter(filtered_df, x="price", y="rating", 
                     color="price_tier", size="sold", 
                     hover_name="name", log_x=True,
                     title="Price vs Rating (Size = Sales)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🤖 AI Price Checker")
    user_price = st.number_input("Enter Price (Rs.)", value=25000)
    user_rating = st.slider("Target Rating", 1.0, 5.0, 4.0)
    
    # Prepare input for prediction
    cat_enc = le_cat.transform([category])[0]
    # We'll assume average 'sold' and 'reviews' for a new prediction
    input_data = np.array([[user_price, user_rating, 10, 5, cat_enc]]) 
    
    is_overpriced = clf_model.predict(input_data)[0]
    predicted_value = reg_model.predict(input_data)[0]

    if is_overpriced == 1:
        st.error("🚩 ML Assessment: Overpriced/Bad Deal")
    else:
        st.success("✅ ML Assessment: Fair Deal")
    
    st.metric("Predicted Value Score", round(predicted_value, 2))

st.divider()

# --- Clustering Visualization ---
st.subheader("🧬 Product Clusters (PCA Analysis)")
fig_pca = px.scatter(df, x="pca_1", y="pca_2", color="category", 
                     hover_name="name", title="High-Dimensional Product Mapping")
st.plotly_chart(fig_pca, use_container_width=True)

# --- Recommendations ---
st.subheader("✨ Intelligent Recommendations")
selected_product = st.selectbox("Pick a product to find similar deals:", df[df['category']==category]['name'].head(50))
if selected_product:
    product_idx = df[df['name'] == selected_product].index[0]
    coords = df.iloc[product_idx][['pca_1', 'pca_2']].values.reshape(1, -1)
    distances, indices = knn_model.kneighbors(coords)
    
    rec_cols = st.columns(4)
    for i, idx in enumerate(indices[0][1:5]):
        with rec_cols[i]:
            st.info(f"**{df.iloc[idx]['name'][:30]}...**")
            st.write(f"Price: Rs. {df.iloc[idx]['price']}")
            st.write(f"Rating: {df.iloc[idx]['rating']} ⭐")