import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="MLB American Indian Fans", page_icon="⚾️", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    return pd.read_parquet('data/Fanflux_Intensity_MLB_AmericanIndian.csv.parquet')

# Load data
df = load_data()

# Application logic
def app():
    st.title("MLB American Indian Fans")
    st.write("This is the MLB American Indian Fans page.")
    st.dataframe(df)
