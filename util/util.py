from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
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


def create_additional_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function aims to create a dummy variable for attrition.
    '''
    df['Year_of_join'] = df['Date_Of_Joining'].apply(lambda t: t.year)
    df['Month_of_join'] = df['Date_Of_Joining'].apply(lambda t: t.month)
    df['Day_of_join'] = df['Date_Of_Joining'].apply(lambda t: t.day)
    df['Year_of_leave'] = df['Last_Working_Date'].apply(lambda t: t.year)
    df['Month_of_leave'] = df['Last_Working_Date'].apply(lambda t: t.month)

    df['Attrition'] = np.nan

    mypop = df.pop('Attrition')
    df.insert(1, 'Attrition', mypop)
    mypop1 = df.pop('Year_of_join')
    df.insert(8, 'Year_of_join', mypop1)
    mypop2 = df.pop('Month_of_join')
    df.insert(9, 'Month_of_join', mypop2)
    mypop3 = df.pop('Day_of_join')
    df.insert(10, 'Day_of_join', mypop3)

    df = df.astype(
        {'Year_of_join': int, 'Month_of_join': int, 'Day_of_join': int})

    df['Attrition'] = np.where(df['Last_Working_Date'].isnull(), 0, 1)

    df = df.drop(columns=["Year_of_join", "Month_of_join",
                 "Day_of_join", "Year_of_leave", "Month_of_leave"])

    return df


def remove_duplicates_and_fill_na(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates("Emp_ID", keep="last")
    df["Last_Working_Date"] = df["Last_Working_Date"].fillna(datetime(2017, 12, 31), inplace=False)

    return df
