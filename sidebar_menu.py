import streamlit as st
from streamlit_option_menu import option_menu
from Pages import home_app, chatbot_page_app, leagues_app
from utils import apply_common_styles

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            "Fanflux",
            ["Home", "Leagues", "Chatbot"],
            icons=["house", "bullhorn", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#262730"},
                "icon": {"color": "white", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#3c3f41"},
                "nav-link-selected": {"background-color": "#4CAF50"},
            }
        )
        
    apply_common_styles()
    
    if selected == "Home":
        home_app()
    elif selected == "Leagues":
        leagues_app()
    elif selected == "Chatbot":
        chatbot_page_app()
