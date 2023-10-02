import os
import uuid

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional

from models import User

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

app = FastAPI()

@app.get("/")
async def root():
    return "Documentation: /generate_key/ - POST; /valid_key/ - GET "

def is_admin(adminapikey: str):
    if adminapikey != os.environ.get("ADMIN_API_KEY"):
        raise HTTPException(status_code=400, detail="Not authorized")
    return True

@app.post("/generate_key/")
def generate_key(user: User, authorized: bool = Depends(is_admin)) -> str:
    if authorized:
        new_key = str(uuid.uuid4())
        try:
            cur.execute(
                "INSERT INTO users (name, email, apikey) VALUES (%s, %s, %s)",
                (user.name, user.email, new_key),
            )
            conn.commit()
        except psycopg2.IntegrityError:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )
        return new_key
    else:
        raise HTTPException(status_code=400, detail="Not authorized")

@app.get("/valid_key/")
def check_key(apikey: str, authorized: bool = Depends(is_admin)) -> bool:
    if authorized:
        cur.execute("SELECT * FROM users WHERE apikey=%s", (apikey,))
        user = cur.fetchone()
        if not user:
            return False
        return True
    else:
        return False