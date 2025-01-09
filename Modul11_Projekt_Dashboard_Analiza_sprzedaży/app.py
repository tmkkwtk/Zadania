import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import datetime as dt
import os
import plotly.graph_objects as go
import tab1
import tab2
import tab3  # Import zakładki "Kanały sprzedaży"

# Klasa do obsługi danych
class db:
    def __init__(self):
        self.transactions = self.transaction_init()
        self.cc = pd.read_csv('db/country_codes.csv', index_col=0)
        self.customers = pd.read_csv('db/customers.csv', index_col=0)
        self.prod_info = pd.read_csv('db/prod_cat_info.csv')

    @staticmethod
    def transaction_init():
        transactions_list = []  # Lista do przechowywania danych
        src = 'db/transactions'
        for filename in os.listdir(src):
            transactions_list.append(pd.read_csv(os.path.join(src, filename), index_col=0))

        # Łączenie danych w jedną ramkę danych
        transactions = pd.concat(transactions_list, ignore_index=True)

        # Konwersja dat
        def convert_dates(x):
            try:
                return dt.datetime.strptime(x, '%d-%m-%Y')
            except:
                return dt.datetime.strptime(x, '%d/%m/%Y')

        transactions['tran_date'] = transactions['tran_date'].apply(convert_dates)
        transactions['day_of_week'] = transactions['tran_date'].dt.day_name()  # Dodanie kolumny z dniem tygodnia
        return transactions

    def merge(self):
        df = self.transactions.join(
            self.prod_info.drop_duplicates(subset=['prod_cat_code'])
            .set_index('prod_cat_code')['prod_cat'], on='prod_cat_code', how='left'
        )
        df = df.join(
            self.prod_info.drop_duplicates(subset=['prod_sub_cat_code'])
            .set_index('prod_sub_cat_code')['prod_subcat'], on='prod_subcat_code', how='left'
        )
        df = df.join(
            self.customers.join(self.cc, on='country_code').set_index('customer_Id'), on='cust_id'
        )
        self.merged = df

# Inicjalizacja bazy danych
df = db()
df.merge()

# Inicjalizacja aplikacji
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Layout aplikacji
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
        dcc.Tab(label='Produkty', value='tab-2'),
        dcc.Tab(label='Kanały sprzedaży', value='tab-3')  # Nowa zakładka
    ]),
    html.Div(id='tabs-content')
])

# Callback do renderowania zawartości zakładek
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.render_tab(df.merged)
    elif tab == 'tab-2':
        return tab2.render_tab(df.merged)
    elif tab == 'tab-3':
        return tab3.render_tab(df.merged)  # Renderowanie nowej zakładki

# Callbacki do zakładki "Sprzedaż globalna"
@app.callback(Output('bar-sales', 'figure'), [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_bar_sales(start_date, end_date):
    truncated = df.merged[(df.merged['tran_date'] >= start_date) & (df.merged['tran_date'] <= end_date)]
    grouped = truncated.groupby([pd.Grouper(key='tran_date', freq='ME'), 'Store_type'])['total_amt'].sum().unstack()
    traces = [go.Bar(x=grouped.index, y=grouped[col], name=col) for col in grouped.columns]
    return go.Figure(data=traces, layout=go.Layout(title='Przychody', barmode='stack'))

@app.callback(Output('choropleth-sales', 'figure'), [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_choropleth_sales(start_date, end_date):
    truncated = df.merged[(df.merged['tran_date'] >= start_date) & (df.merged['tran_date'] <= end_date)]
    grouped = truncated.groupby('country')['total_amt'].sum()
    return go.Figure(data=[go.Choropleth(
        locations=grouped.index, z=grouped.values, locationmode='country names', colorscale='Viridis'
    )], layout=go.Layout(title='Mapa sprzedaży', geo=dict(showframe=False, projection={'type': 'natural earth'})))

# Callback do zakładki "Produkty"
@app.callback(Output('barh-prod-subcat', 'figure'), [Input('prod_dropdown', 'value')])
def tab2_barh_prod_subcat(chosen_cat):
    grouped = df.merged[df.merged['prod_cat'] == chosen_cat].pivot_table(
        index='prod_subcat', columns='Gender', values='total_amt', aggfunc='sum'
    ).assign(_sum=lambda x: x.sum(axis=1)).sort_values(by='_sum')
    traces = [go.Bar(x=grouped[col], y=grouped.index, name=col, orientation='h') for col in ['F', 'M']]
    return go.Figure(data=traces, layout=go.Layout(barmode='stack'))

if __name__ == '__main__':
    app.run_server(debug=True)
