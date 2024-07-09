import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from Pages import home, mlb_aapi, mlb_american_indian, mlb_asian, mlb_black, mlb_hispanic, mlb_white, chatbot_page

def sidebar_menu():
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
        "🏠 Home": home.app,
        "📊 AAPI Baseball Fans": mlb_aapi.app,
        "📊 American Indian Baseball Fans": mlb_american_indian.app,
        "📊 Asian Baseball Fans": mlb_asian.app,
        "📊 Black Baseball Fans": mlb_black.app,
        "📊 Hispanic Baseball Fans": mlb_hispanic.app,
        "📊 White Baseball Fans": mlb_white.app,
        "🤖 Chatbot": chatbot_page.coming_soon
    }

    selected = st.sidebar.radio("Choose an option", list(menu_options.keys()))

    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    # Debugging information
    print("Available keys in dataframes dictionary:", dataframes.keys())
    print("Selected key:", selected.split()[0] + " " + selected.split()[1])

    if selected != "🏠 Home" and selected != "🤖 Chatbot":
        df = dataframes[selected.split()[0] + " " + selected.split()[1]]
        print("Columns in the DataFrame:", df.columns)

        selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique())
        selected_race = st.sidebar.multiselect("Select Race", df['Race'].unique())
        selected_league = st.sidebar.selectbox("Select League", df['League'].unique())
        selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique())
        selected_income_level = st.sidebar.selectbox("Select Income Level", df.columns[15:])

    return menu_options[selected]
