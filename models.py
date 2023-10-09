from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

class APIKey(BaseModel):
    apikey: str
    authProvider: str = "lit"