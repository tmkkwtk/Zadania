import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import json

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

# Standaryzacja cech numerycznych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział danych na zbiory treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Budowa i optymalizacja modelu Random Forest
model = RandomForestClassifier(random_state=42)
siatka_parametrow = {
    'n_estimators': [100, 200, 500],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}
wyszukiwanie_siatki = GridSearchCV(model, siatka_parametrow, cv=3, scoring='roc_auc', verbose=2, n_jobs=-1)
wyszukiwanie_siatki.fit(X_train, y_train)

# Zapis najlepszego modelu
najlepszy_model = wyszukiwanie_siatki.best_estimator_
joblib.dump(najlepszy_model, 'model_karta_kredytowa.pkl')

# Wyliczanie metryk na zbiorze treningowym
y_train_pred = najlepszy_model.predict(X_train)
y_train_pred_proba = najlepszy_model.predict_proba(X_train)[:, 1]
roc_auc_train = roc_auc_score(y_train, y_train_pred_proba)
raport_train = classification_report(y_train, y_train_pred, output_dict=True)

# Zapis metryk treningowych do pliku JSON
training_metrics = {
    'roc_auc': roc_auc_train,
    'accuracy': raport_train['accuracy'],
    'precision': raport_train['1']['precision'],
    'recall': raport_train['1']['recall'],
    'f1_score': raport_train['1']['f1-score']
}

with open('training_metrics.json', 'w') as f:
    json.dump(training_metrics, f)

print("Model został wytrenowany i zapisany jako model_karta_kredytowa.pkl")
print("Metryki treningowe zostały zapisane w pliku training_metrics.json")
