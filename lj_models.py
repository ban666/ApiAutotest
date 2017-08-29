# coding: utf-8
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Information(Base):
    __tablename__ = 'information'

    village = Column(String(100))
    type = Column(String(100))
    size = Column(String(100))
    position = Column(String(100))
    total = Column(Integer)
    unit = Column(Integer)
    tags = Column(String(100))
    mask = Column(String(200), primary_key=True, server_default=text("''"))


class InformationWeb(Base):
    __tablename__ = 'information_web'

    village = Column(String(100))
    type = Column(String(100))
    size = Column(String(100))
    position = Column(String(100))
    total = Column(Integer)
    unit = Column(Integer)
    tags = Column(String(100))
    mask = Column(String(200), primary_key=True, server_default=text("''"))
