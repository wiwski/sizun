from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True)
    ref = Column(String)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    source = Column(String)
    url = Column(String)
    house_area = Column(Integer)
    garden_area = Column(Integer)
    picture_url = Column(String)
    localization = Column(String)
    date = Column(DateTime)
    type = Column(String)