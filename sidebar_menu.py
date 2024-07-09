import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from Pages import home, mlb_aapi, mlb_american_indian, mlb_asian, mlb_black, mlb_hispanic, mlb_white, chatbot_page

def sidebar_menu():
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
        "🏠 Home": home.app,
        "📊 AAPI Baseball Fans": mlb_aapi.app,
        "📊 American Indian Baseball Fans": mlb_american_indian.app,
        "📊 Asian Baseball Fans": mlb_asian.app,
        "📊 Black Baseball Fans": mlb_black.app,
        "📊 Hispanic Baseball Fans": mlb_hispanic.app,
        "📊 White Baseball Fans": mlb_white.app,
        "🤖 Chatbot": chatbot_page.coming_soon
    }

    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=list(menu_options.keys()),
            icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#565656"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    # Load your dataframes here
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet"),
    }

    if selected != "🏠 Home" and selected != "🤖 Chatbot":
        key = selected.split()[1] + " " + selected.split()[2]
        df = dataframes[key]

        selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique())
        selected_race = st.sidebar.multiselect("Select Race", df['Race'].unique())
        selected_league = st.sidebar.selectbox("Select League", df['League'].unique())
        selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique())
        selected_income_level = st.sidebar.multiselect("Select Income Level", df.columns[14:])

        # Apply the filtering
        if selected_fandom_level:
            df = df[df['Fandom Level'].isin(selected_fandom_level)]
        if selected_race:
            df = df[df['Race'].isin(selected_race)]
        if selected_league:
            df = df[df['League'] == selected_league]
        if selected_teams:
            df = df[df['Team'].isin(selected_teams)]
        if selected_income_level:
            df = df[df[selected_income_level].sum(axis=1) > 0]

        return menu_options[selected](df)

    return menu_options[selected]()

# Run the sidebar menu
sidebar_menu()
