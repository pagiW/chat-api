import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

name = os.getenv('DATA_NAME')
path_data = os.path.dirname(os.path.realpath(__file__))

url = f'sqlite:///{os.path.join(path_data, name)}'

my_engine = create_engine(url, echo=True)

Session = sessionmaker(bind=my_engine)

Base = declarative_base()