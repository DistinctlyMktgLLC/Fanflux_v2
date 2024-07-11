import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home, leagues_analysis, chatbot_page

def sidebar_menu():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar menu options
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
            key="main_menu_unique_key_12345",  # Ensuring this key is unique
            styles={
                "container": {"padding": "5!important", "background-color": "#262730"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#565656"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    # Run the selected app
    if selected in menu_options:
        menu_options[selected]()

# Run the sidebar menu
sidebar_menu()
