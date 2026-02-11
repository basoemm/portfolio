import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def connection():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    database = os.getenv("database")

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    return engine