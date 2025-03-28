from fastapi import FastAPI, Depends
import asyncpg
from database import get_db_connection

app = FastAPI()

# Fetch all users
@app.get("/users")
async def get_users():
    conn = await get_db_connection()
    users = await conn.fetch("SELECT * FROM users;")
    await conn.close()
    return users

# Fetch a single user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    conn = await get_db_connection()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1;", user_id)
    await conn.close()
    if not user:
        return {"error": "User not found"}
    return dict(user)

# Insert a new user
@app.post("/users")
async def create_user(name: str, email: str):
    conn = await get_db_connection()
    await conn.execute("INSERT INTO users (name, email) VALUES ($1, $2);", name, email)
    await conn.close()
    return {"message": "User created successfully"}
