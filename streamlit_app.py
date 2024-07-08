import streamlit as st
from multiapp import MultiApp
import utils
import os

# Add the authentication code here
import streamlit_authenticator as stauth

# Configuration for the authenticator
authenticator = stauth.Authenticate(
    names=["User1", "User2"],
    usernames=["user1", "user2"],
    passwords=["password1", "password2"],
    cookie_name="streamlit_auth",
    key="abcdef",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
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

    # Run the app
    if __name__ == "__main__":
        app.run()
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
