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
        db.close()

#Yeah, this whole thing... a bit messy. gave it to gbt twice to tell me what i could do to simplify, the code is 100% Human though, eventhough it ain't quite 100% from me, feel free to change things or just straight up rewrite it if it doesn't fit with other parts of the assignment
