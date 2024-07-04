import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

# Sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# Display DataFrame using AgGrid
AgGrid(df, height=400, width='100%', theme='streamlit', fit_columns_on_grid_load=True)
