from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .schema import predictRequestSchema, rewardsRequestSchema, updateVersionSchema
from . import crud, models
from . import loadData
from .batch_process import process_CSV_records

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# enlists all the API calls

@app.get("/is-alive")
def isAlive(db=Depends(db)):
    # response = requests.get('http://127.0.0.1:80/openapi.json')
    # response_json =  json.loads(response.content)
    # the_most_recent_version = response_json["info"]["version"] 
    the_most_recent_version = crud.fetch_latest_verion(db)
    return {"status": "I’m alive and running", "agent-version": f"{the_most_recent_version}-API"}

@app.post("/predict")
def predict(info: predictRequestSchema,db=Depends(db)):
    return crud.get_best_offers(db, info)
    
@app.put("/rewards")
def rewards(info: rewardsRequestSchema, db=Depends(db)):
    crud.update_rewards_data(db,info)
    return "Sucess"

@app.post("/predict-v2")
def predictV2(info: predictRequestSchema, db=Depends(db)):
    return crud.get_best_offers_with_name(db, info)

@app.get("/batch-process")
def batchProcess(db=Depends(db)):
    return process_CSV_records(db)


@app.get("/readRewardsTable")
def readRewardsTable(db=Depends(db)):
    return crud.get_reward_a_tab(db)

@app.get("/readAgentsTable")
def readAgentsTable(db=Depends(db)):
    return crud.get_agents_a_tab(db)


@app.get("/readEpisodeTable")
def readEpisodeTable(db=Depends(db)):
    return crud.get_epi_a_tab(db)

@app.post("/addVersion")
def addVersion(info: updateVersionSchema, db=Depends(db)):
    return crud.add_version(db, info)

@app.get("/uploadObjectNameMapping")
def uploadObjectNameMapping(db=Depends(db)):
    return loadData.uploadObjectNameMapping(db)

@app.get("/viewProductMapping")
def viewProductMapping(db=Depends(db)):
    return crud.get_product_name_mapping(db)
