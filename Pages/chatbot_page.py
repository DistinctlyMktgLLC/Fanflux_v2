# Pages/chatbot.py
import streamlit as st
from streamlit_chat import message

def generate_bot_response(user_input, data):
    response = ""
    if "summary" in user_input.lower():
        response = "This is a summary of the AAPI data: " + str(data["MLB - AAPI"].describe())
    elif "max score" in user_input.lower():
        response is f"The maximum score in the AAPI dataset is: {data['MLB - AAPI']['score'].max()}"
    else:
        response = "I'm not sure how to help with that. Try asking for a summary or max score."
    return response

def app(dataframes):
    st.header("Chat with our Data Strategist")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input text box
    user_input = st.text_input("Ask something about the data:")

    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"message": user_input, "is_user": True})
        # Generate bot response
        response = generate_bot_response(user_input, dataframes)
        # Add bot message to chat history
        st.session_state.chat_history.append({"message": response, "is_user": False})

    # Display chat history
    for chat in st.session_state.chat_history:
        message(chat['message'], is_user=chat['is_user'])
