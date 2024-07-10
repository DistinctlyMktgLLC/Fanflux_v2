import pandas as pd

# Load the cleaned parquet file
cleaned_parquet_file = "data/Fanflux_Intensity_All_Leagues_Cleaned_Final.parquet"
df = pd.read_parquet(cleaned_parquet_file)

# Print basic information about the dataframe
print("Columns in the dataframe:")
print(df.columns)

print("\nData types of each column:")
print(df.dtypes)

print("\nFirst few rows of the dataframe:")
print(df.head())

# Check for missing columns
required_columns = [
    'League', 'Team', 'Fandom Level', 'Race',
    'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
    'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
    'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print("\nMissing columns:")
    print(missing_columns)
else:
    print("\nAll required columns are present.")
