import pandas as pd
import os

# Directory where the CSV files are located
csv_dir = 'data'

# Directory where the Parquet files will be saved
parquet_dir = 'data'

# List of CSV files to be converted
csv_files = [
    'Fanflux_Intensity_NFL_Black.csv',
    'Fanflux_Intensity_NFL_Hispanic.csv',
    'Fanflux_Intensity_NFL_White.csv'
]

for csv_file in csv_files:
    # Read the CSV file
    df = pd.read_csv(os.path.join(csv_dir, csv_file))
    
    # Define the Parquet file name
    parquet_file = csv_file.replace('.csv', '.parquet')
    
    # Write the DataFrame to a Parquet file
    df.to_parquet(os.path.join(parquet_dir, parquet_file))

print("Conversion completed.")

