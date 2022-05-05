from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from dataclasses import field

class updateVersionSchema(BaseModel):
    VERSION: str
    LAST_UPDATE: Optional[date]

    class Config:
        orm_mode = True

class OffersList(BaseModel):
    OFFER_1: bool
    OFFER_2: bool
    OFFER_3: bool
    OFFER_4: bool
    OFFER_5: bool
    OFFER_6: bool
    OFFER_7: bool
    OFFER_8: bool
    OFFER_9: bool
    OFFER_10: bool

    class Config:
        orm_mode = True

class statesSchema(BaseModel):
    age: Optional[int]
    gender: Optional[str]
    client_since: Optional[date]
    region: Optional[str]
    last_offer: Optional[str]

    class Config:
        orm_mode = True


class predictRequestSchema(BaseModel):
    customer_id: str
    timestamp: Optional[date]
    states: statesSchema
    offers: OffersList
    
    class Config:
        orm_mode = True

class predictResponseSchema(BaseModel):
    customer_id: str
    response_date: date
    best_offers: List[str]

    class Config:
        orm_mode = True

class rewardsRequestSchema(BaseModel):
    customer_id: str
    timestamp: date
    accepted_one_of_the_three_offers: bool

    class Config:
        orm_mode = True

class statesSchemaStr(BaseModel):
    age: Optional[int]
    gender: Optional[str]
    client_since: Optional[str]
    region: Optional[str]
    last_offer: Optional[str]

    class Config:
        orm_mode = True


class predictRequestSchemaStr(BaseModel):
    customer_id: str
    timestamp: Optional[str]
    states: statesSchemaStr
    offers: OffersList
    
    class Config:
        orm_mode = True
        




