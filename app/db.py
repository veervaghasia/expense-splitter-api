# This file is responsible for:
# - Connecting to the database
# - Creating the database tables
# - Providing a session for database operations to our API

# SQLModel gives use tools to define models and interact with database
from sqlmodel import SQLModel, create_engine, Session

# If models.py isn't imported anywhere, tables won't be created because SQLModel won't know about them.
# So we import it here to ensure all models are registered before we create tables.
from app import models


# -----------------------------
# 1. CREATE DATABASE ENGINE
# -----------------------------

# "sqlite:///database.db" - this is the connection string.
# It means:
# - use SQLite
# - store data in a file named "database.db" in our project folder
DATABASE_URL = "sqlite:///database.db"

# create_engine sets up the connection to the database
# echo = True -> prints SQL queries in terminal (useful for debigging)
engine = create_engine(DATABASE_URL, echo=True)


# -----------------------------
# 2. CREATE TABLES IN DATABASE
# -----------------------------

def create_db_and_tables():
    """
    This function creates all tables defined in models.py
    It reads metadata from SQLModel classes and creates tables in DB
    """

    # SQLModel.metadata contains all table definitions
    # create_all() creates tables if they don't already exist
    SQLModel.metadata.create_all(engine) 


# -----------------------------
# 3. CREATE SESSION (DB CONNECTION)
# -----------------------------

def get_session():
    """
    This function provides a database session.

    A session is like a temporary connection to the Database.
    We use it to:
    - add data
    - query data
    - commit changes
    """

    # 'with' ensures:
    # - session is opened
    # - automatically closed after use (this part is important to avoid connection leaks)
    with Session(engine) as session:
        # 'yield' is used instead of 'return' because FastAPI expects a generator
        # It will:
        # - give session to the route
        # - close it after request finishes
        yield session