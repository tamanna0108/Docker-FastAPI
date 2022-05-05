### Requirement ###

* Create RestAPI for two companies
  * GET /is-alive : check database connectivity
  * POST /predict : accept new customer and predict best 3 offers for it
  * PUT /rewards : update customers offer acceptance 
* Requirement for company A
  * API endpoints
  * Offer name along with offer ID in the predict response, new api /predict-v2
* Requirement for company B
  * Batch processing file which accept inputs as csv and give the out for all records in csv file

### Infrastructure ###

* FastAPI : python API building framework
* Postgres
* Docker : 2 containers
  * Postgres SQL
  * Rest API calls
* SQLAlchemy : loading and manipulating tables
* Uvicorn : binding element, handles web connections from browser/API client 


### Running the app ###

* Go to the root folder and run
 ```
$ docker-compose up -d --build
 ```
 * Swagger UI link : [http://127.0.0.1/docs#/](http://127.0.0.1/docs#/)

