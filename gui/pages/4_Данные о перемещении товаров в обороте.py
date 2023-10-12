import streamlit as st
import os
import json 
import pandas as pd
from pandas.api.types import is_numeric_dtype
import plotly.graph_objects as go
from plots.pie_chart import generate_pie_chart
from plots.box_plot import generate_box_plot
from plots.countplot import generate_countplot
from utils import empty_page

with open('interface.json') as f:
    config = json.load(f)

st.set_page_config(page_title=config["upload_3"], page_icon="📊")

def page4_gui():
    st.title(config['upload_3'])
    
    df = pd.read_parquet(os.path.join(config["download_folder"], config["transition_filename"]))
    
    st.write(df.head(config["n_rows_table"]))
    st.write(df.describe().transpose())

    st.plotly_chart(generate_countplot(df, "dt"))
    st.plotly_chart(
        generate_box_plot(
            df.sample(config["max_data_points"]),
            "cnt_moved"
        )
    )


if os.path.exists(os.path.join(config["download_folder"], "output.parquet")):
    page4_gui()
else:
    empty_page()
 