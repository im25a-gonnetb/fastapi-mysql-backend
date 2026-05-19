from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

#Loads .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

#Creates Fastapi app
app = FastAPI()


# Defines that requests(in our case the sql select thingy's) come in strings
class StatementRequest(BaseModel):
    statement: str


# Test if server works, on http://127.0.0.1:8000/ it should say message: hello world
@app.get("/")
def read_root():
    return {"message": "Hello World"}



#IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//

#This down here creates ONE Route, in this route, all kinds of statements can be executed which is -obviously,
# very unsafe as anyone can just run drop database hence its not actually what we are supposed to do,
# we are supposed to create individual routes which only permit once single -for example- SELECT, so,

# to summarize, what we have:

# One open route that allows everything. What we need: multiple routes that only allow ONE thing

#What we need to do now:

#Use the one Route we have as a template to create about 3 Billion more locked down, super duper, secure +++, perfectly pretty individual Routes

#IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//IMPORTANT//

# Here the complicated stuff, we create a route for POST(called statement)
@app.post("/statement")
def execute_statement(req: StatementRequest):
    db = SessionLocal()
    try:
        #runs the request
        result = db.execute(text(req.statement))
        rows = result.fetchall()

        # Returns result, this shit was 6 rows until gbt told me im stupid and do it this way
        return {
            "result": [dict(row._mapping) for row in rows]
        }

    finally:
        #No clue what this is for, but was in the tutorial and it won't work without so...
        db.close()
