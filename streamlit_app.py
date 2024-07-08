import streamlit as st
from multiapp import MultiApp
import utils
import sidebar_menu

# Import your application modules here
from Pages import home, mlb_aapi, mlb_americanindian, mlb_asian, mlb_black, mlb_hispanic, mlb_white

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("MLB AAPI", mlb_aapi.app)
app.add_app("MLB American Indian", mlb_americanindian.app)
app.add_app("MLB Asian", mlb_asian.app)
app.add_app("MLB Black", mlb_black.app)
app.add_app("MLB Hispanic", mlb_hispanic.app)
app.add_app("MLB White", mlb_white.app)

utils.apply_common_styles()

# Initialize sidebar menu
page_function = sidebar_menu.sidebar_menu()

if page_function:
    page_function()
else:
    app.run()
