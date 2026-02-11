"""
Pagina “Voorspelling” – dashboard-sectie
combineert oude + nieuwe features met robuuste NaN-afhandeling.
"""
from __future__ import annotations
import json, streamlit as st, pandas as pd, plotly.express as px
from sqlalchemy import text
from database.connection import connection

# ── MODEL & DB ──────────────────────────────────────────────────────────
engine = connection()

# import pickle

# with open("xgb_model.pkl", "rb") as f:
#     mdl = pickle.load(f)

# st.title("🎯 Voorspelling & Experimenten")
# if mdl is None:
#     st.error("Geen model geladen – herstart de app."); st.stop()

@st.cache_data
def load_from_db():
    df_risk = pd.read_sql("SELECT * FROM view_material", con=engine)
    df_risk["ratio"] = (df_risk["unieke_leidingen"] / df_risk["leidingen"]).round(2)

    df_pred = pd.read_sql(
    "SELECT pipeid, mat, age, kans_op_storing*100 AS probability, "
    "uitleg, breakages_last_3m FROM predictions_new2", con=engine)    

    def classify_risk(p: float) -> str:
        return "Laag" if p < 10 else ("Matig" if p < 60 else "⚠️ Hoog")
    
    df_pred["Risico"] = df_pred["probability"].apply(classify_risk)

    return df_risk, df_pred

with st.spinner("Data wordt geladen..."):
    df_risk, df_pred = load_from_db()


# ── HELPERS ─────────────────────────────────────────────────────────────
def classify_risk(p: float) -> str:
    return "Laag" if p < 10 else ("Matig" if p < 60 else "⚠️ Hoog")

def vertaal_afkortingen(df, kolom, mapping, nieuwe_kolom=None):
    tgt = df.copy()
    tgt[nieuwe_kolom or kolom] = tgt[kolom].map(mapping).fillna(tgt[kolom])
    return tgt

MAT_MAPPING = {  # (zoals eerder)
    "PVC":"Polyvinyl-<br>chloride","PE":"Polyethyleen <br>(medium-/low-density)",
    "GG":"Grijs <br>gietijzer","GN":"Nodulair <br>(sferoïdaal) <br>gietijzer",
    "GVL":"Gietijzer <br>(verzinkt/gelakt)","ST":"Staal <br>(ongecoat <br>of gecoat)",
    "K":"Koper","AC":"Asbestcement","B A":"Beton <br>(asbestvrij)"
}

# ── 1. Één-leiding test (sidebar) ───────────────────────────────────────
with st.sidebar:
    st.header("↳ Test één leiding")
    yr   = st.number_input("Installatie-jaar", 1900, 2050, 2000)
    mat  = st.selectbox("Materiaal", list(MAT_MAPPING))
    dia  = st.number_input("Diameter (mm)", 10, 2000, 110)
    lengte = st.number_input("Lengte (m)", 0.0, 5000.0, 250.0, step=0.1)
    prot = st.radio("Corrosiebescherming", ["Beschermd", "Onbekend"], horizontal=True)
    breaks_3m = st.number_input("Breuken laatste 3 mnd", 0, 10, 0)
    stor_gew  = st.number_input("Storingen gewogen", 0.0, 100.0, 0.0, step=0.1)
    stor_aantal = st.number_input("Aantal storingen",  0, 10, 0, step=1)
    storingen_gewogen_score = stor_gew * (2025-yr)
    corrosie_risico = 1 if prot == "Onbekend" else 0

    # Zoek de bijbehorende ratio in df_risk
    
    materiaal_risico_row = df_risk.loc[df_risk["mat"] == mat, "ratio"]

    if not materiaal_risico_row.empty:
        materiaal_risico = materiaal_risico_row.iloc[0]
    else:
        materiaal_risico = 0.0

    
    materiaal_risico.round(2)
    
    materiaal_leeftijds_risico = materiaal_risico * (2025-yr)
    materiaal_leeftijds_risico.round(2)

    storingen_impact_score = stor_aantal * (2025-yr)
       

    # Weers afhankelijkheden
    avg_temp_3w  = st.number_input("Gemiddelde temperatuur (3w)")
    frost_3w  = st.number_input("Aantal vriesdagen (3w)", step=1)
    rain_3w  = st.number_input("Regenval de afgelopen 3 weken (mm)")

    input_data = {
        "mat": [mat],
        "cor_protect": [prot],
        "len": [lengte],
        "dia": [dia],
        "breakages_last_3m": [breaks_3m],
        "avg_temp_3w": [avg_temp_3w],
        "frost_3w": [frost_3w],
        "rain_3w": [rain_3w],
        "storingen_gewogen": [stor_gew],
        "age": [2025 - yr],
        "years_since_rehab": [2025 - yr],
        "storingen_impact_score": [storingen_impact_score],
        "storingen_gewogen_score": storingen_gewogen_score,
        "corrosie_risico": corrosie_risico,
        "materiaal_risico": materiaal_risico,
        "materiaal_leeftijds_risico": materiaal_leeftijds_risico
    }


    if st.button("Bereken kans"):
        df_in = pd.DataFrame(input_data)
        for c in ("mat","cor_protect"): df_in[c] = df_in[c].astype("category")
        prob = mdl.predict_proba(df_in)[0,1]
        st.success(f"**Kans op breuk binnen 3 mnd: {prob*100:.6f}%**")

