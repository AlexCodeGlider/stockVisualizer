import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app

tickers = [
 'MMM',
 'AOS',
 'ABT',
 'ABBV',
 'ACN',
 'ATVI',
 'AYI',
 'ADBE',
 'ADT',
 'AAP',
 'AMD',
 'AES',
 'AMG',
 'AFL',
 'A',
 'API',
 'AKAM',
 'ALB',
 'AA',
 'ALGN',
 'ATI',
 'ALLE',
 'LNT',
 'ALL',
 'GOOGL',
 'GOOG',
 'ALTR',
 'MO',
 'AMZN',
 'AEE',
 'AAL',
 'AEP',
 'AXP',
 'AIG',
 'AMT',
 'AMP',
 'AME',
 'AMGN',
 'APH',
 'ADI',
 'BUD',
 'APA',
 'AAPL',
 'APTV',
 'ADM',
 'ANET',
 'AJG',
 'ASML',
 'AIZ',
 'T',
 'TEAM',
 'ATO',
 'LIFE',
 'ADSK',
 'ADP',
 'AN',
 'AVB',
 'AVY',
 'BALL',
 'BAC',
 'BAX',
 'BDX',
 'BBBY',
 'BRK.B',
 'BIDU',
 'BIG',
 'BIIB',
 'BLK',
 'BCAT',
 'HRB',
 'BA',
 'BKNG',
 'BWA',
 'BXP',
 'BSX',
 'BMY',
 'AVGO',
 'BR',
 'BC',
 'CDNS',
 'CPB',
 'COF',
 'CAH',
 'KMX',
 'CCL',
 'CARR',
 'CAT',
 'CBOE',
 'CBRE',
 'CDW',
 'CE',
 'COR',
 'CNC',
 'CF',
 'SCHW',
 'CHTR',
 'CC',
 'CVX',
 'CMG',
 'CB',
 'CHD',
 'CIEN',
 'CI',
 'CTAS',
 'CSCO',
 'C',
 'CLF',
 'CME',
 'CMS',
 'KO',
 'CTSH',
 'CL',
 'CMCSA',
 'CMA',
 'CCU',
 'COP',
 'ED',
 'CPRT',
 'GLW',
 'COST',
 'CCI',
 'CCK',
 'CSX',
 'CMI',
 'CVS',
 'DHI',
 'DHR',
 'DVA',
 'DE',
 'DELL',
 'DAL',
 'FANG',
 'DLR',
 'DDS',
 'DFS',
 'DISH',
 'DG',
 'DLTR',
 'DPZ',
 'DOV',
 'DOW',
 'DUK',
 'DD',
 'EMN',
 'EBAY',
 'ECL',
 'EIX',
 'EW',
 'EA',
 'EMR',
 'EOG',
 'EQT',
 'EFX',
 'EQ',
 'EQR',
 'ESS',
 'EL',
 'EG',
 'EVRG',
 'ES',
 'EXC',
 'EXPE',
 'XOM',
 'FFIV',
 'FAST',
 'FDX',
 'FIS',
 'FITB',
 'FSLR',
 'FE',
 'FI',
 'FLEX',
 'FLR',
 'FMC',
 'FL',
 'F',
 'FTNT',
 'FTV',
 'FBHS',
 'FOSL',
 'BEN',
 'FCX',
 'GME',
 'GCI',
 'GPS',
 'GRMN',
 'IT',
 'GD',
 'GE',
 'GIS',
 'GM',
 'GNW',
 'GILD',
 'GPN',
 'GL',
 'GS',
 'GHC',
 'GWW',
 'HAL',
 'HBI',
 'HOG',
 'HIG',
 'HAS',
 'HCA',
 'PEAK',
 'HP',
 'HSIC',
 'HES',
 'HPE',
 'HLT',
 'HOLX',
 'HD',
 'HON',
 'HRL',
 'HST',
 'HPQ',
 'HUM',
 'HBAN',
 'HII',
 'IAC',
 'IEX',
 'IDXX',
 'ITW',
 'ILMN',
 'INCY',
 'INFY',
 'IR',
 'INTC',
 'ICE',
 'IBM',
 'IGT',
 'IP',
 'IPG',
 'IFF',
 'INTU',
 'ISRG',
 'IVZ',
 'IPGP',
 'IQV',
 'IRM',
 'JBHT',
 'JKHY',
 'J',
 'JAMF',
 'JD',
 'JEF',
 'SJM',
 'JNJ',
 'JCI',
 'JPM',
 'JNPR',
 'KBH',
 'K',
 'KEY',
 'KEYS',
 'KMB',
 'KIM',
 'KMI',
 'KLAC',
 'KSS',
 'KHC',
 'KR',
 'LHX',
 'LH',
 'LW',
 'LVS',
 'LEG',
 'LDOS',
 'LEN',
 'LBTYK',
 'LLY',
 'LNC',
 'LIN',
 'LKQ',
 'LMT',
 'L',
 'LOGI',
 'LOW',
 'MTB',
 'MAC',
 'M',
 'MTW',
 'MRO',
 'MPC',
 'MMI',
 'MKTX',
 'MAR',
 'MMC',
 'MLM',
 'MRVL',
 'MAS',
 'MA',
 'MAT',
 'MBI',
 'MKC',
 'MCD',
 'MCK',
 'MDT',
 'MELI',
 'MRK',
 'META',
 'MET',
 'MTD',
 'MGM',
 'MCHP',
 'MU',
 'MSFT',
 'MAA',
 'MHK',
 'TAP',
 'MDLZ',
 'MNST',
 'MCO',
 'MS',
 'MSI',
 'MSCI',
 'MUR',
 'NBR',
 'NDAQ',
 'NOV',
 'NAVI',
 'NCNO',
 'NKTR',
 'NTAP',
 'NTES',
 'NFLX',
 'NYT',
 'NWL',
 'NEM',
 'NWSA',
 'NWS',
 'NEE',
 'NKE',
 'NI',
 'NE',
 'JWN',
 'NSC',
 'NTRS',
 'NOC',
 'NLOK',
 'NCLH',
 'NRG',
 'NUE',
 'NVDA',
 'NVR',
 'OXY',
 'ODP',
 'OI',
 'ODFL',
 'OMC',
 'ORCL',
 'ORLY',
 'OTIS',
 'PCAR',
 'PCG',
 'PKG',
 'PH',
 'PDCO',
 'PYPL',
 'BTU',
 'PNR',
 'PEP',
 'PRGO',
 'PFE',
 'PM',
 'PSX',
 'PLL',
 'PDD',
 'PNW',
 'PXD',
 'PBI',
 'PNC',
 'PPG',
 'PPL',
 'PFG',
 'PG',
 'PGR',
 'PLD',
 'PRU',
 'PEG',
 'PSA',
 'PHM',
 'QGEN',
 'QRVO',
 'QCOM',
 'DGX',
 'RRC',
 'RTX',
 'O',
 'REG',
 'REGN',
 'RF',
 'RSG',
 'RMD',
 'RVTY',
 'RHI',
 'ROK',
 'ROL',
 'ROP',
 'ROST',
 'RCL',
 'RPRX',
 'RYAAY',
 'R',
 'SPGI',
 'CRM',
 'SLB',
 'SAIC',
 'SE',
 'SEE',
 'SRE',
 'NOW',
 'SHW',
 'SIG',
 'SPG',
 'SIRI',
 'SWKS',
 'SLG',
 'SNA',
 'SNOW',
 'SO',
 'LUV',
 'SWN',
 'S',
 'SWK',
 'SBUX',
 'STT',
 'SRCL',
 'STE',
 'SYK',
 'SYF',
 'SNPS',
 'SYY',
 'TROW',
 'TTWO',
 'TPR',
 'TGT',
 'TEL',
 'FTI',
 'TGNA',
 'TFX',
 'THC',
 'TDC',
 'TER',
 'TSLA',
 'TEVA',
 'TXN',
 'TXT',
 'BK',
 'CLX',
 'COO',
 'GT',
 'HSY',
 'MOS',
 'DIS',
 'TMO',
 'TJX',
 'TMUS',
 'TSCO',
 'RIG',
 'TRIP',
 'TFC',
 'FOX',
 'TSN',
 'USB',
 'UAA',
 'UA',
 'UNP',
 'UAL',
 'UNH',
 'UPS',
 'URI',
 'X',
 'UHS',
 'UNM',
 'URBN',
 'VFC',
 'VLO',
 'VRSN',
 'VRSK',
 'VZ',
 'VRTX',
 'VIAV',
 'V',
 'VOD',
 'VNO',
 'WRB',
 'WAB',
 'WBA',
 'WMT',
 'WAT',
 'WEC',
 'WFC',
 'WELL',
 'WDC',
 'WU',
 'WY',
 'WDAY',
 'WYNN',
 'XEL',
 'XRX',
 'XYL',
 'YUM',
 'ZBRA',
 'ZBH',
 'ZION',
 'ZTS',
 'ZM'
]

