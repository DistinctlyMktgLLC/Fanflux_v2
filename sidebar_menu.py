import streamlit as st
from streamlit_option_menu import option_menu

def sidebar_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Leagues Analysis", "Chatbot"],
        icons=["house", "bar-chart", "robot"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        key="main_menu_option_sidebar_unique"
    )

    if selected == "Home":
        st.write("Welcome to Fanflux")
        # Home page content
    elif selected == "Leagues Analysis":
        from Pages.leagues_analysis import app as leagues_analysis
        leagues_analysis()
    elif selected == "Chatbot":
        from Pages.chatbot_page import app as chatbot_page
        chatbot_page()

sidebar_menu()
