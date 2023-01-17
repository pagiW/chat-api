from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from services.User_service import Users
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from schemas.user_schema import UserSchemaCreate
from pydantic import Field, BaseModel

load_dotenv()

user_router = APIRouter()

class New_Password(BaseModel):
    new_password: str = Field(min_length=8)

@user_router.get('/users')
def get_users():
    data = Users().getAll()
    return data
@user_router.get('/users/{id}')
def get_user(id: int = Path(ge=1)):
    data = Users().getOne(id)
    if not data:
        return JSONResponse(content={'message': 'User not found'}, status_code=404)
    return JSONResponse(jsonable_encoder(data))
@user_router.post('/users/signin')
def signin(user: UserSchemaCreate):
    data = dict(user)
    res = Users().create(data)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])


@user_router.post('/users/signin/{token}')
def verify(token: str):
    res = Users().signin(token)
    return JSONResponse(content=res, status_code=201)

@user_router.post('/users/login')
def login(data: UserSchemaCreate):
    user = dict(data)
    res = Users().get_user(user)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])

@user_router.post('/users/login/{token}')
def verfy(token:str):
    data = Users().login(token)
    return JSONResponse(content=data, status_code=200)

@user_router.post('/users/change_password')
def change_password(email: str):
    res = Users().change_password(email)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])

@user_router.put('/users/change_password/{token}')
def create_password(token: str, data: New_Password):
    new_password = dict(data)['new_password']
    res = Users().create_new_password(token, new_password)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])

@user_router.post('/users/delete_user/{id}')
def delete(id: int):
    res = Users().delete_user(id)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])


@user_router.delete('/users/{token}')
def delete(token:str):
    res = Users().delete(token)

    return JSONResponse(content={'message': res}, status_code=200)