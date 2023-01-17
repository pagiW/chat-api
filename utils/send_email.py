import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from data_base.data_config import Session

load_dotenv()

def send_email_signin(email, token):
    try:
        em = EmailMessage()
        em['From'] = os.getenv('APP_EMAIL')
        em['To'] = email
        em['Subject'] = 'Account Verification'
        em.set_content(f'token: {token}')

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as  smtp:
            smtp.login(os.getenv('APP_EMAIL'), os.getenv('APP_PASSWORD'))
            smtp.sendmail(os.getenv('APP_EMAIL'), email, em.as_string())
        return {
            'message': 'confirma tu registro, inicio de sesión o cambio de contraseña en tu correo electrónico',
            'status': 202
        }
    except:
        return {
            'message': 'verifica tu correo',
            'status': 406
        }