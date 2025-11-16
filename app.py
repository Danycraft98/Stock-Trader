import os
import pandas as pd
import yfinance as yf
from flask import Flask, render_template, request, url_for


from data_prep.data import *
from predict import *


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    comp = request.form.get("ticker", "AAPL")
    
    # Default ticker and period
    comp = request.form.get("ticker", "AAPL")
    period = request.form.get("period", "2")
    data = get_stock_data(comp, int(period))

    # File path for saving plot
    plot_file = f"static/plots/{comp}.png"
    draw_graph(data, comp, plot_file)
    predict_proj(data)
    return render_template("index.html", plot_url=plot_file, ticker=comp, period=period)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)