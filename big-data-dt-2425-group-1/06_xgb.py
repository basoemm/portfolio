"""
Predictie van storingen in waterleidingen met XGBoost.

Laadt en verwerkt data uit een database, traint een XGBoost-model en evalueert prestaties 

"""

import xgboost as xgb
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from database.connection import connection

## Data in DF laden
engine = connection() # Oege

query = """
SELECT dia, mat, len, cor_protect, snapshot,age, storing_binnen_3m, storingen_6m, storingen_gewogen, avg_temp_3w, frost_3w, rain_3w, breakages_last_3m, years_since_rehab, storingen_impact_score, storingen_gewogen_score, corrosie_risico, materiaal_risico, materiaal_leeftijds_risico
FROM zlangelw.snapshots_traintest
"""

df = pd.read_sql(query, con=engine)

## Verwijder rijen met Null waardes:
df = df.dropna(subset=['dia'])
df = df.dropna(subset=['mat'])


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

# Checken of omgezet zijn:
print(X.dtypes)

# Splitten op target en cutoff_date, we willen hem niet de toekomst laten zien
target = 'storing_binnen_3m'
cutoff_date = pd.to_datetime('2017-01-01')

train_df = X[(X['snapshot'] <= cutoff_date)]
test_df  = X[X['snapshot'] > cutoff_date]
test_df = test_df[~test_df['snapshot'].dt.year.isin([2019, 2020])] # 2019 en 2020 zijn onvolledig

# Features en target splitsen
X_train = train_df.drop(columns=[target]) # targetweghalen
y_train = train_df[target] # de target

X_test = test_df.drop(columns=[target])
y_test = test_df[target]

# Snapshot is nu niet nodig, droppen voor fitten
X_test = X_test.drop(columns='snapshot')
X_train = X_train.drop(columns='snapshot')

# XGboost model
model = xgb.XGBClassifier(
    max_depth=4,
    min_child_weight=5,
    gamma=0.2,
    scale_pos_weight=50, # Vanwege inbalans in pos / neg
    eval_metric='aucpr',
    use_label_encoder=False,
    enable_categorical=True,
    tree_method='hist'
)

# Trainen
model.fit(X_train, y_train)

# Voorspellen
y_pred = model.predict(X_test)

# Feature importances uitprinten, welke features dragen het meeste bij:
importances = model.feature_importances_
feature_names = X_test.columns

importances_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print(importances_df)

# Uitleggen met SHAP - build tools :(
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)

shap.summary_plot(shap_values, X_train)  # geeft globaal overzicht

# XGBoost importance
model.get_booster().get_score(importance_type='gain')

# SHAP importance (gemiddelde absolute waarde)
import numpy as np
np.mean(np.abs(shap_values), axis=0)


## AUC curve:
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

y_true = y_test         
y_scores = model.predict_proba(X_test)[:, 1]  

# Bereken ROC-curve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

# Plotten
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray') 
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.grid(True)
plt.show()

print(X_test.dtypes)

### Predict
df_predict = pd.read_sql("SELECT mat,cor_protect,len,dia,breakages_last_3m,storingen_gewogen,age FROM zlangelw.snapshots_01102020", con=engine)

categorical_cols = ['mat', 'cor_protect'] 

for col in categorical_cols:
    df_predict[col] = df_predict[col].astype('category')


# Bereken predictie-probabilities en sla op
probabilities = model.predict_proba(df_predict)[:, 1] 
df_predict['probability'] = probabilities

model.get_booster().get_score(importance_type='gain')

# Maak een kopie van df_predict en converteer categoricals naar numerieke codes
df_dmatrix = df_predict.copy()
df_dmatrix = df_dmatrix.drop(columns=["probability"])
for col in df_dmatrix.select_dtypes(['category']).columns:
    df_dmatrix[col] = df_dmatrix[col].cat.codes

contribs = model.get_booster().predict(xgb.DMatrix(df_dmatrix), pred_contribs=True)
feature_names = df_dmatrix.columns
contribs_df = pd.DataFrame(contribs[:, :-1], columns=feature_names)

# Bepaal per rij de belangrijkste feature qua bijdrage
# Voor elke rij: haal de top 3 features met grootste absolute bijdrage
def top_features_with_values(row, top_n=3):
    top = row.abs().nlargest(top_n)
    return [f"{feature}({row[feature]:+.2f})" for feature in top.index]

# Pas toe per rij
df_predict['top_3_redenen'] = contribs_df.apply(top_features_with_values, axis=1).apply(lambda x: ', '.join(x))


plt.hist(probabilities, bins=100)
plt.title("Verdeling van voorspelde kansen (klasse 1)")
plt.xlabel("Kans op storing")
plt.ylabel("Aantal voorspellingen")
plt.show()


import pickle

with open("xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)
