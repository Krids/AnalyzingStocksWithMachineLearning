import numpy as np
import pandas as pd


def get_max_close(symbol):
    """Return the maximum closing value for stock indicated by symbol"""

    df = pd.read_csv("data/{}.csv".format(symbol), )  # read in data
    return df['Close'].max()  # Compute and return max


def get_mean_volume(symbol):
    """Return the mean volume value for stock indicated by symbol"""

    df = pd.read_csv("data/{}.csv".format(symbol))
    return df['Volume'].mean()


def test_run():
    """Function called by Test Run."""
    for symbol in ['^BVSP', 'ITSA4.SA', 'BBAS3.SA', 'BBDC4.SA']:
        print("Max close")
        print(symbol, get_max_close(symbol))
