import pandas as pd
import numpy as np
from config import *

input_data = pd.read_parquet("dataset/input.parquet").iloc[::5]
transition_data = pd.read_parquet("dataset/transition.parquet").iloc[::100]
output_data = pd.read_parquet(
    "dataset/output.parquet"
).iloc[::200]

input_data.to_parquet("dataset/input_small.parquet")
transition_data.to_parquet("dataset/transition.parquet")
output_data.to_parquet("dataset/output.parquet")