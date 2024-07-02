import streamlit as st
from multiapp import MultiApp
import pages.home as home
import pages.mlb_aapi as mlb_aapi
import pages.mlb_americanindian as mlb_americanindian
import pages.mlb_asian as mlb_asian
import pages.mlb_black as mlb_black
import pages.mlb_hispanic as mlb_hispanic
import pages.mlb_white as mlb_white

# Set page configuration
st.set_page_config(page_title="Fanflux Intensity Finder", page_icon="🏆", layout="wide")

# Apply custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

app = MultiApp()

# Add your application pages here
app.add_app("Home", home.app)
app.add_app("MLB White", mlb_white.app)
app.add_app("MLB Black", mlb_black.app)
app.add_app("MLB Hispanic", mlb_hispanic.app)
app.add_app("MLB Asian", mlb_asian.app)
app.add_app("MLB AAPI", mlb_aapi.app)
app.add_app("MLB American Indian", mlb_americanindian.app)

app.run()
