import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://utente_db:password@localhost/tesi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

