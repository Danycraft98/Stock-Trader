from data import *
import pandas as pd
import numpy as np

comp = "GOOGL"

#data = get_stock_data("AAPL")
data = get_stock_data(comp, 2)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None) # Adjust width to prevent line wrapping for long rows
pd.set_option('display.max_colwidth', None) # Display full content of each cell
print(data[["MA5", "MA10", "RSI", "ADX", "Buy", "Sell", "Buy2", "Sell2"]].tail(120))

draw_graph(data, comp)