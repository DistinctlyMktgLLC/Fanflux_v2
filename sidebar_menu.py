import streamlit as st
import pandas as pd
from Pages import home_app, mlb_aapi_app, mlb_american_indian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app, chatbot_page

def sidebar_menu():
    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
        # Add more dataframes for other leagues as you add them
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
        unsafe_allow_html=True
    )

    # Sidebar menu options with emojis/icons
    menu_options = {
        "Home": "🏠 Home",
        "MLB - AAPI": "📊 MLB - AAPI",
        "MLB - American Indian": "📊 MLB - American Indian",
        "MLB - Asian": "📊 MLB - Asian",
        "MLB - Black": "📊 MLB - Black",
        "MLB - Hispanic": "📊 MLB - Hispanic",
        "MLB - White": "📊 MLB - White",
        "Chatbot": "🤖 Chatbot"
    }

    selected = st.sidebar.selectbox("Choose an option", list(menu_options.values()))

    if selected == menu_options["Home"]:
        return home_app.app
    elif selected == menu_options["MLB - AAPI"]:
        return lambda: mlb_aapi_app.app(dataframes["MLB - AAPI"])
    elif selected == menu_options["MLB - American Indian"]:
        return lambda: mlb_american_indian_app.app(dataframes["MLB - American Indian"])
    elif selected == menu_options["MLB - Asian"]:
        return lambda: mlb_asian_app.app(dataframes["MLB - Asian"])
    elif selected == menu_options["MLB - Black"]:
        return lambda: mlb_black_app.app(dataframes["MLB - Black"])
    elif selected == menu_options["MLB - Hispanic"]:
        return lambda: mlb_hispanic_app.app(dataframes["MLB - Hispanic"])
    elif selected == menu_options["MLB - White"]:
        return lambda: mlb_white_app.app(dataframes["MLB - White"])
    elif selected == menu_options["Chatbot"]:
        return chatbot_page.coming_soon
    else:
        return home_app.app