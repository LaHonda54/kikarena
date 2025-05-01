import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    conn = sqlite3.connect("fifa_start.db")
    c = conn.cursor()
    c.execute("SELECT id, password_hash, role FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user:
        user_id, stored_hash, role = user
        if stored_hash == hash_password(password):
            return {"id": user_id, "username": username, "role": role}
    return None

def create_user(username, password, role):
    conn = sqlite3.connect("fifa_start.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                  (username, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
