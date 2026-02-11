"""
Hoofd-entry voor Streamlit-dashboard – laadt XGBoost-model
en zet navigatie op.
"""
import streamlit as st, importlib.util, sys, os
from pathlib import Path

st.set_page_config(layout="wide")

# ── Project-root toevoegen aan PYTHONPATH ────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent   # …/dashboard/..
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))



# ── Navigatie ───────────────────────────────────────────────────────────
pg = st.navigation([
    st.Page("reports/home.py",       title="🏠 Home"),
    st.Page("reports/model.py",      title="🎯 Voorspelling"),
    st.Page("reports/breakages.py",  title="🧐 Analyses"),
    st.Page("reports/informatie.py", title="📖 Informatiepagina"),
])
pg.run()
