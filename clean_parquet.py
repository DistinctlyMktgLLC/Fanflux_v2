import pandas as pd

# Load the parquet file
parquet_file = "data/Fanflux_Intensity_All_Leagues_Cleaned.parquet"
df = pd.read_parquet(parquet_file)

# List of needed columns
needed_columns = [
    'dCategory', 'Team', 'League', 'City', 'Neighborhood',
    'zipcode', 'US lat', 'US lon', 'Intensity', 'Fandom Level', 'Race',
    'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
    'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
    'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
]

# Remove unwanted columns
df_cleaned = df[needed_columns]

# Save the cleaned dataframe to a new parquet file
cleaned_parquet_file = "data/Fanflux_Intensity_All_Leagues_Cleaned_Final.parquet"
df_cleaned.to_parquet(cleaned_parquet_file)

print("Cleaned dataset saved to", cleaned_parquet_file)
