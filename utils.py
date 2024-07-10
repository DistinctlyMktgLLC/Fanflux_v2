import streamlit as st

def apply_common_styles():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f0f0;
        }
        .sidebar .sidebar-content {
            background-color: #1d1d1d;
        }
        .css-1d391kg {
            background-color: #1d1d1d;
            padding: 10px 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
