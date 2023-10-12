import streamlit as st
import os
import json 
import pandas as pd

from plots.pie_chart import generate_pie_chart
from plots.box_plot import generate_box_plot
from utils import empty_page

with open('interface.json') as f:
    config = json.load(f)

st.set_page_config(page_title=config["upload_1"], page_icon="📊")

def page2_gui():
    st.title(config['upload_1'])
    
    df = pd.read_parquet(os.path.join(config["download_folder"], config["input_filename"]))
    
    st.write(df.head(config["n_rows_table"]))
    st.write(df.describe().transpose())

    st.plotly_chart(generate_pie_chart(df, "operation_type"))
    st.plotly_chart(generate_box_plot(df.sample(config["max_data_points"]), "cnt"))


if os.path.exists(os.path.join(config["download_folder"], config["input_filename"])):
    page2_gui()
else:
    empty_page()
 