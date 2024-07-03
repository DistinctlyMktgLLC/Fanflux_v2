import streamlit as st

def apply_common_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #000000;
        }
        .stButton>button {
            color: white;
        }
        .stButton>button:hover {
            color: black;
            background-color: white;
        }
        .metric-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px;
            padding: 10px;
            border-radius: 5px;
            background-color: #333333;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .metric-container p {
            margin: 0;
            padding: 0;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def style_aggrid():
    gridOptions = {
        "defaultColDef": {
            "filter": True,
            "sortable": True,
            "floatingFilter": True,
            "resizable": True,
        },
        "pagination": True,
        "paginationPageSize": 25,
    }
    return gridOptions

def apply_scorecard_styles():
    st.markdown("""
        <style>
        .scorecard {
            display: flex;
            align-items: center;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        }
        .scorecard .highlight {
            width: 10px;
            height: 100%;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_scorecard(label, value, color):
    st.markdown(f"""
        <div class="scorecard" style="background-color: {color};">
            <div class="highlight" style="background-color: {color};"></div>
            <div>
                <p>{label}</p>
                <p>{value}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def add_map_markers(m, df, color_column, color_key):
    for _, row in df.iterrows():
        m.add_point(row['latitude'], row['longitude'], color=color_key.get(row[color_column], 'blue'))
