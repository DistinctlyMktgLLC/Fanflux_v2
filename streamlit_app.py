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

# reCAPTCHA configuration
recaptcha_site_key = st.secrets["recaptcha"]["siteKey"]
recaptcha_secret_key = st.secrets["recaptcha"]["secretKey"]

def verify_recaptcha(response_token):
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': recaptcha_secret_key,
        'response': response_token
    }
    response = requests.post(verify_url, data=payload)
    result = response.json()
    return result.get("success", False)

def send_email_notification(email):
    yag = yagmail.SMTP(st.secrets["email"]["username"], st.secrets["email"]["password"])
    yag.send(
        to="info@distinctlymktg.com",
        subject="New Registration Notification",
        contents=f"A new user has registered: {email}"
    )

# UI setup
st.title("Fanflux")
st.subheader("Dive into the Metrics that Matter")

st.write("""
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
""")

# Action selection
action = st.radio("Choose Action", ["Sign Up", "Log In"])

if action == "Sign Up":
    st.subheader("Sign Up")
    signup_email = st.text_input("New Email", key="signup_email")
    signup_password = st.text_input("New Password", type="password", key="signup_password")

    recaptcha_response = st.text_input("Recaptcha response", key="recaptcha_response", type="hidden")
    st.components.v1.html(f"""
        <div 
