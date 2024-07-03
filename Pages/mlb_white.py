import streamlit as st
import utils
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit_folium import st_folium

def app():
    race = "White"  # Set the race dynamically here
    st.title(f"{race} Baseball Fans")

    # Data Loading
    file_path = f'data/Fanflux_Intensity_MLB_{race}.parquet'
    df = utils.load_data(file_path)

    # Sidebar Filters
    with st.sidebar:
        st.header("Filters")
        team = st.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
        league = st.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
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
        income_level = st.selectbox('Select Income Levels', ['Choose an option'] + income_columns)
        fandom_level = st.selectbox('Select a Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    # Filter the dataframe based on selections
    filtered_df = df.copy()
    if team != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Team'] == team]
    if league != 'Choose an option':
        filtered_df = filtered_df[filtered_df['League'] == league]
    if income_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df[income_level] > 0]
    if fandom_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_level]

    # Scorecards
    avid_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Avid'])
    casual_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Casual'])
    convertible_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Convertible Fans'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Avid Fans", avid_fans)
    col2.metric("Casual Fans", casual_fans)
    col3.metric("Convertible Fans", convertible_fans)

    # Data Table
    st.markdown("### Fan Opportunity Table")
    columns_to_show = [
        'Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'
    ]
    gb = GridOptionsBuilder.from_dataframe(filtered_df[columns_to_show])
    gb.configure_default_column(editable=True)
    if income_level != 'Choose an option':
        gb.configure_column(income_level, hide=False)  # Show selected income column
    else:
        for col in income_columns:
            gb.configure_column(col, hide=True)  # Hide all income columns initially
    grid_options = gb.build()
    AgGrid(filtered_df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)

    # Map Visualization
    st.markdown("### Fan Opportunity Map")
    m = utils.create_map()
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'green',
        'Casual': 'yellow',
        'Convertible Fans': 'red'
    })
    st_folium(m, width=700, height=500)

if __name__ == "__main__":
    app()
