# sidebar_menu.py
import streamlit as st
import pandas as pd
from Pages import home, mlb_aapi, mlb_american_indian, mlb_asian, mlb_black, mlb_hispanic, mlb_white, chatbot_page

def sidebar_menu():
    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #1d1d1d;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Menu options
    menu_options = ["Home", "MLB - AAPI", "MLB - American Indian", "MLB - Asian", "MLB - Black", "MLB - Hispanic", "MLB - White", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", menu_options)

    # Page selection logic
    if selected == "Home":
        return home.app
    elif selected == "MLB - AAPI":
        return lambda: mlb_aapi.app(dataframes["MLB - AAPI"])
    elif selected == "MLB - American Indian":
        return lambda: mlb_american_indian.app(dataframes["MLB - American Indian"])
    elif selected == "MLB - Asian":
        return lambda: mlb_asian.app(dataframes["MLB - Asian"])
    elif selected == "MLB - Black":
        return lambda: mlb_black.app(dataframes["MLB - Black"])
    elif selected == "MLB - Hispanic":
        return lambda: mlb_hispanic.app(dataframes["MLB - Hispanic"])
    elif selected == "MLB - White":
        return lambda: mlb_white.app(dataframes["MLB - White"])
    elif selected == "Chatbot":
        return chatbot_page.app
    else:
        return home.app
