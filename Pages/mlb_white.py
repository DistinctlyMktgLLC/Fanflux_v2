import streamlit as st
import utils

# Load data
df = utils.load_data('White')

def app():
    st.title("White Baseball Fans")

    avid_fans = df[df['Fandom Level'] == 'Avid'].shape[0]
    casual_fans = df[df['Fandom Level'] == 'Casual'].shape[0]
    convertible_fans = df[df['Fandom Level'] == 'Not at all'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Avid Fans", avid_fans)
    col2.metric("Casual Fans", casual_fans)
    col3.metric("Convertible Fans", convertible_fans)

    # Sidebar filters
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox('Select a Team', ['Choose an option'] + sorted(df['Team'].unique()))
    league = st.sidebar.selectbox('Select a League', ['Choose an option'] + sorted(df['League'].unique()))
    income_level = st.sidebar.selectbox('Select Income Levels', ['Choose an option'] + df.columns[14:].tolist())
    fandom_level = st.sidebar.selectbox('Select a Fandom Level', ['Choose an option'] + sorted(df['Fandom Level'].unique()))

    filtered_df = df.copy()

    if team != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Team'] == team]

    if league != 'Choose an option':
        filtered_df = filtered_df[filtered_df['League'] == league]

    if income_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df[income_level] > 0]

    if fandom_level != 'Choose an option':
        filtered_df = filtered_df[filtered_df['Fandom Level'] == fandom_level]

    # Render AgGrid
    st.subheader("Fan Opportunity Data")
    utils.render_aggrid(filtered_df)

    # Render map
    st.subheader("Fan Opportunity Map")
    basemap = st.sidebar.selectbox("Select a basemap:", options=['OpenStreetMap', 'Stamen Toner', 'Stamen Terrain', 'Stamen Watercolor', 'CartoDB positron', 'CartoDB dark_matter'], index=0)
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    folium.TileLayer(basemap).add_to(m)
    utils.add_map_markers(m, filtered_df, 'Fandom Level', {
        'Avid': 'green',
        'Casual': 'blue',
        'Not at all': 'red'
    })
    st.markdown(m._repr_html_(), unsafe_allow_html=True)
