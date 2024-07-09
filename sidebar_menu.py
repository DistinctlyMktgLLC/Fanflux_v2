import streamlit as st
import pandas as pd
from Pages import home_app, mlb_aapi_app, mlb_americanindian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app, chatbot_page_app

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

    # Sidebar menu options
    with st.sidebar:
        st.header("Sports Analysis")
        selected = st.selectbox(
            "Choose an option",
            ["Home", "MLB", "NBA", "NFL", "NHL", "MLS", "Chatbot"],
        )

        if selected == "Home":
            return home_app.app
        elif selected == "MLB":
            submenu_items = {
                "AAPI": mlb_aapi_app.app,
                "American Indian": mlb_americanindian_app.app,
                "Asian": mlb_asian_app.app,
                "Black": mlb_black_app.app,
                "Hispanic": mlb_hispanic_app.app,
                "White": mlb_white_app.app,
            }
            submenu_selected = st.selectbox("Select Category", list(submenu_items.keys()))
            return lambda: submenu_items[submenu_selected](dataframes)
        elif selected == "Chatbot":
            return lambda: chatbot_page_app.app(dataframes)

    return home_app.app
