import sqlite3
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Verbindung zur Datenbank aufbauen
conn = sqlite3.connect("fifa_start.db")
c = conn.cursor()

# Tabelle für Benutzer erstellen
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'player')) NOT NULL,
    coins INTEGER DEFAULT 100
)
""")

# Tabelle für Matches erstellen
c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player1_id INTEGER,
    player2_id INTEGER,
    result TEXT,
    coins INTEGER,
    winner_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Test-Accounts einfügen
c.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
          ("admin", hash_password("admin123"), "admin"))
c.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
          ("player1", hash_password("pass123"), "player"))

conn.commit()
conn.close()
print("Datenbank fifa_start.db erstellt.")