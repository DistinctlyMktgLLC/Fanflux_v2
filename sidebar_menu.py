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

    # Custom CSS for Sidebar Menu
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #1d1d1d;
        }
        .highlight {
            background-color: green;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .menu-item {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .sidebar .sidebar-content {
            padding-top: 20px;
        }
        .sidebar .sidebar-content h1 {
            color: white;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content hr {
            border: 0;
            height: 1px;
            background: #666;
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar menu title
    st.sidebar.markdown("<h1>Fanflux</h1><hr>", unsafe_allow_html=True)

    # Sidebar menu options with emojis/icons
    menu_options = {
        "Home": "🏠 Home",
        "MLB - AAPI": "📊 AAPI Baseball Fans",
        "MLB - American Indian": "📊 American Indian Baseball Fans",
        "MLB - Asian": "📊 Asian Baseball Fans",
        "MLB - Black": "📊 Black Baseball Fans",
        "MLB - Hispanic": "📊 Hispanic Baseball Fans",
        "MLB - White": "📊 White Baseball Fans",
        "Chatbot": "🤖 Chatbot"
    }

    # Get the selected option from the session state or set default to "Home"
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "🏠 Home"

    # Display sidebar menu options
    for key, value in menu_options.items():
        if value == st.session_state.selected_menu:
            st.sidebar.markdown(f"<div class='highlight'>{value}</div>", unsafe_allow_html=True)
        else:
            if st.sidebar.button(value, key=value):
                st.session_state.selected_menu = value
                st.experimental_rerun()

    # Page selection logic with filters
    selected = st.session_state.selected_menu
    if selected == menu_options["Home"]:
        return home.app
    else:
        selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", ["Avid", "Casual", "Not at All"])
        selected_race = st.sidebar.multiselect("Select Race", ["White", "Black", "Hispanic", "Asian", "American Indian", "AAPI"])
        selected_league = st.sidebar.multiselect("Select League", ["MLB", "NBA", "NFL", "NHL", "MLS"])
        selected_teams = st.sidebar.multiselect("Select Team", dataframes[key.split(" - ")[1]]['Team'].unique())
        selected_income_level = st.sidebar.multiselect("Select Income Level", dataframes[key.split(" - ")[1]].columns[14:])

        filters = {
            "Fandom Level": selected_fandom_level,
            "Race": selected_race,
            "League": selected_league,
            "Team": selected_teams,
            "Income Level": selected_income_level
        }

        def filter_dataframe(df):
            for key, value in filters.items():
                if value:
                    df = df[df[key].isin(value)]
            return df

        if selected == menu_options["MLB - AAPI"]:
            return lambda: mlb_aapi.app(filter_dataframe(dataframes["MLB - AAPI"]))
        elif selected == menu_options["MLB - American Indian"]:
            return lambda: mlb_american_indian.app(filter_dataframe(dataframes["MLB - American Indian"]))
        elif selected == menu_options["MLB - Asian"]:
            return lambda: mlb_asian.app(filter_dataframe(dataframes["MLB - Asian"]))
        elif selected == menu_options["MLB - Black"]:
            return lambda: mlb_black.app(filter_dataframe(dataframes["MLB - Black"]))
        elif selected == menu_options["MLB - Hispanic"]:
            return lambda: mlb_hispanic.app(filter_dataframe(dataframes["MLB - Hispanic"]))
        elif selected == menu_options["MLB - White"]:
            return lambda: mlb_white.app(filter_dataframe(dataframes["MLB - White"]))
        elif selected == menu_options["Chatbot"]:
            return chatbot_page.app
        else:
            return home.app
