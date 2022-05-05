from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func, desc
from . import schema, models
from .schema import predictRequestSchema, predictResponseSchema, rewardsRequestSchema, updateVersionSchema
from datetime import date
from .models import TB_EPISODES, TB_REWARDS, TB_AGENTS, TB_PRODUCTS
import json

def error_message(message):
    return {
        'error': message
    }

def get_reward_a_tab(db:Session):
    return db.query(models.TB_REWARDS).all()

def get_agents_a_tab(db:Session):
    return db.query(models.TB_AGENTS).all()

def get_product_name_mapping(db:Session):
    return db.query(models.TB_PRODUCTS).all()

def get_epi_a_tab(db: Session):
    return db.query(models.TB_EPISODES).all()


def get_best_offers(db: Session, info: predictRequestSchema):
    bestOffers = get_top_3_offers(info.dict()["offers"], info.dict()["states"])
    add_entry_episodes_table(db, info.dict(), bestOffers)
    add_entry_rewards_table(db, info.dict())
    return predictResponseSchema(customer_id=info.dict()["customer_id"], response_date=date.today(), best_offers=bestOffers)

def get_top_3_offers(offers, states):
    trueOffersList = []
    for key, value in offers.items():
        if value:
            trueOffersList.append(key)
    if len(trueOffersList) > 3:
        return trueOffersList[0:3]
    else:
        return trueOffersList

def add_entry_episodes_table(db, infoDict, bestOffers):
    object_in_db = db.query(models.TB_EPISODES).filter(models.TB_EPISODES.CUSTOMER_ID == infoDict["customer_id"]).all()
    if object_in_db:
        raise HTTPException(400, detail=error_message('customerId already exists in episodes table'))
    addRecord = TB_EPISODES(CUSTOMER_ID=infoDict["customer_id"], STATES=str(infoDict["states"]), PREDICTED_OFFER_1=bestOffers[0], PREDICTED_OFFER_2=bestOffers[1], PREDICTED_OFFER_3=bestOffers[2], UP_TO_DATE=infoDict["timestamp"])
    db.add(addRecord)
    db.commit()
    db.refresh(addRecord)

def add_entry_rewards_table(db, infoDict):
    object_in_db = db.query(models.TB_REWARDS).filter(models.TB_REWARDS.CUSTOMER_ID == infoDict["customer_id"]).all()
    if object_in_db:
        raise HTTPException(400, detail=error_message('customerId already exists in rewards table'))
    addRecord = TB_REWARDS(CUSTOMER_ID=infoDict["customer_id"])
    db.add(addRecord)
    db.commit()
    db.refresh(addRecord)

def update_rewards_data(db: Session, info: rewardsRequestSchema):
    object_in_db = db.query(models.TB_REWARDS).filter(models.TB_REWARDS.CUSTOMER_ID == info.dict()["customer_id"]).all()
    if object_in_db:
        updateRecord = db.query(TB_REWARDS).filter(TB_REWARDS.CUSTOMER_ID == info.dict()["customer_id"]).first()
        setattr(updateRecord, 'LAST_UPDATE', info.dict()["timestamp"])
        setattr(updateRecord, 'ACCEPTED_OFFER', info.dict()["accepted_one_of_the_three_offers"])
        db.commit()
        db.refresh(updateRecord)
    else:
        raise HTTPException(400, detail=error_message('customerId does not exist in rewards table'))
    
def get_best_offers_with_name(db: Session, info: predictRequestSchema):
    bestOffersID = get_best_offers(db, info)
    return replace_id_offer_names(db, bestOffersID)

def replace_id_offer_names(db, bestOffersID):
    offerNameList = {}
    for offer in bestOffersID.dict()["best_offers"]:
        offerName = db.query(TB_PRODUCTS).filter(TB_PRODUCTS.OFFER_ID == offer).first()
        offerNameList[offer] = offerName.PRODUCT_NAME
    setattr(bestOffersID, 'best_offers', offerNameList)
    return bestOffersID

def fetch_latest_verion(db:Session):
    latestEntry = db.query(func.max(models.TB_AGENTS.VERSION)).first()
    return latestEntry[0]

def add_version(db:Session, info: updateVersionSchema):
    object_in_db = db.query(models.TB_AGENTS).filter(models.TB_AGENTS.VERSION == info.dict()["VERSION"]).all()
    if object_in_db:
        raise HTTPException(400, detail=error_message('version already exists in agents table'))
    addRecord = TB_AGENTS(VERSION=info.dict()["VERSION"], LAST_UPDATE=info.dict()["LAST_UPDATE"])
    db.add(addRecord)
    db.commit()
    db.refresh(addRecord)
    return addRecord