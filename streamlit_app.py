import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_black as black
import Pages.mlb_white as white
import Pages.mlb_hispanic as hispanic  # Updated to the correct module
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Black Baseball Fans", black.app)
app.add_app("White Baseball Fans", white.app)
app.add_app("Hispanic Baseball Fans", hispanic.app)
app.add_app("Asian American/Pacific Islander Baseball Fans", aapi.app)
app.add_app("American Indian/Alaska Native Baseball Fans", americanindian.app)
app.add_app("Asian Baseball Fans", asian.app)

# The main app
app.run()
