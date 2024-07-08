import streamlit as st
from multiapp import MultiApp
import utils
import os
import streamlit_authenticator as stauth

# Configuration for the authenticator
credentials = st.secrets["credentials"]

# Create hashed passwords manually if necessary
hashed_passwords = stauth.Hasher([credentials[user]["password"] for user in credentials]).generate()

authenticator = stauth.Authenticate(
    credentials={"usernames": {user: {"name": credentials[user]["name"], "password": hash_pass} for user, hash_pass in zip(credentials, hashed_passwords)}},
    cookie_name="auth",
    key="auth",
    cookie_expiry_days=30,
    cookie_key="some_random_cookie_key"
)

# Check authentication
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    from Pages import home, mlb_aapi, mlb_americanindian, mlb_asian, mlb_black, mlb_hispanic, mlb_white

    import sidebar_menu

    app = MultiApp()

    app.add_app("Home", home.app)
    app.add_app("MLB AAPI", mlb_aapi.app)
    app.add_app("MLB American Indian", mlb_americanindian.app)
    app.add_app("MLB Asian", mlb_asian.app)
    app.add_app("MLB Black", mlb_black.app)
    app.add_app("MLB Hispanic", mlb_hispanic.app)
    app.add_app("MLB White", mlb_white.app)

    utils.apply_common_styles()

    filters = sidebar_menu.sidebar()

    if __name__ == "__main__":
        app.run()

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")
