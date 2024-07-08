import streamlit as st
import yagmail
import requests
import json
from firebase_config import auth, db
import streamlit.components.v1 as components

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Access reCAPTCHA keys
recaptcha_site_key = st.secrets["recaptcha"]["siteKey"]
recaptcha_secret_key = st.secrets["recaptcha"]["secretKey"]

# Access email credentials
email_username = st.secrets["email"]["username"]
email_password = st.secrets["email"]["password"]

# Initialize yagmail for sending emails
yag = yagmail.SMTP(email_username, email_password)

def send_verification_email(to_email, verification_link):
    subject = "Verify your email"
    contents = f"Please verify your email by clicking the following link: {verification_link}"
    yag.send(to=to_email, subject=subject, contents=contents)

def verify_recaptcha(response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": recaptcha_secret_key,
        "response": response
    }
    r = requests.post(url, data=data)
    result = json.loads(r.text)
    return result.get("success", False)

def display_recaptcha(site_key):
    recaptcha_html = f"""
    <div id="recaptcha-container"></div>
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    <script>
        function onSubmit(token) {{
            document.getElementById("recaptcha-response").value = token;
            document.getElementById("recaptcha-form").submit();
        }}
    </script>
    <form id="recaptcha-form" action="?" method="POST">
        <input type="hidden" id="recaptcha-response" name="recaptcha-response">
        <button class="g-recaptcha" data-sitekey="{site_key}" data-callback="onSubmit">
            Submit
        </button>
    </form>
    """
    components.html(recaptcha_html)

# Registration form
st.header("Sign Up")
new_email = st.text_input("New Email")
new_password = st.text_input("New Password", type="password")

if st.button("Create Account"):
    recaptcha_response = st.experimental_get_query_params().get("recaptcha-response", [None])[0]
    if recaptcha_response and verify_recaptcha(recaptcha_response):
        try:
            user = auth.create_user_with_email_and_password(new_email, new_password)
            auth.send_email_verification(user['idToken'])
            st.success("Registration successful! Please verify your email before logging in.")
        except Exception as e:
            st.error(f"Failed to register: {e}")
    else:
        st.error("reCAPTCHA verification failed. Please try again.")
    display_recaptcha(recaptcha_site_key)

# Login form
st.header("Sign In")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        if not auth.get_account_info(user['idToken'])['users'][0]['emailVerified']:
            st.error("Email not verified. Please check your inbox.")
        else:
            st.success("Login successful!")
    except Exception as e:
        st.error(f"Failed to log in: {e}")

# Show reCAPTCHA
display_recaptcha(recaptcha_site_key)
