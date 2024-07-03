import streamlit as st
import pandas as pd
import utils
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data
def load_data():
    return pd.read_parquet('data/Fanflux_Intensity_MLB_White.parquet')

def app():
    utils.apply_common_styles()
    
    df = load_data()

    # Sidebar filters
    teams = df['Team'].unique().tolist()
    leagues = df['League'].unique().tolist()
    zipcodes = df['zipcode'].unique().tolist()
    fandom_levels = df['Fandom Level'].replace({'Not at all': 'Convertible Fans'}).unique().tolist()
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

    selected_team = st.sidebar.multiselect("Select a Team", teams)
    selected_league = st.sidebar.multiselect("Select a League", leagues)
    selected_zipcode = st.sidebar.multiselect("Select a Zipcode", zipcodes)
    selected_fandom = st.sidebar.multiselect("Select a Fandom Level", fandom_levels)
    selected_income = st.sidebar.multiselect("Select Income Levels to Display", income_levels)

    # Apply filters
    if selected_team:
        df = df[df['Team'].isin(selected_team)]
    if selected_league:
        df = df[df['League'].isin(selected_league)]
    if selected_zipcode:
        df = df[df['zipcode'].isin(selected_zipcode)]
    if selected_fandom:
        df = df[df['Fandom Level'].replace({'Not at all': 'Convertible Fans'}).isin(selected_fandom)]

    # Update the dataframe to replace "Not at all" with "Convertible Fans"
    df['Fandom Level'] = df['Fandom Level'].replace({'Not at all': 'Convertible Fans'})

    # Calculate counts for scorecards
    total_avid = df[df['Fandom Level'] == 'Avid']['Fandom Level'].count()
    total_casual = df[df['Fandom Level'] == 'Casual']['Fandom Level'].count()
    total_convertible = df[df['Fandom Level'] == 'Convertible Fans']['Fandom Level'].count()

    # Display scorecards
    st.markdown(
        """
        <div style="display: flex; justify-content: space-around;">
            <div style="border-left: 5px solid red; padding: 10px; background-color: black; color: white;">
                <h3>Avid Fans</h3>
                <p>{}</p>
            </div>
            <div style="border-left: 5px solid blue; padding: 10px; background-color: black; color: white;">
                <h3>Casual Fans</h3>
                <p>{}</p>
            </div>
            <div style="border-left: 5px solid green; padding: 10px; background-color: black; color: white;">
                <h3>Convertible Fans</h3>
                <p>{}</p>
            </div>
        </div>
        """.format(total_avid, total_casual, total_convertible),
        unsafe_allow_html=True
    )

    # Display data using AgGrid
    st.title("White Baseball Fans")
    columns_to_display = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race'] + selected_income
    
    gb = GridOptionsBuilder.from_dataframe(df[columns_to_display])
    gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
    gb.configure_side_bar()  # Add a sidebar to the grid
    gridOptions = gb.build()

    AgGrid(df[columns_to_display], gridOptions=gridOptions, enable_enterprise_modules=True)

    # Map visualization
    st.markdown('<div style="height: 600px; width: 100%;">', unsafe_allow_html=True)
    utils.render_map(df)
    st.markdown('</div>', unsafe_allow_html=True)

