import pandas as pd

df = pd.read_csv('../data/processed/customer_segments.csv')
print(f'Total customers: {len(df):,}')
print(f'\nColumns: {list(df.columns)}')
print(f'\nSegment distribution:')
print(df['Segment'].value_counts())
print(f'\nCluster distribution:')
print(df['Cluster_Name'].value_counts())
print(f'\nSample data:')
print(df.head())
