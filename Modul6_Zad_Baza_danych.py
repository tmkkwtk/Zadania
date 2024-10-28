import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

stations_df = pd.read_csv('clean_stations.csv')
measure_df = pd.read_csv('clean_measure.csv')

engine = create_engine('sqlite:///weather_data.db')
metadata = MetaData()

stations_table = Table('stations', metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       *[Column(col, String if stations_df[col].dtype == 'O' else Float) 
                         for col in stations_df.columns])

measure_table = Table('measure', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      *[Column(col, String if measure_df[col].dtype == 'O' else Float) 
                        for col in measure_df.columns])

metadata.create_all(engine)

stations_df.to_sql('stations', con=engine, if_exists='replace', index=False)
measure_df.to_sql('measure', con=engine, if_exists='replace', index=False)

with engine.connect() as conn:
    result = conn.execute("SELECT * FROM stations LIMIT 5").fetchall()

print(result)
