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
# 3) Werkelijk aantal breuken per 3 maanden in 2019 berekenen
# ────────────────────────────────────────────────────────────────────
q_echte_2019 = """
WITH maand_breuken AS (
    SELECT
      YEAR(date) AS jaar,
      MONTH(date) AS maand,
      COUNT(*) AS breuken
    FROM zlangelw.breaks_original
    WHERE YEAR(date) = 2019
      AND date IS NOT NULL
    GROUP BY jaar, maand
)
SELECT AVG(breuken * 3) AS gemiddelde_breuken_3mnd
FROM maand_breuken
"""

result_df = pd.read_sql(text(q_echte_2019), con=engine)
echte = result_df.loc[0, "gemiddelde_breuken_3mnd"]

if echte is None:
    print("DEBUG: Waarde gemiddelde_breuken uit DB: None, zet op 0")
    echte = 0

# ────────────────────────────────────────────────────────────────────
# 4) Bereken afwijking en toon rapport
# ────────────────────────────────────────────────────────────────────
afwijking = abs(verwacht_r - echte) / echte * 100 if echte else 0

report = f"""
========================================================
Kalibratie-check lekkage-model  |  Horizon: 3 maanden
========================================================
Aantal leidingen in voorspellingstabel : {n_pipes:>8}
Som van alle kanspercentages           : {verwacht:>8.1f}
→ Verwachte breuken in 3 mnd           : {verwacht_r:>8}
--------------------------------------------------------
Gemiddeld aantal breuken (3 mnd, 2019) : {echte:>8.1f}
--------------------------------------------------------
Afwijking model vs. werkelijkheid      : {afwijking:>7.1f} %
========================================================
Interpretatie:
  • Som kansen ≈ werkelijk aantal  ➔ model is goed gekalibreerd
  • Afwijking > ±10 %              ➔ hertrainen of calibratie-plot maken
========================================================
"""

print(report)
