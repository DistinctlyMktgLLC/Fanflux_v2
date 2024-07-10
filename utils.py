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
        .stApp {
            background-color: white;
            opacity: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_fan_demographics(df):
    # Check if required columns exist
    required_columns = ["Avid Fans", "Casual Fans", "Convertible Fans"]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"The column '{col}' is missing in the dataset.")
            return

    total_avid_fans = df["Avid Fans"].sum()
    total_casual_fans = df["Casual Fans"].sum()
    total_convertible_fans = df["Convertible Fans"].sum()

    st.metric(label="Total Avid Fans", value=total_avid_fans)
    st.metric(label="Total Casual Fans", value=total_casual_fans)
    st.metric(label="Total Convertible Fans", value=total_convertible_fans)

def load_data():
    df = pd.read_parquet("data/Fanflux_Intensity_All_Leagues_Cleaned.parquet")
    
    # Check if all required columns exist
    income_columns = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)', 
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)', 
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)', 
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)', 
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]

    for col in income_columns + ["Avid Fans", "Casual Fans", "Convertible Fans"]:
        if col not in df.columns:
            st.error(f"The column '{col}' is missing in the dataset.")
            return pd.DataFrame()  # Return an empty DataFrame to avoid further errors
    
    return df

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
        df = df[income_levels]

    return df
