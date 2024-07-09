import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
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
        "🤖 Chatbot": chatbot_page.app
    }

    # Render the sidebar menu
    with st.sidebar:
        selected = option_menu(
            menu_title='Fanflux',
            options=list(menu_options.keys()),
            icons=['house', 'bar-chart', 'bar-chart', 'bar-chart', 'bar-chart', 'bar-chart', 'bar-chart', 'robot'],
            menu_icon='menu-button-fill',
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#0e1117"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#262730"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

    # Load dataframes
    dataframes = {
        "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
        "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
        "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
        "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
        "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
        "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")
    }

    # Add filter widgets to the sidebar
    selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", ["Avid", "Casual", "Convertible"])
    selected_race = st.sidebar.multiselect("Select Race", ["AAPI", "American Indian", "Asian", "Black", "Hispanic", "White"])
    selected_league = st.sidebar.selectbox("Select League", ["MLB", "NBA", "NFL", "NHL", "MLS"])
    selected_teams = st.sidebar.multiselect("Select Team", dataframes[selected.split()[0] + " " + selected.split()[1]].Team.unique())

    # Call the appropriate app function with the filtered data
    if selected in menu_options:
        filtered_df = dataframes[selected.split()[0] + " " + selected.split()[1]]
        if selected_fandom_level:
            filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_level)]
        if selected_race:
            filtered_df = filtered_df[filtered_df['Race'].isin(selected_race)]
        if selected_teams:
            filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]

        # Call the selected app with the filtered dataframe
        menu_options[selected](filtered_df)
