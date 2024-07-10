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

# Create a combined 'Income Level' column for tooltip purposes
income_columns = [
    'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

# Merge the income columns into a single 'Income Level' column for tooltips
def merge_income_levels(row):
    levels = [col for col in income_columns if row[col] == '1.0']
    return ', '.join(levels)

df_combined['Income Level'] = df_combined.apply(merge_income_levels, axis=1)

# Save the combined DataFrame as a new Parquet file
df_combined.to_parquet('data/combined_leagues.parquet')
