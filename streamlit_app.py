import os
import streamlit as st
from multiapp import MultiApp
import Pages.home as home
import Pages.mlb_black as black
import Pages.mlb_white as white
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_latino as latino
import Pages.mlb_mixed as mixed
import Pages.mlb_other as other

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("Black Baseball Fans", black.app)
app.add_app("White Baseball Fans", white.app)
app.add_app("AAPI Baseball Fans", aapi.app)
app.add_app("American Indian Baseball Fans", americanindian.app)
app.add_app("Asian Baseball Fans", asian.app)
app.add_app("Latino Baseball Fans", latino.app)
app.add_app("Mixed Race Baseball Fans", mixed.app)
app.add_app("Other Race Baseball Fans", other.app)

app.run()
