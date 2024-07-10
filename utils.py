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
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_fan_demographics(df):
    total_avid_fans = df[df['fandom_level'] == 'avid'].shape[0]
    total_casual_fans = df[df['fandom_level'] == 'casual'].shape[0]
    total_convertible_fans = df[df['fandom_level'] == 'convertible'].shape[0]

    st.metric(label="Total Avid Fans", value=total_avid_fans)
    st.metric(label="Total Casual Fans", value=total_casual_fans)
    st.metric(label="Total Convertible Fans", value=total_convertible_fans)
