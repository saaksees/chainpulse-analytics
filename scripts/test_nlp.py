import pandas as pd
import nltk

print("Testing NLP setup...")

# Download NLTK data
print("Downloading NLTK data...")
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')

print("Loading data...")
df = pd.read_csv('../data/raw/DataCoSupplyChainDataset.csv', encoding='latin-1')
print(f"Loaded {len(df)} rows")
print(f"Unique products: {df['Product Name'].nunique()}")
print("Test complete!")
