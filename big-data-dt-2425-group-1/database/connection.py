import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")

    if not all([user, password, host, database]):
        raise RuntimeError("Environment variables not loaded correctly")

    connection_string = (
        f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    )

    engine = create_engine(connection_string)
    return engine
