from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="user", surname="test", url = "url test", age = 10),
    User(id=2, name="user", surname="test", url = "url test", age = 10),
    User(id=3, name="user", surname="test", url = "url test", age = 10)
]

@router.get("/users")
async def users(): 
    return users_list

#Path
@router.get("/user/{id}")
async def user(id: int): 
    return search_user(id)
    
#Query
@router.get("/user/") 
async def user(id: int): 
    return search_user(id)

@router.post("/user/", response_model= User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        #Raise propaga la excepción
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el id"}
