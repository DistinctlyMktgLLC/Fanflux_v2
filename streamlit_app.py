import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_white as white
# Add other imports as needed

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

app = MultiApp()

# Add all your applications here
app.add_app("Home", home.app)
app.add_app("White Baseball Fans", white.app)
# Add other apps here

# The main app
app.run()