# Function to process the data
def process_data(filepath):
    data = pd.read_csv(filepath)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['20_SMA'] = data['close'].rolling(window=20).mean()
    data['50_SMA'] = data['close'].rolling(window=50).mean()
    data['Middle_Band'] = data['20_SMA']
    data['Upper_Band'] = data['20_SMA'] + 2*data['close'].rolling(window=20).std()
    data['Lower_Band'] = data['20_SMA'] - 2*data['close'].rolling(window=20).std()
    data['20_Volume_SMA'] = data['volume'].rolling(window=20).mean()
    return data

# Load and process datasets for each ticker
data_dict = {}
for ticker in tickers:
    data_dict[ticker] = {
        '5min': process_data(f'data/frd_sample_stock/{ticker}_5min_sample.csv'),
        '1min': process_data(f'data/frd_sample_stock/{ticker}_1min_sample.csv')
    }

# Function to generate normalized heatmap data (Modified to filter columns)
def generate_normalized_heatmap_data(data):
    data['time_of_day'] = data['timestamp'].dt.time
    grouped_data = data[['time_of_day', 'open', 'high', 'low', 'close', 'volume']].groupby('time_of_day').mean().reset_index()
    normalized_data = (grouped_data.set_index('time_of_day') - grouped_data.set_index('time_of_day').min()) / (grouped_data.set_index('time_of_day').max() - grouped_data.set_index('time_of_day').min())
    return normalized_data

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
                            id='intraday-stock-input',
                            options=[{'label': f"({ticker})", 'value': ticker} for ticker in tickers],
                            value=[
                                'AAPL',
                                'MSFT',
                                'AMZN',
                                'META',
                                'GOOG',
                                # 'GOOGL',
                                'TSLA',
                                # 'JNJ',
                                # 'V',
                                # 'PG',
                                # 'JPM',
                            ],
                            multi=True,
                            searchable=True,
                            clearable=False,
                            style=dropdown_style
                        )
                    ), 
                    width=8, 
                    className="mr-0"  # fixed the closing parenthesis
                )
            ],
            className="navbar-row"
        )
    ],
    brand="Intraday Stock Visualizer",
    color="#1E1E1E",
    dark=True,
    brand_style={"color": COLORS['text'], "fontSize": "18px"},
    fluid=True,
    className="navbar-simple"
)

