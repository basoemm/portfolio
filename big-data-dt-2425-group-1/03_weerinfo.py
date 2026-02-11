# -----------------------------------------------------------------------------
# Snapshots verrijken met weerdata (KNMI Schiphol)
# Berekening over 3 weken vóór elke snapshot:
# - Gemiddelde temperatuur
# - Aantal vorstdagen (min_temp < 0°C)
# - Totale neerslag (regen in mm)
# Resultaat wordt opgeslagen in de tabel 'snapshots_part3'
# -----------------------------------------------------------------------------

import pandas as pd
from database.connection import connection

# Database connectie:
engine = connection() # Oege

# Snapshots ophalen van 02
df_snapshots = pd.read_sql("SELECT * FROM snapshots_part2", con=engine)
df_weer = pd.read_csv('Data/etmgeg_240.txt') # Schiphol data KNMI

# Datum veld naar datetime
df_weer['date'] = pd.to_datetime(df_weer['YYYYMMDD'], format='%Y%m%d')

# Alleen weer data van:
start_date = '1999-12-01'
end_date = '2020-12-31'

# Filter dataframe op start en end date:
df_weer = df_weer[(df_weer['date'] >= start_date) & (df_weer['date'] <= end_date)]

# Temp tussen 0 - 0.05 wordt weergegeven als -1, 0 van maken
df_weer['RH'] = df_weer['RH'].replace(-1, 0)

# Naar hele getallen
df_weer['TN'] = df_weer['TN'] * 0.1 # min_temp
df_weer['TX'] = df_weer['TX'] * 0.1 # max_temp
df_weer['TG'] = df_weer['TG'] * 0.1 # avg_temp
df_weer['RH'] = df_weer['RH'] * 0.1 # regen

# Afronden
df_weer['TN'] = df_weer['TN'].round(1)
df_weer['TX'] = df_weer['TX'].round(1)
df_weer['TG'] = df_weer['TG'].round(1)
df_weer['RH'] = df_weer['RH'].round(1)

# Nieuwe DF van deze velden
selected_columns = ['date', 'TN', 'TX', 'TG', 'RH']
df_selected = df_weer[selected_columns].copy()

# Kolommen hernoemen
df_selected.rename(columns={'TN': 'min_temp'}, inplace=True)
df_selected.rename(columns={'TX': 'max_temp'}, inplace=True)
df_selected.rename(columns={'TG': 'avg_temp'}, inplace=True)
df_selected.rename(columns={'RH': 'rain_amount'}, inplace=True)

# Weer info naar DB:
df_selected.to_sql('weather_info',
                   con=engine,
                   index=False,
                   chunksize=5000,
                   if_exists='fail')


### Duckdb: SQL queries met dataframes :)
import duckdb

# Drie weken voor de snapshot berekenen
df_snapshots['start_date'] = df_snapshots['snapshot'] - pd.Timedelta(days=21)

# Query om gemiddelde temp uit te rekenen
result = duckdb.query("""
    SELECT
        s.snapshot,
        AVG(w.avg_temp) AS avg_temp_3w
    FROM df_snapshots s
    JOIN df_selected w
      ON w.date >= s.start_date AND w.date < s.snapshot
    GROUP BY s.snapshot
""").to_df()

# Merge met df_snapshots
df_snapshots = df_snapshots.merge(result, on='snapshot', how='left')

# Aantal vorstdagen
result_frost = duckdb.query("""
    SELECT
        s.snapshot,
        COUNT(DISTINCT w.date) AS frost_3w
    FROM df_snapshots s
    JOIN df_selected w
      ON w.date >= s.start_date AND w.date < s.snapshot
    WHERE w.min_temp < 0.0
    GROUP BY s.snapshot
""").to_df()

# Merge
df_snapshots = df_snapshots.merge(result_frost, on='snapshot', how='left')
# Geen vorst, 0 invullen
df_snapshots['frost_3w'].fillna(0, inplace=True)

# Regen optellen:
result_rain = duckdb.query("""
    SELECT
        s.snapshot,
        COUNT(DISTINCT w.date) AS frost_3w
    FROM df_snapshots s
    JOIN df_selected w
      ON w.date >= s.start_date AND w.date < s.snapshot
    GROUP BY s.snapshot
""").to_df()

result_rain = result_rain.drop('frost_3w', axis=1)

result_rain['start_date'] = result_rain['snapshot'] - pd.Timedelta(weeks=3)

result_rain = duckdb.query("""
    SELECT
        s.snapshot,
        sum(w.rain_amount) AS rain_3w
    FROM result_rain s
    JOIN df_selected w
      ON w.date >= s.start_date AND w.date < s.snapshot
    GROUP BY s.snapshot
""").to_df()

# Merge
df_snapshots = df_snapshots.merge(result_rain, on='snapshot', how='left')

# Afronden 
df_snapshots['avg_temp_3w'] = df_snapshots['avg_temp_3w'].round(2)
df_snapshots['frost_3w'] = df_snapshots['frost_3w'].round(2)
df_snapshots['rain_3w'] = df_snapshots['rain_3w'].round(2)
df_snapshots['age'] = df_snapshots['age'].round(2)

# Kolommen weggooien die we niet gebruiken
print(df_snapshots.columns)
df_snapshots = df_snapshots.drop('avg_temp_3w_y', axis=1)
df_snapshots = df_snapshots.drop('start_date', axis=1)

# Sorteer op snapshot
df_snapshots = df_snapshots.sort_values('snapshot')

# Wegschrijven naar database
df_snapshots.to_sql('snapshots_part3',
                   con=engine,
                   index=False,
                   chunksize=5000,
                   if_exists='fail'
                   )