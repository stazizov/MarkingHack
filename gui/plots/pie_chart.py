import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

with open('interface.json') as f:
    config = json.load(f)

with open('interface.json') as f:
    config = json.load(f)

def generate_pie_chart(df:pd.DataFrame, column:str) -> go.Figure():
    counts = df.value_counts(column)

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=counts.index, values=counts.values, hole=0.3))
    fig.update_layout(title=f"{config['plot_messages']['piechart_title_prefix']} <<{column}>><br>")
    return fig