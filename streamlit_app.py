import os
import streamlit as st
from streamlit_navigation_bar import st_navbar
import Pages.home as home
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_black as black
import Pages.mlb_hispanic as hispanic
import Pages.mlb_white as white
import utils

st.set_page_config(initial_sidebar_state="collapsed")

# Define the pages
pages = ["Home", "AAPI Baseball Fans", "American Indian Baseball Fans", "Asian Baseball Fans", "Black Baseball Fans", "Hispanic Baseball Fans", "White Baseball Fans"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "logo.svg")  # Ensure you have a logo.svg file in the root directory
urls = {
    "Home": "#",
    "AAPI Baseball Fans": "#",
    "American Indian Baseball Fans": "#",
    "Asian Baseball Fans": "#",
    "Black Baseball Fans": "#",
    "Hispanic Baseball Fans": "#",
    "White Baseball Fans": "#"
}
styles = {
    "nav": {"background-color": "var(--primary-color)"},
    "span": {"color": "white"},
}
options = {"show_sidebar": False}

# Display the navigation bar
page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=urls,
    styles=styles,
    options=options,
)

# Load the selected page
if page == "Home":
    home.app()
elif page == "AAPI Baseball Fans":
    aapi.app()
elif page == "American Indian Baseball Fans":
    americanindian.app()
elif page == "Asian Baseball Fans":
    asian.app()
elif page == "Black Baseball Fans":
    black.app()
elif page == "Hispanic Baseball Fans":
    hispanic.app()
elif page == "White Baseball Fans":
    white.app()

with st.sidebar:
    st.write("The sidebar button will not be shown.")
