import json
import csv
from sqlalchemy.orm import Session
from . import schema, models, crud
from datetime import date
from .models import TB_PRODUCTS
from fastapi import HTTPException


def rl_agent(customer_state, offers):
    from random import choices as rl_agent_decisioning
    weights = []
    print(f"logging customer_state age: {customer_state['age']}" )
    if customer_state["age"] < 30:
       weights = [10, 8 ,6, 6, 6, 4]
    else:
       weights = [8 ,6, 10, 6, 4]
    print(f"logging customer_state region: {customer_state['region']}")
    numeric_region = replace_region(customer_state['region'])
    if numeric_region == 0:
       weights = [10, 8 ,6, 6, 10, 10]
    elif numeric_region == 1:
       weights = [4, 8 ,6, 6, 10, 10]
    elif numeric_region == 2:
       weights = [4, 10 , 10, 6, 4, 4]
    else:
       raise Exception(f"weight by region not applied, is categorical data ?")
    print(f"logging customer_state gender: {customer_state['gender']}" )
    numeric_gender = replace_gender(customer_state['gender'])
    if numeric_gender == 0:
       weights = [10, 10 , 10, 6, 4, 4]
    elif numeric_gender == 1:
       weights = [4, 4, 6, 10, 10, 10]
    else:
       raise Exception(f"weight by gender was not applied, is categorical data?")
    return rl_agent_decisioning(offers, weights=weights, k=3)


def replace_region(region):
    return {
        'Europa': 2,
        'Americas': 0,
        'Asia': 1,
    }[region]

def replace_gender(gender):
	return {
    	'M': 0,
    	'F': 1,
	}[gender]


def uploadObjectNameMapping(db:Session):
	with open('company_A_products.csv') as file:
		reader = csv.reader(file)
		heading = next(reader)
		mapping = []
		for row in reader:
			addRecord = TB_PRODUCTS(OFFER_ID=row[1], PRODUCT_NAME=row[2])
			mapping.append(addRecord)
	db.add_all(mapping)
	db.commit()    	
	return "Sucess"




