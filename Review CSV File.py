import pandas as pd

# Load the CSV file
file_path = '/mnt/data/Intensity_MLB_ALLRaces.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
data.head()
