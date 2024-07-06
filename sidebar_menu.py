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
    .sidebar .sidebar-content {
        background-color: #1d1d1d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def sidebar_menu():
    selected = option_menu(
        menu_title="Sports Analysis",
        options=["Home", "MLB", "NBA", "NFL", "NHL", "MLS"],
        icons=["house", "bar-chart", "bar-chart", "bar-chart", "bar-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1d1d1d"},
            "icon": {"color": "white", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#343a40"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )
    
    submenu_items = {
        "MLB": {
            "AAPI": mlb_aapi.app,
            "American Indian": mlb_americanindian.app,
            "Asian": mlb_asian.app,
            "Black": mlb_black.app,
            "Hispanic": mlb_hispanic.app,
            "White": mlb_white.app,
        },
        "NBA": {},
        "NFL": {},
        "NHL": {},
        "MLS": {}
    }
    
    if selected == "Home":
        home.app()
    elif selected in submenu_items:
        submenu_selected = st.selectbox("Select Category", list(submenu_items[selected].keys()))
        submenu_items[selected][submenu_selected]()

# Initialize the MultiApp
app = MultiApp()

# Add all your applications here
app.add_app("Home", home.app)
app.add_app("MLB - AAPI", mlb_aapi.app)
app.add_app("MLB - American Indian", mlb_americanindian.app)
app.add_app("MLB - Asian", mlb_asian.app)
app.add_app("MLB - Black", mlb_black.app)
app.add_app("MLB - Hispanic", mlb_hispanic.app)
app.add_app("MLB - White", mlb_white.app)

# Run the selected app
sidebar_menu()
