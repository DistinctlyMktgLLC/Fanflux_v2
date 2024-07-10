import pandas as pd

# Load all individual CSV files into a single DataFrame
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
    # Add paths for NBA, NFL, NHL, MLS files as needed
]

df_list = [pd.read_csv(file) for file in csv_files]
df_all = pd.concat(df_list, ignore_index=True)

# Save the combined DataFrame to a Parquet file
df_all.to_parquet("data/Fanflux_Intensity_All_Leagues.parquet")
