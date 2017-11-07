#!/usr/bin/env python
import sys
from sqlaclchemy import Column, ForeignKey, Integer, String
from sqlaclchemy.ext.declarative import declarative_base
from sqlaclchemy import create_engine
from sqlaclchemy.orm import relationship
from database_table import createTableClass

db_string = "postgres://restaurantmenu.db"
Base = declarative_base()


createTableClass(Base)
engine = create_engine(db_string)

Base.metadata.create_all(engine)