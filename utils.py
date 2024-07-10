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
    total_avid_fans = df[df['Fandom Level'] == 'Avid']['Intensity'].sum()
    total_casual_fans = df[df['Fandom Level'] == 'Casual']['Intensity'].sum()
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible']['Intensity'].sum()

    st.metric(label="Total Avid Fans", value=total_avid_fans)
    st.metric(label="Total Casual Fans", value=total_casual_fans)
    st.metric(label="Total Convertible Fans", value=total_convertible_fans)
