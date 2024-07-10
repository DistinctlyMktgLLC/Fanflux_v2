import streamlit as st

def apply_common_styles():
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #262730;
    }
    .sidebar .sidebar-content .element-container {
        color: #f3f4f6;
    }
    .sidebar .sidebar-content .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def display_fan_demographics(df):
    total_avid_fans = df[df['Fandom Level'] == 'Avid'].shape[0]
    total_casual_fans = df[df['Fandom Level'] == 'Casual'].shape[0]
    total_convertible_fans = df[df['Fandom Level'] == 'Convertible'].shape[0]

    st.markdown(f"**Total Avid Fans:** {total_avid_fans}")
    st.markdown(f"**Total Casual Fans:** {total_casual_fans}")
    st.markdown(f"**Total Convertible Fans:** {total_convertible_fans}")
