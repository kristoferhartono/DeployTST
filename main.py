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
    return{'Modul Sign Up'}

def check_user(user: str, password: str):
    for account in data['account']:
        if user == account['user'] and password == account['password']:
            return True
    return False

@app.post("/user/signup", tags=["user"])
async def user_signup(user: str, email:str, password: str):
    if check_user(user, password):
        return {
            "error": "Account sudah terdaftar!"
        }
    else:
        id=1
        if(len(data['account'])>0):
            id=data['account'][len(data['account'])-1]['id']+1
        new_data={'id': id,'user': user,'email' : email, 'password': password}
        data['account'].append(dict(new_data))
        read_file.close()
        with open("account.json", "w") as write_file:
            json.dump(data,write_file,indent=4)
        write_file.close()
        return {"message": "SignUp Berhasil"}
        raise HTTPException(
            status_code=500, detail=f'Internal Server Error'
            )


