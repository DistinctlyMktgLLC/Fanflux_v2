import pandas as pd

# Load the CSV file
csv_file_path = 'data/Intensity_MLB_ALLRaces.csv'
data = pd.read_csv(csv_file_path)

# Save the DataFrame as a Parquet file
parquet_file_path = 'data/Intensity_MLB_ALLRaces.parquet'
data.to_parquet(parquet_file_path, index=False)

print(f"CSV file has been converted to Parquet and saved at {parquet_file_path}")

