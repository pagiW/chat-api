from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from services.User_service import Users
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from schemas.user_schema import UserSchemaCreate

load_dotenv()

user_router = APIRouter()

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
@user_router.post('/users')
def signin(user: UserSchemaCreate):
    data = dict(user)
    res = Users().create(data)
    return JSONResponse(content={'message': res['message']}, status_code=res['status'])


@user_router.post('/users/{token}')
def verify(token: str):
    res = Users().signin(token)
    return JSONResponse(content=res, status_code=201)