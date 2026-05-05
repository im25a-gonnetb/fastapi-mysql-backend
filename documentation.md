# FastAPI + MySQL Backend — Documentation

## Ziel

REST API mit FastAPI (Python) und MySQL-Datenbank. Übungsproject im Rahmen des Moduls.

## Stack

| Komponente | Technologie |
|-----------|------------|
| Backend | FastAPI (Python 3.11+) |
| Datenbank | MySQL 8.x |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Validation | Pydantic v2 |
| Server | Uvicorn |

## Projektstruktur (geplant)

```
fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # DB connection & session
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API routes
│   └── crud/            # DB operations
├── alembic/             # DB migrations
├── tests/
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

### Voraussetzungen

- Python 3.11+
- MySQL 8.x
- pip / venv

### Installation

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Umgebungsvariablen

Datei `.env` anlegen (nicht committen):

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fastapi_db
DB_USER=root
DB_PASSWORD=yourpassword
```

### Datenbank starten

```bash
# MySQL-Tabellen erstellen via Alembic
alembic upgrade head
```

### Server starten

```bash
uvicorn app.main:app --reload
```

API erreichbar unter: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

## API-Endpunkte

_Werden während der Übung ergänzt._

## Abhängigkeiten

```
fastapi
uvicorn[standard]
sqlalchemy
pymysql
alembic
pydantic-settings
python-dotenv
```
