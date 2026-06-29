#this is for handling connection when using ORM. 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
#this is the format of a connection string that we have to pass into SQL alchemy # '''SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/hostname>/<database_name>' # ''' 
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Laxmi%402811@localhost:5432/fastapi"
#now we gotta create en engine. Engine is what is responsible for SQL alchemy to connect to Postgres DB.
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
''' When you actually want to talk to SQL database, we have to make use of session. ''' 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
