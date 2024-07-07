# sidebar_menu.py
import streamlit as st
from streamlit_option_menu import option_menu
import Pages.mlb_white as mlb_white
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic

def sidebar_menu():
    selected = option_menu(
        menu_title="Sports Analysis",
        options=["Home", "MLB", "NBA", "NFL", "NHL", "MLS"],
        icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5px", "background-color": "#333"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#444"},
            "nav-link-selected": {"background-color": "#02ab21"}
        }
    )

    if selected == "Home":
        st.write("Welcome to the Sports Analysis App")
    elif selected == "MLB":
        submenu_items = {
            "White": mlb_white.app,
            "AAPI": mlb_aapi.app,
            "American Indian": mlb_americanindian.app,
            "Asian": mlb_asian.app,
            "Black": mlb_black.app,
            "Hispanic": mlb_hispanic.app
        }
        submenu_selected = st.sidebar.selectbox("Select Category", list(submenu_items.keys()))
        submenu_items[submenu_selected]()
    # Add other conditions for NBA, NFL, etc. when you have pages for them

    return selected