# Define the body layout
body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(id='intraday-price-graph-container'), width=12),
                dbc.Col(html.Div(id='heatmap-container'), width=12)  # Added this for the heatmaps
            ]
        ),
    ],
    style={'backgroundColor': '#34495e'}
)

# Define the app layout
layout = html.Div([
    html.Div([
        dcc.Link('Home', href='/', className="menu-font"),
        dcc.Link('Daily', href='/apps/daily', className="menu-font"),
        dcc.Link('Ticker', href='/apps/tickerView', className="menu-font"),
    ], className="top-menu"),
    navbar, 
    body,
    dcc.Store(id='xaxis-range')  
], style={'backgroundColor': '#34495e'})

@app.callback(
    [Output('intraday-price-graph-container', 'children'),
     Output('heatmap-container', 'children')],
    [Input('intraday-stock-input', 'value')]
)
def update_graphs(selected_tickers):
    container = []  # Single container for both price graphs and heatmaps

    for ticker in selected_tickers:
        # 5-minute graph for the current ticker
        data_5min = data_dict[ticker]['5min']
        figure_5min = {
            'data': [
                go.Scatter(
                    x=data_5min['timestamp'],
                    y=data_5min['close'],
                    mode='lines',
                    name='Closing Prices'
                ),
                go.Bar(
                    x=data_5min['timestamp'],
                    y=data_5min['volume'],
                    name='Volume',
                    yaxis='y2'
                )
            ],
            'layout': go.Layout(
                title=f'{ticker} 5-Minute Closing Prices and Trading Volume',
                xaxis=dict(title='Timestamp'),
                yaxis=dict(title='Closing Price'),
                yaxis2=dict(title='Volume',
                            overlaying='y',
                            side='right'),
                legend=dict(x=0, y=1.0)
            )
        }
        container.append(dcc.Graph(figure=figure_5min))

        # Heatmap for the current ticker
        normalized_data = generate_normalized_heatmap_data(data_5min)
        heatmap_figure = {
            'data': [go.Heatmap(
                z=normalized_data.T.values,
                y=normalized_data.columns,
                x=normalized_data.index,
                colorscale='YlGnBu'
            )],
            'layout': go.Layout(
                title=f'{ticker} Normalized Average Values by Time of Day',
                yaxis=dict(title='Metrics'),
                xaxis=dict(title='Time of Day'),
                height=700
            )
        }
        container.append(dcc.Graph(figure=heatmap_figure))

    return container, []  # Return the container and an empty list for the heatmap container