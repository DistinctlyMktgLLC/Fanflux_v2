import pandas as pd
import sys

def print_columns(file_path):
    df = pd.read_parquet(file_path)
    print("Columns in DataFrame:", df.columns.tolist())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python print_columns.py <path_to_parquet_file>")
    else:
        print_columns(sys.argv[1])
