import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic
import Pages.mlb_white as mlb_white

# Set page configuration
st.set_page_config(page_title="Fanflux", page_icon="🏆", layout="wide")

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("AAPI Baseball Fans", mlb_aapi.app)
app.add_app("American Indian Baseball Fans", mlb_americanindian.app)
app.add_app("Asian Baseball Fans", mlb_asian.app)
app.add_app("Black Baseball Fans", mlb_black.app)
app.add_app("Hispanic Baseball Fans", mlb_hispanic.app)
app.add_app("White Baseball Fans", mlb_white.app)

# The main app
app.run()
