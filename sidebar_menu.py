from streamlit_option_menu import option_menu
import streamlit as st
from Pages.home import app as Home  # Adjusted import path to correct location
from Pages.leagues_analysis import app as Leagues_analysis  # Adjusted import path
from Pages.chatbot_page import app as Chatbot  # Adjusted import path

def sidebar_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Leagues Analysis", "Chatbot"],
        icons=["house", "bar-chart", "robot"],
        menu_icon="cast",
        default_index=0,
        key="main_menu_option_sidebar_unique_12345"
    )

    # Clear the previous content
    st.session_state.clear()

    if selected == "Home":
        Home()
    elif selected == "Leagues Analysis":
        Leagues_analysis()
    elif selected == "Chatbot":
        Chatbot()

sidebar_menu()
