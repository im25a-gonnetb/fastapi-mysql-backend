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

#Creates prefix for SELECT Routes
def create_route(path: str, fixed_statement: str):
    @app.post(path)
    def route_handler():
        db = SessionLocal()
        try:
            #runs the request
            result = db.execute(text(fixed_statement))
            rows = result.fetchall()

            # Returns result
            return {
                "result": [dict(row._mapping) for row in rows]
            }

        finally:

            db.close()

    #no fucking clue what this is #Ben'sShit
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}"

# All routes for SELECT
create_route("/select/benutzer",    "SELECT * FROM taskplaner.benutzer")
create_route("/select/aufgabe",     "SELECT * FROM taskplaner.aufgabe")
create_route("/select/kategorie",   "SELECT * FROM taskplaner.kategorie")
create_route("/select/material",    "SELECT * FROM taskplaner.material")
create_route("/select/prioritaet",  "SELECT * FROM taskplaner.prioritaet")
create_route("/select/fortschritt", "SELECT * FROM taskplaner.fortschritt")
