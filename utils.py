# utils.py
import streamlit as st
import pandas as pd

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

def load_data():
    try:
        df = pd.read_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned.parquet")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def filter_data(df, leagues, teams, fandom_levels, races, income_levels):
    if leagues:
        df = df[df['League'].isin(leagues)]
    if teams:
        df = df[df['Team'].isin(teams)]
    if fandom_levels:
        df = df[df['Fandom Level'].isin(fandom_levels)]
    if races:
        df = df[df['Race'].isin(races)]
    if income_levels:
        df = df[df[income_levels].sum(axis=1) > 0]  # Example filter for income levels

    return df

def display_fan_demographics(df):
    total_avid_fans = df["Avid Fans"].sum()
    total_casual_fans = df["Casual Fans"].sum()
    total_convertible_fans = df["Convertible Fans"].sum()

    st.metric(label="Total Avid Fans", value=total_avid_fans)
    st.metric(label="Total Casual Fans", value=total_casual_fans)
    st.metric(label="Total Convertible Fans", value=total_convertible_fans)
