import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB White Fans", page_icon="⚾️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')

def app():
    st.title("MLB White Fans")
    df = load_data()
    st.dataframe(df)

if __name__ == "__main__":
    app()
