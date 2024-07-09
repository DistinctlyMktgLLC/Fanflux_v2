import streamlit as st
import pandas as pd
from Pages import home_app, mlb_aapi_app, mlb_americanindian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app, chatbot_page_app

# Custom CSS for Sidebar Menu
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #1d1d1d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def sidebar_menu():
    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_AmericanIndian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    st.sidebar.title("Sports Analysis")
    options = ["Home", "MLB", "NBA", "NFL", "NHL", "MLS", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", options)

    if selected == "Home":
        return lambda: home_app()
    elif selected == "Chatbot":
        return lambda: chatbot_page_app(dataframes)
    # Add logic for other pages if necessary

    return lambda: home_app()
