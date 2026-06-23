'''
MYSQL Backend for Uvicorn
'''

#Imports
from fastapi import FastAPI, HTTPException, Path, Body
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

#Loads .env file for different SQL DB Paths
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

#Creates Fastapi app
app = FastAPI()

#Creates Select Path framework
def create_select_all(path: str, statement: str):
    @app.post(path) #registers thing
    def route_handler():
        db = SessionLocal()
        try:
            result = db.execute(text(statement)) #text(statement) tells the program that statement is a completely written piece of SQL db.execute executes it and stores the result/reply in result
            return {"result": [dict(row._mapping) for row in result.fetchall()]} #formats result to be able to be displayed in web ui nicely (formats mysql to python dict)
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates Select Path framework for singular(...)
def create_select_one(path: str, statement: str):
    @app.post(path) #registers thing
    def route_handler(id: int = Path(...)): #id taken from url path (the {id} part), Path(...) makes it required
        db = SessionLocal()
        try:
            result = db.execute(text(statement), {"id": id}) #runs the SQL and swaps :id in the statement for the actual id value (safe, no SQL injection)
            row = result.fetchone() #grabs just the first matching row
            if row is None: #nothing found with that id
                raise HTTPException(status_code=404, detail="Not found") #sends back a 404 error instead of crashing
            return {"result": dict(row._mapping)} #formats the one row to python dict for the web ui
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates insert Path framework
def create_write_route(path: str, statement: str):
    @app.post(path) #registers thing
    def route_handler(data: dict = Body(...)):  #data is the json body sent with the request, Body(...) makes it required
        db = SessionLocal()
        try:
            result = db.execute(text(statement), data) #runs the INSERT, swapping the :placeholders in statement for the matching keys in data
            db.commit() #saves the change permanently to the db (writes need this, reads dont)
            return {"result": "success"} #tells the caller it worked
        except Exception as e: #something went wrong (bad data, db error)
            db.rollback() #undoes the half done change so the db stays clean
            raise HTTPException(status_code=500, detail=str(e)) #sends back a 500 error with the reason
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates UPDATE Path framework
def create_update_route(path: str, statement: str):
    @app.put(path) #registers thing, put is the http method used for updating existing data
    def route_handler(data: dict = Body(...)): #data is the json body holding the new values + the id of the row to change
        db = SessionLocal()
        try:
            db.execute(text(statement), data) #runs the UPDATE, swapping :placeholders for the keys in data
            db.commit() #saves the change permanently

            return {
                "result": "success" #tells the caller it worked
            }
        except Exception as e: #something went wrong
            db.rollback() #undoes the half done change
            raise HTTPException(status_code=500, detail=str(e)) #sends back a 500 error with the reason
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates DELETE Path framework
def create_delete_route(path: str, statement: str):
    @app.delete(path) #registers thing, delete is the http method used for removing data
    def route_handler(data: dict = Body(...)): #data is the json body holding the id of the row to delete
        db = SessionLocal()
        try:
            result = db.execute(text(statement), data) #runs the DELETE, swapping :placeholders for the keys in data
            db.commit() #saves the change permanently

            return {
                "result": "success", #tells the caller it worked
                "rows_affected": result.rowcount #how many rows got deleted (0 means nothing matched the id)
            }
        except Exception as e: #something went wrong
            db.rollback() #undoes the half done change
            raise HTTPException(status_code=500, detail=str(e)) #sends back a 500 error with the reason
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates SELECT view
def create_select_view(path: str, statement: str):
    @app.get(path) #registers thing, get is the http method used for plain reading (view opens in browser by url)
    def route_handler():
        db = SessionLocal()
        try:
            result = db.execute(text(statement)) #runs the SQL against the db view and stores the reply in result
            return {"result": [dict(row._mapping) for row in result.fetchall()]} #formats every row to python dict for the web ui
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions

#Creates stored procedure
def create_procedure_route(path: str, call_statement: str):
    @app.post(path) #registers thing
    def route_handler(data: dict = Body(default={})): #data is the json body with the procedure arguments, Body(default={}) makes it optional (empty if none sent)
        db = SessionLocal()
        try:
            result = db.execute(text(call_statement), data) #runs the CALL to the stored procedure, swapping :placeholders for the keys in data
            rows = result.fetchall() #grabs whatever rows the procedure returned
            db.commit() #saves any changes the procedure made
            return {"result": [dict(row._mapping) for row in rows]} #formats every returned row to python dict for the web ui
        except Exception as e: #something went wrong
            db.rollback() #undoes the half done change
            raise HTTPException(status_code=500, detail=str(e)) #sends back a 500 error with the reason
        finally:
            db.close() #closes db
    route_handler.__name__ = f"handle_{path.strip('/').replace('/', '_')}" #avoids name collisions


