import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Load the data
@st.cache_data
def load_data():
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')
    return df

df = load_data()

# Calculate totals for scorecards
def calculate_total(df, fandom_level):
    filtered_df = df[df['Fandom Level'] == fandom_level]
    income_levels = [
        'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
        'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
        'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
        'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
        'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
        'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
        'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
        'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
    ]
    numeric_df = filtered_df[income_levels]
    return numeric_df.sum().sum()

avid_total = calculate_total(df, 'Avid')
casual_total = calculate_total(df, 'Casual')
convertible_total = calculate_total(df, 'Convertible Fans')

# Create styled scorecards
def create_scorecard(title, value, color):
    st.markdown(
        f"""
        <div style="background-color:#333333; padding:10px; border-radius:10px; box-shadow: 2px 2px 2px #000;">
            <h2 style="color:{color};">{title}</h2>
            <h1 style="color:white;">{value:,}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("White Baseball Fans")
create_scorecard("Avid Fans", avid_total, "#FF5733")
create_scorecard("Casual Fans", casual_total, "#FFC300")
create_scorecard("Convertible Fans", convertible_total, "#3498DB")

# Create the map
m = leafmap.Map(center=[40, -100], zoom=4)
m.add_points_from_xy(
    df,
    x="US lon",
    y="US lat",
    color_column="Fandom Level",
    icon_names=["gear", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
)

m.to_streamlit(height=700)
