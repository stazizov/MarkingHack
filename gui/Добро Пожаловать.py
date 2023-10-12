from utils import upload_form 
import plotly.express as px
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import json 

with open('interface.json') as f:
    config = json.load(f)

st.set_page_config(
    page_title=f"{config['title']}" ,
    page_icon=config["emojies"]["pushpin"],
)

st.title(f"{config['title']} {config['emojies']['uptrend']}")

input_circulation_data = upload_form(
    config["upload_1"], 
    config["required_columns"][config["upload_1"]],
    file_format='.parquet'
    )
output_circulation_data = upload_form(
    config["upload_2"], 
    config["required_columns"][config["upload_2"]],
    file_format='.parquet'
    )
transition_circulation_data = upload_form(
    config["upload_3"], 
    config["required_columns"][config["upload_3"]],
    file_format='.parquet'
    )
