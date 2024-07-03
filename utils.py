import pandas as pd
import streamlit as st

def load_data(page_name):
    file_path = f"data/Fanflux_Intensity_MLB_{page_name}.parquet"
    return pd.read_parquet(file_path)

def apply_common_styles():
    st.markdown(
        """
        <style>
        .main-content {
            background-color: black;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #333;
            color: white;
        }
        .css-1aumxhk {
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
