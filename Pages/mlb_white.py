import streamlit as st
import utils
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit_folium import st_folium

def app():
    st.title("White Baseball Fans")

    # Sidebar Filters
    with st.sidebar:
        st.header("Filters")
        team = st.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
        league = st.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
        income_level = st.selectbox('Select Income Levels', ['Choose an option'] + sorted(df['Income Levels'].unique()))
        fandom_level = st.selectbox('Select a Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    # Data Loading
    df = utils.load_data('data/Fanflux_Intensity_MLB_White.parquet')
    filtered_df = df[(df['Team'] == team) & (df['League'] == league) & (df['Income Levels'] == income_level) & (df['Fandom Level'] == fandom_level)]

    # Scorecards
    avid_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Avid'])
    casual_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Casual'])
    convertible_fans = len(filtered_df[filtered_df['Fandom Level'] == 'Convertible Fans'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Avid Fans", avid_fans)
    col2.metric("Casual Fans", casual_fans)
    col3.metric("Convertible Fans", convertible_fans)

    # Data Table
    st.markdown("### White Baseball Fan Opportunity")
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_default_column(editable=True)
    gb.configure_column("Income Levels", hide=True)  # Hide initially
    grid_options = gb.build()
    AgGrid(filtered_df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)

    # Map Visualization
    st.markdown("### Map Visualization")
    m = utils.create_map()
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'green',
        'Casual': 'yellow',
        'Convertible Fans': 'red'
    })
    st_folium(m, width=700, height=500)
