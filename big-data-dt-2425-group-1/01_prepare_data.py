# ---------------------------------------------
# Snapshotmodel: leidingen combineren met lekkages per 3 maanden
# ---------------------------------------------
# Dit script haalt leiding- en lekkagedata op uit de OEGE-database,
# maakt snapshots aan voor elke 3 maanden tussen 2000 en 2021,
# koppelt deze aan de leidingen, berekent de leeftijd van de leiding per snapshot,
# en bepaalt of er binnen die snapshotperiode een lekkage is geweest.
# Het resultaat wordt opgeslagen als nieuwe tabel in de database


# Imports:
import pandas as pd
from database.connection import connection
from datetime import datetime

# Connectiestring om met OEGE te verbinden:
engine = connection()

# MySQL queries voor leidingen en lekkages:
queryPipes = """
    SELECT pipeid,dia,mat,len,cor_protect,joints,inst_date ,rehab_date, water_type, roughness, pressure_class, inside_dia, outside_dia 
    FROM zlangelw.pipes_original
"""

queryBreakage = """
    SELECT a.pipeid, c.date FROM zlangelw.breaks_pipes_match_original a
    JOIN zlangelw.pipes_original b ON a.pipeid = b.pipeid
    JOIN zlangelw.breaks_original c ON a.brid = c.brid
    WHERE c.isbr = 1
"""

# SQL tabel inlezen in een DF:
df_pipes = pd.read_sql(queryPipes, con=engine)
df_breaks = pd.read_sql(queryBreakage, con=engine)

# Snapshot aanmaken voor elke 3 maanden en omzetten naar DF:
snapshots = pd.date_range(start="2000-01-01", end="2021-01-01", freq="3MS")
snapshots_df = pd.DataFrame({'snapshot': snapshots})

# Cross join snapshots met pipes (85 x 165429)
snapshots_all = df_pipes.merge(snapshots_df, how="cross")

# Leeftijd berekenen van de leiding
snapshots_all["age"] = (snapshots_all["snapshot"] - snapshots_all["inst_date"]).dt.days / 365.25

# Alleen positieve getallen voor leeftijd, alleen snapshots wanneer de leiding al 'geboren' is
snapshots_all = snapshots_all[snapshots_all["age"] >= 0]

# Inst_date is niet meer nodig, leeftijd is al berekend
snapshots_all.drop('inst_date', axis=1)

# WL: Dit werkt niet omdat de DF te groot is, laat hem toch staan misschien ooit nodig
# def storing_binnen_3m(row):
#     start = row["snapshot"]
#     eind = start + pd.DateOffset(months=3)
#     storingen = df_breaks.query(
#         "pipeid == @row['pipeid'] and date >= @start and date < @eind"
#     )
#     return 1 if not storingen.empty else 0
# snapshots_all["storing_binnen_3m"] = snapshots_all.apply(storing_binnen_3m, axis=1)

# Einde van snapshot toevoegen, einde van de window van 3 maanden
snapshots_all["snapshot_end"] = snapshots_all["snapshot"] + pd.DateOffset(months=3)

# Left join snapshots en breuken. Een breuk gevonden, voegt hij deze 85 keer toe (aantal snapshots)
merged = snapshots_all.merge(df_breaks, on="pipeid", how="left")

# Alleen wanneer de breuk datum binnen snapshot en einde snapshot ligt
mask = (merged["date"] >= merged["snapshot"]) & (merged["date"] < merged["snapshot_end"])
filtered = merged[mask]

# Groepeer per leiding en snapshot en telt het aantal lekkages
has_storing = filtered.groupby(["pipeid", "snapshot"]).size().reset_index(name="count")
has_storing["storing_binnen_3m"] = 1  # Leiding heeft lekkage gehad binnne 3 maanden 

# Samenvoegen
snapshots_all = snapshots_all.merge(
    has_storing[["pipeid", "snapshot", "storing_binnen_3m"]],
    on=["pipeid", "snapshot"],
    how="left" 
)

# Leidingen zonder lekkage op 0 zetten
snapshots_all["storing_binnen_3m"] = snapshots_all["storing_binnen_3m"].fillna(0).astype(int)

# Wegschrijven naar DB:
snapshots_all.to_sql("snapshots_part1", con=engine,  chunksize=10000, method="multi", if_exists='fail', index=False )


