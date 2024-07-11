import streamlit as st
import uuid

def app():
    st.title("Chatbot")
    st.write("This is the chatbot page.")

    # Example widget with unique key
    st.text_input("Enter your message", key=f"text_input_{uuid.uuid4()}")
