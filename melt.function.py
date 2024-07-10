import pandas as pd
import glob

# List of parquet files
parquet_files = glob.glob('data/*.parquet')

# Read each parquet file into a DataFrame
dfs = []
for file in parquet_files:
    df = pd.read_parquet(file)
    dfs.append(df)

# Combine all DataFrames into one
df_combined = pd.concat(dfs, ignore_index=True)

# Ensure correct data types
for column in df_combined.columns:
    if df_combined[column].dtype == 'object':
        try:
            df_combined[column] = pd.to_numeric(df_combined[column], errors='coerce')
        except:
            df_combined[column] = df_combined[column].astype(str)

# Save the combined DataFrame to a new parquet file
df_combined.to_parquet('data/combined_leagues.parquet')

print("Combined parquet file created successfully.")
