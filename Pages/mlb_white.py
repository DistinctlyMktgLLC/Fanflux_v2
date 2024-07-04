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

# Income levels columns
income_levels = [
    'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)', 'Getting By ($15,000 to $19,999)',
    'Starting Out ($20,000 to $24,999)', 'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
    'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)', 'Middle Class ($45,000 to $49,999)',
    'Comfortable ($50,000 to $59,999)', 'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
    'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)', 'Wealthy ($150,000 to $199,999)',
    'Affluent ($200,000 or more)'
]

# Calculate totals for scorecards
def calculate_total(df, fandom_level):
    filtered = df[df['Fandom Level'] == fandom_level]
    numeric_df = filtered[income_levels]
    return numeric_df.sum().sum()

avid_total = calculate_total(filtered_df, 'Avid')
casual_total = calculate_total(filtered_df, 'Casual')
convertible_total = calculate_total(filtered_df, 'Convertible Fans')

# Function to create styled scorecards
def create_scorecard(title, value, color):
    st.markdown(
        f"""
        <div style="background-color:black; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5); margin-bottom: 20px; position: relative;">
            <div style="background-color:{color}; height:100%; width:10px; position: absolute; left: 0; top: 0; bottom: 0; border-top-left-radius: 10px; border-bottom-left-radius: 10px;"></div>
            <div style="margin-left: 20px;">
                <h2 style="color:white;">{title}</h2>
                <p style="color:white; font-size:24px;">{value}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("White Baseball Fans")

# Display scorecards
create_scorecard("Avid Fans", avid_total, "#FF5733")
create_scorecard("Casual Fans", casual_total, "#FFC300")
create_scorecard("Convertible Fans", convertible_total, "#3498DB")

# Display map
m = leafmap.Map(center=[40, -100], zoom=4)
m.add_points_from_xy(
    filtered_df,
    x="US lon",
    y="US lat",
    color_column="Fandom Level",
    colors=["red", "orange", "blue"],  # Only provide colors for the unique values in the 'Fandom Level' column
    icon_names=["circle", "info-sign", "star"],
    spin=True,
    add_legend=True,
)
m.to_streamlit()
