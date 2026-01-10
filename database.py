# all the database imports
# sqlalchemy is an Object Relational Mapper
# instead of writing sql queries, we work with Python objects=
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# connection string
DATABASE_URL = "postgresql://postgres:Le%40nderTexa$7864!@localhost:5432/fakenews"

engine = create_engine(DATABASE_URL)    # sqlalchemy's connection manager - handles connection pooling (reusing connections instead of opening new ones each time)
SessionLocal = sessionmaker(bind=engine)    # creates the session so I can start a conversation (read/writes)
Base = declarative_base()   # base class where db models inherit from

# a model. Python class that maps to a table in the database
class Analysis(Base):
    __tablename__ = "analyses"  # actual name of table in postgresql

    id = Column(Integer, primary_key=True, index=True)  # declaring this column as primary key. index=True makes lookups faster
    text = Column(String, nullable=False)   # column - nullable=False means field is required. DB will reject inserts without it
    label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # timestamp for when record was created. default=datetime.utcnow means sqlalchemy will auto-fill if not provided

# create the tables
# looks at all classes inheriting Base and creates corresponding tables in the DB.
# if table already exists - it skips it
Base.metadata.create_all(bind=engine)