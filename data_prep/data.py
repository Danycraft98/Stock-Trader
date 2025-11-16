import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
from datetime import date, timedelta

from .calculate import *

__all__ = ["get_stock_data", "draw_graph", "generate_signal_data"]


def get_n_year(curr_date, n):
    today = date.today()
    mmdd = curr_date.strftime("%m-%d")
    if mmdd == "02-29" and n % 4 != 0:
        mmdd = "02-28"
    return "{}-{}".format(today.year-n, mmdd)


def get_stock_data(comp, n=1):
    # Retrieve n years worth of data
    today = date.today()
    str_today = today.strftime("%Y-%m-%d")
    str_past = get_n_year(today, n)
    data = yf.download(comp, start=str_past, end=str_today)
    data = data.xs(comp, level=1, axis=1)
    print()

    # Get 5-day and 10-day moving average
    data["Return"] = data["Close"].pct_change()
    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA10"] = data["Close"].rolling(10).mean()

    
    calculate_adx(data)
    calculate_rsi(data)

    generate_signal_data(data)
    return data

"""
When MA5 crosses above MA10 → Buy signal

When MA5 crosses below MA10 → Sell signal
"""



def generate_signal_data(data):
    data['Buy'] = np.nan
    data['Sell'] = np.nan

    buy_cond = (data['MA5'] > data['MA10']) & (data['MA5'].shift(1) <= data['MA10'].shift(1))
    sell_cond = (data['MA5'] < data['MA10']) & (data['MA5'].shift(1) >= data['MA10'].shift(1))

    data['Buy'] = np.where(buy_cond, data['Close'], np.nan)
    data['Sell'] = np.where(buy_cond, data['Close'], np.nan)

    # ------------------------
    data['Buy2'] = np.nan
    data['Sell2'] = np.nan

    threshold = 20
    data['Buy2'] = np.where(buy_cond & (data['ADX'] > threshold), data['Close'], np.nan)
    data['Sell2'] = np.where(sell_cond & (data['ADX'] > threshold), data['Close'], np.nan)



def draw_graph(data, comp, plot_file="test.png"):
    data = data
    
    # Flatten the data if necessary
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    apds = [
        mpf.make_addplot(data['Buy'], type='scatter', markersize=100, marker='^', color='green'),
        mpf.make_addplot(data['Sell'], type='scatter', markersize=100, marker='v', color='red'),
        mpf.make_addplot(data['Buy2'], type='scatter', markersize=100, marker='^', color='blue'),
        mpf.make_addplot(data['Sell2'], type='scatter', markersize=100, marker='v', color='orange')
    ]
    
    mpf.plot(
        data,
        addplot=apds,
        type='candle',
        mav=(5, 10),            # MA5 and MA10
        volume=True,            # show volume bars
        title=f"{comp} Stock Chart with Buy/Sell Signals",
        style='yahoo',        # you can change style: 'charles', 'yahoo', 'nightclouds'
        figsize=(12, 8),
        savefig=plot_file
    )