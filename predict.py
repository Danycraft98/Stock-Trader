import numpy as np
import mplfinance as mpf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from data_prep.calculate import *


def predict_proj(data):
    # Label: 1 = tomorrow goes up, 0 = down
    data["Target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)
    data = data.dropna(subset=['MA5', 'MA10'])
    calculate_macd(data)

    X = data[["Return", "MA5", "MA10", "RSI", "MACD"]]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("Accuracy:", model.score(X_test, y_test))

    MA5 = data['Close'][-5:].mean()
    MA10 = data['Close'][-10:].mean()
    RSI = calculate_last_rsi(data)
    MACD = calculate_last_macd(data)

    # Return (percent change from yesterday)
    Return = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]
    X_next = np.array([[Return, MA5, MA10, RSI, MACD]]) 

    prediction_prob = model.predict_proba(X_next)
    print(prediction_prob)