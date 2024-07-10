import pandas as pd
import os

# Define the directory containing the Parquet files
parquet_dir = 'data/'

# List all Parquet files in the directory
parquet_files = [f for f in os.listdir(parquet_dir) if f.endswith('.parquet')]

# Read and combine the Parquet files
df_list = [pd.read_parquet(os.path.join(parquet_dir, file)) for file in parquet_files]
df_combined = pd.concat(df_list, ignore_index=True)

# Ensure all columns are strings to avoid mixed data type issues
df_combined = df_combined.applymap(str)

# Save the combined DataFrame as a new Parquet file
df_combined.to_parquet('data/combined_leagues.parquet')
