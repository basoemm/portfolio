# -----------------------------------------------------------------------------
# Snapshots verrijken met lekkages (aantal breuken laatste 3 maanden)
# Voor elke (pipeid, snapshot) wordt geteld hoeveel breuken plaatsvonden
# in de 90 dagen vóór de snapshotdatum.
# Resultaat wordt opgeslagen in 'snapshots_part4'
# -----------------------------------------------------------------------------

import pandas as pd
from database.connection import connection

# Connectie met database
engine = connection()

# Snapshots 03 ophalen:
df_snapshots = pd.read_sql("SELECT * FROM zlangelw.snapshots_part3", 
                           con=engine
                           )

# Vergeten weg te halen in 03
df_snapshots = df_snapshots.drop('snapshot_end', axis=1)

# Query voor de lekkages
query = """SELECT distinct c.pipeid, a.date, event_class 
FROM zlangelw.breaks_original a
inner join zlangelw.breaks_pipes_match_original b on a.brid = b.brid
inner join zlangelw.pipes_original c on b.pipeid = c.pipeid
where isbr = 1 
"""

# Lekkages ophalen
df_breakages = pd.read_sql(query, 
                           con=engine
                           )

# Voeg alle combinaties samen op pipeid
df_merged = df_snapshots[['pipeid', 'snapshot']].merge(
    df_breakages[['pipeid', 'date']],
    on='pipeid',
    how='left'
)

# Bereken het verschil in dagen
df_merged['days_diff'] = (df_merged['snapshot'] - df_merged['date']).dt.days

mask = (df_merged['days_diff'] > 0) & (df_merged['days_diff'] <= 90)
df_filtered = df_merged[mask]

# Groepeer en tel per snapshot
breakage_counts = (
    df_filtered.groupby(['pipeid', 'snapshot'])
    .size()
    .reset_index(name='breakages_last_3m')
)

# Voeg terug aan originele df_snapshots
df_snapshots = df_snapshots.merge(breakage_counts, on=['pipeid', 'snapshot'], how='left')

# Vul NaN (geen lekkages) met 0
df_snapshots['breakages_last_3m'] = df_snapshots['breakages_last_3m'].fillna(0).astype(int)

# Naar DB schrijven:
df_snapshots.to_sql("snapshots_part4", con=engine,  chunksize=5000, method="multi", if_exists='fail', index=False )