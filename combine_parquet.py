import pandas as pd
import glob

files = glob.glob("data/*.csv")
df_list = []

for file in files:
    df = pd.read_csv(file)
    df_list.append(df)

df_combined = pd.concat(df_list, ignore_index=True)

# Convert relevant columns to numeric, replacing any errors with NaN and then with 0
for col in df_combined.columns:
    if 'struggling' in col.lower() or 'getting by' in col.lower() or 'starting out' in col.lower() or 'middle class' in col.lower() or 'comfortable' in col.lower() or 'doing well' in col.lower() or 'prosperous' in col.lower() or 'wealthy' in col.lower() or 'affluent' in col.lower():
        df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce').fillna(0)

df_combined.to_parquet('data/combined_leagues.parquet', index=False)
