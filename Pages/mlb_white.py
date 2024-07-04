import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Load data
@st.cache_data
def load_data():
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Fanflux Navigation")
selected_fandom = st.sidebar.multiselect("Select Fandom Level", df["Fandom Level"].unique())
selected_race = st.sidebar.multiselect("Select Race", df["Race"].unique())
selected_team = st.sidebar.multiselect("Select Teams", df["Team"].unique())

# Filter data based on selections
filtered_df = df.copy()
if selected_fandom:
    filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom)]
if selected_race:
    filtered_df = filtered_df[filtered_df['Race'].isin(selected_race)]
if selected_team:
    filtered_df = filtered_df[filtered_df['Team'].isin(selected_team)]

# Columns representing income levels
income_levels = [
    'Struggling (Less than $10,000)',
    'Getting By ($10,000 to $14,999)',
    'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)',
    'Starting Out ($25,000 to $29,999)',
    'Steady ($30,000 to $34,999)',
    'Steady ($35,000 to $39,999)',
    'Stable ($40,000 to $44,999)'
]

# Function to calculate the sum of income levels for a specific fandom level
def calculate_total(df, fandom_level):
    numeric_df = df[income_levels]
    total = numeric_df[df['Fandom Level'] == fandom_level].sum().sum()
    return total

# Calculate totals for scorecards
avid_total = calculate_total(filtered_df, 'Avid')
casual_total = calculate_total(filtered_df, 'Casual')
convertible_total = calculate_total(filtered_df, 'Convertible Fans')

# Function to create styled scorecards
def create_scorecard(label, value, color):
    card_html = f"""
    <div style="background-color: black; border-radius: 10px; padding: 20px; box-shadow: 5px 5px 10px #000; margin: 10px 0; position: relative;">
        <div style="width: 10px; height: 100%; background-color: {color}; position: absolute; left: 0; top: 0; bottom: 0; border-top-left-radius: 10px; border-bottom-left-radius: 10px;"></div>
        <div style="margin-left: 20px;">
            <h2 style="color: white;">{label}</h2>
            <p style="font-size: 24px; color: white;">{value}</p>
        </div>
    </div>
    """
    return card_html

# Display scorecards
st.markdown(create_scorecard('Avid Fans', avid_total, 'red'), unsafe_allow_html=True)
st.markdown(create_scorecard('Casual Fans', casual_total, 'orange'), unsafe_allow_html=True)
st.markdown(create_scorecard('Convertible Fans', convertible_total, 'blue'), unsafe_allow_html=True)

# Create and display the map
m = leafmap.Map(center=[40, -100], zoom=4)
m.add_points_from_xy(filtered_df, x="US lon", y="US lat", color_column="Fandom Level")

m.to_streamlit(height=700)
