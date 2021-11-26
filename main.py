from fastapi import FastAPI, Body, Depends, HTTPException
import json
from app.model import UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

app = FastAPI()

with open("account.json", "r") as read_file:
    data = json.load(read_file)

@app.get('/')
def root():
    return{'Silahkan tambahkan "/docs" pada url'}

def check_user(user: str, password: str):
    for account in data['account']:
        if user == account['user'] and password == account['password']:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: str, password: str):
    if check_user(user, password):
        return signJWT(user)
    return {
        "error": "Wrong login details!"
    }

