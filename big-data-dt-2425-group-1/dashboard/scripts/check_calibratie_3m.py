from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
import os
 
# ────────────────────────────────────────────────────────────────────
# 1) .env inladen  (eerst lokaal zoeken, dan in Streamlit-map)
# ────────────────────────────────────────────────────────────────────
def connection():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    database = os.getenv("database")

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    return engine

engine = connection()

 
# ────────────────────────────────────────────────────────────────────
# 2) Verwacht aantal breuken = som(probabilities)
# ────────────────────────────────────────────────────────────────────
preds_df = pd.read_sql(
    text("SELECT probability FROM zlangelw.predictions"),
    con=engine
)
n_pipes    = len(preds_df)
verwacht   = preds_df["probability"].sum()          # prob staat in %
verwacht_r = round(verwacht)
 
# ────────────────────────────────────────────────────────────────────
# 3) Werkelijk aantal breuken in de laatste 3 maanden
# ────────────────────────────────────────────────────────────────────
q_echte = """
SELECT COUNT(*) AS echte_breuken
FROM   zlangelw.breaks_original
WHERE  date BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                      AND     CURDATE()
"""
echte = pd.read_sql(text(q_echte), con=engine).loc[0, "echte_breuken"]
 
# ────────────────────────────────────────────────────────────────────
# 4) Presentatie – één oogopslag duidelijk
# ────────────────────────────────────────────────────────────────────
afwijking = (
    abs(verwacht_r - echte) / echte * 100 if echte else 0
)
 
report = f"""
========================================================
Kalibratie-check lekkage-model  |  Horizon: 3 maanden
========================================================
Aantal leidingen in voorspellingstabel : {n_pipes:>8}
Som van alle kanspercentages           : {verwacht:>8.1f}
→ Verwachte breuken in 3 mnd           : {verwacht_r:>8}
--------------------------------------------------------
Werkelijk gemeten breuken (3 mnd)      : {echte:>8}
--------------------------------------------------------
Afwijking model vs. werkelijkheid      : {afwijking:>7.1f} %
========================================================
Interpretatie:
  • Som kansen ≈ werkelijk aantal  ➔ model is goed gekalibreerd
  • Afwijking > ±10 %              ➔ hertrainen of calibratie-plot maken
========================================================
"""
 
print(report)