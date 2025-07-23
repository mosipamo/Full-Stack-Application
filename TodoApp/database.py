from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" 
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:msina83#@localhost:5432/TodoApplicationDatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()