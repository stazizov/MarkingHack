import plotly.express as px
import pandas as pd
import json

def generate_countplot(df:pd.DataFrame, column:str) -> px.bar:
    counts = df.value_counts(column)
    bar = px.bar(
        x=counts.index, 
        y=counts.values,  
        )
    return bar