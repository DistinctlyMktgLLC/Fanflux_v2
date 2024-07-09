import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import folium
from streamlit_folium import folium_static
from Pages import home, mlb_aapi, mlb_american_indian, mlb_asian, mlb_black, mlb_hispanic, mlb_white, chatbot_page

# List of income columns
income_columns = [
    'Struggling (Less than $10,000)',
    'Getting By ($10,000 to $14,999)',
    'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)',
    'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)',
    'Middle Class ($40,000 to $44,999)',
    'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)',
    'Comfortable ($60,000 to $74,999)',
    'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)',
    'Prosperous ($125,000 to $149,999)',
    'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

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
            menu_title='Fanflux',
            options=list(menu_options.keys()),
            icons=['house', 'bar-chart-line', 'bar-chart-line', 'bar-chart-line', 'bar-chart-line', 'bar-chart-line', 'bar-chart-line', 'robot'],
            menu_icon='cast',
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "white", "font-size": "23px"},
                "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

        # Load your dataframes here
        dataframes = {
            "MLB - AAPI": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
            "MLB - American Indian": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
            "MLB - Asian": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
            "MLB - Black": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
            "MLB - Hispanic": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
            "MLB - White": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")
        }

        if selected != "🏠 Home":
            selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", dataframes[selected.split()[0] + " " + selected.split()[1]]['Fandom Level'].unique())
            selected_race = st.sidebar.multiselect("Select Race", dataframes[selected.split()[0] + " " + selected.split()[1]]['Race'].unique())
            selected_league = st.sidebar.selectbox("Select League", ["MLB"])
            selected_teams = st.sidebar.multiselect("Select Team", dataframes[selected.split()[0] + " " + selected.split()[1]]['Team'].unique())
            selected_income_level = st.sidebar.multiselect("Select Income Level", income_columns)

            # Filter data based on selections
            filtered_df = dataframes[selected.split()[0] + " " + selected.split()[1]]
            if selected_fandom_level:
                filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_level)]
            if selected_race:
                filtered_df = filtered_df[filtered_df['Race'].isin(selected_race)]
            if selected_teams:
                filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
            if selected_income_level:
                filtered_df = filtered_df[selected_income_level + ['US lat', 'US lon', 'Team', 'League', 'Neighborhood', 'Fandom Level', 'Race']]

            page_function = menu_options[selected]
            page_function(filtered_df)
        else:
            page_function = menu_options[selected]
            page_function()

