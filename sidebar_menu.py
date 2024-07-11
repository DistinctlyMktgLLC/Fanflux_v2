import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os

# Load all data into a single dataframe
data_dir = "data"
df_list = []
for file in os.listdir(data_dir):
    if file.endswith(".parquet"):
        df_list.append(pd.read_parquet(os.path.join(data_dir, file)))
df = pd.concat(df_list, ignore_index=True)

def sidebar_menu():
    # Custom CSS for Sidebar Menu
    st.markdown("""
    <style>
        .main {
            background-color: #262730;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        selected = option_menu(
            menu_title="Fanflux",
            options=["Home", "Leagues Analysis", "Chatbot"],
            icons=["house", "bar-chart", "robot"],
            menu_icon="cast",
            default_index=0,
            key="main_menu_option_sidebar",
            styles={
                "container": {"padding": "5!important", "background-color": "#262730"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#555"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    # Import the different pages
    from Pages.home import app as home_app
    from Pages.leagues_analysis import app as leagues_analysis_app
    from Pages.chatbot_page import app as chatbot_app

    menu_options = {
        "Home": home_app,
        "Leagues Analysis": leagues_analysis_app,
        "Chatbot": chatbot_app
    }

    if selected == "Home":
        menu_options[selected]()
    else:
        menu_options[selected](df)

# Run the sidebar menu
sidebar_menu()
