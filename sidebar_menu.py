import streamlit as st
import pandas as pd
import folium
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
from Pages import home, chatbot_page  # Import all other pages as needed

# Load the combined Parquet file
df_all = pd.read_parquet("data/Fanflux_Intensity_All_Leagues.parquet")

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

# Sidebar menu options with emojis/icons
menu_options = {
    "🏠 Home": home.app,
    "⚾ MLB": {
        "📊 AAPI Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'AAPI'),
        "📊 American Indian Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'American Indian'),
        "📊 Asian Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'Asian'),
        "📊 Black Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'Black'),
        "📊 Hispanic Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'Hispanic'),
        "📊 White Baseball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'MLB'], 'White'),
    },
    "🏀 NBA": {
        "📊 AAPI Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'AAPI'),
        "📊 American Indian Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'American Indian'),
        "📊 Asian Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'Asian'),
        "📊 Black Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'Black'),
        "📊 Hispanic Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'Hispanic'),
        "📊 White Basketball Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NBA'], 'White'),
    },
    "🏈 NFL": {
        "📊 Black Football Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NFL'], 'Black'),
        "📊 Hispanic Football Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NFL'], 'Hispanic'),
        "📊 White Football Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NFL'], 'White'),
    },
    "🏒 NHL": {
        "📊 AAPI Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'AAPI'),
        "📊 American Indian Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'American Indian'),
        "📊 Asian Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'Asian'),
        "📊 Black Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'Black'),
        "📊 Hispanic Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'Hispanic'),
        "📊 White Hockey Fans": lambda: render_filtered_page(df_all[df_all['dCategory'] == 'NHL'], 'White'),
    },
    "⚽ MLS": {
        # Add options for MLS as needed
    },
    "🤖 Chatbot": chatbot_page.app,
}

def render_filtered_page(df, race):
    selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique())
    selected_race = st.sidebar.multiselect("Select Race", df['Race'].unique())
    selected_league = st.sidebar.selectbox("Select League", df['League'].unique())
    selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique())
    selected_income_levels = st.sidebar.multiselect("Select Income Level", income_columns)

    # Apply filters
    if selected_fandom_level:
        df = df[df['Fandom Level'].isin(selected_fandom_level)]
    if selected_race:
        df = df[df['Race'].isin(selected_race)]
    if selected_league:
        df = df[df['League'] == selected_league]
    if selected_teams:
        df = df[df['Team'].isin(selected_teams)]
    if selected_income_levels:
        df = df[['Team', 'League', 'Fandom Level', 'Race'] + selected_income_levels]

    # Call the app function for the selected race
    page_function(df)

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=list(menu_options.keys()),
            icons=["house", "baseball", "basketball", "football", "hockey-puck", "soccer-ball", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "23px"},
                "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                "nav-link-selected": {"background-color": "#02ab21"},
            },
        )

        # Check if the selected option is a submenu
        if isinstance(menu_options[selected], dict):
            selected_submenu = option_menu(
                menu_title=selected,
                options=list(menu_options[selected].keys()),
                icons=["bar-chart"] * len(menu_options[selected]),
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "black"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                },
            )
            page_function = menu_options[selected][selected_submenu]
        else:
            page_function = menu_options[selected]

    return page_function
