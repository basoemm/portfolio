from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import os
from database.connection import connection


## Load data in df
engine = connection() # Oege

query = """
SELECT dia, mat, len, cor_protect, water_type, snapshot,age, storing_binnen_3m, storingen_6m, storingen_gewogen, avg_temp_1w, frost_1w,breakages_last_3m, years_since_rehab, storingen_impact_score, storingen_gewogen_score, corrosie_risico, materiaal_risico, materiaal_leeftijds_risico
FROM zlangelw.snapshots
"""

df = pd.read_sql(query, con=engine)



## dorp nan
df = df.dropna(subset=['dia'])
df = df.dropna(subset=['mat'])
df = df.dropna(subset=['water_type'])

## fill nan values
df['cor_protect'] = df['cor_protect'].fillna('Onbekend')
df["storingen_gewogen"] = df["storingen_gewogen"] * 100

X = df[['snapshot', 'mat','materiaal_risico','storingen_gewogen','cor_protect','water_type','avg_temp_1w', 'storing_binnen_3m']]

categorical_cols = ['mat', 'cor_protect', 'water_type']
X = pd.get_dummies(X, columns=categorical_cols)
X.drop('mat', axis=1, inplace=True)



# Splitten op target en cutoff_date, we willen hem niet de toekomst zien
target = 'storing_binnen_3m'
cutoff_date = pd.to_datetime('2017-01-01')

train_df = X[X['snapshot'] <= cutoff_date]
test_df  = X[X['snapshot'] > cutoff_date]

# Features en target splitsen
X_train = train_df.drop(columns=[target]) # targetweghalen
y_train = train_df[target] # de target

X_test = test_df.drop(columns=[target])
y_test = test_df[target]


# Snapshot is nu niet nodig, droppen voor fitten
X_test = X_test.drop(columns='snapshot')
X_train = X_train.drop(columns='snapshot')

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy op testset:", accuracy)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

y_probs = model.predict_proba(X_test)[:, 1]  # kans op class 1
y_pred = (y_probs > 0.1).astype(int)  
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
