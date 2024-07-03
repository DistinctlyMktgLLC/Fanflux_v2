import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

import Pages.home as home
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_black as black
import Pages.mlb_white as white
from multiapp import MultiApp

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("AAPI Baseball Fans", aapi.app)
app.add_app("American Indian Baseball Fans", americanindian.app)
app.add_app("Asian Baseball Fans", asian.app)
app.add_app("Black Baseball Fans", black.app)
app.add_app("White Baseball Fans", white.app)

app.run()
