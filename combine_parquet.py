import pandas as pd
import os

# Define the directory containing the CSV files
data_dir = 'data'

# Define the columns with their desired data types
column_types = {
    'dCategory': 'object',
    'Team': 'object',
    'League': 'object',
    'City': 'object',
    'City Alt.': 'object',
    'Neighborhood': 'object',
    'zipcode': 'float64',
    'US lat': 'float64',
    'US lon': 'float64',
    'Intensity Score': 'float64',
    'Race': 'object',
    'Fandom Level': 'object',
    'Struggling (Less than $10,000)': 'float64',
    'Getting By ($10,000 to $14,999)': 'float64',
    'Getting By ($15,000 to $19,999)': 'float64',
    'Starting Out ($20,000 to $24,999)': 'float64',
    'Starting Out ($25,000 to $29,999)': 'float64',
    'Starting Out ($30,000 to $34,999)': 'float64',
    'Middle Class ($35,000 to $39,999)': 'float64',
    'Middle Class ($40,000 to $44,999)': 'float64',
    'Middle Class ($45,000 to $49,999)': 'float64',
    'Comfortable ($50,000 to $59,999)': 'float64',
    'Comfortable ($60,000 to $74,999)': 'float64',
    'Doing Well ($75,000 to $99,999)': 'float64',
    'Prosperous ($100,000 to $124,999)': 'float64',
    'Prosperous ($125,000 to $149,999)': 'float64',
    'Wealthy ($150,000 to $199,999)': 'float64',
    'Affluent ($200,000 or more)': 'float64'
}

# Function to clean data by replacing non-numeric values with 0
def clean_data(df):
    for column, dtype in column_types.items():
        if column in df.columns and dtype == 'float64':
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
    return df

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over each file in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(data_dir, filename)
        
        # Read the CSV file
        df = pd.read_csv(filepath)
        
        # Clean the data
        df = clean_data(df)
        
        # Ensure consistent data types
        for column, dtype in column_types.items():
            if column in df.columns:
                df[column] = df[column].astype(dtype)
        
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames
df_combined = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a Parquet file
df_combined.to_parquet('data/combined_leagues.parquet', index=False)
