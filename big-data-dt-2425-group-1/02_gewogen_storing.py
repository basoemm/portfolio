# ------------------------------------------------------------
# Analyse: aantal en zwaarte van storingen in de 6 maanden vóór elke snapshot
# ------------------------------------------------------------
# Dit script haalt storingsdata (niet-lekkages) en snapshotdata op uit OEGE.
# Daarna koppelt het storingen aan leidingen, berekent of er binnen 6 maanden vóór een snapshot
# een storing was, en geeft zwaardere waarde aan recentere storingen.
# Het resultaat bevat per leiding en snapshot:
#   - Het aantal storingen in de afgelopen 6 maanden
#   - Een gewogen score (storingen dichter bij de snapshot tellen zwaarder mee)
# Deze data wordt toegevoegd aan het snapshotbestand en opgeslagen als 'snapshots_part2'.

import pandas as pd
from database.connection import connection
from datetime import datetime

# Connectie met database
engine = connection() # Oege

# TODO Mogelijk meer cleanen
query = """SELECT distinct c.pipeid, a.date, event_class FROM zlangelw.breaks_original a
inner join zlangelw.breaks_pipes_match_original b on a.brid = b.brid
inner join zlangelw.pipes_original c on b.pipeid = c.pipeid
where isbr = 0 and (event_class != 'Andere melding' and event_class != 'Meteropname' and event_class != 'Diversen' and event_class != 'Noodprocedure') """

# Snapshots gemaakt in 01 ophalen
query2 = "SELECT * FROM zlangelw.snapshots_part1"

storingen_df = pd.read_sql(query, con=engine)
snapshots_df = pd.read_sql(query2 , con=engine)

# Twee DF joinen. Alle snapshots blijven behouden en voegt evt storning toe
merged = snapshots_df.merge(storingen_df, on='pipeid', how='left')

# Bereken verschil in dagen tussen snapshot en storing datum
merged['dagen_voor_snapshot'] = (merged['snapshot'] - merged['date']).dt.days

# Filter alleen storingen in de 6 maanden (ongeveer 183 dagen)
filtered = merged[(merged['dagen_voor_snapshot'] > 0) & (merged['dagen_voor_snapshot'] <= 183)]

# Gewogen score: gewicht = 1 / (dagen + 1), zo krijgen storingen dichterbij de snapshot meer waarde
filtered['gewogen_score'] = 1 / (filtered['dagen_voor_snapshot'] + 1)

# Groepeer: som per leiding_id + snapshot_date
result = filtered.groupby(['pipeid', 'snapshot']).agg(
    storingen_6m=('dagen_voor_snapshot', 'count'),
    storingen_gewogen=('gewogen_score', 'sum')
).reset_index()

# Merge terug in snapshots_df
snapshots_df = snapshots_df.merge(result, on=['pipeid', 'snapshot'], how='left')

# Vul lege waarden (geen storingen) met 0
snapshots_df[['storingen_6m', 'storingen_gewogen']] = snapshots_df[['storingen_6m', 'storingen_gewogen']].fillna(0)

# Schrijven naar DB
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Writing DF to SQL")

snapshots_df.to_sql("snapshots_part2", 
                    con=engine,  
                    chunksize=5000, 
                    method="multi", 
                    if_exists='fail', 
                    index=False )