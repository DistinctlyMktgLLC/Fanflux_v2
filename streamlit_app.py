# streamlit_app.py
import streamlit as st
from multiapp import MultiApp
from sidebar_menu import sidebar_menu

# Set the page config at the top
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Initialize the MultiApp
app = MultiApp()

# Add all your applications here
app.add_app("Home", sidebar_menu)
app.add_app("MLB - AAPI", mlb_aapi.app)
app.add_app("MLB - American Indian", mlb_americanindian.app)
app.add_app("MLB - Asian", mlb_asian.app)
app.add_app("MLB - Black", mlb_black.app)
app.add_app("MLB - Hispanic", mlb_hispanic.app)
app.add_app("MLB - White", mlb_white.app)

# Run the selected app
app.run()
