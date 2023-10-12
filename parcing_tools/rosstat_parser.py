import pandas as pd
import rosstat_to_dict


def get_data_frame() -> pd.DataFrame:
    data = rosstat_to_dict.get_dict()
    data_frame = pd.DataFrame(data)

    return data_frame.transpose()
