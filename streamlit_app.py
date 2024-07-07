# streamlit_app.py
import streamlit as st
from multiapp import MultiApp
from sidebar_menu import sidebar_menu

# Set the page config at the top
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Initialize the MultiApp
app = MultiApp()

# Add all your applications here
import Pages.home as home
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic
import Pages.mlb_white as mlb_white

app.add_app("Home", home.app)
app.add_app("MLB - AAPI", mlb_aapi.app)
app.add_app("MLB - American Indian", mlb_americanindian.app)
app.add_app("MLB - Asian", mlb_asian.app)
app.add_app("MLB - Black", mlb_black.app)
app.add_app("MLB - Hispanic", mlb_hispanic.app)
app.add_app("MLB - White", mlb_white.app)

# Get the selected app
selected_app = sidebar_menu()

# Run the selected app
if selected_app:
    try:
        selected_app()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.error("The selected app is not available.")
