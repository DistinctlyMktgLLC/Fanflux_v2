# convert_csv_to_parquet.py
import pandas as pd
import os

# Define a list of CSV file paths and their corresponding Parquet file paths
files = [
    ('data/Fanflux_Intensity_MLB_AAPI.csv', 'data/Fanflux_Intensity_MLB_AAPI.parquet'),
    ('data/Fanflux_Intensity_MLB_AmericanIndian.csv', 'data/Fanflux_Intensity_MLB_AmericanIndian.parquet'),
    ('data/Fanflux_Intensity_MLB_Asian.csv', 'data/Fanflux_Intensity_MLB_Asian.parquet'),
    ('data/Fanflux_Intensity_MLB_Black.csv', 'data/Fanflux_Intensity_MLB_Black.parquet'),
    ('data/Fanflux_Intensity_MLB_Hispanic.csv', 'data/Fanflux_Intensity_MLB_Hispanic.parquet'),
    ('data/Fanflux_Intensity_MLB_White.csv', 'data/Fanflux_Intensity_MLB_White.parquet'),
    # Add more files as needed
]

# Convert each CSV file to a Parquet file
for csv_file_path, parquet_file_path in files:
    if os.path.exists(csv_file_path):
        # Load the CSV file
        data = pd.read_csv(csv_file_path)
        # Save the DataFrame as a Parquet file
        data.to_parquet(parquet_file_path, index=False)
        print(f"CSV file {csv_file_path} has been converted to Parquet and saved at {parquet_file_path}")
    else:
        print(f"CSV file {csv_file_path} does not exist")
