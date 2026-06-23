# Arbeitsjournal - FastAPI MySQL Backend

---

## 05.05.2026

**Ben:** GitHub-Repo erstellt und Projektstruktur aufgesetzt (`backend.py`, `.gitignore`, `arbeitsjournal.md`, `documentation.md`). FastAPI-Instanz in `backend.py` angelegt, Hello-World-Route (`GET /`) hinzugefügt.

**Elio:** "Backend" und "Framework" recherchiert. FastAPI und Uvicorn installiert. FastAPI-Tutorial durchgearbeitet. Installations-Commands in `documentation.md` festgehalten (`fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`). Erste Hello-World-Route in `backend.py` geschrieben.

---

## 12.05.2026

**Ben:** Datenbankverbindung in `backend.py` aufgebaut. `python-dotenv`, `sqlalchemy`, `create_engine` und `SessionLocal` eingebunden. Datenbankpfad in `.env`-Datei ausgelagert. Zone-Identifier-Dateien aus dem Repo entfernt. WSL-Zugriff auf die Windows-MySQL-Datenbank konfiguriert (Host-IP via `/etc/resolv.conf`).

**Elio:** FastAPI-Tutorial weiter vertieft und recherchiert. Erste universelle Route implementiert: `POST /statement` nimmt einen SQL-String entgegen und führt ihn direkt aus.

---

## 19.05.2026

**Ben:** `create_route()`-Hilfsfunktion geschrieben, die dynamisch POST-Routen mit festem SQL-Statement registriert. Erste Testrouten erstellt (`/select`, `/insert`, `/update`, `/delete`).

**Elio:** Alle spezifischen SELECT-Routen für jede Tabelle angelegt (`benutzer`, `aufgabe`, `kategorie`, `material`, `prioritaet`, `fortschritt`). Test-Statement aus `backend.py` entfernt. Eigene FastAPI-Dokumentation begonnen.

---

## 26.05.2026

**Ben:** `create_route()` in separate Funktionen aufgeteilt (`create_select_all`, `create_select_one`, `create_write_route`, `create_update_route`). SELECT-Routen auf die korrekten Primärschlüsselnamen in den WHERE-Klauseln angepasst. Weitere WSL/Windows-Verbindungsprobleme behoben.

**Elio:** Fehler in den SELECT-one-Routen korrigiert (falsche Spaltennamen in WHERE-Klauseln). Eigene Dokumentation fertiggestellt. Offizielle Projektdokumentation bereinigt, Uvicorn-Startbefehl in `documentation.md` ergänzt.

---

## 02.06.2026

**Ben:** Zusammen mit Elio die bestehenden Routen debuggt und Lösungsansätze besprochen. Hauptsächlich auf Elios Gerät gearbeitet. Recherche für die nächsten Schritte (DELETE-Routen, Stored Procedures).

**Elio:** Auf Basis von Bens `create_write_route()` alle INSERT-Routen für die restlichen Tabellen implementiert. Alle UPDATE-Routen für sämtliche Tabellen angelegt. Sehr lange Fehlersuche: falsche HTTP-Methode (PUT statt PATCH), Parameter wurden nicht korrekt übergeben, `db.commit()` fehlte. Am Ende funktionierten INSERT und UPDATE für fast alle Tabellen, einzige Ausnahme war `aufgabenmaterial`.

---

## 09.06.2026

**Ben:** Merge-Konflikt gelöst (diff-Viewer war kaputt, Änderungen manuell zusammengeführt). View-Route (`GET /select/benutzer`) als Test hinzugefügt mit `create_select_view()`.

**Elio:** Schlecht implementierte DELETE-Routen entfernt (verwendeten falsch `PUT` statt `DELETE`). INSERT- und UPDATE-Routen final gefixt: `Body(...)` und `Path(...)` korrekt importiert und eingebunden. Gesamten Code aufgeräumt. Danach durch einen ungewollten Revert fast alles verloren, zurück zu Commit `f44a85f`.

---

## 16.06.2026

**Ben:** `create_procedure_route()`-Funktion implementiert für Stored-Procedure-Aufrufe als POST-Route. Sieben Stored Procedures angebunden (`loeschen`, `loeschenmaterial`, `loeschenbenutzer`, `loeschenmaterialbenutzer`, `loeschenkategorie`, `loeschenfortschritt`, `loeschenprioritaet`). Kommentar zu `create_select_view()` ergänzt. Arbeitsjournal anhand des Git-Changelogs nachgeführt und `documentation.md` bereinigt.

**Elio:** Benutzer-View durch `AufgabenDetails`-View ersetzt (`/view/aufgabendetails`). Alle Delete-Stored-Procedures entfernt und durch eine einzelne `UpdateFortschritt`-Procedure ersetzt (`/procedure/update-fortschritt`). Kleines Cleanup in `create_update_route()`, `rows_affected` aus der Response entfernt.
