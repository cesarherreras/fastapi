from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITH = "HS256" 
ACCESS_TOKEN_DURATION = 1
SECRET =  "3d8dd702b2b2fc63d4e90eecebd8ddce8ea89d3ff3bbd5a9653a3997824e6327"

router = APIRouter(prefix="/jwtauth", 
                #El tag se utiliza para separación en la documentación
                tags = ['jwtauth'],
                responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "usertest": {
        "username": "usertest",
        "full_name": "Test full name",
        "email": "test@mail.com",
        "disabled": False,
        "password": "$2a$12$PTQ/rJMl4ZgbaZTR3r1qAOGiHD6D1uVFoZtV6fasovGGxe1WwYb/G"
    },
    "usertest2": {
        "username": "usertest2",
        "full_name": "Test full name 2",
        "email": "test2@mail.com",
        "disabled": True,
        "password": "$2a$12$/ocAEiyzyms9N875ZGkuLeN0/WzdPwoad5ABna1nHPfoFdfpclxdi"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas", 
                            headers={"WWW-Authenticate":"Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITH).get("sub")
        if username is None:
            raise exeption
    except JWTError:
        raise exeption
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
        "sub":user.username,
        "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITH), "token_type":"bearer"}

@router.get("/users/me")
#Criterios de dependencia. Operarios para validar el token
async def me(user: User = Depends(current_user)):
    return user
