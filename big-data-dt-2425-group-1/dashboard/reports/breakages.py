import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os, sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ── PATH-FIX zodat  database.connection elders te importeren is 
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv()
# st.set_page_config(page_title="Lekkages", layout="wide")

def connection():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    database = os.getenv("database")

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    return engine

engine = connection()

def vertaal_afkortingen(
    df: pd.DataFrame,
    kolom: str,
    mapping: dict,
    nieuwe_kolom: str | None = None,
    inplace: bool = False
) -> pd.DataFrame:
    """
    Vervang afkortingen in `kolom` door volledige termen.
    Zie docstring voor details.
    """
    if inplace:
        target_df = df
    else:
        target_df = df.copy()

    if nieuwe_kolom is None:
        target_df[kolom] = target_df[kolom].map(mapping).fillna(target_df[kolom])
    else:
        target_df[nieuwe_kolom] = target_df[kolom].map(mapping).fillna(target_df[kolom])

    return target_df

MAT_MAPPING = {
    # kunststof
    "PVC":  "Polyvinyl-chloride",
    "PE":   "Polyethyleen (medium-/low-density)",

    # gietijzer‑familie
    "GG":   "Grijs gietijzer",
    "GN":   "Nodulair (sferoïdaal) gietijzer",  # ductile iron
    "GVL":  "Gietijzer (verzinkt/gelakt)",

    # staal / metalen
    "ST":   "Staal (ongecoat of gecoat)",
    "K":    "Koper",

    # cementgebonden
    "AC":   "Asbestcement",
    "B A":  "Beton (asbestvrij)",

    # overige placeholder – vul verder aan zodra nodig
}



# Queries, SQL Alchemy gaf foutmelding met SP, Views werkt wel:
queryMat = "SELECT * FROM view_material"
queryDagen = "SELECT * FROM view_dagen"
queryJaren = "SELECT * FROM view_jaren"
queryMaanden = "SELECT * FROM view_maanden"
queryAge = "SELECT * FROM view_age"
queryMatAge = "SELECT * FROM view_matage"

@st.cache_data
def load_from_db():
    df_mat = pd.read_sql(queryMat, con=engine)
    df_dagen = pd.read_sql(queryDagen, con=engine)
    df_jaar = pd.read_sql(queryJaren, con=engine)
    df_maand = pd.read_sql(queryMaanden, con=engine)

    df_age = pd.read_sql(queryAge, con=engine)
    df_matage = pd.read_sql(queryMatAge, con=engine) 

    return df_mat, df_matage, df_dagen, df_jaar, df_maand, df_age

with st.spinner("Data wordt geladen..."):
    df_mat, df_matage, df_dagen, df_jaar, df_maand, df_age = load_from_db()



df_matage['aantal_lekkages'] = df_matage['aantal_lekkages'].fillna(0)



df_mat = df_mat.sort_values(by='leidingen', ascending=False).head(8)
df_mat_plot = vertaal_afkortingen(df_mat, kolom="mat",
                                  mapping=MAT_MAPPING,
                                  nieuwe_kolom=None,   # zelfde kolom overschrijven
                                  inplace=False)
df_matage_plot = vertaal_afkortingen(df_matage, "materiaal", MAT_MAPPING)

####
# Lekkages per materiaal
###

st.title("🔧 Analyse van lekkages en leidingen gesorteerd per materialen")
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_mat_plot['mat'],
    y=df_mat_plot['leidingen'],
    name='Leidingen',
    marker=dict(color='#323175')
))

fig.add_trace(go.Bar(
    x=df_mat_plot['mat'],
    y=df_mat_plot['lekkages'],
    name='Lekkages',
    marker=dict(color='#01A5F0')
))

fig.add_trace(go.Bar(
    x=df_mat_plot['mat'],
    y=df_mat_plot['unieke_leidingen'],
    name='Unieke Leidingen',
    marker=dict(color='#FFA500')
))

fig.update_layout(
    barmode='group', 
    xaxis_title='Materiaal',
    yaxis_title='Aantal',
    legend_title='Categorieën',
)

st.plotly_chart(fig, use_container_width=True)

####
# Per jaar
###
st.title("🕒 Meldingen van lekkages per jaar")
fig = px.bar(df_jaar, x='Jaar', y='Aantal')
fig.update_traces(marker_color='#323175') 
st.plotly_chart(fig, use_container_width=True)

####
# Per maand
###
st.title("🕡 Meldingen van lekkages per maand")
fig = px.bar(df_maand, x='maand', y='aantal')
fig.update_traces(marker_color='#323175')
st.plotly_chart(fig, use_container_width=True)

###
# Per dag
##
st.title("🕤 Meldingen van lekkages per dag")
fig = px.bar(df_dagen, x='Dag', y='Aantal')
fig.update_traces(marker_color='#323175')
st.plotly_chart(fig, use_container_width=True)

####
# Per leeftijd
###

st.title("👴🏻 Analyse van Lekkages gesorteerd per leeftijd")
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_age['groep'],
    y=df_age['aantal'],
    name='Aantal leidingen',
    marker=dict(color='#323175')    
))

fig.add_trace(go.Bar(
    x=df_age['groep'],
    y=df_age['lekkages'],
    name='Lekkages',
    marker=dict(color='#01A5F0')
))

fig.update_layout(
    barmode='group', 
    xaxis_title='Leeftijdgroep',
    yaxis_title='Aantal',
    legend_title='Categorieën',
)

st.plotly_chart(fig, use_container_width=True)

###
# Per mat/age
##
st.title("⚙️ Leidingen en lekkages per leeftijdsgroep, sorteerbaar per materiaal")

# Dropdown voor materiaalkeuze
materiaal_opties = df_matage_plot['materiaal'].unique()
materiaal = st.selectbox("Kies materiaal", materiaal_opties)

# Filter op geselecteerd materiaal
df_filtered = df_matage_plot[df_matage_plot['materiaal'] == materiaal]

# Plotly bar chart
fig = go.Figure(data=[
    go.Bar(
        name='Aantal leidingen',
        x=df_filtered['leeftijdsgroep'],
        y=df_filtered['aantal_leidingen'],
        marker=dict(color='#323175')    
    ),
    go.Bar(
        name='Aantal lekkages',
        x=df_filtered['leeftijdsgroep'],
        y=df_filtered['aantal_lekkages'],
        marker=dict(color='#01A5F0')
    )
])

# Layout aanpassen
fig.update_layout(
    barmode='group',
    title=f"Materiaal: {materiaal}",
    xaxis_title="Leeftijdsgroep",
    yaxis_title="Aantal",
    legend_title="Categorie"
)

st.plotly_chart(fig)

