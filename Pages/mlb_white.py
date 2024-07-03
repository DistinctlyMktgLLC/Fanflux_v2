import streamlit as st
import utils
from st_aggrid import AgGrid, GridOptionsBuilder

def app():
    st.title("White Baseball Fans")

    df = utils.load_data('data/Fanflux_Intensity_MLB_White.parquet')

    # Calculate Total Fans
    df['Total Fans'] = df[
        [
            'Struggling (Less than $10,000)', 'Getting By ($10,000 to $14,999)',
            'Getting By ($15,000 to $19,999)', 'Starting Out ($20,000 to $24,999)',
            'Starting Out ($25,000 to $29,999)', 'Starting Out ($30,000 to $34,999)',
            'Middle Class ($35,000 to $39,999)', 'Middle Class ($40,000 to $44,999)',
            'Middle Class ($45,000 to $49,999)', 'Comfortable ($50,000 to $59,999)',
            'Comfortable ($60,000 to $74,999)', 'Doing Well ($75,000 to $99,999)',
            'Prosperous ($100,000 to $124,999)', 'Prosperous ($125,000 to $149,999)',
            'Wealthy ($150,000 to $199,999)', 'Affluent ($200,000 or more)'
        ]
    ].sum(axis=1)

    st.sidebar.title("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    fandom_level = st.sidebar.selectbox('Select Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    filters = {}
    if team != 'Choose an option':
        filters['Team'] = team
    if league != 'Choose an option':
        filters['League'] = league
    if fandom_level != 'Choose an option':
        filters['Fandom Level'] = fandom_level

    filtered_df = df.copy()
    for key, value in filters.items():
        filtered_df = filtered_df[filtered_df[key] == value]

    st.subheader("Fan Opportunity Data")
    
    # Select columns to display
    columns_to_display = ['Team', 'League', 'Neighborhood', 'zipcode', 'Intensity', 'Fandom Level', 'Race', 'Total Fans']
    filtered_df = filtered_df[columns_to_display]

    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gridOptions = gb.build()
    AgGrid(filtered_df, gridOptions=gridOptions, enable_enterprise_modules=True, theme='alpine')

    st.subheader("Fan Opportunity Map")
    m = utils.create_map()
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'yellow',
        'Casual': 'green',
        'Convertible': 'red'
    })
    st.components.v1.html(m._repr_html_(), height=500)

if __name__ == "__main__":
    app()
