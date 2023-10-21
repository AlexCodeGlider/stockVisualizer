from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from flask_caching import Cache
import yfinance as yf
import plotly.graph_objects as go
import talib
import pandas as pd
from app import app

app.title = 'Trading View'

# Load the CSV data into a pandas DataFrame with ISO-8859-1 encoding
df = pd.read_csv('data/SPY_tickers.csv')

# Create the tickers_data dictionary
tickers_data = {row['Symbol']: row['Security'] for _, row in df.iterrows()}

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

cache.clear()

@cache.memoize(timeout=3600)  # Cache data for 1 hour
def fetch_data(ticker):
    df = yf.download(ticker)
    df['SMA50'] = talib.SMA(df['Close'], timeperiod=50)
    df['SMA200'] = talib.SMA(df['Close'], timeperiod=200)
    df['EMA50'] = talib.EMA(df['Close'], timeperiod=50)
    df['EMA200'] = talib.EMA(df['Close'], timeperiod=200)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['Signal Line'], _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['Upper Band'], df['Middle Band'], df['Lower Band'] = talib.BBANDS(df['Close'], timeperiod=20)
    df['SlowK'], df['SlowD'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['FastK'], df['FastD'] = talib.STOCHF(df['High'], df['Low'], df['Close'], fastk_period=5, fastd_period=3, fastd_matype=0)
    df['WILLR'] = talib.WILLR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['MOM'] = talib.MOM(df['Close'], timeperiod=10)
    df['OBV'] = talib.OBV(df['Close'], df['Volume'])
    df['ROC'] = talib.ROC(df['Close'], timeperiod=10)
    df['CCI'] = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    df['AD'] = talib.AD(df['High'], df['Low'], df['Close'], df['Volume'])
    df['OBV'] = talib.OBV(df['Close'], df['Volume'])
    df['HT_TRENDLINE'] = talib.HT_TRENDLINE(df['Close'])
    df['LEAD SINE'], df['SINE'] = talib.HT_SINE(df['Close'])
    return df

# List of indicators for the checklist
indicator_list = [
    'SMA50', 'SMA200', 'EMA50', 'EMA200', 'RSI', 'MACD', 'Signal Line', 'Upper Band', 'Middle Band', 
    'Lower Band', 'SlowK', 'SlowD', 'ADX', 'MOM', 'OBV', 'ROC', 'CCI', 'ATR', 'TRANGE'
]

indicator_descriptions = {
    'SMA50': [
        html.Strong('SMA50 (Simple Moving Average - 50 days):'),
        html.Br(),
        html.Strong('Meaning:'), " It's an average of the past 50 closing prices.",
        html.Br(),
        html.Strong('Use:'), " Helps to identify potential support or resistance levels and to gauge the overall trend over a short-medium timeframe."
    ],
    'SMA200': [
        html.Strong('SMA200 (Simple Moving Average - 200 days):'),
        html.Br(),
        html.Strong('Meaning:'), " It's an average of the past 200 closing prices.",
        html.Br(),
        html.Strong('Use:'), " Used to gauge the overall trend over a longer timeframe. It's often compared with SMA50 to identify golden/death crosses."
    ],
    'EMA50': [
        html.Strong('EMA50 (Exponential Moving Average - 50 days):'),
        html.Br(),
        html.Strong('Meaning:'), " It's an exponentially weighted average of the past 50 closing prices.",
        html.Br(),
        html.Strong('Use:'), " Helps to identify potential support or resistance levels and to gauge the overall trend over a short-medium timeframe."
    ],
    'EMA200': [
        html.Strong('EMA200 (Exponential Moving Average - 200 days):'),
        html.Br(),
        html.Strong('Meaning:'), " It's an exponentially weighted average of the past 200 closing prices.",
        html.Br(),
        html.Strong('Use:'), " Used to gauge the overall trend over a longer timeframe. It's often compared with EMA50 to identify golden/death crosses."
    ],
    'RSI': [
        html.Strong('RSI (Relative Strength Index):'),
        html.Br(),
        html.Strong('Meaning:'), " Momentum oscillator that measures the speed and change of price movements, with values ranging between 0 and 100.",
        html.Br(),
        html.Strong('Use:'), " A value above 70 suggests overbought conditions, while below 30 indicates oversold conditions."
    ],
    'MACD': [
        html.Strong('MACD (Moving Average Convergence Divergence):'),
        html.Br(),
        html.Strong('Meaning:'), " A trend-following momentum indicator showing the relationship between two moving averages of a security’s price.",
        html.Br(),
        html.Strong('Use:'), " Used to identify potential buy/sell signals. When the MACD crosses above the signal line, it's a bullish sign, and vice versa."
    ],
    'Signal Line': [
        html.Strong('Signal Line:'),
        html.Br(),
        html.Strong('Meaning:'), " A moving average of the MACD.",
        html.Br(),
        html.Strong('Use:'), " Used in conjunction with MACD to trigger trading signals."
    ],
    'Upper Band': [
        html.Strong('Upper Band, Middle Band, Lower Band (Bollinger Bands):'),
        html.Br(),
        html.Strong('Meaning:'), " The middle band is an SMA, while the upper and lower bands are standard deviations away from the middle band.",
        html.Br(),
        html.Strong('Use:'), " Measures volatility. Prices are considered high at the upper band and low at the lower band."
    ],
    'Middle Band': [
        html.Strong('Upper Band, Middle Band, Lower Band (Bollinger Bands):'),
        html.Br(),
        html.Strong('Meaning:'), " The middle band is an SMA, while the upper and lower bands are standard deviations away from the middle band.",
        html.Br(),
        html.Strong('Use:'), " Measures volatility. Prices are considered high at the upper band and low at the lower band."
    ],
    'Lower Band': [
        html.Strong('Upper Band, Middle Band, Lower Band (Bollinger Bands):'),
        html.Br(),
        html.Strong('Meaning:'), " The middle band is an SMA, while the upper and lower bands are standard deviations away from the middle band.",
        html.Br(),
        html.Strong('Use:'), " Measures volatility. Prices are considered high at the upper band and low at the lower band."
    ],
    'SlowK': [
        html.Strong('SlowK and SlowD (Stochastic Oscillator):'),
        html.Br(),
        html.Strong('Meaning:'), " Momentum indicators comparing a particular closing price to a range of prices over a certain period. SlowK is the stochastic value, and SlowD is a moving average of SlowK.",
        html.Br(),
        html.Strong('Use:'), " Used to identify overbought and oversold conditions."
    ],
    'SlowD': [
        html.Strong('SlowK and SlowD (Stochastic Oscillator):'),
        html.Br(),
        html.Strong('Meaning:'), " Momentum indicators comparing a particular closing price to a range of prices over a certain period. SlowK is the stochastic value, and SlowD is a moving average of SlowK.",
        html.Br(),
        html.Strong('Use:'), " Used to identify overbought and oversold conditions."
        ],
    'ADX': [
        html.Strong('ADX (Average Directional Index):'),
        html.Br(),
        html.Strong('Meaning:'), " Measures the strength of a trend but not its direction.",
        html.Br(),
        html.Strong('Use:'), " Values above 20-25 indicate a strong trend, while values below 20 suggest a weak trend."
    ],
    'MOM': [
        html.Strong('MOM (Momentum):'),
        html.Br(),
        html.Strong('Meaning:'), " Difference between the current closing price and the closing price a certain number of days ago.",
        html.Br(),
        html.Strong('Use:'), " Used to evaluate the speed or velocity of price change."
    ],
    'OBV': [
        html.Strong('OBV (On-Balance Volume):'),
        html.Br(),
        html.Strong('Meaning:'), " A cumulative indicator that adds volume on up days and subtracts volume on down days.",
        html.Br(),
        html.Strong('Use:'), " Used to confirm price moves. If OBV is rising and the price isn't, it could be an indicator of an upcoming bullish move."
    ],
    'ROC': [
        html.Strong('ROC (Rate of Change):'),
        html.Br(),
        html.Strong('Meaning:'), " Measures the percentage change in price from one period to another.",
        html.Br(),
        html.Strong('Use:'), " Used to identify overbought or oversold conditions."
    ],
    'CCI': [
        html.Strong('CCI (Commodity Channel Index):'),
        html.Br(),
        html.Strong('Meaning:'), " Momentum oscillator used to determine overbought and oversold levels.",
        html.Br(),
        html.Strong('Use:'), " Values above +100 indicate an overbought condition, while values below -100 indicate an oversold condition."
    ],
    'ATR': [
        html.Strong('ATR (Average True Range):'),
        html.Br(),
        html.Strong('Meaning:'), " Measures market volatility. It's the average of the true ranges over a specified period.",
        html.Br(),
        html.Strong('Use:'), " Used to set stop-loss orders or to determine the volatility of a market."
    ],
    'TRANGE': [
        html.Strong('TRANGE (True Range):'),
        html.Br(),
        html.Strong('Meaning:'), " Measures the volatility of a security. It's the greatest of the following: current high less the current low; the absolute value of the current high less the previous close; the absolute value of the current low less the previous close.",
        html.Br(),
        html.Strong('Use:'), " Used in the computation of other indicators like the ATR."
    ]
}

# Common color palette for consistent styling
COLORS = {
    'background': '#34495e',
    'text': '#EAEAEA',
    'control_background': '"#1E1E1E"',
    'border': '#333'
}

# Dropdown styling using the color palette
dropdown_style = {
    'control': {'className': 'dropdown-control'},
    'menu': {'className': 'dropdown-menu'},
    'option': {'className': 'dropdown-option'},
    'singleValue': {'className': 'dropdown-single-value'}
}

navbar = dbc.NavbarSimple(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavItem(
                        dcc.Dropdown(
                            id='stock-input',
                            options=[{'label': f"{name} ({ticker})", 'value': ticker} for ticker, name in tickers_data.items()],
                            value=[
                                'SPY', 
                                'AAPL', 
                                #'MSFT', 
                                #'AMZN', 
                                #'META', 
                                #'GOOG', 
                                #'TSLA'
                                ],
                            multi=True,
                            searchable=True,
                            clearable=False,
                            style=dropdown_style
                        )
                    ), 
                    width=4, 
                    className="mr-0"
                ),  
                dbc.Col(
                    [
                        dbc.NavItem(html.Label('Select Indicators:', style={'color': COLORS['text'], 'marginRight': '10px'})),  
                        dbc.NavItem(
                            dcc.Checklist(
                                id='indicator-checklist',
                                options=[{'label': i, 'value': i} for i in indicator_list],
                                value=['SMA50', 'EMA50', 'Upper Band', 'Middle Band', 'Lower Band'],
                                inline=True,
                                style={
                                    'backgroundColor': COLORS['background'],
                                    'padding': '10px',
                                    'borderRadius': '5px'
                                },
                                inputStyle={'marginRight': '10px', 'cursor': 'pointer'},
                                labelStyle={
                                    'color': COLORS['text'],
                                    'fontSize': '14px',
                                    'cursor': 'pointer'
                                }
                            )
                        )
                    ],
                    width=6, className="ml-0"
                )
            ],
            className="navbar-row"
        )
    ],
    brand="Select tickers and indicators to compare",
    color="#1E1E1E",
    dark=True,
    brand_style={"color": COLORS['text'], "fontSize": "18px"},
    fluid=True,
    className="navbar-simple"
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(id='price-graph-container'), width=12, style={"padding": "20px"}),
                dbc.Col(html.Div(id='price-descriptions'), width=12, style={"padding": "20px"})
            ]
        ),
    ],
    fluid=True,  # Make the container use full width
    className="body-container"
)

