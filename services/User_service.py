from data_base.data_config import Session
from models.users_model import User_Model
from utils.jwt_manager import create_token, get_data_by_token
from utils.send_email import send_email_signin

class Users:
    def __init__(self):
        self.db = Session()

    def getAll(self):
        res = self.db.query(User_Model).all()
        return res
    def getOne(self, id: int):
        res = self.db.query(User_Model).filter(User_Model.id == id).first()
        return res
    def create(self, user: dict):
        user['password'] = create_token({'content': user['password']})
        user['messages'] = ''
        user['contacts'] = ''
        user['recived'] = ''
        data = User_Model(**user)
        try:
            self.db.add(data)
            self.db.commit()
        except:
            return {
                'message': 'Modifica tu email, usuario y/o contraseña. Seguramente están en uso',
                'status': 400
            }
        self.db.delete(data)
        self.db.commit()
        account_token = create_token(user)
        res = send_email_signin(user['email'], account_token)
        return res
    def signin(self, token):
        data = get_data_by_token(token)
        user = User_Model(**data)
        self.db.add(user)
        self.db.commit()
        return data