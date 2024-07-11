import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from Pages import home, chatbot_page, leagues_analysis

def sidebar_menu():
    # Load your data
    df = pd.read_parquet("data/combined_leagues.parquet")

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
        "Home": home.app,
        "Leagues Analysis": leagues_analysis.app,
        "Chatbot": chatbot_page.app
    }

    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=list(menu_options.keys()),
            icons=["house", "bar-chart", "robot"],
            menu_icon="cast",
            default_index=0,
            key="main_menu_option"
        )

    # Run the selected app
    if selected == "Home":
        menu_options[selected]()
    else:
        menu_options[selected](df)

# Run the sidebar menu
sidebar_menu()
