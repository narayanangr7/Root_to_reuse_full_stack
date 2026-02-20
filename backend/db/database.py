from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Guard against missing DATABASE_URL during build time or environment initialization
if not DATABASE_URL:
    # Use a dummy sqlite path if URL is missing just to allow the module to load
    # This won't be used for real transactions
    print("WARNING: DATABASE_URL not found. Using temporary dummy engine.")
    DATABASE_URL = "sqlite:///./temp_dummy.db"

# pool_pre_ping ensures the connection is still alive before using it (good for serverless)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
