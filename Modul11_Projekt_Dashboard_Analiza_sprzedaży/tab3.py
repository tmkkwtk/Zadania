from dash import dcc, html
import plotly.graph_objects as go

def render_tab(df):
    # Grupowanie danych wg dnia tygodnia i kanału sprzedaży
    grouped_days = df.groupby(['day_of_week', 'Store_type'])['total_amt'].sum().unstack()

    # Tworzenie wykresu słupkowego (sprzedaż w dniach tygodnia dla kanałów sprzedaży)
    traces_days = [go.Bar(x=grouped_days.index, y=grouped_days[col], name=col) for col in grouped_days.columns]
    fig_days = go.Figure(data=traces_days, layout=go.Layout(
        title="Sprzedaż w dniach tygodnia",
        barmode='group',
        xaxis=dict(title='Dzień tygodnia'),
        yaxis=dict(title='Sprzedaż (kwota)')
    ))

    # Grupowanie danych o klientach wg kanału sprzedaży i płci
    grouped_customers = df.groupby(['Store_type', 'Gender'])['cust_id'].nunique().unstack()
    traces_customers = [go.Bar(x=grouped_customers.index, y=grouped_customers[col], name=col) for col in grouped_customers.columns]
    fig_customers = go.Figure(data=traces_customers, layout=go.Layout(
        title="Klienci wg płci i kanałów sprzedaży",
        barmode='group',
        xaxis=dict(title='Kanał sprzedaży'),
        yaxis=dict(title='Liczba unikalnych klientów')
    ))

    # Layout zakładki "Kanały sprzedaży"
    layout = html.Div([
        # Nagłówek
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
        
        # Wykres słupkowy: Sprzedaż w dniach tygodnia
        html.Div([
            dcc.Graph(id='days-sales', figure=fig_days)
        ], style={'width': '100%', 'margin-bottom': '40px'}),
        
        # Wykres słupkowy: Klienci wg płci i kanałów sprzedaży
        html.Div([
            dcc.Graph(id='channel-customers', figure=fig_customers)
        ], style={'width': '100%'})
    ])
    
    return layout
