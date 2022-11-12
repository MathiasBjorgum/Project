from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
try:
    import tikzplotlib
except ImportError:
    tikzplotlib = None


FIG_PATH = Path.cwd().joinpath("figures")


def plot_attrtion_by_group_count(dataset: pd.DataFrame, groupby: str, relative: bool = False, stacked: bool = False, save: bool = True, col_labels: bool = False):
    '''
    Plots attrition counts based on a categorical variable.

    Parameters
    ----------
    dataset: the dataset to get counts from.
    groupby: a string representing the name of the column to group on.
    relative: boolean for choosing if the counts should be displayed in percent
    stacked: boolean for choosing if the chart should be stacked
    save: boolean for choosing if the plot should be saved as a .tex
    col_labels: boolean for choosing if the columns should have the number of counts
    '''

    attrition_0 = dataset.groupby(groupby)['Attrition'].apply(
        lambda x: (x == 0).sum()).reset_index(name='attr = 0')
    attrition_1 = dataset.groupby(groupby)['Attrition'].apply(
        lambda x: (x == 1).sum()).reset_index(name='attr = 1')

    combined = attrition_0.copy()
    combined["attr = 0"] = combined["attr = 0"].astype("int")
    combined["attr = 1"] = attrition_1["attr = 1"].astype("int")

    combined = combined.set_index(pd.Index(combined[groupby]))
    combined = combined.drop(groupby, axis=1)

    if relative:
        combined = combined.div(combined.sum(axis=1), axis=0)

    ax = combined.plot(kind="bar", stacked=stacked,
                       color=['#ff7f0e', '#1f77b4'])
    
    if col_labels:
        ax.bar_label(ax.containers[0])
        ax.bar_label(ax.containers[1])

    if tikzplotlib is None:
        plt.show()
    else:
        tikzplotlib.save(FIG_PATH.joinpath(f"group_by_{groupby}.tex"))