import csv
from .schema import predictRequestSchemaStr, predictResponseSchema, rewardsRequestSchema,statesSchemaStr, OffersList
from datetime import date
import requests
import json
import pandas as pd
import os


def process_CSV_records(db):
	jsonArray = convert_csv_to_json()
	mappings = predict_request_schema_list(jsonArray)
	apiUrl = "http://127.0.0.1/predict"
	responseList = []
	for row in mappings:
		response =  requests.post(apiUrl, json.dumps(row))
		responseList.append(response.json())
	dirpath = os.getcwd()
	output_path = os.path.join(dirpath,'output.csv')
	# output csv file
	output_path_json = os.path.join(dirpath, 'data.json')
	with open(output_path_json, 'w') as f:
		json.dump(responseList, f)
	df = pd.read_json(output_path_json)
	df.to_csv(output_path)
	return responseList
	
def convert_csv_to_json():
	jsonArray = []
	# input csv here
	with open('company_B.csv') as csvf:
		csvReader = csv.DictReader(csvf, delimiter=';') 
		for row in csvReader: 
			jsonArray.append(row)
	return jsonArray

def predict_request_schema_list(jsonArray):
	mapping=[]
	for row in jsonArray:
		if(len(row["client_since"])> 0):
			stateSchemaRecord = statesSchemaStr(age=int(row["age"]), gender=row["gender"], client_since=row["client_since"], region=row["region"], last_offer=row["last_offer"])
		else:
			stateSchemaRecord = statesSchemaStr(age=int(row["age"]), gender=row["gender"], client_since="1900-01-01", region=row["region"], last_offer=row["last_offer"])	

		offersListSchema = OffersList(OFFER_1=row["Offer_1"],OFFER_2=row["Offer_2"],OFFER_3=row["Offer_3"],OFFER_4=row["Offer_4"],OFFER_5=row["Offer_5"],OFFER_6=row["Offer_6"],OFFER_7=row["Offer_7"],OFFER_8=row["Offer_8"],OFFER_9=row["Offer_9"],OFFER_10=row["Offer_10"])
		offersListSchemaUpdated = map_false_offers(stateSchemaRecord, offersListSchema)
		if(len(row["timestamp"])>0):
			# date.fromisoformat(row["timestamp"])
			predictRequestSchemaList = predictRequestSchemaStr(customer_id=row["customer_id"], timestamp=row["timestamp"], states=stateSchemaRecord, offers=offersListSchemaUpdated)
		mapping.append(predictRequestSchemaList.dict())

	return mapping

def map_false_offers(states, offers):
	if(states.age>65):
		setattr(offers, "OFFER_1", False)
		setattr(offers, "OFFER_3", False)
		setattr(offers, "OFFER_4", False)
	if(states.region == "Europa"):
		setattr(offers, "OFFER_4", False)
		setattr(offers, "OFFER_5", False)
		setattr(offers, "OFFER_6", False)
	return offers
