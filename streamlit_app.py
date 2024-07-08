import streamlit as st
import pyrebase
import yagmail
import requests

# Page configuration to avoid multipage error
st.set_page_config(page_title="Fanflux", layout="wide")

# Firebase configuration
firebaseConfig = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "databaseURL": st.secrets["firebase"]["databaseURL"],
    "projectId": st.secrets["firebase"]["projectId"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId": st.secrets["firebase"]["appId"],
    "measurementId": st.secrets["firebase"]["measurementId"]
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Email configuration
email_username = st.secrets["email"]["username"]
email_password = st.secrets["email"]["password"]

# Function to send email notification
def send_email_notification(email):
    try:
        yag = yagmail.SMTP(email_username, email_password)
        yag.send(
            to="info@distinctlymktg.com",
            subject="New Registration Notification",
            contents=f"A new user has registered: {email}"
        )
        return True
    except Exception as e:
        st.error(f"Failed to send email notification: {e}")
        return False

# UI Layout
st.title("Welcome to Fanflux")
st.markdown("""
## Dive into the Metrics that Matter
Ever wondered why certain fans are more dedicated than others? Or why some regions have higher concentrations of specific fan types? Welcome to Fanflux, where data meets fandom in the most intriguing ways. Here’s what you’ll get:
- **Discover Fan Distribution**: Visualize the geographical spread of different fan types.
- **Analyze Fan Intensity**: Understand how passionate fans are about their teams.
- **Uncover Economic Insights**: See how income levels correlate with fan engagement.

### Why It’s Important
Sports teams, marketers, and fan clubs alike can leverage these insights to:
- **Target Marketing Efforts**: Focus your campaigns where they’ll have the most impact.
- **Boost Fan Engagement**: Tailor your strategies to convert casual fans into avid supporters.
- **Optimize Merchandising**: Stock the right products in the right places based on fan demographics.

### Partnered with DonnLynn Partners
We are proud to collaborate with DonnLynn Partners, who brought us this innovative idea. Combined with our data and tech expertise, we have brought Fanflux to life. Together, we have transformed the way you understand and engage with sports fans.

Ready to transform your understanding of the sports fan landscape? Let’s get started!
""")

# Selection for Sign Up or Log In
action = st.radio("Choose Action", ("Sign Up", "Log In"))

if action == "Sign Up":
    signup_email = st.text_input("New Email", key="signup_email")
    signup_password = st.text_input("New Password", type="password", key="signup_password")

    if st.button("Create Account"):
        try:
            user = auth.create_user_with_email_and_password(signup_email, signup_password)
            st.success("Registration successful! Please verify your email before logging in.")
            send_email_notification(signup_email)
        except requests.exceptions.HTTPError as e:
            st.error(f"Registration failed: {e}")
elif action == "Log In":
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(login_email, login_password)
            st.success("Login successful!")
        except requests.exceptions.HTTPError as e:
            st.error(f"Login failed: {e}")
