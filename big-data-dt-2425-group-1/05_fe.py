# -----------------------------------------------------------------------------
# Verrijking van snapshots met risico-indicatoren
# - Jaren sinds rehabilitatie (of leeftijd als geen rehab)
# - Gewogen storing-scores (storingen x leeftijd)
# - Corrosierisico op basis van beschermingsmaatregel
# - Materiaalrisico + leeftijdsfactor
# Opslag in 'snapshots_part5' en splitsing op snapshotdatum (voor/na 01-10-2020)
# -----------------------------------------------------------------------------

import pandas as pd
from database.connection import connection

# Connectie met database
engine = connection()

# Snapshots ophalen:
df_snapshots = pd.read_sql("SELECT * FROM zlangelw.snapshots_part4", 
                           con=engine
                           )

# Tijd sinds rehab toevoegen
df_snapshots["years_since_rehab"] = (df_snapshots["snapshot"] - df_snapshots["rehab_date"]).dt.days / 365
# Nan vullen met age want geen rehab
df_snapshots["years_since_rehab"] = df_snapshots["years_since_rehab"].fillna(df_snapshots["age"])

# Afronden
df_snapshots["years_since_rehab"] = df_snapshots["years_since_rehab"].round(2)

# Een oudere leiding met recente storingen is mogelijk zorgwekkender dan een jonge leiding met storingen.
df_snapshots["storingen_impact_score"] = df_snapshots["storingen_6m"] * df_snapshots["age"]

# Leidingen met recente en veelvuldige storingen en hoge leeftijd is meer risico
df_snapshots["storingen_gewogen_score"] = df_snapshots["storingen_gewogen"] * df_snapshots["age"]

# Corrosie risico
df_snapshots["corrosie_risico"] = df_snapshots["cor_protect"].isin(["None", "Practisch geen"]).astype(int)

# Mat risico op basis van aantal lekkages
materiaal_risico = {
    "A": 0.00,
    "AC": 0.16,
    "AL": 0.00,
    "B": 0.00,
    "B A": 0.00,
    "B A/ST": 0.01,
    "B B": 0.09,
    "B B/ST": 0.02,
    "B S": 0.00,
    "B S/ST": 0.00,
    "GG": 0.18,
    "GN": 0.09,
    "GVK": 0.03,
    "K": 0.24,
    "L": 0.03,
    "PE": 0.16,
    "PVC": 0.14,
    "ST": 0.02
}
df_snapshots["materiaal_risico"] = df_snapshots["mat"].map(materiaal_risico)
df_snapshots["materiaal_leeftijds_risico"] = df_snapshots["materiaal_risico"] * df_snapshots["age"]
df_snapshots["materiaal_leeftijds_risico"] = df_snapshots["materiaal_leeftijds_risico"].round(2)

df_snapshots.to_sql("snapshots_part5", con=engine,  chunksize=5000, method="multi", if_exists='fail', index=False )

# Laatste snapshot om te predicten als model gemaakt is:
datumgrens = pd.Timestamp("2020-10-01")

df_voor_2020_10_01 = df_snapshots[df_snapshots["snapshot"] < datumgrens].copy()
df_na_2020_10_01 = df_snapshots[df_snapshots["snapshot"] >= datumgrens].copy()

df_na_2020_10_01.to_sql("snapshots_predict", con=engine,  chunksize=5000, method="multi", if_exists='fail', index=False )
df_voor_2020_10_01.to_sql("snapshots_traintest", con=engine,  chunksize=5000, method="multi", if_exists='fail', index=False )
