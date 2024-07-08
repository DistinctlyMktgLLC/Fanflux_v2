import streamlit as st
from multiapp import MultiApp
import utils
import os

# Import your application modules here
from Pages import home, mlb_aapi, mlb_americanindian, mlb_asian, mlb_black, mlb_hispanic, mlb_white

# Initialize the multi-page app
app = MultiApp()

# Add all your application pages here
app.add_app("Home", home.app)
app.add_app("MLB AAPI", mlb_aapi.app)
app.add_app("MLB American Indian", mlb_americanindian.app)
app.add_app("MLB Asian", mlb_asian.app)
app.add_app("MLB Black", mlb_black.app)
app.add_app("MLB Hispanic", mlb_hispanic.app)
app.add_app("MLB White", mlb_white.app)

# Apply common styles
utils.apply_common_styles()

# Ensure that the script runs only when executed as the main module
if __name__ == "__main__":
    app.run()
