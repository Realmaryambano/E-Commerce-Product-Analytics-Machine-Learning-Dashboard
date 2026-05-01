import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    print("📊 Starting Phase 4: Exploratory Data Analysis...")
    
    # Load the cleaned data
    if not os.path.exists('data/clean_products.csv'):
        print("❌ Error: data/clean_products.csv not found!")
        return

    df = pd.read_csv('data/clean_products.csv')
    
    # Create a folder for plots if it doesn't exist
    os.makedirs('plots', exist_ok=True)
    
    # Set the visual style
    sns.set_theme(style="whitegrid")

    # --- Chart 1: Price Distribution by Category (Boxplot) ---
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='category', y='price', data=df, palette='viridis')
    plt.yscale('log') # Log scale because phone prices vary so much
    plt.title('Price Range by Category (Log Scale)')
    plt.ylabel('Price (Rs.)')
    plt.xlabel('Category')
    plt.savefig('plots/1_price_distribution.png')
    plt.close()

    # --- Chart 2: Ratings vs Price (Scatter Plot) ---
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='price', y='rating', hue='price_tier', size='sold', 
                    data=df, alpha=0.6, sizes=(20, 200))
    plt.xscale('log')
    plt.title('Ratings vs Price (Size = Sold Count)')
    plt.xlabel('Price (Log Scale)')
    plt.ylabel('User Rating')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('plots/2_ratings_vs_price.png')
    plt.close()

    # --- Chart 3: Correlation Heatmap ---
    plt.figure(figsize=(8, 6))
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    correlation = numeric_df.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Feature Correlation Heatmap')
    plt.savefig('plots/3_correlation_heatmap.png')
    plt.close()

    print("✅ EDA Complete!")
    print("Check the 'plots' folder in your project directory for the images.")

if __name__ == "__main__":
    run_eda()