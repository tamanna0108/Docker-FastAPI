from .database import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Date, Identity

# list all the tables and their schema

class TB_EPISODES(Base):
    __tablename__ = 'TB_EPISODES'
    ID = Column(Integer, Identity(start=1, cycle=True), primary_key = True)
    CUSTOMER_ID = Column(String, nullable=False, primary_key = True)
    STATES = Column(String, nullable=False)
    PREDICTED_OFFER_1 = Column(String, nullable=False)
    PREDICTED_OFFER_2 = Column(String, nullable=True)
    PREDICTED_OFFER_3 = Column(String, nullable=True)
    LAST_UPDATE = Column(Date, nullable=True)
    UP_TO_DATE = Column(Date, nullable=False)

class TB_REWARDS(Base):
    __tablename__ = 'TB_REWARDS'
    ID = Column(Integer, Identity(start=1, cycle=True), primary_key = True)
    CUSTOMER_ID = Column(String, nullable=False, primary_key = True)
    ACCEPTED_OFFER = Column(Boolean, nullable=True)
    LAST_UPDATE = Column(Date, nullable=True)

class TB_PRODUCTS(Base):
    __tablename__ = 'TB_PRODUCTS'
    ID = Column(Integer, Identity(start=1, cycle=True), primary_key = True)
    OFFER_ID = Column(String, nullable=True)
    PRODUCT_NAME = Column(String, nullable=True)

class TB_AGENTS(Base):
    __tablename__ = 'TB_AGENTS'
    ID = Column(Integer, Identity(start=1, cycle=True), primary_key = True)
    VERSION = Column(String, nullable=False, primary_key = True)
    LAST_UPDATE = Column(Date, nullable=True)    
