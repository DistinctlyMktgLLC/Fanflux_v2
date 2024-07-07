# sidebar_menu.py
import streamlit as st
from streamlit_option_menu import option_menu
import Pages.home as home
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic
import Pages.mlb_white as mlb_white
# Import other league pages similarly...

import pandas as pd

# Dictionary to map categories to parquet files
parquet_files = {
    "MLB": {
        "AAPI": "data/Fanflux_Intensity_MLB_AAPI.parquet",
        "American Indian": "data/Fanflux_Intensity_MLB_AmericanIndian.parquet",
        "Asian": "data/Fanflux_Intensity_MLB_Asian.parquet",
        "Black": "data/Fanflux_Intensity_MLB_Black.parquet",
        "Hispanic": "data/Fanflux_Intensity_MLB_Hispanic.parquet",
        "White": "data/Fanflux_Intensity_MLB_White.parquet"
    },
    "NBA": {
        # Add parquet files for NBA categories here
    },
    "NFL": {
        # Add parquet files for NFL categories here
    },
    "NHL": {
        # Add parquet files for NHL categories here
    },
    "MLS": {
        # Add parquet files for MLS categories here
    }
}

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

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Sports Analysis",
            options=["Home", "MLB", "NBA", "NFL", "NHL", "MLS"],
            icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "white", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#343a40"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
        
        submenu_items = {
            "MLB": {
                "AAPI": mlb_aapi.app,
                "American Indian": mlb_americanindian.app,
                "Asian": mlb_asian.app,
                "Black": mlb_black.app,
                "Hispanic": mlb_hispanic.app,
                "White": mlb_white.app,
            },
            "NBA": {
                # Add corresponding page functions for NBA categories here
            },
            "NFL": {
                # Add corresponding page functions for NFL categories here
            },
            "NHL": {
                # Add corresponding page functions for NHL categories here
            },
            "MLS": {
                # Add corresponding page functions for MLS categories here
            }
        }
        
        if selected == "Home":
            return home.app
        elif selected in submenu_items:
            if submenu_items[selected]:
                submenu_selected = st.selectbox("Select Category", list(submenu_items[selected].keys()))
                if submenu_selected:
                    # Load the appropriate data based on the selected category
                    data_file = parquet_files[selected][submenu_selected]
                    df = pd.read_parquet(data_file)

                    # Filter options
                    st.markdown("### Filters")
                    team_filter = st.selectbox("Team", options=["All"] + list(df['Team'].unique()))
                    league_filter = st.selectbox("League", options=["All"] + list(df['League'].unique()))
                    fandom_filter = st.selectbox("Fandom Level", options=["All", "Avid", "Casual", "Convertible"])
                    income_filter = st.selectbox("Income Level", options=["All"] + income_columns)
                    
                    # Apply filters
                    filtered_df = df.copy()
                    if team_filter != "All":
                        filtered_df = filtered_df[filtered_df['Team'] == team_filter]
                    if league_filter != "All":
                        filtered_df = filtered_df[filtered_df['League'] == league_filter]
                    if fandom_filter != "All":
                        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_filter]
                    if income_filter != "All":
                        filtered_df = filtered_df[filtered_df[income_filter] > 0]

                    # Pass the filtered dataframe to the app
                    return lambda: submenu_items[selected][submenu_selected](filtered_df)
                return submenu_items[selected].get(submenu_selected, lambda: st.error("No page selected"))
            else:
                st.error("No subpages available for the selected league.")
                return None
        else:
            return lambda: st.error("Page not implemented yet.")