layout = html.Div([
    html.Div([
        dcc.Link('Home', href='/', className="menu-font"),
        dcc.Link('Intraday', href='/apps/intradayView', className="menu-font"),
        dcc.Link('Ticker', href='/apps/tickerView', className="menu-font"),
    ], className="top-menu"),

    navbar,

    body,

    dcc.Store(id='xaxis-range')
],
className="body-container"
)

@app.callback(
    [Output('price-graph-container', 'children'),
     Output('xaxis-range', 'data'),
     Output('price-descriptions', 'children')],
    [Input('stock-input', 'value'),
     Input('indicator-checklist', 'value')],
    [State('xaxis-range', 'data')]
)
def update_graph(stock_inputs, selected_indicators, xaxis_range):
    graphs = []
    for stock_input in stock_inputs:
        df = fetch_data(stock_input)
        

        # Create traces based on selected indicators
        traces = []
        if 'SMA50' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['SMA50'], mode='lines', name='SMA50'))
        if 'SMA200' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['SMA200'], mode='lines', name='SMA200'))
        if 'MACD' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD'))
        # ... Add similar conditions for other indicators ...
        if 'Signal Line' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['Signal Line'], mode='lines', name='Signal Line'))
        if 'Upper Band' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['Upper Band'], mode='lines', name='Upper Band'))
        if 'Middle Band' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['Middle Band'], mode='lines', name='Middle Band'))
        if 'Lower Band' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['Lower Band'], mode='lines', name='Lower Band'))
        if 'SlowK' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['SlowK'], mode='lines', name='SlowK'))
        if 'SlowD' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['SlowD'], mode='lines', name='SlowD'))
        if 'ADX' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['ADX'], mode='lines', name='ADX'))
        if 'MOM' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['MOM'], mode='lines', name='MOM'))
        if 'OBV' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['OBV'], mode='lines', name='OBV'))
        if 'ROC' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['ROC'], mode='lines', name='ROC'))
        if 'CCI' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['CCI'], mode='lines', name='CCI'))
        if 'ATR' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['ATR'], mode='lines', name='ATR'))
        if 'TRANGE' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['TRANGE'], mode='lines', name='TRANGE'))
        if 'AD' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['AD'], mode='lines', name='AD'))
        if 'OBV' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['OBV'], mode='lines', name='OBV'))
        if 'HT_TRENDLINE' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['HT_TRENDLINE'], mode='lines', name='HT_TRENDLINE'))
        if 'LEAD SINE' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['LEAD SINE'], mode='lines', name='LEAD SINE'))
        if 'SINE' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['SINE'], mode='lines', name='SINE'))
        if 'EMA50' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['EMA50'], mode='lines', name='EMA50'))
        if 'EMA200' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['EMA200'], mode='lines', name='EMA200'))
        if 'RSI' in selected_indicators:
            traces.append(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'))
        
        price_trace = go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Candlesticks')
        traces.insert(0, price_trace)  # Add candlestick trace as the first trace

        dark_layout = {
            'paper_bgcolor': '#34495e',  # setting the background color of the entire plot
            'plot_bgcolor': '#34495e',  # setting the background color of the plotting area
            'font': {
                'color': '#ecf0f1'  # setting the font color to a light shade
            },
            'yaxis': {
                'gridcolor': '#7f8c8d',  # setting the y-axis grid color
            },
            'xaxis': {
                'gridcolor': '#7f8c8d',  # setting the x-axis grid color
            }
        }

        price_fig = {
            'data': traces,
            'layout': {**dark_layout, **{'title': f'Price: {stock_input}', 'height': 800, 'width': 1400}}
        }
        graphs.append(dcc.Graph(figure=price_fig, id=f'price-graph-{stock_input}'))
    
    graphs_div = html.Div(graphs)

    # Apply the x-axis range to the figure, if available
    if xaxis_range:
        price_fig['layout']['xaxis'] = {'range': xaxis_range}
    
    price_descriptions = [html.P(indicator_descriptions[indicator], style={'color': '#EAEAEA'}) for indicator in selected_indicators]
   
    return graphs_div, xaxis_range, price_descriptions