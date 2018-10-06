import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir="data/"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if '^BVSP' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, '^BVSP')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol),
                              index_col='Date',
                              parse_dates=True,
                              usecols=['Date', 'Adj Close'],
                              na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        df = df.dropna(subset=[symbol])
        df[symbol] = df[symbol].astype(np.float64)

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=18, figsize=(30, 20))
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)
    plt.show()


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # Note: Returned DataFrame must have the same number of rows
    # daily_returns = df.copy()
    # daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0, :] = 0  # set daily returns for row 0 to 0
    return daily_returns


def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.Series.rolling(values, window=window).mean()


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.Series.rolling(values, window=window).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


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
