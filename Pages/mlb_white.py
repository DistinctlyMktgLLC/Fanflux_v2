import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import leafmap.foliumap as leafmap
import utils

def app():
    st.title("White Baseball Fans")

    utils.apply_common_styles()
    utils.apply_scorecard_styles()

    # Load data specific to this page
    df = pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')

    # Sidebar filters
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox("Select a Team", options=df["Team"].unique())
    league = st.sidebar.selectbox("Select a League", options=df["League"].unique())
    income_levels = st.sidebar.multiselect("Select Income Levels", options=df.columns[7:])
    fandom_level = st.sidebar.selectbox("Select a Fandom Level", options=df["Fandom Level"].unique())

    # Filter data
    filtered_df = df[(df["Team"] == team) & (df["League"] == league) & (df["Fandom Level"] == fandom_level)]

    # Display scorecards
    avid_fans = filtered_df[filtered_df["Fandom Level"] == "Avid"].shape[0]
    casual_fans = filtered_df[filtered_df["Fandom Level"] == "Casual"].shape[0]
    convertible_fans = filtered_df[filtered_df["Fandom Level"] == "Convertible Fans"].shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        utils.create_scorecard("Avid Fans", avid_fans, "#FFD700")
    with col2:
        utils.create_scorecard("Casual Fans", casual_fans, "#ADFF2F")
    with col3:
        utils.create_scorecard("Convertible Fans", convertible_fans, "#FF6347")

    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    if income_levels:
        gb.configure_columns(income_levels, hide=False)
    grid_options = utils.style_aggrid()
    grid_options.update(gb.build())

    # Display AgGrid
    st.markdown("### Filtered Data")
    AgGrid(filtered_df, gridOptions=grid_options)

    # Display map
    st.markdown("### Map")
    m = leafmap.Map(center=[40, -100], zoom=4)
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        "Avid": "yellow",
        "Casual": "green",
        "Convertible Fans": "red"
    })
    m.to_streamlit(height=500)
