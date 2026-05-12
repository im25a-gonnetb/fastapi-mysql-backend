pip install fastAPI
pip install "uvicorn[standard]"

pip install sqlalchemy
pip install pymysql
pip install python-dotenv

## MySQL Connection Setup

Create a `.env` file in the project root (never commit this to git):
```
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST/DBNAME
```

**Windows:** Use `localhost` as HOST. MySQL Workbench runs on same machine.

**WSL:** `localhost` points to WSL itself, not Windows. Get Windows host IP:    
```bash
cat /etc/resolv.conf | grep nameserver
```
Use that IP (e.g. `172.x.x.x`) as HOST in your `.env`.
Also grant MySQL access from WSL — run this in MySQL Workbench:
```sql
GRANT ALL PRIVILEGES ON your_db.* TO 'root'@'%';
FLUSH PRIVILEGES;
```
