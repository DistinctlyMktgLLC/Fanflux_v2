import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_black as black
import Pages.mlb_white as white
import Pages.mlb_hispanic as hispanic

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

app = MultiApp()

# Add all your applications here
app.add_app("Home", home.app)
app.add_app("Black Baseball Fans", black.app)
app.add_app("White Baseball Fans", white.app)
app.add_app("Hispanic Baseball Fans", hispanic.app)

# The main app
app.run()
