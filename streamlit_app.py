import os
import streamlit as st
import Pages.home as home
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_black as black
import Pages.mlb_hispanic as hispanic
import Pages.mlb_white as white
import utils

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Define the pages
pages = {
    "Home": home,
    "AAPI Baseball Fans": aapi,
    "American Indian Baseball Fans": americanindian,
    "Asian Baseball Fans": asian,
    "Black Baseball Fans": black,
    "Hispanic Baseball Fans": hispanic,
    "White Baseball Fans": white,
}

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Function to handle page routing
def router():
    if selection in pages:
        pages[selection].app()
    else:
        st.error("Page not found")

# Custom CSS for sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white;
        text-decoration: none;
    }
    .sidebar .sidebar-content a:hover {
        color: #F39C12;
    }
    .sidebar .sidebar-content .stRadio label {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-content">', unsafe_allow_html=True)
router()
st.markdown('</div>', unsafe_allow_html=True)
