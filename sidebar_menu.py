import streamlit as st
import pandas as pd
from Pages import home, mlb_aapi, mlb_americanindian, mlb_asian, mlb_black, mlb_hispanic, mlb_white

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
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    menu_options = ["Home", "MLB - AAPI", "MLB - American Indian", "MLB - Asian", "MLB - Black", "MLB - Hispanic", "MLB - White", "Chatbot"]
    selected = st.sidebar.selectbox("Choose an option", menu_options)

    if selected == "Home":
        return home.app
    elif selected == "MLB - AAPI":
        return mlb_aapi.app
    elif selected == "MLB - American Indian":
        return mlb_americanindian.app
    elif selected == "MLB - Asian":
        return mlb_asian.app
    elif selected == "MLB - Black":
        return mlb_black.app
    elif selected == "MLB - Hispanic":
        return mlb_hispanic.app
    elif selected == "MLB - White":
        return mlb_white.app
    elif selected == "Chatbot":
        from Pages import chatbot_page
        return lambda: chatbot_page.app(dataframes)
