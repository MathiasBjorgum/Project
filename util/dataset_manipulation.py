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

    dataset.City = dataset["City"].replace({"C1": "C01", 
                                                  "C2": "C02", 
                                                  "C3": "C03",
                                                  "C4": "C04",
                                                  "C5": "C05",
                                                  "C6": "C06",
                                                  "C7": "C07",
                                                  "C8": "C08",
                                                  "C9": "C09"})

    return dataset

def create_attrition(df: pd.DataFrame) -> pd.DataFrame:
    '''Creates the `Attrition` column in the dataset'''

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

def create_duration_of_work(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Computes the duration of work. Here we assume that the last working day was
    2017-12-31.
    '''

    df["Last_Working_Date"] = df["Last_Working_Date"].fillna(datetime(2017, 12, 31), inplace=False)
    df["Work_Duration"] = (df.Last_Working_Date - df.Date_Of_Joining).dt.days

    return df


def create_additional_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function aims to create a dummy variable for attrition
    and how long the employee worked at the company in days.\\
    The function also removes duplicate entries.
    '''

    df = create_attrition(df)
    df = create_duration_of_work(df)
    df = df.drop_duplicates("Emp_ID", keep="last")

    return df

def create_categorical_variables(df: pd.DataFrame, create_dummies: bool = True) -> pd.DataFrame:
    '''Creates categorical variables for `Gender`, `City` and `Education_level`'''
    df.Gender = df.Gender.astype("category")
    df.City = df.City.astype("category")
    df.Education_Level = df.Education_Level.astype("category")

    if create_dummies:
        df = pd.get_dummies(df, prefix_sep="_")

    return df

def get_and_process_df(filename: str, create_dummies: bool = True) -> pd.DataFrame:
    '''Combines functions to create and process the dataset'''
    df = get_dataset(filename)
    df = clean_attrition_dataset(df)
    df = create_additional_columns(df)
    df = create_categorical_variables(df, create_dummies)

    return df