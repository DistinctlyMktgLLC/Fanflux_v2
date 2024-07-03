import streamlit as st
import Pages.home as home
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_black as black
import Pages.mlb_hispanic as hispanic
import Pages.mlb_white as white
import utils

st.set_page_config(initial_sidebar_state="collapsed")

# Function to display navigation bar
def navigation():
    st.markdown(
        """
        <style>
        .nav {background-color: #333; overflow: hidden;}
        .nav a {float: left; display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
        .nav a:hover {background-color: #ddd; color: black;}
        </style>
        <div class="nav">
            <a href="#home" id="home-link">Home</a>
            <a href="#aapi-baseball-fans" id="aapi-link">AAPI Baseball Fans</a>
            <a href="#american-indian-baseball-fans" id="americanindian-link">American Indian Baseball Fans</a>
            <a href="#asian-baseball-fans" id="asian-link">Asian Baseball Fans</a>
            <a href="#black-baseball-fans" id="black-link">Black Baseball Fans</a>
            <a href="#hispanic-baseball-fans" id="hispanic-link">Hispanic Baseball Fans</a>
            <a href="#white-baseball-fans" id="white-link">White Baseball Fans</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

navigation()

# Function to handle page routing
def router():
    page = st.experimental_get_query_params().get("page", ["home"])[0]

    if page == "home":
        home.app()
    elif page == "aapi-baseball-fans":
        aapi.app()
    elif page == "american-indian-baseball-fans":
        americanindian.app()
    elif page == "asian-baseball-fans":
        asian.app()
    elif page == "black-baseball-fans":
        black.app()
    elif page == "hispanic-baseball-fans":
        hispanic.app()
    elif page == "white-baseball-fans":
        white.app()

router()

# JavaScript to handle link clicks and update URL
st.markdown(
    """
    <script>
    document.getElementById('home-link').onclick = function() {window.location.hash = '';};
    document.getElementById('aapi-link').onclick = function() {window.location.hash = '#aapi-baseball-fans';};
    document.getElementById('americanindian-link').onclick = function() {window.location.hash = '#american-indian-baseball-fans';};
    document.getElementById('asian-link').onclick = function() {window.location.hash = '#asian-baseball-fans';};
    document.getElementById('black-link').onclick = function() {window.location.hash = '#black-baseball-fans';};
    document.getElementById('hispanic-link').onclick = function() {window.location.hash = '#hispanic-baseball-fans';};
    document.getElementById('white-link').onclick = function() {window.location.hash = '#white-baseball-fans';};
    </script>
    """,
    unsafe_allow_html=True,
)
