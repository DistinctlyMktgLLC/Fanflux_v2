import os
import pandas as pd

data_dir = 'data'
required_files = [
    "Fanflux_Intensity_MLB_AAPI.parquet",
    "Fanflux_Intensity_MLB_American_Indian.parquet",
    "Fanflux_Intensity_MLB_Asian.parquet",
    "Fanflux_Intensity_MLB_Black.parquet",
    "Fanflux_Intensity_MLB_Hispanic.parquet",
    "Fanflux_Intensity_MLB_White.parquet",
    # Add other files for NBA, NFL, NHL, MLS, etc.
]

required_columns = ["Race", "Team", "League", "Fandom_Level", "Income_Level"]

for file in required_files:
    file_path = os.path.join(data_dir, file)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        df = pd.read_parquet(file_path)
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"File {file_path} is missing columns: {missing_columns}")
        else:
            print(f"File {file_path} is valid.")
