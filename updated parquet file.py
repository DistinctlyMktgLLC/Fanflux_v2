import polars as pl

# Load the data
df = pl.read_parquet('data/combined_leagues.parquet')

# Define the income columns
income_columns = [
    'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
    'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
    'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
]

# Ensure no existing 'Total Fans' column
df = df.drop('Total Fans', None)  # `None` avoids error if the column doesn't exist

# Add the Total Fans column by summing across income columns
df = df.with_columns([
    pl.sum_horizontal([pl.col(col) for col in income_columns]).alias('Total Fans')
])

# Correct the Fandom Level column to title case
df = df.with_columns([
    pl.col("Fandom Level").str.to_lowercase().str.to_title_case().alias("Fandom Level")
])

# Save the updated dataframe back to a parquet file
df.write_parquet('data/updated_combined_leagues.parquet')

print("Parquet file updated with Total Fans column and corrected Fandom Level.")