#be aware of danger big dense block of code ahead


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
# All routes for INSERT
create_write_route("/insert/benutzer",    "INSERT INTO taskplaner.benutzer (benutzername, benutzerpwd) VALUES (:benutzername, :benutzerpwd)")
create_write_route("/insert/material", "INSERT INTO taskplaner.material (Material, IstAktiv) VALUES (:material, :istaktiv)")
create_write_route("/insert/kategorie", "INSERT INTO taskplaner.kategorie (Kategorie, IstAktiv) VALUES (:kategorie, :istaktiv)")
create_write_route("/insert/prioritaet", "INSERT INTO taskplaner.prioritaet (Prioritaet) VALUES (:prioritaet)")
create_write_route("/insert/aufgabe", "INSERT INTO taskplaner.aufgabe (Titel, Beginn, Ende, Ort, Koordinaten, Notiz, KategorieID, PrioritaetID, FortschrittID, BenutzerID) VALUES (:titel, :beginn, :ende, :ort, :koordinaten, :notiz, :kategorieid, :prioritaetid, :fortschrittid, :benutzerid)")
create_write_route("/insert/datei", "INSERT INTO taskplaner.datei (AufgabeID, Dateipfad, DateiBLOB) VALUES (:aufgabeid, :dateipfad, :dateiblob)")
create_write_route("/insert/aufgabematerial", "INSERT INTO taskplaner.aufgabematerial (AufgabeID, MaterialID, Anzahl) VALUES (:aufgabeid, :materialid, :anzahl)")
# All routes for UPDATE
create_update_route("/update/benutzer","UPDATE taskplaner.benutzer SET benutzerpwd = :benutzerpwd,benutzername = :benutzername WHERE benutzerid = :benutzerid")
create_update_route("/update/material", "UPDATE taskplaner.material SET material = :material, istaktiv = :istaktiv WHERE materialid = :materialid")
create_update_route("/update/kategorie", "UPDATE taskplaner.kategorie SET kategorie = :kategorie, istaktiv = :istaktiv WHERE kategorieid = :kategorieid")
create_update_route("/update/prioritaet", "UPDATE taskplaner.prioritaet SET prioritaet = :prioritaet WHERE prioritaetid = :prioritaetid")
create_update_route("/update/fortschritt", "UPDATE taskplaner.fortschritt SET fortschritt = :fortschritt WHERE fortschrittid = :fortschrittid")
create_update_route("/update/aufgabe", "UPDATE taskplaner.aufgabe SET titel = :titel, beginn = :beginn, ende = :ende, ort = :ort, koordinaten = :koordinaten, notiz = :notiz, kategorieid = :kategorieid, prioritaetid = :prioritaetid, fortschrittid = :fortschrittid, benutzerid = :benutzerid WHERE aufgabeid = :aufgabeid")
create_update_route("/update/datei", "UPDATE taskplaner.datei SET aufgabeid = :aufgabeid, dateipfad = :dateipfad, dateiblob = :dateiblob WHERE dateiid = :dateiid")
create_update_route("/update/aufgabematerial", "UPDATE taskplaner.aufgabematerial SET anzahl = :anzahl WHERE aufgabeid = :aufgabeid AND materialid = :materialid")
# All routes for DELETE
create_delete_route("/delete/benutzer", "DELETE FROM taskplaner.benutzer WHERE benutzerid = :benutzerid")
create_delete_route("/delete/material", "DELETE FROM taskplaner.material WHERE materialid = :materialid")
create_delete_route("/delete/kategorie", "DELETE FROM taskplaner.kategorie WHERE kategorieid = :kategorieid")
create_delete_route("/delete/prioritaet", "DELETE FROM taskplaner.prioritaet WHERE prioritaetid = :prioritaetid")
create_delete_route("/delete/fortschritt", "DELETE FROM taskplaner.fortschritt WHERE fortschrittid = :fortschrittid")
create_delete_route("/delete/aufgabe", "DELETE FROM taskplaner.aufgabe WHERE aufgabeid = :aufgabeid")
create_delete_route("/delete/datei", "DELETE FROM taskplaner.datei WHERE dateiid = :dateiid")
create_delete_route("/delete/aufgabematerial", "DELETE FROM taskplaner.aufgabematerial WHERE aufgabeid = :aufgabeid AND materialid = :materialid")
#view
create_select_view("/view/aufgabendetails", "SELECT * FROM taskplaner.AufgabenDetails")
#stored procedure
create_procedure_route("/procedure/update-fortschritt", "call UpdateFortschritt(:aufgabe_id, :fortschritt_id)")
