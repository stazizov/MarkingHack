import plotly.express as px
import pandas as pd
import json

with open('interface.json') as f:
    config = json.load(f)

def generate_box_plot(df:pd.DataFrame, column:str) -> px.box:
    fig = px.box(
        df, 
        y=column, 
        title=f"{config['plot_messages']['boxplot_title_prefix']} <<{column}>>",
        )
    return fig