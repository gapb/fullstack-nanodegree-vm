import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,\
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__author__ = 'gilbertpodell-blume'

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zipCode = Column(Integer, nullable=False)
    email = Column(String(250))


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date_of_birth = Column(Date)
    breed = Column(String(250))
    gender = Column(String(1), nullable=False)
    weight = Column(Float)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)