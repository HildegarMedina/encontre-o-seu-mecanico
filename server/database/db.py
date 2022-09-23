"""Database."""
from config import config
import databases
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = config.DB_URL

meta = MetaData()

Base = declarative_base()

if os.environ.get("RUNNING_TESTS"):
    if "_test" not in DB_URL:
        DB_URL += "_test"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = databases.Database(DB_URL)
