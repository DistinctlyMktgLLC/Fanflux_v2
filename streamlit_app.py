import os
import streamlit as st
import Pages.home as home
import Pages.mlb_aapi as aapi
import Pages.mlb_americanindian as americanindian
import Pages.mlb_asian as asian
import Pages.mlb_black as black
import Pages.mlb_hispanic as hispanic
import Pages.mlb_white as white
import utils

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Define the pages
pages = {
    "Home": home,
    "AAPI Baseball Fans": aapi,
    "American Indian Baseball Fans": americanindian,
    "Asian Baseball Fans": asian,
    "Black Baseball Fans": black,
    "Hispanic Baseball Fans": hispanic,
    "White Baseball Fans": white,
}

# Function to display navigation bar
def navigation():
    st.markdown(
        """
        <style>
        .nav {
            background-color: #333; 
            overflow: hidden;
            display: flex;
            justify-content: center;
        }
        .nav a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            font-size: 18px;
        }
        .nav a:hover {
            background-color: #ddd;
            color: black;
        }
        .main-content {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }
        </style>
        <div class="nav">
            <a href="?page=Home" id="home-link">Home</a>
            <a href="?page=AAPI Baseball Fans" id="aapi-link">AAPI Baseball Fans</a>
            <a href="?page=American Indian Baseball Fans" id="americanindian-link">American Indian Baseball Fans</a>
            <a href="?page=Asian Baseball Fans" id="asian-link">Asian Baseball Fans</a>
            <a href="?page=Black Baseball Fans" id="black-link">Black Baseball Fans</a>
            <a href="?page=Hispanic Baseball Fans" id="hispanic-link">Hispanic Baseball Fans</a>
            <a href="?page=White Baseball Fans" id="white-link">White Baseball Fans</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

navigation()

# Function to handle page routing
def router():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["Home"])[0]

    if page in pages:
        pages[page].app()
    else:
        st.error("Page not found")

st.markdown('<div class="main-content">', unsafe_allow_html=True)
router()
st.markdown('</div>', unsafe_allow_html=True)

# JavaScript to handle link clicks and update URL
st.markdown(
    """
    <script>
    document.getElementById('home-link').onclick = function() {window.location.href = '?page=Home';};
    document.getElementById('aapi-link').onclick = function() {window.location.href = '?page=AAPI Baseball Fans';};
    document.getElementById('americanindian-link').onclick = function() {window.location.href = '?page=American Indian Baseball Fans';};
    document.getElementById('asian-link').onclick = function() {window.location.href = '?page=Asian Baseball Fans';};
    document.getElementById('black-link').onclick = function() {window.location.href = '?page=Black Baseball Fans';};
    document.getElementById('hispanic-link').onclick = function() {window.location.href = '?page=Hispanic Baseball Fans';};
    document.getElementById('white-link').onclick = function() {window.location.href = '?page=White Baseball Fans';};
    </script>
    """,
    unsafe_allow_html=True,
)
