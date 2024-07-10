import pandas as pd

# Load the combined Parquet file
df_combined = pd.read_parquet('data/combined_leagues.parquet')

# Display the first few rows
print(df_combined.head())
