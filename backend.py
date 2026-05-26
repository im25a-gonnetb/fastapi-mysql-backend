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
def create_route(path: str, fixed_statement: str, action: str):
    @app.post(path)
    def route_handler():
        db = SessionLocal()
        try:
            #runs the request
            result = db.execute(text(fixed_statement))
            data = action(result, db)

            # if data is a list of rows, format them
            if isinstance(data, list):
                return {"result": [dict(row._mapping) for row in data]}
            else:
                return {"result": "success"}

        finally:

            db.close()

    #no fucking clue what this is #Ben's Shit
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}"

# All routes for SELECT all
create_route("/select/benutzer",    "SELECT * FROM taskplaner.benutzer", lambda r, db: r.fetchall())
create_route("/select/aufgabe",     "SELECT * FROM taskplaner.aufgabe", lambda r, db: r.fetchall())
create_route("/select/kategorie",   "SELECT * FROM taskplaner.kategorie", lambda r, db: r.fetchall())
create_route("/select/material",    "SELECT * FROM taskplaner.material", lambda r, db: r.fetchall())
create_route("/select/prioritaet",  "SELECT * FROM taskplaner.prioritaet", lambda r, db: r.fetchall())
create_route("/select/fortschritt", "SELECT * FROM taskplaner.fortschritt", lambda r, db: r.fetchall())

# All routes for SELECT one
create_route("/select/benutzer/{id}",    "SELECT * FROM taskplaner.benutzer WHERE id = :id", lambda r, db: r.fetchone())
create_route("/select/aufgabe/{id}",     "SELECT * FROM taskplaner.aufgabe WHERE id = :id", lambda r, db: r.fetchone())
create_route("/select/kategorie/{id}",   "SELECT * FROM taskplaner.kategorie WHERE id = :id", lambda r, db: r.fetchone())
create_route("/select/material/{id}",    "SELECT * FROM taskplaner.material WHERE id = :id", lambda r, db: r.fetchone())
create_route("/select/prioritaet/{id}",  "SELECT * FROM taskplaner.prioritaet WHERE id = :id", lambda r, db: r.fetchone())
create_route("/select/fortschritt/{id}", "SELECT * FROM taskplaner.fortschritt WHERE id = :id", lambda r, db: r.fetchone())

# insert

# update

# delete



