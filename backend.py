from fastapi import FastAPI, HTTPException
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





# Test if server works, on http://127.0.0.1:8000/ it should say message: hello world
@app.get("/")
def read_root():
    return {"message": "Hello World"}

def create_select_all(path: str, statement: str):
    @app.post(path)
    def route_handler():
        db = SessionLocal()
        try:
            result = db.execute(text(statement))
            return {"result": [dict(row._mapping) for row in result.fetchall()]}
        finally:
            db.close()
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}"

def create_select_one(path: str, statement: str):
    @app.post(path)
    def route_handler(id: int):          # id is now properly captured
        db = SessionLocal()
        try:
            result = db.execute(text(statement), {"id": id})
            row = result.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Not found")
            return {"result": dict(row._mapping)}
        finally:
            db.close()
    
    #no fucking clue what this is #Ben's Shit
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}"

def create_write_route(path: str, statement: str):
    @app.post(path)
    def route_handler(data: dict):  # receives the request body
        db = SessionLocal()
        try:
            db.execute(text(statement), data)
            db.commit()
            return {"result": "success"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}"

# All routes for SELECT all
create_select_all("/select/benutzer",    "SELECT * FROM taskplaner.benutzer")
create_select_all("/select/aufgabe",     "SELECT * FROM taskplaner.aufgabe")
create_select_all("/select/kategorie",   "SELECT * FROM taskplaner.kategorie")
create_select_all("/select/material",    "SELECT * FROM taskplaner.material")
create_select_all("/select/prioritaet",  "SELECT * FROM taskplaner.prioritaet")
create_select_all("/select/fortschritt", "SELECT * FROM taskplaner.fortschritt")

# All routes for SELECT one
create_select_one("/select/benutzer/{id}",    "SELECT * FROM taskplaner.benutzer WHERE benutzerid = :id")
create_select_one("/select/aufgabe/{id}",     "SELECT * FROM taskplaner.aufgabe WHERE aufgabeid = :id")
create_select_one("/select/kategorie/{id}",   "SELECT * FROM taskplaner.kategorie WHERE kategorieid = :id")
create_select_one("/select/material/{id}",    "SELECT * FROM taskplaner.material WHERE materialid = :id")
create_select_one("/select/prioritaet/{id}",  "SELECT * FROM taskplaner.prioritaet WHERE PrioritaetID = :id")
create_select_one("/select/fortschritt/{id}", "SELECT * FROM taskplaner.fortschritt WHERE fortschrittid = :id")

# insert


# update

# delete



