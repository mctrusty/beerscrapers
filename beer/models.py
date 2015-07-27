from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings

def db_connect():
    """
    Connects to DB using DATABASE settings in settings.py
    """
    return create_engine(URL(**settings.DATABASE), implicit_returning=False)

DeclarativeBase = declarative_base()

def create_beers_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Beers(DeclarativeBase):
    """Beer Model for sqlalchemy"""
    __tablename__ = "beers"
    id = Column(Integer, primary_key=True)
    store = Column('store', String, nullable=True)
    brewer = Column('brewer', String, nullable=True)
    beer = Column('beer', String, nullable=True)
    link = Column('link', String, nullable=True)
    size = Column('size', String, nullable=True)
    quantity = Column('qty', String, nullable=True)
    pkg = Column('pkg', String, nullable=True)
    price = Column('price', String, nullable=True)