# ── 2. Data laden ───────────────────────────────────────────────────────
#df_pred = load_from_db()

# ── 3. Hoog-risicotabel (>60 %) ─────────────────────────────────────────
high = df_pred[df_pred.probability > 60].sort_values("probability", ascending=False)
st.subheader("🚨 Leidingen met hoog risico (> 60 %)")
st.write(f"Aantal resultaten: {len(high)}")
st.dataframe(high, use_container_width=True)

# ── 4. Verdeling risico-klassen ─────────────────────────────────────────
risico_counts = df_pred["Risico"].value_counts().reset_index()
risico_counts.columns = ["Risico","Aantal"]
fig = px.bar(risico_counts, x="Risico", y="Aantal", text="Aantal",
             color_discrete_sequence=["#006FA2"])
st.markdown("#### 📶 Verdeling risico’s"); st.plotly_chart(fig, use_container_width=True)

# ── 5. Leeftijdsgroepen (NaN → median) ─────────────────────────────────
median_age = pd.to_numeric(df_pred["age"], errors="coerce").median()
high_age = high.copy()
high_age["age"] = (
    pd.to_numeric(high_age["age"], errors="coerce")
      .fillna(median_age)
)
high_age["Leeftijdsgroep"] = pd.cut(high_age["age"], bins=range(0,151,10),
                                    right=False).astype(str)
age_counts = (high_age["Leeftijdsgroep"].value_counts()
              .sort_index().reset_index())
age_counts.columns = ["Leeftijdsgroep","Aantal"]
fig = px.bar(age_counts, x="Leeftijdsgroep", y="Aantal", text="Aantal",
             color_discrete_sequence=["#006FA2"])
fig.update_layout(showlegend=False, yaxis_title="Aantal leidingen")
st.markdown("#### 📶 Welke leeftijden hebben de meeste hoog-risicoleidingen?")
st.plotly_chart(fig, use_container_width=True)

# ── 6. Materiaal-analyse ───────────────────────────────────────────────
high_mat = high.dropna(subset=["mat"])
if high_mat.empty:
    st.info("Geen materiaaldata beschikbaar in hoog-risicotabel.")
else:
    high_vertaald = vertaal_afkortingen(high_mat, "mat", MAT_MAPPING)
    mat_counts = high_vertaald["mat"].value_counts().reset_index()
    mat_counts.columns = ["Materiaal","Aantal"]
    fig = px.bar(mat_counts, x="Materiaal", y="Aantal", text="Aantal",
                 color_discrete_sequence=["#006FA2"])
    fig.update_layout(showlegend=False, yaxis_title="Aantal")
    st.markdown("#### 📶 Meest voorkomende materialen (hoog risico)")
    st.plotly_chart(fig, use_container_width=True)

# ── 7. Lekkages laatste 3 mnd ──────────────────────────────────────────
high["breakages_last_3m"] = (
    pd.to_numeric(high["breakages_last_3m"], errors="coerce")
      .fillna(0).astype(int)
)
breakage_counts = high["breakages_last_3m"].value_counts().reset_index()
breakage_counts.columns = ["Breuk_afgelopen_3mnd","Aantal"]
breakage_counts["Breuk_afgelopen_3mnd"] = breakage_counts["Breuk_afgelopen_3mnd"]\
    .map({1:"Wel lekkage",0:"Geen lekkage"})
fig = px.bar(breakage_counts, x="Breuk_afgelopen_3mnd", y="Aantal", text="Aantal",
             color_discrete_sequence=["#006FA2"])
fig.update_layout(showlegend=False, yaxis_title="Aantal leidingen")
st.markdown("#### 💧 Lekkages afgelopen 3 maanden (hoog risico)")
st.plotly_chart(fig, use_container_width=True)

# ── 8. SHAP ────────────────────────────────────────────────────────────
st.markdown("#### Belangrijkste factoren")
st.image("shap_plot.png", caption="SHAP Summary Plot")

# ── 9. Experiment-historie + ROC ───────────────────────────────────────
@st.cache_data(show_spinner=False)
def _load_rows(): return pd.read_sql(
    "SELECT * FROM model_experiments ORDER BY timestamp DESC", con=engine)
rows = _load_rows()
st.subheader("🗂 Model-experimenten"); st.dataframe(rows, use_container_width=True)

meta = next((json.loads(r.metrics or "{}") for _,r in rows.iterrows()
             if {"fpr","tpr","auc"} <= (json.loads(r.metrics or "{}")).keys()), None)
if meta:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(4,4))
    plt.plot(meta["fpr"], meta["tpr"], label=f"AUC={meta['auc']:.3f}")
    plt.plot([0,1],[0,1],"--", color="gray"); plt.legend(); plt.grid()
    st.markdown("#### ROC – laatste run"); st.pyplot(plt.gcf())

# ── 10. Inline-notities ────────────────────────────────────────────────
st.markdown("#### Notities aanpassen")
if len(rows):
    rid  = st.number_input("Row-id", int(rows.id.min()), int(rows.id.max()), step=1)
    note = st.text_input("Nieuwe notitie")
    if st.button("Opslaan"):
        with engine.begin() as c:
            c.execute(text("UPDATE model_experiments SET notes=:n WHERE id=:i"),
                      {"n": note, "i": int(rid)})
        st.success("Notitie opgeslagen – ververs om te zien")
