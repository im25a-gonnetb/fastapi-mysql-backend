## `/insert/benutzer` — POST
```json
{
  "benutzername": "ben.gonnet",
  "benutzerpwd": "passwort123"
}
```

## `/update/benutzer` — PUT
```json
{
  "benutzerid": 1,
  "benutzername": "max.mustermann",
  "benutzerpwd": "neuespasswort"
}
```

## `/delete/benutzer` — DELETE
```json
{
  "benutzerid": 4
}
```

## `/procedure/update-fortschritt` — POST
```json
{
  "aufgabe_id": 1,
  "fortschritt_id": 5
}
```
