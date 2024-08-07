import streamlit as st
import leafmap.foliumap as leafmap
import polars as pl
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the updated data
@st.cache_data
def load_data():
    logger.info("Loading data...")
    df = pl.read_parquet('data/updated_combined_leagues.parquet')
    logger.info("Data loaded successfully.")
    return df

try:
    # Convert Polars DataFrame to pandas DataFrame using fastparquet
    df = load_data().to_pandas(engine='fastparquet')
except Exception as e:
    logger.error(f"Error loading data: {e}")
    df = pd.DataFrame()  # Initialize an empty DataFrame in case of error

# Sample 10% of the dataset for initial display
sampled_df = df.sample(frac=0.1, random_state=42)

# Main app function for leagues analysis
def app():
    st.title("Leagues Analysis")

    # Filters
    st.sidebar.header("Filters")
    try:
        logger.info("Setting up filters...")
        selected_fandom_levels = st.sidebar.multiselect("Select Fandom Level", df['Fandom Level'].unique(), key="fandom_level_filter_leagues")
        selected_races = st.sidebar.multiselect("Select Race", df['Race'].unique(), key="race_filter_leagues")
        selected_leagues = st.sidebar.multiselect("Select League", df['League'].unique(), key="league_filter_leagues")
        selected_teams = st.sidebar.multiselect("Select Team", df['Team'].unique(), key="team_filter_leagues")
        selected_income_levels = st.sidebar.multiselect("Select Income Level", df.columns[12:], key="income_level_filter_leagues")
        logger.info("Filters set up successfully.")
    except Exception as e:
        logger.error(f"Error setting up filters: {e}")
        selected_fandom_levels = selected_races = selected_leagues = selected_teams = selected_income_levels = []

    # Apply filters to the sampled dataset
    filtered_df = sampled_df.copy()
    try:
        if selected_fandom_levels:
            filtered_df = filtered_df[filtered_df['Fandom Level'].isin(selected_fandom_levels)]
        if selected_races:
            filtered_df = filtered_df[filtered_df['Race'].isin(selected_races)]
        if selected_leagues:
            filtered_df = filtered_df[filtered_df['League'].isin(selected_leagues)]
        if selected_teams:
            filtered_df = filtered_df[filtered_df['Team'].isin(selected_teams)]
        if selected_income_levels:
            filtered_df = filtered_df[filtered_df[selected_income_levels].sum(axis=1) > 0]
    except Exception as e:
        logger.error(f"Error applying filters: {e}")

    # Calculate metrics
    try:
        total_avid_fans = filtered_df[filtered_df['Fandom Level'] == 'Avid']['Total Fans'].sum()
        total_casual_fans = filtered_df[filtered_df['Fandom Level'] == 'Casual']['Total Fans'].sum()
        total_convertible_fans = filtered_df[filtered_df['Fandom Level'] == 'Convertible']['Total Fans'].sum()
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}")

    # Display metrics in scorecards
    col1, col2, col3 = st.columns(3)
    try:
        with col1:
            st.metric(label="Total Avid Fans", value=int(total_avid_fans))
        with col2:
            st.metric(label="Total Casual Fans", value=int(total_casual_fans))
        with col3:
            st.metric(label="Total Convertible Fans", value=int(total_convertible_fans))
    except Exception as e:
        logger.error(f"Error displaying metrics: {e}")

    # Add explanatory note
    st.markdown("""
        **Note:** The initial data displayed is a 10% sample of the total dataset. Adjusting filters will apply to this sample.
    """)

    # Add conditional explanatory note
    if selected_teams and selected_leagues:
        st.markdown("""
            **Additional Note:** The total fans displayed in the scorecards represent the sum of fans for the selected teams and leagues. If both teams and leagues are selected, the total fans will be a combined sum.
        """)

    # Add note for selecting teams and leagues
    st.markdown("""
        **Selection Tip:** You can pick different teams in different leagues. Ensure your league choices sync with the teams you select to get accurate insights.
    """)

    # Create the map with marker clustering
    st.subheader("Fan Opportunity Map")
    with st.spinner("Finding Fandom..."):
        try:
            m = leafmap.Map(center=[40, -100], zoom=4, draw_export=False)
            color_column = "Fandom Level"
            color_map = {
                "Avid": "red",
                "Casual": "blue",
                "Convertible": "green"
            }
            popup = ["Team", "League", "Neighborhood", "Fandom Level", "Race", "Total Fans"]

            m.add_points_from_xy(
                filtered_df,
                x="US lon",
                y="US lat",
                color_column=color_column,
                colors=[color_map[val] for val in filtered_df[color_column].unique()],
                popup=popup,
                min_width=200,
                max_width=300
            )

            m.to_streamlit(width=1200, height=700)
        except Exception as e:
            logger.error(f"Error creating map: {e}")

# Run the app function
app()
