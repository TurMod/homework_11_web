from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import configparser

config = configparser.ConfigParser()
config.read('db/config.ini')

user = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
host = config.get('DB', 'HOST')
port = config.get('DB', 'PORT')
db_name = config.get('DB', 'DB_NAME')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()