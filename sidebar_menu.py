# sidebar_menu.py
import streamlit as st
from streamlit_option_menu import option_menu

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
        return "Home"
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
