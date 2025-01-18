import os
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import subprocess
import json

# Ścieżka do pliku modelu
model_path = 'model_karta_kredytowa.pkl'
training_metrics_path = 'training_metrics.json'

# Sprawdź, czy model istnieje, jeśli nie, uruchom skrypt trenowania
if not os.path.exists(model_path):
    print("Model nie istnieje. Rozpoczynam trenowanie...")
    subprocess.run(['python', 'train_model.py'], check=True)

# Wczytaj zapisany model
najlepszy_model = joblib.load(model_path)

# Wczytaj metryki treningowe
if os.path.exists(training_metrics_path):
    with open(training_metrics_path, 'r') as f:
        training_metrics = json.load(f)
else:
    training_metrics = {}

# Wczytaj dane
plik_danych = 'default_of_credit_card_clients.xls'
dane = pd.read_excel(plik_danych, header=1)
dane.rename(columns={dane.columns[0]: "ID"}, inplace=True)

# Przygotowanie danych
X = dane.drop(columns=['ID', 'default payment next month'])
y = dane['default payment next month']

# Obsługa zmiennych kategorycznych
kolumny_kat = ['SEX', 'EDUCATION', 'MARRIAGE']
X = pd.get_dummies(X, columns=kolumny_kat, drop_first=True)

# Pobierz nazwy cech użytych do trenowania modelu
feature_names = X.columns

# Upewnij się, że dane do predykcji mają te same kolumny w tej samej kolejności
X = X[feature_names]

# Predykcja na pełnym zbiorze
y_pred = najlepszy_model.predict(X)
y_pred_proba = najlepszy_model.predict_proba(X)[:, 1]

# Wyliczanie metryk
tablica_pomyłek = confusion_matrix(y, y_pred)
raport = classification_report(y, y_pred, output_dict=True)
roc_auc = roc_auc_score(y, y_pred_proba)

# Wyliczanie korelacji
dane_korelacje = dane.corr()

# Dashboard
aplikacja = Dash(__name__)

aplikacja.layout = html.Div([
    html.H1('Model Przyznawania Kart Kredytowych', style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Przegląd danych', children=[
            html.H3('Dane źródłowe', style={'textAlign': 'center'}),
            dash_table.DataTable(
                data=dane.to_dict('records'),
                page_size=20,
                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '500px'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
            )
        ]),
        dcc.Tab(label='Wyniki modelu', children=[
            html.H3('Podsumowanie Wyników Modelu', style={'textAlign': 'center'}),
            html.Div([
                html.H4('Opis modelu:', style={'marginTop': '20px'}),
                html.P("Model użyty do predykcji to Random Forest Classifier, który jest wszechstronnym modelem klasyfikacyjnym bazującym na zbiorze drzew decyzyjnych. Optymalizacja została przeprowadzona za pomocą GridSearchCV."),
                html.H4('Parametry najlepszego modelu:', style={'marginTop': '20px'}),
                html.Pre(
                    '\n'.join([f'{k}: {v}' for k, v in najlepszy_model.get_params().items()]),
                    style={
                        'whiteSpace': 'pre-wrap',
                        'backgroundColor': '#f9f9f9',
                        'padding': '10px',
                        'border': '1px solid #ddd',
                        'borderRadius': '5px'
                    }
                ),
                html.H4('Metryki modelu treningowego:', style={'marginTop': '20px'}),
                html.Div([
                    html.P(f"ROC AUC (trening): {training_metrics.get('roc_auc', 'Brak danych'):.4f}"),
                    html.P(f"Dokładność (trening): {training_metrics.get('accuracy', 'Brak danych'):.4f}"),
                    html.P(f"Precyzja (1) (trening): {training_metrics.get('precision', 'Brak danych'):.4f}"),
                    html.P(f"Czułość (1) (trening): {training_metrics.get('recall', 'Brak danych'):.4f}"),
                    html.P(f"F1-score (1) (trening): {training_metrics.get('f1_score', 'Brak danych'):.4f}")
                ], style={
                    'backgroundColor': '#f9f9f9',
                    'padding': '10px',
                    'border': '1px solid #ddd',
                    'borderRadius': '5px',
                    'marginBottom': '20px'
                }),
                html.H4('Metryki modelu testowego:', style={'marginTop': '20px'}),
                html.Div([
                    html.P(f"ROC AUC (test): {roc_auc:.4f}"),
                    html.P(f"Dokładność (test): {raport['accuracy']:.4f}"),
                    html.P(f"Precyzja (1) (test): {raport['1']['precision']:.4f}"),
                    html.P(f"Czułość (1) (test): {raport['1']['recall']:.4f}"),
                    html.P(f"F1-score (1) (test): {raport['1']['f1-score']:.4f}")
                ], style={
                    'backgroundColor': '#f9f9f9',
                    'padding': '10px',
                    'border': '1px solid #ddd',
                    'borderRadius': '5px',
                    'marginBottom': '20px'
                }),
                dcc.Graph(
                    figure=px.imshow(
                        tablica_pomyłek,
                        labels=dict(x="Predykcja", y="Rzeczywiste", color="Liczba"),
                        x=['Brak domyślności', 'Domyślność'],
                        y=['Brak domyślności', 'Domyślność'],
                        title='Macierz pomyłek',
                        color_continuous_scale='Blues'
                    )
                ),
                dcc.Graph(
                    figure=px.histogram(
                        pd.DataFrame({'Prawdopodobieństwo Predykcji': y_pred_proba, 'Rzeczywista': y}),
                        x='Prawdopodobieństwo Predykcji',
                        color='Rzeczywista',
                        title='Rozkład prawdopodobieństw predykcji',
                        nbins=50
                    )
                )
            ])
        ]),
        dcc.Tab(label='Analiza korelacji', children=[
            html.H3('Korelacje między zmiennymi', style={'textAlign': 'center'}),
            dcc.Graph(
                figure=px.imshow(
                    dane_korelacje,
                    title='Mapa korelacji zmiennych',
                    labels=dict(color="Współczynnik korelacji"),
                    color_continuous_scale='Viridis'
                )
            )
        ])
    ])
])

if __name__ == '__main__':
    aplikacja.run_server(debug=True)
