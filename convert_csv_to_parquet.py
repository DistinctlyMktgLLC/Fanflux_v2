import pandas as pd

# List of all individual CSV files
csv_files = [
    "data/Fanflux_Intensity_MLB_AAPI.csv",
    "data/Fanflux_Intensity_MLB_American_Indian.csv",
    "data/Fanflux_Intensity_MLB_Asian.csv",
    "data/Fanflux_Intensity_MLB_Black.csv",
    "data/Fanflux_Intensity_MLB_Hispanic.csv",
    "data/Fanflux_Intensity_MLB_White.csv",
    "data/Fanflux_Intensity_NBA_AAPI.csv",
    "data/Fanflux_Intensity_NBA_American Indian.csv",
    "data/Fanflux_Intensity_NBA_Asian.csv",
    "data/Fanflux_Intensity_NBA_Black.csv",
    "data/Fanflux_Intensity_NBA_Hispanic.csv",
    "data/Fanflux_Intensity_NBA_White.csv",
    "data/Fanflux_Intensity_NFL_Black.csv",
    "data/Fanflux_Intensity_NFL_Hispanic.csv",
    "data/Fanflux_Intensity_NFL_White.csv",
    "data/Fanflux_Intensity_NHL_AAPI.csv",
    "data/Fanflux_Intensity_NHL_American_Indian.csv",
    "data/Fanflux_Intensity_NHL_Asian.csv",
    "data/Fanflux_Intensity_NHL_Black.csv",
    "data/Fanflux_Intensity_NHL_Hispanic.csv",
    "data/Fanflux_Intensity_NHL_White.csv",
    # Add paths for MLS files as needed
]

# Load all individual CSV files into a single DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
df_all = pd.concat(df_list, ignore_index=True)

# Clean the data: Remove 'mapping' column if it exists
if 'mapping' in df_all.columns:
    df_all.drop(columns=['mapping'], inplace=True)

# Convert columns to appropriate data types
def convert_columns_to_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# List of income columns that need conversion
income_columns = [
    "Struggling (Less than $10,000)",
    "Getting By ($10,000 to $14,999)",
    "Getting By ($15,000 to $19,999)",
    "Starting Out ($20,000 to $24,999)",
    "Starting Out ($25,000 to $29,999)",
    "Starting Out ($30,000 to $34,999)",
    "Middle Class ($35,000 to $39,999)",
    "Middle Class ($40,000 to $44,999)",
    "Middle Class ($45,000 to $49,999)",
    "Comfortable ($50,000 to $59,999)",
    "Comfortable ($60,000 to $74,999)",
    "Doing Well ($75,000 to $99,999)",
    "Prosperous ($100,000 to $124,999)",
    "Prosperous ($125,000 to $149,999)",
    "Wealthy ($150,000 to $199,999)",
    "Affluent ($200,000 or more)"
]

# Apply the conversion function
df_all = convert_columns_to_numeric(df_all, income_columns)

# Save the cleaned DataFrame to a Parquet file
df_all.to_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned.parquet")
