import streamlit as st
import utils

def app():
    utils.apply_common_styles()

    st.sidebar.title("Fanflux Navigation")
    page = st.sidebar.selectbox("Select a page", ["White Baseball Fans"])
    st.title("White Baseball Fans")

    # Load the data
    df = utils.load_data("data/Fanflux_Intensity_MLB_White.parquet")

    # Debugging: Print the columns of the DataFrame
    st.write("DataFrame Columns:", df.columns.tolist())

    # Filter options
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + sorted(df['Income Levels'].unique()))

    # Filter the DataFrame
    if team != 'Choose an option' and income_level != 'Choose an option':
        filtered_df = df[(df['Team'] == team) & (df['Income Levels'] == income_level)]
    elif team != 'Choose an option':
        filtered_df = df[df['Team'] == team]
    elif income_level != 'Choose an option':
        filtered_df = df[df['Income Levels'] == income_level]
    else:
        filtered_df = df

    # Create and display the table
    gb = utils.create_grid_options(filtered_df)
    grid_response = st.datatable(filtered_df, gridOptions=gb, height=500, width='100%', reload_data=True)

    # Create and display the map
    m = utils.create_map()
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'red',
        'Casual': 'blue',
        'Convertible': 'green'
    })
    st_folium(m, width=700, height=500)
