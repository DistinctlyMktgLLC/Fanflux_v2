import pandas as pd

# Load the original dataset
df = pd.read_parquet("data/Fanflux_Intensity_All_Leagues.parquet")

# Drop unnecessary columns
df_cleaned = df.drop(columns=['helper', 'match', 'cheat', 'Match'])

# Save the cleaned dataset
df_cleaned.to_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned.parquet")
