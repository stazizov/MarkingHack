from dbfread import DBF
import pandas as pd


def get_data_frame() -> pd.DataFrame:
    index_dbf = DBF("raw_data/index.dbf")
    data_frame = pd.DataFrame(index_dbf)
    return data_frame
