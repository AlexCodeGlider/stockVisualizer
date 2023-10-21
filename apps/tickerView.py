import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from flask_caching import Cache
import glob
from app import app

# Function to process the data
def process_data(filepath, data_type):
    print(f'Processing {filepath}...')
    try:
        data = pd.read_csv(filepath, header=None, delimiter=',')
    except pd.errors.ParserError:
        data = pd.read_csv(filepath, header=None, delimiter=',', engine='python')
    
    if data_type == "trade":
        columns = ['timestamp', 'price', 'volume', 'exchange_code', 'trade_conditions']
    elif data_type == "quote":
        columns = ['timestamp', 'bid_price', 'bid_volume', 'bid_exchange', 'offer_price', 'offer_volume', 'offer_exchange']
    
    data.columns = columns
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    return data

# Load and process datasets using glob
data_dict = {}
filepaths = glob.glob('data/firstratedata_tick_bundle_sample/*.txt')

for filepath in filepaths:
    print(f'Processing {filepath}...')
    ticker = filepath.split('/')[-1].split('_')[0].upper() # Assuming filenames are in the format: 'ticker_dataType_date.txt'
    data_type = filepath.split('/')[-1].split('_')[1]
    
    if ticker not in data_dict:
        data_dict[ticker] = {}
    
    data_dict[ticker][data_type] = process_data(filepath, data_type)

tickers = list(data_dict.keys())

# Set up caching
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# Clear the cache directory on start (optional)
cache.clear()

# Define the app layout
layout = html.Div([
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value='MSFT',
        clearable=False
    ),
    dcc.Graph(id='quote-graph'),
    dcc.Graph(id='trade-graph')
])

@cache.memoize(timeout=60*60*24)  # Cache results for 1 day
@app.callback(
    [Output('quote-graph', 'figure'),
     Output('trade-graph', 'figure')],
    [Input('ticker-dropdown', 'value')]
)

def update_graphs(selected_ticker):
    # Quote data
    data_quote = data_dict[selected_ticker]['quote']
    
    # Define figure for quote data using dictionaries
    figure_quote = {
        'data': [
            {
                'type': 'scatter',
                'x': data_quote['timestamp'],
                'y': data_quote['bid_price'],
                'mode': 'lines',
                'name': 'Bid Prices'
            },
            {
                'type': 'scatter',
                'x': data_quote['timestamp'],
                'y': data_quote['offer_price'],
                'mode': 'lines',
                'name': 'Offer Prices',
                'line': {'dash': 'dash'}
            }
        ],
        'layout': {
            'title': f'{selected_ticker} Quote Data (Bid and Offer Prices)',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Price'},
            'legend': {'x': 0, 'y': 1.0}
        }
    }

    # Trade data
    data_trade = data_dict[selected_ticker]['trade']
    
    # Define figure for trade data using dictionaries
    figure_trade = {
        'data': [
            {
                'type': 'scatter',
                'x': data_trade['timestamp'],
                'y': data_trade['price'],
                'mode': 'lines',
                'name': 'Trade Prices',
                'line': {'width': 2},
                'yaxis': 'y1'  # Explicitly set to use the left y-axis for trade prices
            },
            {
                'type': 'bar',
                'x': data_trade['timestamp'],
                'y': data_trade['volume'],
                'name': 'Volume',
                'opacity': 0.6,
                'yaxis': 'y2'  # Explicitly set to use the right y-axis for volume
            }
        ],
        'layout': {
            'title': f'{selected_ticker} Trade Data',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {
                'title': 'Trade Price',
                'side': 'left',  # Set to appear on left side of the plot
                'range': [min(data_trade['price']) - 10, max(data_trade['price']) + 10]  # Adjust the padding as needed
            },
            'yaxis2': {
                'title': 'Volume',
                'side': 'right',  # Set to appear on right side of the plot
                'overlaying': 'y',  # Ensure this axis is overlaying the first y-axis
                'showgrid': False  # Removes the secondary grid lines to reduce clutter
            },
            'legend': {'x': 0, 'y': 1.0}
        }
    }


    return figure_quote, figure_trade
