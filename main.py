from fastapi import FastAPI
from data_base.data_config import Base, my_engine
from uvicorn import run
import os
from dotenv import load_dotenv
from routers.users_router import user_router
from middlewares.ErrorHandler import ErrorHandler
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

Base.metadata.create_all(bind=my_engine)

app = FastAPI()
app.title = 'Chat Api Project'

origins = [
    os.getenv('URL1')
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandler)
app.include_router(user_router)

if __name__ == '__main__':
    run(app, port=os.getenv('PORT'), host='0.0.0.0')