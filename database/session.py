import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session

# Initialize database tables (called on startup in main.py)
def init_db():
    SQLModel.metadata.create_all(engine)
