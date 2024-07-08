import streamlit as st
import yagmail
from firebase_config import auth, db

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

from multiapp import MultiApp
from sidebar_menu import sidebar_menu
import Pages.home as home
import Pages.mlb_aapi as mlb_aapi
import Pages.mlb_americanindian as mlb_americanindian
import Pages.mlb_asian as mlb_asian
import Pages.mlb_black as mlb_black
import Pages.mlb_hispanic as mlb_hispanic
import Pages.mlb_white as mlb_white

def send_email_notification(email):
    try:
        yag = yagmail.SMTP('darnel.m@distinctlymktg.com', 'wrkl qykt dvon eeyd')
        yag.send(
            to="info@distinctlymktg.com",
            subject="New Registration Notification",
            contents=f"A new user has registered: {email}"
        )
    except Exception as e:
        st.error(f"Failed to send email notification: {e}")

def register_user(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        send_email_notification(email)
        st.success("Registration successful! Please verify your email before logging in.")
    except Exception as e:
        st.error(f"Failed to register: {e}")

def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state['logged_in'] = True
        st.session_state['user'] = user
        st.success("Login successful!")
    except Exception as e:
        st.error(f"Failed to log in: {e}")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.sidebar.success(f"Welcome {st.session_state['user']['email']}")

    # Initialize the MultiApp
    app = MultiApp()

    # Add all your applications here
    app.add_app("Home", home.app)
    app.add_app("MLB - AAPI", mlb_aapi.app)
    app.add_app("MLB - American Indian", mlb_americanindian.app)
    app.add_app("MLB - Asian", mlb_asian.app)
    app.add_app("MLB - Black", mlb_black.app)
    app.add_app("MLB - Hispanic", mlb_hispanic.app)
    app.add_app("MLB - White", mlb_white.app)

    # Run the selected app
    selected_app = sidebar_menu()
    if selected_app:
        selected_app()
else:
    st.title("Welcome to Fanflux")
    st.markdown(
        """
        ### Dive into the Metrics that Matter

        Ever wondered why certain fans are more dedicated than others? Or why some regions have higher concentrations of specific fan types? Welcome to Fanflux, where data meets fandom in the most intriguing ways. Here’s what you’ll get:

        - **Discover Fan Distribution:** Visualize the geographical spread of different fan types.
        - **Analyze Fan Intensity:** Understand how passionate fans are about their teams.
        - **Uncover Economic Insights:** See how income levels correlate with fan engagement.

        ### Why It’s Important

        Sports teams, marketers, and fan clubs alike can leverage these insights to:

        - **Target Marketing Efforts:** Focus your campaigns where they’ll have the most impact.
        - **Boost Fan Engagement:** Tailor your strategies to convert casual fans into avid supporters.
        - **Optimize Merchandising:** Stock the right products in the right places based on fan demographics.

        ### Partnered with DonnLynn Partners

        We are proud to collaborate with DonnLynn Partners, who brought us this innovative idea. Combined with our data and tech expertise, we have brought Fanflux to life. Together, we have transformed the way you understand and engage with sports fans.

        Ready to transform your understanding of the sports fan landscape? Let’s get started!
        """,
        unsafe_allow_html=True
    )

    st.header("Sign In")
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        login_user(email, password)
    
    st.header("Sign Up")
    new_email = st.text_input('New Email')
    new_password = st.text_input('New Password', type='password')
    if st.button('Create Account'):
        register_user(new_email, new_password)
