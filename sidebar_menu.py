# sidebar_menu.py
import streamlit as st
from streamlit_option_menu import option_menu
import Pages.home as home
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic
import Pages.mlb_white as mlb_white

# Custom CSS for Sidebar Menu
st.markdown(
    """
    <style>
    .css-1v0mbdj {
        width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Sports Analysis",
            options=["Home", "MLB", "NBA", "NFL", "NHL", "MLS"],
            icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#2c2f38"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#06c"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

    if selected == "Home":
        home.app()
    elif selected == "MLB":
        submenu_items = {
            "White": mlb_white.app,
            "AAPI": mlb_aapi.app,
            "American Indian": mlb_americanindian.app,
            "Asian": mlb_asian.app,
            "Black": mlb_black.app,
            "Hispanic": mlb_hispanic.app,
        }
        submenu_selected = st.selectbox("Select Category", list(submenu_items.keys()))
        return submenu_items[submenu_selected]

    return None

selected_app = sidebar_menu()
if selected_app:
    selected_app()
