from data_base.data_config import Base
from sqlalchemy import Column, Integer, String

class User_Model(Base):
    __tablename__ = 'Users_Table_V3'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    email = Column(String, unique=True)
    messages = Column(String)
    contacts = Column(String)
    recived = Column(String)