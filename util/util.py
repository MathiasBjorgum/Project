from pathlib import Path
from typing import Any

import pandas as pd

CWD = Path.cwd()
DATA_PATH = CWD.joinpath("data")


def get_dataset(filename: str) -> pd.DataFrame | Any:
    '''
    Returns a dataset with the given filename, 
    given that it exists in the `data` directory.
    Returns none otherwise.
    '''

    try:
        return pd.read_csv(DATA_PATH.joinpath(filename))
    except:
        print("Could not read the file, please check that it exists.")
        return None

def clean_attrition_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    '''Clean the dataset'''
    dataset.columns = [col.replace(
    " ", "_") for col in dataset.columns]
    dataset = dataset.rename(columns={"Dateofjoining": "Date_Of_Joining",
                                                      "LastWorkingDate": "Last_Working_Date",
                                                      "MMM-YY": "Date"})

    dataset.Date = pd.to_datetime(dataset.Date)
    dataset.Date_Of_Joining = pd.to_datetime(dataset.Date_Of_Joining)
    dataset.Last_Working_Date = pd.to_datetime(dataset.Last_Working_Date)

    return dataset