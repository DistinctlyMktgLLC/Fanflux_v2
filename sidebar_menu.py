import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home as home_app, chatbot_page as chatbot_page_app, leagues as leagues_app

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            "Fanflux",
            ["🏠 Home", "📣 Leagues", "🤖 Chatbot"],
            icons=["house", "menu-button-fill", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#1d1d1d"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#00c853"},
            }
        )

    if selected == "🏠 Home":
        home_app()
    elif selected == "📣 Leagues":
        leagues_app()
    elif selected == "🤖 Chatbot":
        chatbot_page_app()
