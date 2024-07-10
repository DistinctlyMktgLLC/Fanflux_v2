import pandas as pd

# Load the combined DataFrame
df_combined = pd.read_parquet('data/combined_leagues.parquet')

# Print the columns to check their names
print(df_combined.columns)
