import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os, sys
from pathlib import Path
import plotly.express as px

# project-root toevoegen
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv()

def connection():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    database = os.getenv("database")
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

engine = connection()
