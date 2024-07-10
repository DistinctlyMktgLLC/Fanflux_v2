import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home_app, chatbot_page_app, leagues_app
from utils import apply_common_styles

def sidebar_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Leagues", "Chatbot"],
        icons=["house", "megaphone", "robot"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "#f3f4f6", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#3c3f41"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

    if selected == "Home":
        home_app()
    elif selected == "Leagues":
        leagues_app()
    elif selected == "Chatbot":
        chatbot_page_app()
