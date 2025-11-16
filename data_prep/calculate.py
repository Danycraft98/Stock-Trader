import pandas as pd
import numpy as np


def calculate_adx(data):
    # Calculate ADX (Average Directional Index)
    window = 14
    high = data['High']
    low = data['Low']
    close = data['Close']

    # True Range
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0).flatten()
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0).flatten()

    # Smoothed averages
    tr14 = tr.rolling(window).sum()
    plus_dm14 = pd.Series(plus_dm, index=data.index).rolling(window).sum()
    minus_dm14 = pd.Series(minus_dm, index=data.index).rolling(window).sum()

    plus_di = 100 * plus_dm14 / tr14.replace(0, np.nan)
    minus_di = 100 * minus_dm14 / tr14.replace(0, np.nan)

    adx = pd.Series(abs(plus_di - minus_di) / (plus_di + minus_di) * 100).rolling(window).mean()
    data["ADX"] = adx


def calculate_rsi(data):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    window = 14

    # EMA of gains and losses, min_periods=1 avoids empty arrays
    avg_gain = gain.ewm(alpha=1/window, min_periods=1).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))
    data["RSI"].fillna(50)


def calculate_last_rsi(data):
    window_length = 14

    # Take last 15 closing prices (14 periods + today)
    last_close = data['Close'].iloc[-(window_length+1):]

    # Price differences
    delta = last_close.diff().dropna()

    # Gains and losses
    gain = delta.clip(lower=0).mean()
    loss = -delta.clip(upper=0).mean()

    # RS and RSI
    RS = gain / loss if loss != 0 else 0
    RSI_next = 100 - (100 / (1 + RS))
    return RSI_next


def calculate_macd(data):
    # Assuming 'data' has a 'Close' column
    fast_ema = data['Close'].ewm(span=12, adjust=False).mean()
    slow_ema = data['Close'].ewm(span=26, adjust=False).mean()

    data['MACD'] = fast_ema - slow_ema
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Hist'] = data['MACD'] - data['Signal']

def calculate_last_macd(data):
    # Parameters
    fast_span = 12
    slow_span = 26
    signal_span = 9

    # Use all available closing prices (or at least slow_span + signal_span)
    ema_fast = data['Close'].ewm(span=fast_span, adjust=False).mean().iloc[-1]
    ema_slow = data['Close'].ewm(span=slow_span, adjust=False).mean().iloc[-1]

    MACD_next = ema_fast - ema_slow
    return MACD_next