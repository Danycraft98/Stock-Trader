# Stock Trader

**Stock Trader** is a web application built with **Flask** that predicts stock prices and visualizes them with financial charts. Users can input stock tickers and parameters, and see predictions and plots in an interactive dashboard.

---

## **Features**

- Predict future stock prices using historical data
- Display financial charts with candlesticks and volume using **mplfinance**
- Interactive sidebar to select:
  - Stock ticker
  - Prediction parameters (e.g., moving averages or forecast horizon)
- Simple, responsive web interface built with **Bootstrap**

---

## **Requirements**

- Python 3.10+
- Flask
- Pandas
- mplfinance
- yfinance (for historical stock data)  
- numpy
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally

Follow these steps to run Stock Trader on your local machine:

1. Clone the repository:

```
git clone <your-repo-url>
cd stock_trader
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3.Run the Flask app:

```
python app.py
```

4. Open your browser and go to:

http://127.0.0.1:5000/


5. Use the sidebar to select a stock ticker and parameters to view predictions and charts.


## Deployment

You can deploy Stock Trader using Gunicorn and NGINX, or cloud services like Heroku, Render, or AWS Elastic Beanstalk.

### Example using Gunicorn:

1. Install Gunicorn if not already installed:

```
pip install gunicorn
```

2. Run the app with Gunicorn:

```
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

```-w 4``` → 4 worker processes

```-b 0.0.0.0:8000``` → bind to all network interfaces on port 8000

### Notes

1. Use matplotlib.use('Agg') if running on a server without GUI to avoid threading issues.

2. Ensure static/plots/ exists and has write permissions for saving plots.


## Future Improvements

- Add real-time plot updates without page reload using AJAX

- Allow multiple stock comparisons

- Integrate machine learning models for more advanced predictions

- Deploy on cloud with auto-scaling for multiple users

## Contributing to Stock Trader
To contribute to Stock Trader, follow these steps:

1. Fork this repository.
2. Create a branch: git checkout -b <branch_name>.
3. Make your changes and commit them: git commit -m '<commit_message>'
4. Push to the original branch: git push origin <project_name>/<location>
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License
This project uses the following license: <b>MIT License</b>.