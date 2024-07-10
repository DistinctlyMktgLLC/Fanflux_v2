import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home_app, chatbot_page_app, leagues_app
from utils import apply_common_styles

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=["🏠 Home", "📣 Leagues", "🤖 Chatbot"],
            icons=["house", "list", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#1d1d1d"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

    apply_common_styles()

    if selected == "🏠 Home":
        home_app()
    elif selected == "📣 Leagues":
        leagues_app()
    elif selected == "🤖 Chatbot":
        chatbot_page_app()
