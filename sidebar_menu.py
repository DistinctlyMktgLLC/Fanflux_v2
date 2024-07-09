import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import folium
from streamlit_folium import folium_static
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

    # Only show filters when a specific race page is selected
    if selected != "🏠 Home" and selected != "🤖 Chatbot":
        # Load dataframes
        dataframes = {
            "AAPI Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_AAPI.parquet"),
            "American Indian Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_American_Indian.parquet"),
            "Asian Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_Asian.parquet"),
            "Black Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_Black.parquet"),
            "Hispanic Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_Hispanic.parquet"),
            "White Baseball Fans": pd.read_parquet("data/Fanflux_Intensity_MLB_White.parquet")
        }

        # Ensure the selected key maps correctly to the dataframes dictionary
        selected_key = selected.split(" ", 1)[1]

        selected_fandom_level = st.sidebar.multiselect("Select Fandom Level", ["Avid", "Casual", "Convertible"])
        selected_race = st.sidebar.multiselect("Select Race", ["AAPI", "American Indian", "Asian", "Black", "Hispanic", "White"])
        selected_league = st.sidebar.selectbox("Select League", ["MLB", "NBA", "NFL", "NHL", "MLS"])
        selected_teams = st.sidebar.multiselect("Select Team", dataframes[selected_key].Team.unique())
        selected_income_levels = st.sidebar.multiselect("Select Income Level", [
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
        ])

        # Filter the dataframe
        filtered_df = dataframes[selected_key]
        if selected_fandom_level:
            filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_level)]
        if selected_race:
            filtered_df = filtered_df[filtered_df['Race'].isin(selected_race)]
        if selected_teams:
            filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
        if selected_income_levels:
            filtered_df = filtered_df[[col for col in filtered_df.columns if col in selected_income_levels]]

        # Create a map
        folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=4, width='100%', height='100%')

        for _, row in filtered_df.iterrows():
            # Replace "Not at All" with "Convertible" in the Fandom Level
            fandom_level = "Convertible" if row['Fandom Level'] == "Not at All" else row['Fandom Level']

            # Update popup content to use "Convertible" instead of "Not at All"
            popup_content = f"Team: {row['Team']}<br>League: {row['League']}<br>Neighborhood: {row['Neighborhood']}<br>Fandom Level: {fandom_level}<br>Race: {row['Race']}<br>Total Fans: {row[income_columns].sum()}"
            color = colors.get(fandom_level, 'black')
            folium.CircleMarker(
                location=[row['US lat'], row['US lon']],
                radius=5,
                popup=popup_content,
                color=color,
                fill=True,
                fill_color=color
            ).add_to(folium_map)

        folium_static(folium_map, width=1200, height=800)

        # Call the selected app with the filtered dataframe
        menu_options[selected](filtered_df)
    else:
        # Call the selected app without filtering
        menu_options[selected]()
