from dash import dcc, html
import plotly.graph_objects as go

def render_tab(df):
    # Layout zakładki "Sprzedaż globalna"
    layout = html.Div([
        # Nagłówek
        html.H1('Sprzedaż globalna', style={'text-align': 'center'}),
        
        # Widget do wyboru zakresu dat
        html.Div([
            dcc.DatePickerRange(
                id='sales-range',
                start_date=df['tran_date'].min(),
                end_date=df['tran_date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '100%', 'text-align': 'center', 'margin-bottom': '20px'}),
        
        # Wykresy: słupkowy i mapa obok siebie
        html.Div([
            html.Div([dcc.Graph(id='bar-sales')], style={'width': '50%'}),
            html.Div([dcc.Graph(id='choropleth-sales')], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    
    return layout
