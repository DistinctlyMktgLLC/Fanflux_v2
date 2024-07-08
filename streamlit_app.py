import streamlit as st
from multiapp import MultiApp
import utils
import sidebar_menu

# Import your application modules here
from Pages import home_app, mlb_aapi_app, mlb_americanindian_app, mlb_asian_app, mlb_black_app, mlb_hispanic_app, mlb_white_app, chatbot_page_app

app = MultiApp()

# Add all your application here
app.add_app("Home", home_app)
app.add_app("MLB AAPI", mlb_aapi_app)
app.add_app("MLB American Indian", mlb_americanindian_app)
app.add_app("MLB Asian", mlb_asian_app)
app.add_app("MLB Black", mlb_black_app)
app.add_app("MLB Hispanic", mlb_hispanic_app)
app.add_app("MLB White", mlb_white_app)
app.add_app("Chatbot", chatbot_page_app)

utils.apply_common_styles()

# Initialize sidebar menu
page_function = sidebar_menu.sidebar_menu()

if page_function:
    page_function()
else:
    app.run()
