from flask import Flask, request, jsonify, render_template
import yfinance as yf
import plotly.graph_objs as go
import plotly
import json
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

def Train(data,symbol = 'AAPL',interval = '1m'):
    # Get live streaming data from Yahoo Finance
    model = ARIMA(data['Close'], order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit

def plot_stock_data(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='OHLC'))
    fig.update_layout(
        title='Stock Chart',
        yaxis_title='Price',
        xaxis_title='Time'
    )
    return fig.to_html(full_html=False)

@app.route('/api')
def index():
    symbol = 'AAPL'
    interval = '1m'
    data = yf.download(tickers=symbol, interval=interval)

    plot_div = plot_stock_data(data)
    model_fit = Train(data=data)
    predictions = model_fit.predict(start=len(data), end=len(data) + 10)

    return render_template('index.html', plot_div=plot_div, data=data.to_html(), predictions=predictions.to_list())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
