from data_base.data_config import Session
from models.users_model import User_Model
from utils.jwt_manager import create_token, get_data_by_token
from utils.send_email import send_email_signin
from fastapi.encoders import jsonable_encoder

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
    def get_user(self, data:dict):
        my_user = self.db.query(User_Model).filter(User_Model.username == data['username']).first()
        if not my_user:
            return {'message': 'tu usuario no se encuentra, revisa tu nombre de usuario', 'status': 404}
        user = jsonable_encoder(my_user)
        password = get_data_by_token(user['password'])
        if password['content'] != data['password'] or user['email'] != data['email']:
            return {'message': 'Revisa tu usuario, contraseña o correo electrónico', 'status': 422}
        user_token = create_token(user)
        res = send_email_signin(user['email'], user_token)
        return res

    def login(self, token:str):
        data = get_data_by_token(token)
        return data

    def change_password(self, email:str):
        user = self.db.query(User_Model).filter(User_Model.email == email).first()
        if not user:
            return {'message': 'no encontramos tu correo electrónico', 'status': 400}
        data = jsonable_encoder(user)
        token = create_token(data)
        res = send_email_signin(email, token)
        return res
    def create_new_password(self, token:str, new_password:str):
        data = get_data_by_token(token)
        user = self.db.query(User_Model).filter(User_Model.id == data['id']).first()
        old_p = jsonable_encoder(user)['password']
        if old_p != data['password']:
            return {'message': 'Estas usando un token viejo', 'status': 422}
        password = create_token({'content': new_password})
        user.password = password
        self.db.commit()
        return {'message': 'contraseña cambiada', 'status': 200}

    def delete_user(self, id: int):
        my_user = self.db.query(User_Model).filter(User_Model.id == id).first()
        user = jsonable_encoder(my_user)
        user_token = create_token(user)
        res = send_email_signin(user['email'], user_token)
        return res

    def delete(self, token:str):
        data = get_data_by_token(token)
        user = self.db.query(User_Model).filter(User_Model.id == data['id']).first()
        self.db.delete(user)
        self.db.commit()
        return 'Usuario eliminado'
