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

    # Income level columns
    income_level_columns = [
        "Struggling (Less than $10,000)",
        "Getting By ($10,000 to $14,999)",
        "Getting By ($15,000 to $19,999)",
        "Starting Out ($20,000 to $24,999)",
        "Starting Out ($25,000 to $29,999)",
        "Starting Out ($30,000 to $34,999)",
        "Middle Class ($35,000 to $39,999)",
        "Middle Class ($40,000 to $44,999)",
        "Middle Class ($45,000 to $49,999)",
        "Comfortable ($50,000 to $59,999)",
        "Comfortable ($60,000 to $74,999)",
        "Doing Well ($75,000 to $99,999)",
        "Prosperous ($100,000 to $124,999)",
        "Prosperous ($125,000 to $149,999)",
        "Wealthy ($150,000 to $199,999)",
        "Affluent ($200,000 or more)"
    ]

    # Calculate Total Fans
    df['Total Fans'] = df[income_level_columns].sum(axis=1)

    # Filter options
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + income_level_columns)

    if team != 'Choose an option':
        df = df[df['Team'] == team]

    if income_level != 'Choose an option':
        df = df[df[income_level] > 0]

    # Display the filtered data in a datatable
    st.subheader('Filtered Data')
    st.dataframe(df)

    # Create map
    st.subheader('Fan Opportunity Map')
    m = utils.create_map()

    color_key = {
        "Avid": "red",
        "Casual": "blue",
        "Convertible": "green"
    }

    utils.add_map_markers(m, df, 'Fandom Level', color_key)

    st_folium(m, width=700, height=500)

if __name__ == "__main__":
    app()
