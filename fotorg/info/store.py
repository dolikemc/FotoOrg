from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    created = Column(DateTime)
    size = Column(Integer)


class Store:
    pass
