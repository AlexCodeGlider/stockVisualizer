from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
from apps import dailyView as daily
from apps import intradayView as intraday
from apps import tickerView as ticker

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/daily':
        return daily.layout
    elif pathname == '/apps/intraday':
        return intraday.layout
    elif pathname == '/apps/ticker':
        return ticker.layout
    elif pathname == '/':
        return html.Div([
            html.H3("Trade View", style={'marginBottom': '30px'}),
            html.Ul([
                html.Li(dcc.Link('Daily', href='/apps/daily', className='index-link')),
                html.Li(dcc.Link('Intraday', href='/apps/intraday', className='index-link')),
                html.Li(dcc.Link('Ticker', href='/apps/ticker', className='index-link')),
            ], style={'listStyleType': 'none', 'padding': '0'}),
        ], style={'textAlign': 'center', 'paddingTop': '50px'})
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
