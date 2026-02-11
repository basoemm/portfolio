import pickle
import xgboost as xgb
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from database.connection import connection

engine = connection()

with open("xgb_model.pkl", "rb") as f:
    model = pickle.load(f)

query = """
SELECT pipeid, dia, mat, len, cor_protect, water_type, snapshot,age, storing_binnen_3m, storingen_6m, storingen_gewogen, avg_temp_3w, frost_3w, rain_3w, breakages_last_3m, years_since_rehab, storingen_impact_score, storingen_gewogen_score, corrosie_risico, materiaal_risico, materiaal_leeftijds_risico
FROM zlangelw.snapshots_predict
"""

df = pd.read_sql(query, con=engine)


## Verwijder rijen met Null waardes:
df = df.dropna(subset=['dia'])
df = df.dropna(subset=['mat'])
df = df.dropna(subset=['water_type'])

## Corrosie protectie op onbekend zetten, zijn er teveel om te verwijderen
df['cor_protect'] = df['cor_protect'].fillna('Onbekend')

# Hogere waarde heeft misschien meer invloed
df["storingen_gewogen"] = df["storingen_gewogen"] * 100 

# De Features:
X = df[['snapshot','mat', 'cor_protect', 'len', 'dia', 'breakages_last_3m','avg_temp_3w', 'frost_3w', 'rain_3w', 'storingen_gewogen' ,'age', 'years_since_rehab', 'storingen_impact_score', 'storingen_gewogen_score', 'corrosie_risico', 'materiaal_risico', 'materiaal_leeftijds_risico', 'storing_binnen_3m']]

# Velden markeren als categorie, XGB kan alleen omgaan met getallen:
categorical_cols = ['mat', 'cor_protect'] 
for col in categorical_cols:
    X[col] = X[col].astype('category')


X = X.drop(columns=['storing_binnen_3m', 'snapshot'])


probs = model.predict_proba(X)
probs = model.predict_proba(X)[:, 1]  # Alleen kans op klasse 1 (bijv. storing)

# Voeg toe als nieuwe kolom in df
df["kans_op_storing"] = probs



import shap
import numpy as np
import pandas as pd

# SHAP explainer aanmaken (1x)
explainer = shap.TreeExplainer(model)

def uitleg_per_rij(row, shap_values_row, columns, top_n=3):
    top_idxs = np.argsort(np.abs(shap_values_row))[::-1][:top_n]
    zinnen = []

    for idx in top_idxs:
        feature = columns[idx]
        waarde = row[feature]
        impact = shap_values_row[idx]
        richting = "verhoogt" if impact > 0 else "verlaagt"

        # Format waarde
        if isinstance(waarde, (int, float, np.number)):
            waarde_tekst = f"{waarde:.2f}"
        else:
            waarde_tekst = str(waarde)

        zinnen.append(f"{feature} = {waarde_tekst} → {richting} de kans op storing")

    return "; ".join(zinnen) + "."

shap_values = explainer.shap_values(X)

df["uitleg"] = [
    uitleg_per_rij(X.iloc[i], shap_values[i], X.columns)
    for i in range(len(X))
]

df.to_sql("predictions_new", chunksize=5000, con=engine, if_exists='replace')

