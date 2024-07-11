import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
from Pages.home import app as home_app
from Pages.leagues_analysis import app as leagues_analysis_app
from Pages.chatbot_page import app as chatbot_page_app

# Load the combined data from a single Parquet file
data_path = "data/combined_leagues.parquet"
df = pd.read_parquet(data_path)

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

    # Sidebar menu options without emojis/icons
    menu_options = {
        "Home": home_app,
        "Leagues Analysis": leagues_analysis_app,
        "Chatbot": chatbot_page_app
    }

    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=list(menu_options.keys()),
            icons=["", "", ""],  # No icons
            menu_icon="cast",
            default_index=0,
            key="fanflux_main_menu_option_" + str(hash(os.urandom(16))),  # Ensure unique key
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#565656"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    # Run the selected app
    if selected == "Home":
        menu_options[selected]()
    else:
        menu_options[selected](df)

# Run the sidebar menu
sidebar_menu()
