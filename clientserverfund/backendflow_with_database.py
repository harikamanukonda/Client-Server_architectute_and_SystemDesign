from fastapi import FastAPI
import sqlite3

app = FastAPI() #here we are creating fastapi server application

def get_db_connection():
    conn = sqlite3.connect("users.db") 
    conn.row_factory = sqlite3.Row #this actually makes database rows into dict/JSON
    return conn

def create_table():
    conn = get_db_connection() #this opens database connection
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL)
                 """)
    conn.commit()
    conn.close()
create_table()


@app.get("/")
def home():
    return {"message": "Client-Server Architecture Practice"}


@app.get("/users")
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return dict(user)

    return {"message": "User not found"}

@app.post("/users")
def create_user(name: str, role: str):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO users (name, role) VALUES (?, ?)",
        (name, role)
    )
    conn.commit()
    new_user_id = cursor.lastrowid
    conn.close()

    return {
        "message": "New user created",
        "user_id": new_user_id
    }