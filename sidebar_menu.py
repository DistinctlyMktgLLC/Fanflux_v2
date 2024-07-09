import streamlit as st
import pandas as pd
from Pages import home_app, mlb_aapi_app, mlb_americanindian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app

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

    menu_options = ["Home", "MLB - AAPI", "MLB - American Indian", "MLB - Asian", "MLB - Black", "MLB - Hispanic", "MLB - White", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", menu_options)

    if selected == "Home":
        return home_app.app
    elif selected == "MLB - AAPI":
        return mlb_aapi_app.app
    elif selected == "MLB - American Indian":
        return mlb_americanindian_app.app
    elif selected == "MLB - Asian":
        return mlb_asian_app.app
    elif selected == "MLB - Black":
        return mlb_black_app.app
    elif selected == "MLB - Hispanic":
        return mlb_hispanic_app.app
    elif selected == "MLB - White":
        return mlb_white_app.app
    elif selected == "Chatbot":
        return chatbot_page_app
    else:
        return home_app.app
