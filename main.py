import os
import uuid
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional

from models import APIKey, User

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    # lazy
    return JSONResponse(status_code=200, content={"Documentation": {"/generate_key/": "POST", "/valid_key/": "GET"}})

def is_admin(adminapikey: str):
    if adminapikey != os.environ.get("ADMIN_API_KEY"):
        raise HTTPException(status_code=400, detail="Not authorized")
    return True

@app.post("/generate_key/")
def generate_key(user: User, authorized: bool = Depends(is_admin)) -> JSONResponse:
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
        return JSONResponse(
            status_code=200,
            content={"name": user.name, "email": user.email, "apikey": new_key},
        )
    else:
        raise HTTPException(status_code=400, detail="Not authorized")

@app.get("/valid_key/")
def valid_key(apikey: APIKey) -> JSONResponse:
    cur.execute("SELECT * FROM users WHERE apikey=%s", (apikey.apikey,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API key")
    return JSONResponse(
        status_code=200,
        content={"name": user[0], "email": user[1], "apikey": user[2], "valid": True},
    )