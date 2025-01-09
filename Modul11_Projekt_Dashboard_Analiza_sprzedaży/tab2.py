from dash import dcc, html
import plotly.graph_objects as go

def render_tab(df):
    # Grupowanie danych dla wykresu kołowego
    grouped = df[df['total_amt'] > 0].groupby('prod_cat')['total_amt'].sum()
    
    # Tworzenie wykresu kołowego
    pie_fig = go.Figure(
        data=[
            go.Pie(labels=grouped.index, values=grouped.values)
        ],
        layout=go.Layout(title='Udział grup produktów w sprzedaży')
    )

    # Layout zakładki "Produkty"
    layout = html.Div([
        # Nagłówek
        html.H1('Produkty', style={'text-align': 'center'}),
        
        # Dwa wykresy obok siebie: kołowy i poziomy słupkowy
        html.Div([
            # Wykres kołowy
            html.Div([dcc.Graph(id='pie-prod-cat', figure=pie_fig)], style={'width': '50%'}),
            
            # Dropdown + wykres słupkowy
            html.Div([
                dcc.Dropdown(
                    id='prod_dropdown',
                    options=[{'label': prod_cat, 'value': prod_cat} for prod_cat in df['prod_cat'].unique()],
                    value=df['prod_cat'].unique()[0],  # Domyślna wartość
                    placeholder="Wybierz kategorię produktu"
                ),
                dcc.Graph(id='barh-prod-subcat')
            ], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    
    return layout
