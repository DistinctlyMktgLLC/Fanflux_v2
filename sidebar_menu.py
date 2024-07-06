# sidebar_menu.py
import streamlit as st
from multiapp import MultiApp
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
    .sidebar .sidebar-content .element-container {
        padding: 5px;
    }
    .sidebar .sidebar-content .element-container h3 {
        color: #ffffff;
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .element-container .menu-item {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: #ffffff;
        font-size: 16px;
    }
    .sidebar .sidebar-content .element-container .menu-item:hover {
        background-color: #343a40;
        cursor: pointer;
    }
    .sidebar .sidebar-content .element-container .menu-item.active {
        background-color: #28a745;
        color: #ffffff;
    }
    .icon {
        margin-right: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def sidebar_menu():
    st.sidebar.header("Sports Analysis")
    
    menu_items = {
        "Home": home.app,
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
    
    # Sidebar navigation logic
    choice = st.sidebar.radio("Select League", list(menu_items.keys()))
    
    if isinstance(menu_items[choice], dict):
        submenu_choice = st.sidebar.selectbox("Select Category", list(menu_items[choice].keys()))
        menu_items[choice][submenu_choice]()
    else:
        menu_items[choice]()

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
