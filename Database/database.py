from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = 'DatabaseURL' # Replace with your actual database URL

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)