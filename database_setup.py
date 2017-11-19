#!/usr/bin/env python
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import OperationalError

# Basic Information of the database
_Base = declarative_base()
_sql_string = "postgresql://postgres:admin@localhost/sample"


class Catagory(_Base):
    __tablename__ = 'catagory'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Items(_Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String())
    date = Column(DateTime(), default=datetime.datetime.utcnow)
    catagory_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship(Catagory)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'date_created': self.date,
            'catagory_id': self.catagory_id
        }

# Bind the Table Class to Base
try:
    _engine = create_engine(_sql_string)
    _Base.metadata.create_all(_engine)
except OperationalError:
    raise Exception(
        "Cannot find the database! Did you create it " +
        "and provide a correct path?")

_Base.metadata.bind = _engine
_DBSession = sessionmaker(bind=_engine)
session = _DBSession()
