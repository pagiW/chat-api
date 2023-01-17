from jwt import encode, decode
from dotenv import load_dotenv
import os
load_dotenv()

def create_token(data: dict):
    token: str = encode(data, key=os.getenv('SECRET'), algorithm=os.getenv('ALGORITHM'))
    return token

def get_data_by_token(token: str):
    data: dict = decode(token, key=os.getenv('SECRET'), algorithms=[os.getenv('ALGORITHM')])
    return data