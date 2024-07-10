import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home_app, chatbot_page_app, leagues_app

def sidebar_menu():
    selected = option_menu(
        "Fanflux",
        ["Home", "Leagues", "Chatbot"],
        icons=["house", "megaphone", "robot"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "white", "font-size": "25px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "color": "white",
            },
            "nav-link-selected": {"background-color": "#1f77b4"},
        },
    )

    if selected == "Home":
        home_app()
    elif selected == "Leagues":
        leagues_app()
    elif selected == "Chatbot":
        chatbot_page_app()
