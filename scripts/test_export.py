import pandas as pd
import os

print("Testing export...")
print(f"Current dir: {os.getcwd()}")

# Load data
df = pd.read_csv('../data/raw/DataCoSupplyChainDataset.csv', encoding='latin-1')
print(f"Loaded {len(df)} rows")

# Create simple export
test_df = df[['Order Id', 'Sales']].head(10)
test_df.to_csv('../data/powerbi/test.csv', index=False)
print("Saved test.csv")

# Check if file exists
if os.path.exists('../data/powerbi/test.csv'):
    print("✅ File created successfully!")
else:
    print("❌ File not found")
